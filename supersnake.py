#coding:utf-8
import random,pygame,time,os
from pygame.locals import *

btex,btey=1000,900
mmtex,mmtey=1280,1024

pygame.init()

io = pygame.display.Info()
mtex,mtey=io.current_w,io.current_h
tex,tey=int(btex/mmtex*mtex),int(btey/mmtey*mtey)
fenetre=pygame.display.set_mode([tex,tey])
pygame.display.set_caption("SuperSnake")

ffont="Serif"

clf=(80,30,200)

def rcl(): return (random.randint(10,240),random.randint(10,240),random.randint(10,240))

def rx(x): return int(x/btex*tex)
def ry(y): return int(y/btey*tey)

def bouton(x,y,tx,ty,cl):
    tb=2
    b=pygame.draw.rect(fenetre,cl,(rx(x),ry(y),rx(tx),ry(ty)),0)
    pygame.draw.rect(fenetre,(0,0,0),(rx(x),ry(y),rx(tx),ry(ty)),tb)
    return b

def texte(texte,x,y,taille,cl):
    fenetre.blit( pygame.font.SysFont(ffont,taille).render(texte,taille,cl) , [rx(x),ry(y)] )

clobjs=[(70,70,70),(150,150,150),(230,230,230),(70,0,0),(150,0,0),(230,0,0)]
clm=(245,245,245)

pkeys=[[K_UP,K_DOWN,K_LEFT,K_RIGHT],[K_KP8,K_KP2,K_KP4,K_KP6],[K_o,K_l,K_k,K_m],[K_t,K_g,K_f,K_h]]

################################jeu

class Snake:
    def __init__(self,x,y,cl,tmin):
        self.posX=x
        self.posY=y
        self.cl=cl
        self.sens=random.choice(["up","down","left","right"])
        self.cubes=[]
        for t in range(2):
            xx,yy=0,0
            if self.sens=="up": yy=+t
            elif self.sens=="down": yy=-t
            elif self.sens=="left": xx=+t
            elif self.sens=="right": xx=-t
            if False: cll=(150,50,0)
            else: cll=self.cl
            c=[self.posX+xx,self.posY+yy,cll,self.sens,self.sens]
            self.cubes.append(c)
        self.keys=[None,None,None,None,None]
        self.points=0
        self.cible=None
        self.taille=tmin
        self.perdu=False
        self.player=0
        self.agr=tmin-1
    def bouger(self,aa):
        if aa == "up": self.sens=aa
        elif aa == "down": self.sens=aa
        elif aa == "left": self.sens=aa
        elif aa == "right": self.sens=aa
            
def affgame(snakes,cubes,mis,tx,ty,objs,affbords,affquadr):
    fenetre.fill(clf)
    bpx,bpy=rx(50),ry(50)
    tc=rx(750)/tx
    pygame.draw.rect(fenetre,(5,5,5),(bpx,bpy,(tx+1)*tc,(ty+1)*tc),0)
    if affquadr:
        for x in range(0,tx+2):
            pygame.draw.line(fenetre,(200,200,200),(bpx+tc*x,bpy),(bpx+tc*x,bpy+(tc*(ty+1))),1)
        for y in range(0,ty+2):
            pygame.draw.line(fenetre,(200,200,200),(bpx,bpy+tc*y),(bpx+(tc*(tx+1)),bpy+tc*y),1)
    for c in cubes:
        pygame.draw.rect(fenetre,clm,(bpx+c[0]*tc,bpy+c[1]*tc,tc,tc),0)
    for o in objs:
        pygame.draw.rect(fenetre,clobjs[o[2]],(bpx+tc*o[0]+rx(4),bpy+tc*o[1]+ry(4),tc-rx(6),tc-ry(6)),0)
    for s in snakes:
        if not s.perdu:
            for c in s.cubes:
                pygame.draw.rect(fenetre,c[2],(bpx+c[0]*tc,bpy+c[1]*tc,tc,tc),0)
                if affbords: pygame.draw.rect(fenetre,(255,255,255),(bpx+c[0]*tc,bpy+c[1]*tc,tc,tc),1)
    texte("scores | sizes",850,5,20,(250,250,250))
    for s in snakes: texte('p'+str(snakes.index(s)+1)+' : '+str(s.points)+" | "+str(len(s.cubes)),850,50+30*snakes.index(s),18,(255,255,255))
    pygame.display.update()

