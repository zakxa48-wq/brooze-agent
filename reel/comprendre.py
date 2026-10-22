"""Comprendre un audio pour un Reel : nettoyage, transcription locale (Whisper), calage mot à mot, verdict de qualité.

Usage : python3 reel/comprendre.py inbox/audio/memo.m4a sorties/<id>/
        python3 reel/comprendre.py --recaler sorties/<id>/   (après correction à la main de segs.json : recale mots.json)
        python3 reel/comprendre.py --nettoyer audio sorties/<id>/  (voix.wav seulement : la transcription existe déjà)
Écrit dans le dossier :
  brut.wav     l'audio d'origine, décodé (48 kHz, mono, float)
  voix.wav     la voix nettoyée : passe-haut, débruitage léger, pauses > 0,55 s ramenées à 0,35 s, −16 LUFS
  segs.json    [[début, fin, texte]] : phrases transcrites, dans le temps de voix.wav
  mots.json    [{w, start, end, g}] : chaque mot calé (mots.py en mode ancré), g = groupe de sous-titre
  rapport.json durée, niveaux, bruit, saturation, transcription, verdict ("ok", "douteux", "inutilisable") et raisons
"""
import sys, os, json, subprocess, re, warnings
import numpy as np, soundfile as sf, pyloudnorm as pyln
from scipy import signal

SR = 48000
warnings.filterwarnings('ignore', message='Possible clipped samples')
ICI = os.path.dirname(os.path.abspath(__file__))
# Whisper medium si présent (nettement plus juste en français : « Tu vois » au lieu de « Je vois »), sinon small
_M = os.path.expanduser('~/.cache/brooze/sherpa-onnx-whisper-medium')
CACHE, TAILLE = (_M, 'medium') if os.path.exists(f'{_M}/medium-encoder.int8.onnx') else (os.path.expanduser('~/.cache/brooze/sherpa-onnx-whisper-small'), 'small')


def decoder(src, dst, filtres=None):
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', src, '-ac', '1', '-ar', str(SR)]
    if filtres: cmd += ['-af', filtres]
    subprocess.run(cmd + ['-c:a', 'pcm_f32le', dst], check=True)


def energie_db(x, pas=.01):
    H = int(SR * pas)
    n = len(x) // H
    e = np.sqrt((x[:n * H].reshape(n, H) ** 2).mean(1) + 1e-12)
    return 20 * np.log10(e)


def pauses(x, seuil_rel=35, mini=.25):
    """Intervalles de silence [début, fin] en secondes, relatifs au niveau de parole (percentile 95)."""
    db = energie_db(x); ref = np.percentile(db, 95); calme = db < ref - seuil_rel
    res = []; i = 0
    while i < len(calme):
        if calme[i]:
            j = i
            while j < len(calme) and calme[j]: j += 1
            if (j - i) * .01 >= mini: res.append([i * .01, j * .01])
            i = j
        else: i += 1
    return res, db, ref


def raccourcir(x, garde=.35, au_dela=.55, bord=.15):
    """Ramène chaque pause plus longue que `au_dela` à `garde` secondes (fondu de 20 ms), et rogne début et fin à `bord`."""
    ps, _, _ = pauses(x, mini=au_dela)
    dur = len(x) / SR; morceaux = []; pos = 0.
    for a, b in ps:
        if a <= .05:                       # silence de tête
            pos = max(pos, b - bord); continue
        if b >= dur - .05:                 # silence de queue
            morceaux.append((pos, a + bord)); pos = None; break
        coupe_a, coupe_b = a + garde / 2, b - garde / 2
        morceaux.append((pos, coupe_a)); pos = coupe_b
    if pos is not None: morceaux.append((pos, dur))
    f = int(.02 * SR); out = []
    for a, b in morceaux:
        seg = x[int(a * SR):int(b * SR)].copy()
        if len(seg) > 2 * f:
            seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        out.append(seg)
    return np.concatenate(out) if out else x


def segmenter(x, maxi=24.):
    """Découpe aux pauses en segments de moins de `maxi` s (limite de Whisper : 30 s)."""
    ps, _, _ = pauses(x, seuil_rel=30, mini=.18)
    dur = len(x) / SR
    # Une pause d'au moins 0,3 s ferme une phrase (dès 4 s de segment) ; sinon on coupe à la dernière pause avant `maxi`.
    coupes = [((a + b) / 2, b - a >= .3) for a, b in ps if .2 < (a + b) / 2 < dur - .2]
    segs = []; debut = 0.; derniere = None
    for c, longue in coupes:
        if c - debut > maxi and derniere is not None:
            segs.append([debut, derniere]); debut = derniere
        if longue and c - debut >= 4:
            segs.append([debut, c]); debut = c; derniere = None
        else:
            derniere = c
    segs.append([debut, dur])
    return [s for s in segs if s[1] - s[0] > .3]


