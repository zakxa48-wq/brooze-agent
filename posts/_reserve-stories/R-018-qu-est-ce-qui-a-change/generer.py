import json, os
INK='#100E0D'; DOUX='#6B675F'; STUDIO='#D7D6D3'; CARTE='#F7F6F2'; CU='#C8834A'; GRIS='#8A8780'
def livres(x,y):
    s=''; xs=x
    for w,h,c in [(38,170,INK),(30,150,DOUX),(44,182,STUDIO),(28,140,INK)]:
        s+=f'<rect x="{xs}" y="{y-h}" width="{w}" height="{h}" rx="4" fill="{c}" stroke="{INK}" stroke-width="4"/>'
        s+=f'<rect x="{xs+6}" y="{y-h+22}" width="{w-12}" height="6" fill="{CARTE if c!=STUDIO else INK}" opacity="0.7"/>'
        xs+=w+4
    return s
def plante(x,y):
    s=f'<path d="M{x-46} {y-96} L{x+46} {y-96} L{x+34} {y} L{x-34} {y} Z" fill="{STUDIO}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
    for dx,dy,r in [(-34,-170,-30),(30,-178,28),(0,-215,0),(-52,-128,-55),(50,-132,52)]:
        s+=f'<ellipse cx="{x+dx}" cy="{y+dy}" rx="20" ry="46" transform="rotate({r} {x+dx} {y+dy})" fill="{DOUX}" stroke="{INK}" stroke-width="4"/>'
    return s
def horloge(x,y):
    return (f'<circle cx="{x}" cy="{y-80}" r="76" fill="{CARTE}" stroke="{INK}" stroke-width="6"/>'
            + ''.join(f'<path d="M{x} {y-148} V{y-136}" stroke="{INK}" stroke-width="5" transform="rotate({a} {x} {y-80})"/>' for a in range(0,360,30))
            + f'<path d="M{x} {y-80} L{x} {y-130}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><path d="M{x} {y-80} L{x+38} {y-62}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><circle cx="{x}" cy="{y-80}" r="7" fill="{INK}"/>')
def appareil(x,y):
    return (f'<rect x="{x-80}" y="{y-112}" width="160" height="112" rx="16" fill="{INK}"/>'
            f'<rect x="{x-46}" y="{y-134}" width="56" height="26" rx="6" fill="{INK}"/>'
            f'<circle cx="{x+6}" cy="{y-56}" r="40" fill="{STUDIO}" stroke="{CARTE}" stroke-width="6"/><circle cx="{x+6}" cy="{y-56}" r="20" fill="{DOUX}"/>'
            f'<rect x="{x+44}" y="{y-100}" width="22" height="12" rx="3" fill="{STUDIO}"/>')
def tasse(x,y):
    return (f'<path d="M{x+42} {y-86} C{x+84} {y-86} {x+84} {y-30} {x+42} {y-30}" fill="none" stroke="{INK}" stroke-width="10"/>'
            f'<rect x="{x-50}" y="{y-110}" width="96" height="110" rx="14" fill="{CARTE}" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M{x-20} {y-130} q10 -18 0 -36 M{x+10} {y-130} q10 -18 0 -36" stroke="{GRIS}" stroke-width="5" fill="none" stroke-linecap="round"/>')
