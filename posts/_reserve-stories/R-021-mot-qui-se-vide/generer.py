import json, os
INK='#100E0D'; DOUX='#6B675F'; GRIS='#8A8780'; STUDIO='#D7D6D3'; CARTE='#F7F6F2'
NB=' '
def svg(inner,h): return f'<svg viewBox="0 0 888 {h}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
def t(x,y,s,size=40,w=800,fill=INK,anchor='middle',ls=0,op=1,rot=0):
    tr=f' transform="rotate({rot} {x} {y})"' if rot else ''
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Inter" font-weight="{w}" font-size="{size}" letter-spacing="{ls}" fill="{fill}" opacity="{op}"{tr}>{s}</text>'
# image 1 : « lundi » x20 ; le mot se défait au fil des répétitions (espacement, couleur, angle, décalage)
cols=[132,354,576,778]; img1=''
jit=[0,0,0,0,0,0,0,0,-1,1,0,-2,2,-2,3,-3,5,-6,7,-9]
dy=[0]*14+[4,-6,8,-10,12,-14]
for i in range(20):
    r,c=divmod(i,4); x=cols[c]; y=78+r*150+dy[i]; k=i/19
    col = INK if k<0.45 else (DOUX if k<0.8 else GRIS)
    mot = 'lundi' if i<18 else ('lun' if i==18 else 'di')
    img1+=t(x,y,mot,58,800 if k<0.6 else 700,col,'middle',round(k*5,1),round(1-0.45*k,2),jit[i])
# image 2 : le sens (un calendrier) → le son (une onde)
g=f'<rect x="70" y="60" width="230" height="230" rx="26" fill="{CARTE}" stroke="{INK}" stroke-width="6"/>'
g+=f'<rect x="70" y="60" width="230" height="64" rx="26" fill="{INK}"/><rect x="70" y="100" width="230" height="24" fill="{INK}"/>'
g+=t(185,106,'LUNDI',34,800,CARTE,'middle',3)
for rr in range(3):
    for cc in range(4):
        g+=f'<rect x="{100+cc*46}" y="{148+rr*44}" width="32" height="30" rx="6" fill="{STUDIO if (rr,cc)!=(1,0) else INK}"/>'
g+=f'<path d="M345 175 H505" stroke="{DOUX}" stroke-width="8" stroke-linecap="round"/><path d="M480 148 L512 175 L480 202" stroke="{DOUX}" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
import math
pts=' '.join(f'{560+i*5:.0f},{175+math.sin(i*0.55)*(18+60*abs(math.sin(i*0.13))):.1f}' for i in range(53))
g+=f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
g+=t(185,352,'LE SENS',34,700,DOUX,'middle',3)+t(690,352,'LE SON',34,700,DOUX,'middle',3)
post={
 "type":"story","role":"attirer","nouveau_format":True,"avatar":"Claire","pilier":"Fais le test",
 "angle":"Mini-expérience à faire soi-même : répéter un mot à voix haute lui fait perdre son sens (saturation sémantique) ; au montage, un mot répété devient un rythme",
 "hypothese":"Une expérience que le spectateur fait sur lui-même (il le dit à voix haute) provoque un sourire et des réponses en message, plus qu'un quiz où il regarde.",
 "savoir":["A-0036","A-0033"],
 "source":"Saturation sémantique : L. Jakobovits James (1962), décrite dès Severance & Washburn (1907) ; https://en.wikipedia.org/wiki/Semantic_satiation et Margulis et al. (2015), Frontiers in Psychology 6:48",
 "emotion":{"quoi":"rire (sourire amusé)","comment":"en le disant vingt fois, le mot familier devient un drôle de son ; l'image 2 nomme ce qu'on vient de sentir","ou":"pendant le test (image 1) puis image 2"},
 "slides":[
  {"layout":"visuel","fond":"papier","label":"Fais le test","titre":"Dis «"+NB+"*lundi*"+NB+"» à voix haute, 20"+NB+"fois, vite.","texte":"Sans t’arrêter. Ensuite, passe.","svg":svg(img1,730),"h":730,"taille":"t-m"},
  {"layout":"visuel","fond":"papier","label":"Ce qui vient de se passer","titre":"À la fin, «"+NB+"lundi"+NB+"» ne voulait plus rien dire"+NB+"?","texte":"C’est la saturation sémantique"+NB+": répété, un mot perd son sens un moment, il ne reste qu’un son. Au montage, un mot répété devient un rythme. Ça a marché sur toi"+NB+"? Dis-le-nous en message.","svg":svg(g,380),"h":380,"taille":"t-m"}
 ]}
json.dump(post,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'post.json'),'w'),ensure_ascii=False,indent=1)
