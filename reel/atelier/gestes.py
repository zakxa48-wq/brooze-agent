"""Gestes de l'Atelier : des SAVOIR-FAIRE réutilisables (comment bouger), jamais des visuels tout faits.
Chaque geste vient d'une technique validée (reel/techniques/techniques.json) et cite ses principes. Un geste renvoie
des valeurs animées (K ou fonctions) que la scène branche où elle veut ; il ne décide ni du contenu ni du style.
"""
import math
from . import K, lin, doux, chute, sortie, val


def choc(t_contact, amplitude=12., tau=.035, montee=.012):
    """Choc caméra d'impact (P-031) : à plein dès le contact, retour amorti critique sans dépassement. La caméra encaisse
    le coup : brancher -choc(...) en y (l'image remonte), sinon le mot dépasse sa place dans le sens de la chute.
    → fonction t ↦ décalage en px (à brancher sur Decaler(dy=…) d'un calque de réglage)."""
    def f(t):
        u = t - t_contact
        if u < 0: return 0.
        if u < montee: return amplitude * u / montee
        u -= montee
        return amplitude * (1 + u / tau) * math.exp(-u / tau)
    return f


def lire_tomber_frapper(t_contact, lecture=(1.26, 1.28), chute_s=.2, anticipation_s=.14, puissance=3):
    """Arrivée d'un mot-impact en trois temps (P-037, technique mot-qui-tombe, validée 8/10 le 22/10) :
    LIRE (échelle de lecture, quasi immobile, petite anticipation) → TOMBER (≤ 0,2 s, chute en t^puissance vers 1,0)
    → FRAPPER au contact. Renvoie dict(echelle, trainee, descente, ombre_distance, ombre_flou, ombre_opacite) animés : à brancher sur le
    calque (echelle, position y + descente), un FlouDirectionnel(longueur=trainee, angle=90) et son OmbrePortee. Le contact tombe au MILIEU de l'obturation d'une image (P-035) : choisis
    t_contact = (n + 0,5) / ips."""
    lire, haut = lecture
    t0 = t_contact - chute_s; ta = t0 - anticipation_s
    echelle = K((0, lire, lin), (ta, lire, doux), (t0, haut, chute(puissance)), (t_contact, 1.0))
    def hauteur(t):                                            # 1 en lecture, 0 au contact (pour l'ombre)
        e = val(echelle, t); return max(0., (e - 1) / (haut - 1))
    def vitesse(t, dt=1 / 240):                                  # vitesse d'échelle (par seconde)
        return abs(val(echelle, t + dt) - val(echelle, t - dt)) / (2 * dt)
    return dict(echelle=echelle,
                trainee=lambda t: 75 * min(1., vitesse(t) / max(1e-6, vitesse(t_contact - 1 / 240))),   # flou vertical ∝ vitesse
                descente=K((0, -34, lin), (t0, -34, chute(puissance)), (t_contact, 0)),               # il « descend » vers sa place
                ombre_distance=lambda t: 6 + 110 * math.sqrt(hauteur(t)),
                ombre_flou=lambda t: 2.5 + 34 * math.sqrt(hauteur(t)),
                ombre_opacite=lambda t: .40 - .22 * math.sqrt(hauteur(t)))


def poussee_tenue(t_debut, t_fin, quantite=.018):
    """Tenue vivante (P-032) : poussée de caméra lente (1,5–2 %), démarrage et fin doux. → facteur d'échelle."""
    return K((t_debut, 1.0, doux), (t_fin, 1.0 + quantite))
