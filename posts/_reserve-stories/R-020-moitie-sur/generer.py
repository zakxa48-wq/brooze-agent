import json, os
INK='#100E0D'; DOUX='#6B675F'; STUDIO='#D7D6D3'; CARTE='#F7F6F2'; CU='#C8834A'
NB=' '
def svg(inner,h): return f'<svg viewBox="0 0 888 {h}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
def t(x,y,s,size=36,w=700,fill=INK,anchor='start',ls=0):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="Inter" font-weight="{w}" font-size="{size}" letter-spacing="{ls}" fill="{fill}">{s}</text>'
def carte(y,lettre,lignes,fond=CARTE):
    s=f'<rect x="40" y="{y}" width="808" height="180" rx="28" fill="{fond}" stroke="{INK}" stroke-width="6"/>'
    s+=f'<circle cx="120" cy="{y+90}" r="46" fill="none" stroke="{INK}" stroke-width="7"/>'+t(120,y+109,lettre,52,800,INK,'middle')
    for i,l in enumerate(lignes):
        s+=t(196,y+78+i*50,l,38,700)
    return s
img1 = carte(20,"A",["Combien de pattes","a une araignée"+NB+"?"]) \
     + carte(230,"B",["Quel instrument a été inventé","pour imiter la voix humaine"+NB+"?"]) \
     + carte(440,"C",["Quel est le troisième mot de la","page 212 de mon dictionnaire"+NB+"?"])
# image 2 : courbe en U inversé, curiosité selon la confiance
X0,X1,Y0,YT=110,820,420,100
def px(p): return X0+(X1-X0)*p
def py(c): return Y0-(Y0-YT)*c
pts=' '.join(f'{px(i/40):.1f},{py(4*(i/40)*(1-i/40)*0.92+0.04):.1f}' for i in range(2,39))
g = f'<path d="M{X0} {YT-30} V{Y0} H{X1+30}" stroke="{DOUX}" stroke-width="5" fill="none" stroke-linecap="round"/>'
g+= f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
def dot(p,c,l,col,lab_dy=-36):
    x,y=px(p),py(c)
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="30" fill="{col}" stroke="{INK}" stroke-width="5"/>'+t(x,y+13,l,36,800,CARTE if col!=CARTE else INK,'middle')
g+= dot(0.03,4*0.03*0.97*0.92+0.04,"C",CARTE) + dot(0.5,0.96,"B",CU) + dot(0.97,4*0.03*0.97*0.92+0.04,"A",CARTE)
g+= t(X0-10,YT-46,"CURIOSITÉ",34,700,DOUX,'start',3)
g+= t(X0,Y0+62,"JE N’EN SAIS RIEN",34,700,DOUX,'start',2) + t(X1+30,Y0+62,"JE SAIS",34,700,DOUX,'end',2)
g+= t(444,Y0+106,"À QUEL POINT TU ES SÛR DE TA RÉPONSE",34,700,INK,'middle',2)
post={
 "type":"story","role":"attirer","nouveau_format":False,"avatar":"Claire","pilier":"Devine",
 "angle":"Test : la curiosité est maximale quand on est à moitié sûr de sa réponse (Kang et al. 2009) ; c'est pour ça qu'un bon hook pose une question où l'on hésite",
 "hypothese":"Un test où le spectateur se reconnaît (il a choisi B) puis comprend pourquoi donne envie de répondre en message et relie la curiosité au métier (hook).",
 "savoir":["A-0032"],
 "source":"Kang et al. (2009), Psychological Science 20(8):963-973, https://doi.org/10.1111/j.1467-9280.2009.02402.x (question B et sa réponse tirées de l'exemple de l'étude)",
 "emotion":{"quoi":"curiosité","comment":"image 1 : la question B donne envie de connaître la réponse ; image 2 : on découvre pourquoi on a choisi B, et la réponse (le violon)","ou":"image 1 puis image 2"},
 "slides":[
  {"layout":"visuel","fond":"papier","label":"Test","titre":"Laquelle te donne le plus envie de connaître la réponse"+NB+"?","texte":"Choisis avant de passer.","svg":svg(img1,640),"h":640,"taille":"t-m"},
  {"layout":"visuel","fond":"papier","label":"Réponse","titre":"Sûrement B"+NB+": tu hésites, donc tu veux savoir.","texte":"La curiosité culmine quand on est à moitié sûr (Kang et al., 2009)"+NB+"; trop facile ou impossible, elle retombe. Un bon hook joue là-dessus. B"+NB+"? Le violon, d’après l’étude. Tu avais choisi laquelle"+NB+"?","svg":svg(g,560),"h":560,"taille":"t-m"}
 ]}
json.dump(post,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'post.json'),'w'),ensure_ascii=False,indent=1)
