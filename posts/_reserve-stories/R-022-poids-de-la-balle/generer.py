import json, os
INK='#100E0D'; DOUX='#6B675F'; GRIS='#8A8780'; STUDIO='#D7D6D3'; CARTE='#F7F6F2'
NB='\u00a0'
def svg(inner,h): return f'<svg viewBox="0 0 888 {h}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
def t(x,y,s,size=40,w=800,fill=INK,anchor='middle',ls=0,op=1):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Inter" font-weight="{w}" font-size="{size}" letter-spacing="{ls}" fill="{fill}" opacity="{op}">{s}</text>'
SOL=560
# même surface pour les trois balles (rx*ry ≈ 92²) : seule la déformation change
balles=[(178,'A',140,60),(470,'B',108,78),(740,'C',92,92)]
def balle(cx,rx,ry,traits=True):
    g=''
    if traits:
        for k,dx in enumerate((-34,0,34)):
            g+=f'<path d="M{cx+dx} {SOL-2*ry-230+k*22} V{SOL-2*ry-36}" stroke="{GRIS}" stroke-width="10" stroke-linecap="round" opacity="0.55"/>'
    g+=f'<ellipse cx="{cx}" cy="{SOL+16}" rx="{rx*1.05:.0f}" ry="10" fill="{STUDIO}"/>'
    g+=f'<ellipse cx="{cx}" cy="{SOL-ry}" rx="{rx}" ry="{ry}" fill="{CARTE}" stroke="{INK}" stroke-width="7"/>'
    g+=f'<ellipse cx="{cx-rx*0.38:.0f}" cy="{SOL-ry*1.45:.0f}" rx="{rx*0.22:.0f}" ry="{ry*0.16:.0f}" fill="{STUDIO}"/>'
    return g
g1=f'<path d="M24 {SOL+3} H864" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
for cx,l,rx,ry in balles:
    g1+=balle(cx,rx,ry)+t(cx,SOL+110,l,64,800)
noms={'A':'mousse','B':'caoutchouc','C':'bowling'}
g2=f'<path d="M24 {SOL+3} H864" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
for cx,l,rx,ry in balles:
    g2+=balle(cx,rx,ry,False)+t(cx,SOL+92,f'{l} · {noms[l]}',38,800 if l=='C' else 700,INK if l=='C' else DOUX)
g2+=t(444,SOL-232,'même volume, seule la forme change',34,700,DOUX,'middle',1)
g2=f'<g transform="translate(0 -150)">{g2}</g>'
post={
 "type":"story","role":"attirer","nouveau_format":True,"avatar":"Claire","pilier":"Devine",
 "angle":"Jeu : trois balles identiques au moment de l'impact, seule la déformation change ; deviner la plus lourde. Règle d'animation (écrasement et étirement) : la déformation dit la matière, le volume reste constant ; c'est ce qui donne du poids à un logo animé",
 "hypothese":"Un jeu où le spectateur trouve la bonne réponse sans savoir pourquoi (puis apprend pourquoi) donne une petite fierté et des réponses en message.",
 "savoir":["A-0011"],
 "source":"Écrasement et étirement, 1er des 12 principes de l'animation : F. Thomas & O. Johnston, The Illusion of Life (1981) ; https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation (S-0016, S-0017)",
 "emotion":{"quoi":"fierté (« je le savais sans le savoir »)","comment":"on désigne C d'instinct, sur la seule forme ; l'image 2 confirme et donne la règle que l'œil connaissait déjà","ou":"image 1 (le choix) puis image 2"},
 "slides":[
  {"layout":"visuel","fond":"papier","label":"Devine","titre":f"Trois balles touchent le sol. Laquelle est la{NB}plus *lourde*{NB}?","texte":"Réponds dans ta tête avant de passer.","svg":svg(g1,700),"h":700,"taille":"t-m"},
  {"layout":"visuel","fond":"papier","label":"La réponse","titre":f"C{NB}: celle qui s’écrase *le moins*.","texte":f"Règle des animateurs (The Illusion of Life, 1981){NB}: plus un objet est dur et lourd, moins il s’écrase, et son volume ne change pas. C’est ce qui donne du poids à un logo qui tombe. Trouvé{NB}? Dis-le-nous en message.","svg":svg(g2,530),"h":530,"taille":"t-m"}
 ]}
json.dump(post,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'post.json'),'w'),ensure_ascii=False,indent=1)