def agrandirsnake(nb,s):
    s.taille+=nb
    for w in range(nb):
        dc=s.cubes[len(s.cubes)-1]
        xx,yy=0,0
        if dc[3]=="up":  yy=1
        elif dc[3]=="down": yy=-1
        elif dc[3]=="left": xx=1
        elif dc[3]=="right": xx=-1
        s.cubes.append([dc[0]+xx,dc[1]+yy,dc[2],dc[3],dc[4]])
    return s

def btmv():
    pass

def bot(s,snakes,cubes,objs):
    if s.cible == None and len(objs)>1:
        s.cible=random.randint(0,len(objs)-1)
    lstb=[]
    if s.cubes[0][3]!="down": lstb.append("up")
    if s.cubes[0][3]!="up": lstb.append("down")
    if s.cubes[0][3]!="right": lstb.append("left")
    if s.cubes[0][3]!="left": lstb.append("right")
    rmv=[]
    for m in lstb:
        ac=[]
        for ss in snakes:
            if s!=ss:
                for c in ss.cubes: ac.append(c)
            else:
                for c in ss.cubes[1:]: ac.append(c)
        for c in cubes: ac.append(c)
        cpt=s.cubes[0]
        if m=="up": cpt[1]-=1    
        elif m=="down": cpt[1]+=1
        elif m=="left": cpt[0]-=1
        elif m=="right": cpt[0]+=1
        tt=False
        for c in ac:
            if cpt[0]==c[0] and cpt[1]==c[1]: tt=True
        if m=="up": cpt[1]+=1    
        elif m=="down": cpt[1]-=1
        elif m=="left": cpt[0]+=1
        elif m=="right": cpt[0]-=1
        if not tt:
            rmv.append(m)
    if rmv!=[]:
        if s.cible!=None and len(objs)>s.cible and objs[s.cible][1]<s.cubes[0][1] and "up" in rmv: s.bouger("up")
        elif s.cible!=None and len(objs)>s.cible and objs[s.cible][1]>s.cubes[0][1] and "down" in rmv: s.bouger("down")
        elif s.cible!=None and len(objs)>s.cible and objs[s.cible][0]<s.cubes[0][0] and "left" in rmv: s.bouger("left")
        elif s.cible!=None and len(objs)>s.cible and objs[s.cible][0]>s.cubes[0][0] and "right" in rmv: s.bouger("right")
        else:
            s.bouger(random.choice(rmv))
    
    


