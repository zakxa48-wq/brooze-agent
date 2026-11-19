import json, os
INK='#100E0D'; DOUX='#6B675F'; GRIS='#8A8780'; STUDIO='#D7D6D3'; CARTE='#F7F6F2'
NB=' '
def svg(inner,h): return f'<svg viewBox="0 0 888 {h}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
def t(x,y,s,size=40,w=800,fill=INK,anchor='middle',ls=0,op=1):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Inter" font-weight="{w}" font-size="{size}" letter-spacing="{ls}" fill="{fill}" opacity="{op}">{s}</text>'
FW,FH=390,520; XA,XB,Y=30,468,30
def cadre(x):
    return f'<rect x="{x}" y="{Y}" width="{FW}" height="{FH}" rx="18" fill="{CARTE}" stroke="{INK}" stroke-width="6"/>'
def plan_large(x,fleche):
    g=cadre(x)+f'<clipPath id="ca{fleche}"><rect x="{x+3}" y="{Y+3}" width="{FW-6}" height="{FH-6}" rx="16"/></clipPath><g clip-path="url(#ca{fleche})">'
    g+=f'<path d="M{x} {Y+300} Q{x+110} {Y+240} {x+210} {Y+290} T{x+FW} {Y+270} V{Y+FH} H{x} Z" fill="{STUDIO}"/>'
    g+=f'<path d="M{x} {Y+360} H{x+FW}" stroke="{DOUX}" stroke-width="5"/>'
    g+=f'<path d="M{x} {Y+400} H{x+FW}" stroke="{DOUX}" stroke-width="3" stroke-dasharray="18 16"/>'
    cx=x+215; cy=Y+372
    g+=f'<g transform="translate({cx} {cy}) scale(1.7) translate({-cx} {-cy})">'
    g+=f'<rect x="{cx-22}" y="{cy-14}" width="44" height="14" rx="5" fill="{INK}"/><rect x="{cx-12}" y="{cy-24}" width="22" height="12" rx="4" fill="{INK}"/>'
    g+=f'<circle cx="{cx-13}" cy="{cy+1}" r="5" fill="{INK}"/><circle cx="{cx+13}" cy="{cy+1}" r="5" fill="{INK}"/>'
    for k in range(3): g+=f'<path d="M{cx-40-k*6} {cy-18+k*8} H{cx-90-k*14}" stroke="{GRIS}" stroke-width="5" stroke-linecap="round"/>'
    g+='</g>'
    if fleche:
        g+=f'<path d="M{cx-6} {cy+40} H{cx+40}" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><path d="M{cx+28} {cy+28} L{cx+42} {cy+40} L{cx+28} {cy+52}" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    return g+'</g>'
def gros_plan(x,fleche):
    g=cadre(x)+f'<clipPath id="cb{fleche}"><rect x="{x+3}" y="{Y+3}" width="{FW-6}" height="{FH-6}" rx="16"/></clipPath><g clip-path="url(#cb{fleche})">'
    cx=x+168; top=Y+140
    g+=f'<path d="M{x-10} {Y+500} H{x+FW+10}" stroke="{STUDIO}" stroke-width="60"/>'
    g+=f'<path d="M{cx-158} {top} H{cx+158} L{cx+136} {top+340} Q{cx+128} {top+362} {cx+106} {top+362} H{cx-106} Q{cx-128} {top+362} {cx-136} {top+340} Z" fill="{CARTE}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
    g+=f'<ellipse cx="{cx}" cy="{top}" rx="158" ry="32" fill="{STUDIO}" stroke="{INK}" stroke-width="7"/>'
    g+=f'<path d="M{cx+152} {top+80} C{cx+222} {top+80} {cx+222} {top+250} {cx+140} {top+250}" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round"/>'
    if fleche:
        g+=f'<path d="M{cx-120} {top-70} Q{cx} {top-130} {cx+150} {top-70}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><path d="M{cx+128} {top-92} L{cx+152} {top-68} L{cx+120} {top-58}" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    else:
        g+=f'<path d="M{cx-40} {top-70} Q{cx} {top-88} {cx+40} {top-70}" fill="none" stroke="{GRIS}" stroke-width="6" stroke-linecap="round"/>'
    return g+'</g>'
g1=plan_large(XA,False)+gros_plan(XB,False)+t(XA+FW/2,Y+FH+70,'A',60)+t(XB+FW/2,Y+FH+70,'B',60)
g1+=t(XA+FW/2,Y+FH+122,'une voiture',38,700,DOUX)+t(XA+FW/2,Y+FH+168,'fonce au loin',38,700,DOUX)+t(XB+FW/2,Y+FH+122,'une tasse',38,700,DOUX)+t(XB+FW/2,Y+FH+168,'tourne lentement',38,700,DOUX)
g2=plan_large(XA,True)+gros_plan(XB,True)+t(XA+FW/2,Y+FH+70,'A',60,700,DOUX)+t(XB+FW/2,Y+FH+70,'B',60)
g2+=t(XA+FW/2,Y+FH+122,'petit trajet',38,700,DOUX)+t(XA+FW/2,Y+FH+168,'à l’écran',38,700,DOUX)+t(XB+FW/2,Y+FH+122,'grand trajet',38,800,INK)+t(XB+FW/2,Y+FH+168,'à l’écran',38,800,INK)
post={
 "type":"story","role":"attirer","nouveau_format":True,"avatar":"Karim","pilier":"Devine",
 "angle":"Devinette de monteur : un plan large où une voiture fonce au loin contre un gros plan où une tasse tourne doucement ; pour les monteurs, la taille du sujet dans le cadre pèse autant que sa vitesse sur le tempo perçu",
 "hypothese":"Une devinette dont la réponse va contre l'intuition (le lent paraît plus rapide) surprend et fait répondre A ou B en message.",
 "savoir":["A-0031"],
 "source":"Monteurs praticiens, pas une étude : Inside The Edit, « Pacing in Film Editing » (https://www.youtube.com/watch?v=CdyTIng0M8Q) et StudioBinder, « What Is Pacing? » (https://www.youtube.com/watch?v=a9reuDw4cnU) ; S-0042, S-0043",
 "emotion":{"quoi":"surprise","comment":"on choisit la voiture qui fonce ; la réponse des monteurs est la tasse, et le dessin montre pourquoi (le trajet à l'écran)","ou":"image 2"},
 "slides":[
  {"layout":"visuel","fond":"papier","label":"Devine","titre":f"Deux plans de 2{NB}secondes. Lequel paraît le plus *rapide*{NB}?","texte":"Choisis avant de passer.","svg":svg(g1,740),"h":740,"taille":"t-m"},
  {"layout":"visuel","fond":"papier","label":"Ce que disent les monteurs","titre":f"Pour un monteur, c’est *B*.","texte":f"Plus le sujet remplit le cadre, plus le moindre geste traverse l’écran, et plus il paraît rapide. Le rythme se règle aussi au cadrage. Et toi, A ou B{NB}? Réponds en message.","svg":svg(g2,740),"h":740,"taille":"t-m"}
 ]}
json.dump(post,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'post.json'),'w'),ensure_ascii=False,indent=1)