def lampe(x,y):
    return (f'<rect x="{x-56}" y="{y-16}" width="112" height="16" rx="8" fill="{INK}"/>'
            f'<path d="M{x} {y-16} L{x-30} {y-140} L{x+40} {y-210}" fill="none" stroke="{INK}" stroke-width="10" stroke-linejoin="round" stroke-linecap="round"/>'
            f'<path d="M{x+20} {y-246} L{x+96} {y-170} L{x+62} {y-150} L{x+4} {y-210} Z" fill="{DOUX}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
def cadre(x,y):
    return (f'<rect x="{x-62}" y="{y-150}" width="124" height="150" rx="6" fill="{CARTE}" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M{x-44} {y-24} L{x-10} {y-80} L{x+12} {y-50} L{x+24} {y-66} L{x+44} {y-24} Z" fill="{DOUX}"/><circle cx="{x+24}" cy="{y-110}" r="12" fill="{STUDIO}" stroke="{INK}" stroke-width="3"/>')
def vase(x,y):
    return f'<path d="M{x-18} {y-120} L{x+18} {y-120} L{x+14} {y-96} C{x+44} {y-70} {x+40} {y-10} {x+22} {y} L{x-22} {y} C{x-40} {y-10} {x-44} {y-70} {x-14} {y-96} Z" fill="{STUDIO}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
def clap(x,y):
    s=f'<rect x="{x-70}" y="{y-96}" width="140" height="96" rx="8" fill="{INK}"/>'
    s+=f'<g transform="rotate(-14 {x-70} {y-100})"><rect x="{x-70}" y="{y-128}" width="140" height="28" rx="4" fill="{CARTE}" stroke="{INK}" stroke-width="5"/>'
    s+=''.join(f'<path d="M{x-58+i*32} {y-100} L{x-40+i*32} {y-128}" stroke="{INK}" stroke-width="10"/>' for i in range(4))+'</g>'
    s+=f'<rect x="{x-52}" y="{y-66}" width="104" height="8" fill="{GRIS}"/><rect x="{x-52}" y="{y-40}" width="70" height="8" fill="{GRIS}"/>'
    return s
def etagere(swap, scale=1.0, tx=0, ty=0, fleche=False):
    top=400; bot=800
    A = horloge if not swap else tasse
    B = tasse if not swap else horloge
    s=f'<g transform="translate({tx} {ty}) scale({scale})">'
    s+=f'<rect x="20" y="20" width="848" height="840" rx="28" fill="{CARTE}" stroke="{INK}" stroke-width="6"/>'
    for yy in (top,bot):
        s+=f'<rect x="20" y="{yy}" width="848" height="22" fill="{STUDIO}" stroke="{INK}" stroke-width="5"/>'
    s+=livres(56,top)+plante(290,top)+A(470,top)+cadre(640,top)+vase(790,top)
    s+=lampe(110,bot)+B(285,bot)+clap(440,bot)+appareil(600,bot)+livres(704,bot).replace(f'fill="{STUDIO}"',f'fill="{CARTE}"').replace('rect x="','rect data-l="1" x="')
    if fleche:
        s+=f'<g fill="none" stroke="{CU}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"><path d="M486 448 C 500 540, 420 590, 330 622"/><path d="M366 598 L326 624 L368 642"/><path d="M462 474 L486 444 L508 476"/></g>'
    s+='</g>'; return s
def svg(inner,h=880): return f'<svg viewBox="0 0 888 {h}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
post={
 "type":"story","role":"attirer","nouveau_format":True,"avatar":"Claire","pilier":"Devine",
 "angle":"Fais le test : un changement gros comme une plante qui passe inaperçu derrière une coupe (cécité au changement)",
 "hypothese":"Un jeu « qu'est-ce qui a changé ? » où la coupe entre deux images cache un échange d'objets, puis la vraie étude, donne envie de répondre et de partager.",
 "savoir":["A-0026","A-0025"],
 "source":"Simons & Levin (1998), Psychonomic Bulletin & Review 5(4), 644-649, https://link.springer.com/content/pdf/10.3758/BF03208840.pdf",
 "emotion":{"quoi":"surprise","comment":"on cherche un petit détail, ce sont deux objets bien visibles qui ont échangé leur place","ou":"image 3"},
 "slides":[
  {"layout":"visuel","fond":"papier","label":"Fais le test","titre":"Regarde bien cette étagère.","texte":"Retiens tout. Puis passe, sans revenir en arrière.","svg":svg(etagere(False)),"h":880,"taille":"t-m"},
  {"layout":"visuel","fond":"papier","label":"Fais le test","titre":"Qu’est-ce qui a changé ?","texte":"Réponds dans ta tête avant de passer.","svg":svg(etagere(True)),"h":880,"taille":"t-m"},
  {"layout":"visuel","fond":"papier","label":"Réponse","titre":"L’horloge et la tasse ont échangé leur place.","texte":"Une personne remplacée derrière une porte qui passe : 7 passants sur 15 l’ont vu (Simons et Levin, 1998). Au montage, on cache nos coupes pareil. Tu l’avais vu ?","svg":svg(etagere(True,scale=0.72,tx=124,fleche=True),640),"h":640,"taille":"t-m"}
 ]}
d='/home/user/brooze-agent/posts/_reserve-stories/R-018-qu-est-ce-qui-a-change'; os.makedirs(d,exist_ok=True)
json.dump(post,open(d+'/post.json','w'),ensure_ascii=False,indent=1)