def transcrire(x, segs):
    import sherpa_onnx
    rec = sherpa_onnx.OfflineRecognizer.from_whisper(
        encoder=f'{CACHE}/{TAILLE}-encoder.int8.onnx', decoder=f'{CACHE}/{TAILLE}-decoder.int8.onnx',
        tokens=f'{CACHE}/{TAILLE}-tokens.txt', language='fr', task='transcribe', num_threads=os.cpu_count() or 4)
    x16 = signal.resample_poly(x, 1, 3).astype(np.float32)
    res = []
    for a, b in segs:
        s = rec.create_stream(); s.accept_waveform(16000, x16[int(a * 16000):int(b * 16000)])
        rec.decode_stream(s)
        res.append([round(a, 3), round(b, 3), nettoyer_texte(s.result.text)])
    return res


LEXIQUE = json.load(open(f'{ICI}/lexique.json'))


def nettoyer_texte(t):
    """Retire les hallucinations connues de Whisper ([Musique], (Applaudissements)…) et applique le lexique Brooze."""
    t = re.sub(r'[\[(][^\])]*([\])]|$)', ' ', t)
    for faux, vrai in LEXIQUE.items():
        t = re.sub(rf'\b{faux}\b', vrai, t, flags=re.I)
    return re.sub(r'\s+', ' ', t).strip()


def affiner(dossier, avant=.14, apres=.10):
    """Recale le début de chaque mot sur l'attaque réelle de la voix (montée d'énergie ou entrée de fricative), quand
    elle est nette et proche de l'estimation ; sinon le mot garde son temps. Corrige la dérive de 0,1–0,2 s du calage
    syllabique au milieu des phrases (même méthode que attaques.py du skill, appliquée à tous les mots)."""
    x, sr = sf.read(f'{dossier}/voix.wav'); n = int(.02 * sr)
    fen = np.hanning(n); f = np.fft.rfftfreq(n, 1 / sr)
    def trame(t):
        a = max(0, int(t * sr)); s = x[a:a + n]
        if len(s) < n: s = np.pad(s, (0, n - len(s)))
        s = s * fen; S = np.abs(np.fft.rfft(s))
        return 20 * np.log10(np.sqrt((s ** 2).mean()) + 1e-7), (S * f).sum() / (S.sum() + 1e-9)
    mots = json.load(open(f'{dossier}/mots.json')); bouges = 0
    for k, w in enumerate(mots):
        T = np.arange(w['start'] - avant, w['start'] + apres, .01); F = [trame(t) for t in T]
        e = np.array([a for a, _ in F]); c = np.array([b for _, b in F])
        cand = [T[j] for j in range(3, len(T)) if (e[j] - e[j - 3] > 9 and e[j] > -36) or (c[j] > 3300 and c[j - 1] <= 3300 and e[j] > -42)]
        if not cand: continue
        t = float(min(cand, key=lambda t: abs(t - w['start']))) - .01      # l'attaque commence juste avant la montée
        bas = mots[k - 1]['start'] + .06 if k else 0.0                      # jamais avant le mot précédent
        haut = (mots[k + 1]['start'] - .06) if k + 1 < len(mots) else w['end']
        t = min(max(t, bas), haut)
        if abs(t - w['start']) >= .02:
            w['avant_affinage'] = w['start']; w['start'] = round(t, 3); bouges += 1
    for k, w in enumerate(mots[:-1]):                                       # fins cohérentes avec le mot suivant
        w['end'] = round(min(max(w['end'], w['start'] + .06), mots[k + 1]['start'] + .25), 3)
    json.dump(mots, open(f'{dossier}/mots.json', 'w'), ensure_ascii=False, indent=1)
    return bouges


PETITS = set('le la les l un une des du de d au aux ce cet cette ces mon ma mes ton ta tes son sa ses notre votre nos vos leur leurs '
              'je tu il elle on nous vous ils elles ne n qui que qu et ou mais à en y se s pour par sur avec dans très plus'.split())


def regrouper(mots):
    """Un sous-titre ne finit jamais sur un petit mot (« Cet | appareil », « la | marque ») ni sur un guillemet ouvrant :
    le mot passe dans le groupe suivant. Les mots qui finissent une phrase ne bougent pas."""
    for k in reversed(range(len(mots) - 1)):         # de la fin vers le début : « ne | se » suit « se » déplacé
        w, n = mots[k], mots[k + 1]
        if w['g'] == n['g'] or re.search(r'[.?!,;:…»"]$', w['w']): continue
        nu = re.sub(r"[^\w']", '', w['w'].lower()).split("'")[0]
        if nu in PETITS or w['w'].startswith(('"', '«')) and not w['w'].endswith(('"', '»')):
            if sum(len(m['w']) + 1 for m in mots if m['g'] == n['g']) + len(w['w']) <= 26:
                w['g'] = n['g']
    return mots