def ccc(snakes,cubes,mis,tx,ty,objs,dtc,tac,nbobjs,nbv):
  if time.time()-dtc >= tac:
    ccccc=[]
    dtc=time.time()
    while len(objs)<nbobjs:
        px,py=random.randint(5,tx-5),random.randint(5,ty-5)
        while [px,py] in cubes: px,py=random.randint(5,tx-5),random.randint(5,ty-5)
        objs.append([px,py,random.randint(0,5)])
    for s in snakes:
        if not s.perdu:
            if s.player==0: bot(s,snakes,cubes,objs)
            for c in s.cubes:
                s.points+=1
                n=s.cubes.index(c)
                c[4]=c[3]
                if s.cubes.index(c)==0: c[3]=s.sens
                else: c[3]=s.cubes[s.cubes.index(c)-1][4]               
                if c[3]=="up": c[1]-=1
                elif c[3]=="down": c[1]+=1
                elif c[3]=="left": c[0]-=1
                elif c[3]=="right": c[0]+=1
                if c[0]<0: c[0]=tx
                elif c[0]>tx: c[0]=0
                if c[1]<0: c[1]=ty
                elif c[1]>ty: c[1]=0
                if n==0:
                    tt=False
                    for cc in s.cubes:
                        if s.cubes.index(cc)!=0:
                            if c[0]==cc[0] and c[1]==cc[1]: tt=True
                    if not tt:
                      for ss in snakes:
                          if not ss.perdu:
                            if ss!=s:
                                for cc in ss.cubes:
                                    if c[0]==cc[0] and c[1]==cc[1]: tt=True
                                if tt:
                                    ss.points+=10*len(s.cubes)
                                    break
                    if not tt:
                      for cc in cubes:
                        if c[0]==cc[0] and c[1]==cc[1]: tt=True
                    if tt:
                        nbv-=1
                        s.perdu=True
                        if s.cubes[0][3]=="up": s.cubes[0][1]+=1
                        elif s.cubes[0][3]=="down": s.cubes[0][1]-=1
                        elif s.cubes[0][3]=="left": s.cubes[0][0]+=1
                        elif s.cubes[0][3]=="right": s.cubes[0][0]-=1
                        for c in s.cubes:
                            l=c[2]
                            cl=[l[0]+20,l[1]+20,l[2]+20]
                            if cl[0] > 255: cl[0]=255
                            if cl[1] > 255: cl[1]=255
                            if cl[2] > 255: cl[2]=255
                            cl=(cl[0],cl[1],cl[2])
                            cubes.append( [c[0],c[1],cl] )
                    for o in objs:
                        if c[0]==o[0] and c[1]==o[1]:
                            if o[2]==0: s.agr+=1
                            elif o[2]==1: s.agr+=3
                            elif o[2]==2: s.agr+=5
                            elif o[2]==3: s.points+=10*len(s.cubes)
                            elif o[2]==4: s.points+=30*len(s.cubes)
                            elif o[2]==5: s.points+=50*len(s.cubes)
                            try: del(objs[objs.index(o)])
                            except: print("error")
            if s.agr>0:
                s=agrandirsnake(1,s)
                s.agr-=1
    
  return snakes,cubes,mis,tx,ty,objs,dtc,tac,nbv

