import json, os
INK='#100E0D'; DOUX='#6B675F'; STUDIO='#D7D6D3'; CARTE='#F7F6F2'; CU='#C8834A'; GRIS='#8A8780'
def pellicule(y, n, coupe_cu=None, labels=True):
    W=808; x0=40; h=200; s=f'<rect x="{x0}" y="{y}" width="{W}" height="{h}" rx="14" fill="{INK}"/>'
    for i in range(22):
        px=x0+16+i*36.5
        s+=f'<rect x="{px}" y="{y+12}" width="18" height="14" rx="3" fill="{CARTE}"/><rect x="{px}" y="{y+h-26}" width="18" height="14" rx="3" fill="{CARTE}"/>'
    fw=(W-24)/n
    for i in range(n):
        fx=x0+12+i*fw
        s+=f'<rect x="{fx+5}" y="{y+40}" width="{fw-10}" height="{h-80}" rx="6" fill="{STUDIO if i%2 else CARTE}"/>'
        cx=fx+fw/2; cy=y+h/2
        # silhouette simple : tête + épaules
        k=[1.0,1.6,0.75,1.35,0.9,1.7,1.1][i%7]; dx=[0,8,-10,6,12,-6,0][i%7]
        s+=f'<clipPath id="c{y}_{i}"><rect x="{fx+5}" y="{y+40}" width="{fw-10}" height="{h-80}" rx="6"/></clipPath><g clip-path="url(#c{y}_{i})"><g transform="translate({cx+dx} {cy+40}) scale({k}) translate({-cx} {-cy-40})">'
        s+=f'<circle cx="{cx}" cy="{cy-14}" r="17" fill="{DOUX}"/><path d="M{cx-34} {cy+40} C{cx-30} {cy+8} {cx+30} {cy+8} {cx+34} {cy+40} Z" fill="{DOUX}"/></g></g>'
    for i in range(1,n):
        fx=x0+12+i*fw; c = CU if coupe_cu==i else CARTE
        w = 10 if coupe_cu==i else 6
        s+=f'<path d="M{fx} {y-18} V{y+h+18}" stroke="{c}" stroke-width="{w}" stroke-linecap="round"/>'
    return s
def carte(x,y,lettre,txt):
    return (f'<rect x="{x}" y="{y}" width="250" height="250" rx="28" fill="{CARTE}" stroke="{INK}" stroke-width="6"/>'
            f'<circle cx="{x+125}" cy="{y+82}" r="48" fill="none" stroke="{INK}" stroke-width="7"/>'
            f'<text x="{x+125}" y="{y+102}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="54" fill="{INK}">{lettre}</text>'
            f'<text x="{x+125}" y="{y+200}" text-anchor="middle" font-family="Inter" font-weight="800" font-size="40" fill="{INK}">{txt}</text>')
def svg(inner,h): return f'<svg viewBox="0 0 888 {h}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
img1 = pellicule(30,6) + f'<text x="444" y="300" text-anchor="middle" font-family="Inter" font-weight="700" font-size="28" letter-spacing="3" fill="{DOUX}">UN TRAIT = UNE COUPE</text>' + carte(40,340,"A","Aucune") + carte(319,340,"B","1 sur 50") + carte(598,340,"C","1 sur 6")
img2 = pellicule(80,7,coupe_cu=4) + f'<text x="444" y="40" text-anchor="middle" font-family="Inter" font-weight="700" font-size="30" letter-spacing="3" fill="{INK}">6 COUPES · 1 RATÉE</text>' \
  + f'<text x="444" y="370" text-anchor="middle" font-family="Inter" font-weight="700" font-size="28" letter-spacing="3" fill="{DOUX}">COUPE SUR UN GESTE : 1 SUR 3</text>'
post={"type":"story","role":"attirer","nouveau_format":False,"avatar":"Karim","pilier":"Devine",
 "angle":"Devine : même quand on leur demande de repérer les coupes, des spectateurs en ratent environ 1 sur 6 (coupes invisibles)",
 "hypothese":"Un quiz en 2 images dont la réponse paraît impossible (on rate des coupes alors qu'on les cherche) surprend et relie au métier de monteur.",
 "savoir":["A-0025"],
 "source":"Smith & Henderson (2008), Journal of Eye Movement Research 2(2):6, https://doi.org/10.16910/jemr.2.2.6",
 "emotion":{"quoi":"surprise","comment":"on choisit « aucune » (on les cherche, on ne peut pas les rater) ; la réponse est 1 sur 6, et 1 sur 3 en coupant sur un geste","ou":"image 2"},
 "slides":[
  {"layout":"visuel","fond":"papier","label":"Devine","titre":"Des gens devaient taper à chaque coupe d’un film. Combien en ont-ils ratées ?","texte":"Choisis avant de passer.","svg":svg(img1,620),"h":620,"taille":"t-m"},
  {"layout":"visuel","fond":"papier","label":"Réponse","titre":"C. Environ 1 sur 6, alors qu’ils les cherchaient.","texte":"Et près de 1 sur 3 quand la coupe tombe pendant un geste (Smith et Henderson, 2008, 7 spectateurs). C’est comme ça qu’on monte : la coupe ne se voit pas. Tu avais choisi laquelle ?","svg":svg(img2,400),"h":400,"taille":"t-m"}
 ]}
d='/home/user/brooze-agent/posts/_reserve-stories/R-019-coupes-ratees'; os.makedirs(d,exist_ok=True)
json.dump(post,open(d+'/post.json','w'),ensure_ascii=False,indent=1)