def caler(dossier):
    # La ponctuation haute française (« toi ? ») est collée au mot pour le calage, sinon « ? » deviendrait un mot.
    segs = [[a, b, re.sub(r'\s+([?!:;»])', r'\1', re.sub(r'«\s+', '«', t))] for a, b, t in json.load(open(f'{dossier}/segs.json'))]
    json.dump(segs, open(f'{dossier}/_segs_calage.json', 'w'), ensure_ascii=False)
    subprocess.run([sys.executable, f'{ICI}/.outils/mots.py', f'{dossier}/voix.wav', '--segs', f'{dossier}/_segs_calage.json',
                    f'{dossier}/mots.json'], check=True, stdout=subprocess.DEVNULL)
    os.remove(f'{dossier}/_segs_calage.json')
    affiner(dossier)
    mots = regrouper(json.load(open(f'{dossier}/mots.json')))
    json.dump(mots, open(f'{dossier}/mots.json', 'w'), ensure_ascii=False, indent=1)
    return mots


def main(src, dossier, transcription=True):
    os.makedirs(dossier, exist_ok=True)
    brut, voix = f'{dossier}/brut.wav', f'{dossier}/voix.wav'
    decoder(src, brut)
    x, _ = sf.read(brut)
    dur_brut = len(x) / SR
    raisons = []

    # Mesures sur l'audio d'origine
    sature = float(np.mean(np.abs(x) > .985))
    _, db, ref = pauses(x)
    bruit = float(np.percentile(db, 10)); snr = float(ref - bruit)

    # Nettoyage : passe-haut 70 Hz, débruitage FFT léger calé sur le bruit mesuré, compression douce, puis pauses
    nf = int(max(-80, min(-20, bruit)))
    decoder(src, f'{dossier}/_filtre.wav',
            f'highpass=f=70,afftdn=nf={nf}:nr=10:tn=1,acompressor=threshold=-24dB:ratio=2.5:attack=8:release=120:makeup=2')
    y, _ = sf.read(f'{dossier}/_filtre.wav'); os.remove(f'{dossier}/_filtre.wav')
    y = raccourcir(y)
    m = pyln.Meter(SR); lufs = m.integrated_loudness(y)
    if np.isfinite(lufs): y = pyln.normalize.loudness(y, lufs, -16.)
    pic = np.max(np.abs(y))
    if pic > .89: y = y * .89 / pic          # crête ≤ −1 dB
    sf.write(voix, y.astype(np.float32), SR, subtype='FLOAT')

    if not transcription: return     # nettoyage déterministe : les temps de segs.json / mots.json déjà calés restent valables
    segs = transcrire(y, segmenter(y))
    segs = [s for s in segs if s[2]]
    with open(f'{dossier}/segs.json', 'w') as f: json.dump(segs, f, ensure_ascii=False, indent=1)
    texte = ' '.join(s[2] for s in segs)

    mots = caler(dossier) if segs else []

    # Verdict de qualité
    dur = len(y) / SR
    debit = len(mots) / max(dur, 1e-6)
    if not mots: raisons.append('aucune parole reconnue')
    if sature > .002: raisons.append(f'saturation : {sature:.2%} des échantillons')
    if snr < 15: raisons.append(f'bruit de fond fort : rapport parole/bruit {snr:.0f} dB')
    if mots and not 1.2 <= debit <= 4.5: raisons.append(f'débit anormal : {debit:.1f} mots/s (transcription douteuse)')
    if re.search(r'(\b\w+\b)(?:\W+\1\b){3,}', texte.lower()): raisons.append('répétitions en boucle dans la transcription')
    if dur < 8: raisons.append(f'trop court : {dur:.1f} s de parole')
    grave = [r for r in raisons if r.startswith(('aucune', 'saturation', 'trop court'))] or (snr < 8 and raisons)
    verdict = 'inutilisable' if grave else 'douteux' if raisons else 'ok'

    rapport = dict(source=src, duree_brut=round(dur_brut, 2), duree_voix=round(dur, 2),
                   rapport_parole_bruit_db=round(snr, 1), saturation=round(sature, 5), mots=len(mots),
                   debit_mots_s=round(debit, 2), transcription=texte, verdict=verdict, raisons=raisons)
    json.dump(rapport, open(f'{dossier}/rapport.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(rapport, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == '--recaler':
        d = sys.argv[2].rstrip('/'); m = caler(d)
        print(f'{len(m)} mots recalés : ' + ' '.join(f"{i}:{w['w']}" for i, w in enumerate(m)))
    elif len(sys.argv) == 4 and sys.argv[1] == '--nettoyer':
        main(sys.argv[2], sys.argv[3].rstrip('/'), transcription=False)
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2].rstrip('/'))
    else:
        sys.exit(__doc__)