def game(modecl,tx,ty,mode,nbb,nbj,dif,affbords,affquadr,tmin):
    bpx,bpy=rx(50),ry(50)
    tc=rx(750)/tx
    dtc=time.time()
    tac=0.1*0.5*abs(4-dif)
    nbobjs=(nbb+nbj)*2
    snakes=[]
    objs=[]
    #0 : +1 taille , 1 : +2 taille , 2 : +3 taille , 3 : +10 points par cubes , 4 : +30 points par cubes , 5 : +50 points par cubes
    mis=[]
    cubes=[]
    nbc=random.randint(0*dif,10*dif)
    for c in range(nbc):
        px,py=random.randint(5,tx-5),random.randint(5,ty-5)
        while [px,py] in cubes: px,py=random.randint(5,tx-5),random.randint(5+5,ty-5)
        cubes.append([px,py])
    for s in range(nbj+nbb):
        px,py=random.randint(5,tx-5),random.randint(5,ty-5)
        while [px,py] in cubes: px,py=random.randint(5,tx-5),random.randint(5,ty-5)
        snakes.append( Snake(px,py,rcl(),tmin) )
        if s<nbj:
            snakes[s].keys=pkeys[s]
            snakes[s].player=s+1
    nbv=len(snakes)
    affgame(snakes,cubes,mis,tx,ty,objs,affbords,affquadr)
    xtx,yty=20,20
    for s in snakes:
        if snakes.index(s)<nbj:
            texte("P"+str(snakes.index(s)+1),(xtx),(yty),20,(255,250,250))
            pygame.draw.line(fenetre,(255,250,250),(xtx+10,yty+20),(bpx+(tc*s.posX),bpy+(tc*s.posY)),2)
            xtx+=50
    pygame.display.update()
    time.sleep(3)
    encourg=True
    while nbv > 0:
        affgame(snakes,cubes,mis,tx,ty,objs,affbords,affquadr)
        snakes,cubes,mis,tx,ty,objs,dtc,tac,nbv=ccc(snakes,cubes,mis,tx,ty,objs,dtc,tac,nbobjs,nbv)
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_q: exit()
                for s in snakes:
                    if event.key==s.keys[0] and s.cubes[0][3]!="down": s.bouger("up")
                    elif event.key==s.keys[1] and s.cubes[0][3]!="up": s.bouger("down")
                    elif event.key==s.keys[2] and s.cubes[0][3]!="right": s.bouger("left")
                    elif event.key==s.keys[3] and s.cubes[0][3]!="left": s.bouger("right")
    lp1=0
    lp2=0
    lp3=0
    if len(snakes)>0:
        for l in range(len(snakes)):
            if snakes[l].points>snakes[lp1].points: lp1=l
    if len(snakes)>1:
        while lp2==lp1: lp2=random.randint(0,len(snakes)-1)
        for l in range(len(snakes)):
            if l!=lp1 and snakes[l].points>snakes[lp2].points: lp2=l
    if len(snakes)>2:
        
        while lp3==lp2 or lp3==lp1: lp3=random.randint(0,len(snakes)-1)
        for l in range(len(snakes)):
            if l!=lp2 and l!=lp1 and snakes[l].points>snakes[lp3].points: lp3=l
    encourfg=True
    fenetre.fill(clf)
    texte("All the snakes died, the game is finished.",100,300,30,(0,0,0))
    texte("Press 'Space' to go to the game menu.",100,400,30,(0,0,0))
    pygame.draw.rect(fenetre,(216,227,2),(rx(500),ry(600),rx(100),ry(250)),0)
    pygame.draw.rect(fenetre,(218,218,218),(rx(400),ry(650),rx(100),ry(200)),0)
    pygame.draw.rect(fenetre,(143,61,5),(rx(600),ry(700),rx(100),ry(150)),0)
    #
    nm="Player"
    if snakes[lp1].player==0: nm="Bot"
    texte(nm+str(lp1+1),500,500,20,(255,255,255))
    texte("score "+str(snakes[lp1].points),500,540,17,(255,255,255))
    texte("size "+str(len(snakes[lp1].cubes)),500,560,17,(255,255,255))
    #
    nm="Player"
    if snakes[lp2].player==0: nm="Bot"
    texte(nm+str(lp2+1),400,550,20,(255,255,255))
    texte("score "+str(snakes[lp2].points),400,590,17,(255,255,255))
    texte("size "+str(len(snakes[lp2].cubes)),400,630,17,(255,255,255))
    #
    nm="Player"
    if snakes[lp2].player==0: nm="Bot"
    texte(nm+str(lp3+1),600,600,20,(255,255,255))
    texte("score "+str(snakes[lp3].points),600,640,17,(255,255,255))
    texte("size "+str(len(snakes[lp3].cubes)),600,660,17,(255,255,255))
    pygame.display.update()
    while encourfg:
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_q: exit()
                elif event.key==K_SPACE: encourfg=False
    return True





##################################menu

ldifs=["easy","medium","hard","hardcore"]

def affmenu(modecl,tx,ty,mode,nbb,nbj,dif,affbords,affquadr,tmin):
    bts=[]
    for w in range(20): bts.append(None)
    fenetre.fill(clf)
    bts[0]=bouton(300,600,200,100,(150,150,50))
    texte("play",320,620,20,(0,0,0))
    #nbj
    bts[1]=bouton(20,150,20,20,(150,0,0))
    bts[2]=bouton(250,150,20,20,(0,150,0))
    texte("-",25,150,20,(0,0,0))
    texte("+",255,150,20,(0,0,0))
    texte("numbers of players : "+str(nbj),55,150,20,(0,0,0))
    #nbb
    bts[3]=bouton(20,200,20,20,(150,0,0))
    bts[4]=bouton(250,200,20,20,(0,150,0))
    texte("-",25,200,20,(0,0,0))
    texte("+",255,200,20,(0,0,0))
    texte("numbers of bots : "+str(nbb),55,200,20,(0,0,0))
    #difficulté
    bts[5]=bouton(20,300,20,20,(150,150,0))
    bts[6]=bouton(150,300,20,20,(150,150,0))
    texte("<",25,300,20,(0,0,0))
    texte(">",155,300,20,(0,0,0))
    texte(ldifs[dif],55,300,20,(0,0,0))
    #taillemin
    bts[7]=bouton(20,240,20,20,(150,0,0))
    bts[8]=bouton(250,240,20,20,(0,150,0))
    texte("-",25,240,20,(0,0,0))
    texte("+",255,240,20,(0,0,0))
    texte("begining size : "+str(tmin),55,240,20,(0,0,0))
    #taillemin
    bts[9]=bouton(20,340,20,20,(150,0,0))
    bts[10]=bouton(250,340,20,20,(0,150,0))
    texte("-",25,340,20,(0,0,0))
    texte("+",255,340,20,(0,0,0))
    texte("resolution : "+str(tx)+"*"+str(ty),55,340,20,(0,0,0))
    #affbords
    clb=(250,0,0)
    if affbords: clb=(0,250,0)
    bts[11]=bouton(400,50,25,20,clb)
    texte("show edges",430,50,20,(0,0,0))
    #affquadr
    clb=(250,0,0)
    if affquadr: clb=(0,250,0)
    bts[12]=bouton(400,90,25,20,clb)
    texte("show grid",430,90,20,(0,0,0))
    #modes de jeu
    #TODO
    #mode couleurs
    #TODO
    #update screen
    pygame.display.update()
    return bts


def menu():
    modecl=0 #0=normal , 1=dégradé
    tx,ty=65,50 #petit : 40*30 , moyen : 50*40 , grand : 65*50
    mode=0
    nbb=10 #min : 0 , max : 15   #bots
    nbj=1 #min : 1 , max : 4    #humains
    dif=0 #facile : 0 , moyen : 1 , difficile : 2 , hardcore : 3
    tmin=5 #min : 1 , max : 6
    affbords=1 #non : 0 , oui : 1
    affquadr=1 #non : 0 , oui : 1
    encourp=False
    encourm=True
    while encourm:
        bts=affmenu(modecl,tx,ty,mode,nbb,nbj,dif,affbords,affquadr,tmin)
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_q: exit()
            elif event.type==MOUSEBUTTONUP:
                pos=pygame.mouse.get_pos()
                rpos=pygame.Rect(pos[0],pos[1],1,1)
                for b in bts:
                    if b!=None and rpos.colliderect(b):
                        di=bts.index(b)
                        if di==0: encourm,encourp=False,True
                        elif di==1 and nbj>0: nbj-=1
                        elif di==2 and nbj<4: nbj+=1
                        elif di==3 and nbb>0: nbb-=1
                        elif di==4 and nbb<15: nbb+=1
                        elif di==5 and dif>0: dif-=1
                        elif di==6 and dif<3: dif+=1
                        elif di==7 and tmin>2: tmin-=1
                        elif di==8 and tmin<6: tmin+=1
                        elif di==9:
                            if tx==50: tx,ty=40,30
                            elif tx==65: tx,ty=50,40
                        elif di==10:
                            if tx==40: tx,ty=50,40
                            elif tx==50: tx,ty=65,50
                        elif di==11: affbords=not affbords
                        elif di==12: affquadr=not affquadr
    if encourp:
        men=game(modecl,tx,ty,mode,nbb,nbj,dif,affbords,affquadr,tmin)
        if men: menu()
    


menu()

