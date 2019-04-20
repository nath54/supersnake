#coding:utf-8
import random,pygame,time,os
from pygame.locals import *

btex,btey=1000,900
mmtex,mmtey=1280,1024

pygame.init()

io = pygame.display.Info()
mtex,mtey=io.current_w,io.current_h
#mtex,mtey=1280,720
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
    fenetre.blit( pygame.font.SysFont(ffont,ry(taille)).render(texte,ry(taille),cl) , [rx(x),ry(y)] )

clobjs=[(70,70,70),(150,150,150),(230,230,230),(0,70,0),(0,150,0),(0,230,0),(70,0,0),(150,0,0),(230,0,0),(70,70,0),(150,150,0),(230,230,0),(255,0,255)]
clm=(245,245,245)

pkeys=[[K_UP,K_DOWN,K_LEFT,K_RIGHT],[K_KP8,K_KP2,K_KP4,K_KP6],[K_o,K_l,K_k,K_m],[K_t,K_g,K_f,K_h]]
pkaff=["up-down-left-right","num8-num2-num4-num6","o-l-k-m","t-g-f-h"]

ldifs=["easy","medium","hard","hardcore"]

gamemodes=["normal","battle-royale","time match","max size match","max points match","teams match","invisible zone"]
colormodes=["normal","dégradé"]
################################jeu

class Zone:
    def __init__(self,x,y,tx,ty):
        self.px=x
        self.py=y
        self.tx=tx
        self.ty=ty
        self.dred=time.time()
        self.ttred=10
        self.active=False
    def tciz(self,c):
        if c[0]>=self.px and c[0]<=self.px+self.tx and c[1]>=self.py and c[1]<=self.py+self.ty : return True
        else: return False
    def reduire(self):
        if time.time()-self.dred >= self.ttred:
            if not self.active:
                self.active=True
                self.dred=time.time()
            else:
                self.dred=time.time()
                self.px+=1
                self.py+=1
                if self.tx>2: self.tx-=2
                if self.ty>2: self.ty-=2
    def change(self,tx,ty):
        if time.time()-self.dred >= self.ttred:
            self.dred=time.time()
            self.px,self.py=random.randint(0,tx-20),random.randint(0,ty-20)
            self.tx,self.ty=random.randint(5,tx-self.px),random.randint(5,ty-self.py)

class Team:
    def __init__(self,nom,cl):
        self.nom=nom
        self.cl=cl
        self.snakes=[]
        self.points=0
        self.kills=0

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
        self.team=None
        self.kills=0
        self.time_survie=0
        self.dt=time.time()
    def bouger(self,aa):
        if aa == "up": self.sens=aa
        elif aa == "down": self.sens=aa
        elif aa == "left": self.sens=aa
        elif aa == "right": self.sens=aa
            
def affgame(snakes,cubes,mis,tx,ty,objs,affbords,affquadr,mode,tps,paliertaille,palierpoints,teams,zone):
    fenetre.fill(clf)
    bpx,bpy=rx(50),ry(50)
    tc=rx(750)/tx
    pygame.draw.rect(fenetre,(5,5,5),(bpx,bpy,(tx+1)*tc,(ty+1)*tc),0)
    if mode==1 and zone.active:
        pygame.draw.rect(fenetre,(100,0,0),(bpx,bpy,zone.px*tc,ty*tc),0)
        pygame.draw.rect(fenetre,(100,0,0),(bpx+tc*(zone.px+zone.tx),bpy,(tx-(zone.px+zone.tx-1))*tc,ty*tc),0)
        pygame.draw.rect(fenetre,(100,0,0),(bpx,bpy,tx*tc,zone.py*tc),0)
        pygame.draw.rect(fenetre,(100,0,0),(bpx,bpy+tc*(zone.py+zone.ty),tx*tc,(ty-(zone.py+zone.ty-1))*tc),0)
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
    if mode==1:
        pygame.draw.rect(fenetre,(200,150,20),(bpx+zone.px*tc,bpy+zone.py*tc,zone.tx*tc,zone.ty*tc),2)
    if mode==6:
        pygame.draw.rect(fenetre,(0,0,0),(bpx+zone.px*tc,bpy+zone.py*tc,zone.tx*tc,zone.ty*tc),0)
    #interface
    if mode==0 or mode==2 or mode==6:
        texte("scores | sizes",830,5,20,(250,250,250))
        for s in snakes:
            sp=""
            if s.perdu: sp=" (dead)"
            texte('p'+str(snakes.index(s)+1)+' : '+str(s.points)+" | "+str(len(s.cubes))+sp,850,50+30*snakes.index(s),18,(255,255,255))
    if mode==1:
        texte("survival time | kills",815,5,17,(250,250,250))
        sk=0
        for s in snakes:
            if not s.perdu:
                texte("p"+str(snakes.index(s)+1)+" : "+str(int(s.time_survie))+"s | "+str(s.kills),830,50+30*sk,16,(255,255,255))
                sk+=1
        if not zone.active: texte("time before activation of the zone : "+str(int(zone.ttred-(time.time()-zone.dred)))+" s",400,20,20,(255,255,255))
        else: texte("time before reduction of the zone : "+str(int(zone.ttred-(time.time()-zone.dred)))+" s",400,20,20,(255,255,255))
    if mode==2 or mode==5:
        texte("remaining time : "+str(int(tps))+" s",400,20,20,(255,255,255))
        if tps<5:
            texte(str(tps)[:5],250,250,50,(255,0,0))
    if mode==3:
        texte("sizes ( goal : "+str(paliertaille)+" )",700,5,20,(250,250,250))
        for s in snakes:
            sp=""
            if s.perdu: sp=" (dead)"
            texte("p"+str(snakes.index(s)+1)+" : "+str(len(s.cubes))+sp,850,50+30*snakes.index(s),18,(255,255,255))
    if mode==4:
        sp=""
        if s.perdu: sp=" (dead)"
        texte("points ( goal : "+str(palierpoints)+" )",700,5,20,(250,250,250))
        for s in snakes: texte("p"+str(snakes.index(s)+1)+" : "+str(s.points)+sp,850,50+30*snakes.index(s),18,(255,255,255))
    if mode==5:
        texte("teams : points | kills",800,5,20,(250,250,250))
        for t in teams:
            bouton(850,50+30*teams.index(t)-1,150,40,t.cl)
            texte("team"+str(teams.index(t)+1)+" : "+str(t.points)+" | "+str(t.kills),850,50+30*teams.index(t),18,(255,255,255))
    if mode==6:
        texte("time before movement of the zone : "+str(int(zone.ttred-(time.time()-zone.dred)))+" s",400,20,20,(255,255,255))
    pygame.display.update()

def agrandirsnake(nb,s,modecl):
    s.taille+=nb
    for w in range(nb):
        dc=s.cubes[len(s.cubes)-1]
        xx,yy=0,0
        if dc[3]=="up":  yy=1
        elif dc[3]=="down": yy=-1
        elif dc[3]=="left": xx=1
        elif dc[3]=="right": xx=-1
        cl=dc[2]
        if modecl==1:
            b=20
            cl=[list(cl)[0]+random.randint(-b,b),list(cl)[1]+random.randint(-b,b),list(cl)[2]+random.randint(-b,b)]
            if cl[0]>255: cl[0]=255
            if cl[1]>255: cl[1]=255
            if cl[2]>255: cl[2]=255
            if cl[0]<0: cl[0]=0
            if cl[1]<0: cl[1]=0
            if cl[2]<0: cl[2]=0
        s.cubes.append([dc[0]+xx,dc[1]+yy,cl,dc[3],dc[4]])
    return s

def btmv():
    pass

def bot(s,snakes,cubes,objs,zone):
    if s.cible == None and len(objs)>1:
        ob=random.randint(0,len(objs)-1)
        if not zone.tciz(objs[ob]):
            ob=random.randint(0,len(objs)-1)
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
    
    


def ccc(snakes,cubes,mis,tx,ty,objs,dtc,tac,nbobjs,nbv,mode,tmin,zone,modecl):
  if time.time()-dtc >= tac:
    ccccc=[]
    dtc=time.time()
    while len(objs)<nbobjs:
        px,py=random.randint(5,tx-5),random.randint(5,ty-5)
        while [px,py] in cubes and (zone.active and not zone.tciz([px,py]) ): px,py=random.randint(5,tx-5),random.randint(5,ty-5)
        objs.append([px,py,random.randint(0,12)])
    if mode==1 : zone.reduire()
    if mode==6 : zone.change(tx,ty)
    for s in snakes:
        if not s.perdu:
            if s.player==0: bot(s,snakes,cubes,objs,zone)
            n=-1
            s.time_survie+=time.time()-s.dt
            s.dt=time.time()
            for c in s.cubes:
                n+=1
                s.points+=1
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
                    if mode==1 and zone.active and not zone.tciz(c):
                        if len(s.cubes)>1: del(s.cubes[len(s.cubes)-1])
                        else: tt=True
                    if not tt:
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
                                    ss.kills+=1
                                    if mode==5 and s.team!=ss.team:
                                        ss.team.points+=50*len(s.cubes)
                                        ss.team.kills+=1
                                    break
                    if not tt:
                      for cc in cubes:
                        if c[0]==cc[0] and c[1]==cc[1]: tt=True
                    for o in objs:
                        if c[0]==o[0] and c[1]==o[1]:
                            if o[2]==0: s.agr+=1
                            elif o[2]==1: s.agr+=3
                            elif o[2]==2: s.agr+=5
                            elif o[2]==3:
                                if mode == 5: s.team.points+=10*len(s.cubes)
                                else: s.points+=10*len(s.cubes)
                            elif o[2]==4:
                                if mode == 5: s.team.points+=30*len(s.cubes)
                                else: s.points+=30*len(s.cubes)
                            elif o[2]==5:
                                if mode == 5: s.team.points+=50*len(s.cubes)
                                else: s.points+=50*len(s.cubes)
                            elif o[2]==6:
                                for hh in range(1):
                                    if len(s.cubes)>3:
                                        del(s.cubes[len(s.cubes)-1])
                            elif o[2]==7:
                                for hh in range(3):
                                    if len(s.cubes)>3:
                                        del(s.cubes[len(s.cubes)-1])
                            elif o[2]==8:
                                for hh in range(5):
                                    if len(s.cubes)>3:
                                        del(s.cubes[len(s.cubes)-1])
                            elif o[2]==9:
                                for hh in range(1):
                                    if len(s.cubes)>3:
                                        cc=s.cubes[len(s.cubes)-1]
                                        del(s.cubes[len(s.cubes)-1])
                                        cubes.append([cc[0],cc[1]])
                            elif o[2]==10:
                                for hh in range(3):
                                    if len(s.cubes)>3:
                                        cc=s.cubes[len(s.cubes)-1]
                                        del(s.cubes[len(s.cubes)-1])
                                        cubes.append([cc[0],cc[1]])
                            elif o[2]==11:
                                for hh in range(5):
                                    if len(s.cubes)>3:
                                        cc=s.cubes[len(s.cubes)-1]        
                                        del(s.cubes[len(s.cubes)-1])
                                        cubes.append([cc[0],cc[1]])
                            elif o[2]==12: tt=True
                            try: del(objs[objs.index(o)])
                            except: print("error")
            if tt:
                """
                if s.cubes[0][3]=="up": s.cubes[0][1]+=1
                elif s.cubes[0][3]=="down": s.cubes[0][1]-=1
                elif s.cubes[0][3]=="left": s.cubes[0][0]+=1
                elif s.cubes[0][3]=="right": s.cubes[0][0]-=1
                """
                if mode == 0 or mode==1 or mode==6:
                    nbv-=1
                    s.perdu=True
                    for c in s.cubes: cubes.append( [c[0],c[1]] )
                else:
                    s.points-=10*len(s.cubes)
                    cl=s.cubes[0][2]
                    s.cubes=[]
                    px,py=random.randint(5,tx-5),random.randint(5,ty-5)
                    while [px,py] in cubes: px,py=random.randint(5,tx-5),random.randint(5,ty-5)
                    s.cubes.append( [px,py,cl,random.choice(["up","down","left","right"]),random.choice(["up","down","left","right"]) ] )
                    s.agr=tmin
            if s.agr>0:
                s=agrandirsnake(1,s,modecl)
                s.agr-=1
    
  return snakes,cubes,mis,tx,ty,objs,dtc,tac,nbv

def game(modecl,tx,ty,mode,nbb,nbj,dif,affbords,affquadr,tmin,keysp,tps,palierpoints,paliertaille,nbteams,teamsp):
    zx,zy,ztx,zty=0,0,0,0
    if mode==1:
        zx=random.randint(0,int(tx/5))
        zy=random.randint(0,int(ty/5))
        ztx=tx-zx-random.randint(0,5)
        zty=ty-zy-random.randint(0,5)
    if mode==6:
        zx,zy=random.randint(0,tx-20),random.randint(0,ty-20)
        ztx,zty=random.randint(5,tx-zx),random.randint(5,ty-zy)
    zone=Zone(zx,zy,ztx,zty)
    teams=[]
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
    nbbpt=int(nbb/nbteams)
    for w in range(nbteams):
        teams.append( Team("team"+str(w+1),rcl()) )
    for s in range(nbj+nbb):
        px,py=random.randint(5,tx-5),random.randint(5,ty-5)
        while [px,py] in cubes: px,py=random.randint(5,tx-5),random.randint(5,ty-5)
        cl=rcl()
        it=0
        if mode==5:
            if s<nbj:
                it=teamsp[s]
                cl=teams[it].cl
            else:
                oo=float(float(s)-float(nbj))/float(nbb)*float(nbteams)
                it=int(oo)
                cl=teams[it].cl
        snakes.append( Snake(px,py,cl,tmin) )
        snakes[s].team=teams[it]
        if s<nbj:
            snakes[s].keys=pkeys[keysp[s]]
            snakes[s].player=s+1
        teams[it].snakes.append( snakes[s] )
                
                
    nbv=len(snakes)
    affgame(snakes,cubes,mis,tx,ty,objs,affbords,affquadr,mode,tps,paliertaille,palierpoints,teams,zone)
    xtx,yty=20,20
    for s in snakes:
        if snakes.index(s)<nbj:
            texte("P"+str(snakes.index(s)+1),(xtx),(yty),20,(255,250,250))
            pygame.draw.line(fenetre,(255,250,250),(xtx+10,yty+20),(bpx+(tc*s.posX),bpy+(tc*s.posY)),2)
            xtx+=50
    pygame.display.update()
    time.sleep(3)
    encourg=True
    encourfg=True
    tt=time.time()
    while encourg:
        tps-=time.time()-tt
        tt=time.time()
        affgame(snakes,cubes,mis,tx,ty,objs,affbords,affquadr,mode,tps,paliertaille,palierpoints,teams,zone)
        snakes,cubes,mis,tx,ty,objs,dtc,tac,nbv=ccc(snakes,cubes,mis,tx,ty,objs,dtc,tac,nbobjs,nbv,mode,tmin,zone,modecl)
        ##
        nbjsurviv=nbj
        for w in range(nbj):
            if snakes[w].perdu: nbjsurviv-=1
        if nbjsurviv==0:
            texte("Press 'Space' to return to the menu",10,10,20,(255,255,255))
            pygame.display.update()
        ##      
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_q: exit()
                if nbjsurviv==0 and event.key==K_SPACE: encourg,encourfg=False,False
                for s in snakes:
                    if event.key==s.keys[0] and s.cubes[0][3]!="down": s.bouger("up")
                    elif event.key==s.keys[1] and s.cubes[0][3]!="up": s.bouger("down")
                    elif event.key==s.keys[2] and s.cubes[0][3]!="right": s.bouger("left")
                    elif event.key==s.keys[3] and s.cubes[0][3]!="left": s.bouger("right")
        if mode==0 or mode==6: #mode normal #mode invisible
            if nbv<=0: encourg=False
        elif mode==1: #battle-royale
            if nbv<=1: encourg=False
        elif mode==2 or mode==5: #time-game #teams match
            if tps<=0: encourg=False
        elif mode==3: #the first at big size
            for s in snakes:
                if len(s.cubes)>=paliertaille: encourg=False
        elif mode==4: #the first at a lot of points
            for s in snakes:
                if s.points>=palierpoints: encourg=False
            
    #fin
    fenetre.fill(clf)
    if mode in [0,2,3,4,6]:
        lp1=0
        lp2=0
        lp3=0
        if mode in [0,2,4,6]:
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
        if mode==3:
            if len(snakes)>0:
                for l in range(len(snakes)):
                    if len(snakes[l].cubes)>len(snakes[lp1].cubes): lp1=l
            if len(snakes)>1:
                while lp2==lp1: lp2=random.randint(0,len(snakes)-1)
                for l in range(len(snakes)):
                    if l!=lp1 and len(snakes[l].cubes)>len(snakes[lp2].cubes): lp2=l
            if len(snakes)>2:
                while lp3==lp2 or lp3==lp1: lp3=random.randint(0,len(snakes)-1)
                for l in range(len(snakes)):
                    if l!=lp2 and l!=lp1 and len(snakes[l].cubes)>len(snakes[lp3].cubes): lp3=l
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
    if mode==5:
        lp1=0
        lp2=0
        lp3=0
        lp4=0
        for t in range(len(teams)):
            if teams[t].points>teams[lp1].points: lp1=t
        while lp2==lp1: lp2=random.randint(0,nbteams-1)
        if nbteams>2:
            for t in range(len(teams)):
                if t!=lp1 and teams[t].points>teams[lp2].points: lp2=t
        if nbteams==3:
            while lp3==lp2 and lp3==lp1: lp3=random.randint(0,nbteams-1)
        if nbteams==4:
            for t in range(len(teams)):
                if t!=lp2 and t!=lp1 and teams[t].points>teams[lp3].points: lp3=t
            while lp4==lp3 and lp4==lp2 and lp4==lp1: lp4=random.randint(0,nbteams-1)
        texte("classement : ",400,450,25,(0,0,0))
        texte("team"+str(lp1+1)+" : "+str(teams[lp1].points),350,490+40*0,20,(0,0,0))
        texte("team"+str(lp2+1)+" : "+str(teams[lp2].points),350,490+40*1,20,(0,0,0))
        if nbteams > 2 : texte("team"+str(lp3+1)+" : "+str(teams[lp3].points),350,490+40*2,20,(0,0,0))
        if nbteams > 3 : texte("team"+str(lp4+1)+" : "+str(teams[lp4].points),350,490+40*3,20,(0,0,0))
    if mode==1:
        sg=0
        for s in snakes:
            if not s.perdu: sg=snakes.index(s)
        si="player"
        if snakes[sg].player==0: si="bot"
        texte("#1 : "+si+str(sg+1),100,500,35,(255,255,255))
    texte("The game is over.",100,300,30,(0,0,0))
    texte("Press 'Space' to go to the game menu.",100,400,30,(0,0,0))
    pygame.display.update()
    while encourfg:
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_q: exit()
                elif event.key==K_SPACE: encourfg=False
    return True





##################################menu

def affmenu(modecl,tx,ty,mode,nbb,nbj,dif,affbords,affquadr,tmin,keysp,tps,palierpoints,paliertaille,nbteams,teamsp):
    bts=[]
    for w in range(40): bts.append(None)
    fenetre.fill(clf)
    texte("SUPERSNAKE",50,50,50,rcl())
    bts[0]=bouton(450,500,100,50,(150,150,50))
    texte("play",460,510,20,(0,0,0))
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
    bts[11]=bouton(100,400,25,20,clb)
    texte("show edges",130,400,20,(0,0,0))
    #affquadr
    clb=(250,0,0)
    if affquadr: clb=(0,250,0)
    bts[12]=bouton(100,450,25,20,clb)
    texte("show grid",130,450,20,(0,0,0))
    #keys_players
    texte("keys",500,100,20,(0,0,0))
    #p1
    if nbj>=1:
        bts[13]=bouton(430,140,25,25,(200,200,200))
        bts[14]=bouton(670,140,25,25,(200,200,200))
        texte("<",435,140,25,(0,0,0))
        texte(">",675,140,25,(0,0,0))
        texte(pkaff[keysp[0]],470,140,20,(0,0,0))
        texte("player1 : ",300,140,20,(0,0,0))
    #p2
    if nbj>=2:
        bts[15]=bouton(430,180,25,25,(200,200,200))
        bts[16]=bouton(670,180,25,25,(200,200,200))
        texte("<",435,180,25,(0,0,0))
        texte(">",675,180,25,(0,0,0))
        texte(pkaff[keysp[1]],470,180,20,(0,0,0))
        texte("player2 : ",300,180,20,(0,0,0))
    #p3
    if nbj>=3:
        bts[17]=bouton(430,220,25,25,(200,200,200))
        bts[18]=bouton(670,220,25,25,(200,200,200))
        texte("<",435,220,25,(0,0,0))
        texte(">",675,220,25,(0,0,0))
        texte(pkaff[keysp[2]],470,220,20,(0,0,0))
        texte("player3 : ",300,220,20,(0,0,0))
    #p4
    if nbj>=4:
        bts[19]=bouton(430,260,25,25,(200,200,200))
        bts[20]=bouton(670,260,25,25,(200,200,200))
        texte("<",435,260,25,(0,0,0))
        texte(">",675,260,25,(0,0,0))
        texte(pkaff[keysp[3]],470,260,20,(0,0,0))
        texte("player4 : ",300,260,20,(0,0,0))
    #teams_players
    if mode==5:
        #p1
        if nbj>=1:
            bts[21]=bouton(700,140,50,25,(200,200,200))
            texte("<>",705,140,25,(0,0,0))
            texte("team "+str(teamsp[0]+1),760,140,20,(0,0,0))
        #p2
        if nbj>=2:
            bts[22]=bouton(700,180,50,25,(200,200,200))
            texte("<>",705,180,25,(0,0,0))
            texte("team "+str(teamsp[0]+1),760,180,20,(0,0,0))
        #p3
        if nbj>=3:
            bts[23]=bouton(700,220,50,25,(200,200,200))
            texte("<>",705,220,25,(0,0,0))
            texte("team "+str(teamsp[0]+1),760,220,20,(0,0,0))
        #p4
        if nbj>=4:
            bts[24]=bouton(700,260,50,25,(200,200,200))
            texte("<>",705,260,25,(0,0,0))
            texte("team "+str(teamsp[0]+1),760,260,20,(0,0,0))
    #modes de jeu
    texte("current game mode : "+gamemodes[mode],350,350,20,(0,0,0))
    bts[25]=bouton(650,350,50,25,(200,200,200))
    texte("<>",655,350,25,(0,0,0))
    if mode==5:
        bts[26]=bouton(350,390,25,25,(250,0,0))
        bts[27]=bouton(505,390,25,25,(0,250,0))
        texte("-",355,390,25,(0,0,0))
        texte("+",510,390,25,(0,0,0))
        texte("nb teams : "+str(nbteams),380,390,20,(0,0,0))
    if mode==2 or mode==5:
        bts[28]=bouton(350,430,25,25,(250,0,0))
        bts[29]=bouton(525,430,25,25,(0,250,0))
        texte("-",355,430,25,(0,0,0))
        texte("+",530,430,25,(0,0,0))
        texte("match time : "+str(tps),380,430,20,(0,0,0))
    if mode==3:
        bts[30]=bouton(350,390,25,25,(250,0,0))
        bts[31]=bouton(505,390,25,25,(0,250,0))
        texte("-",355,390,25,(0,0,0))
        texte("+",510,390,25,(0,0,0))
        texte("max size : "+str(paliertaille),380,390,20,(0,0,0))
    if mode==4:
        bts[32]=bouton(350,390,25,25,(250,0,0))
        bts[33]=bouton(555,390,25,25,(0,250,0))
        texte("-",355,390,25,(0,0,0))
        texte("+",560,390,25,(0,0,0))
        texte("max points : "+str(palierpoints),380,390,20,(0,0,0))
    #règles
    texte("Tips : ",18,570,20,(255,255,255))
    texte("Small gray cubes enlarge the body of your snake",20,600,20,(150,150,150))
    texte("Small red cubes reduce the body of your snake",20,630,20,(150,0,0))
    texte("Small yellow cubes replace the end of your snake's body with a wall",20,660,20,(150,150,0))
    texte("Small green cubes give you points",20,690,20,(0,150,0))
    texte("Small purple cubes kill you",20,720,20,(150,0,150))
    texte("Small blue cubes make you invincible for a while",20,750,20,(0,0,150))
    #mode couleurs
    bts[34]=bouton(20,500,50,25,(150,150,150))
    texte("<>",25,500,25,(0,0,0))
    texte("color mode : "+colormodes[modecl],80,500,20,(150,150,150))
    #update screen
    pygame.display.update()
    return bts


def menu():
    keysp=[0,1,2,3]
    teamsp=[0,0,1,1]
    modecl=0 #0=normal , 1=dégradé
    tx,ty=65,50 #petit : 40*30 , moyen : 50*40 , grand : 65*50
    mode=0 #0=normal , 1=battle-royale , 2=time match , 3=max size match , 4=max points match , 5=team match , 6=invisible zone
    nbb=10 #min : 0 , max : 15   #bots
    nbj=1 #min : 1 , max : 4    #humains
    dif=0 #facile : 0 , moyen : 1 , difficile : 2 , hardcore : 3
    tmin=3 #min : 1 , max : 6
    affbords=1 #non : 0 , oui : 1
    affquadr=1 #non : 0 , oui : 1
    tps=300 #min : 60 , max : 600 (en secondes)
    paliertaille=50 #min : 30 , max : 100
    palierpoints=30000 #min : 10000 , max : 100000
    nbteams=2 #min : 2 , max : 4
    encourp=False
    encourm=True
    needtoaff=True
    while encourm:
        if needtoaff:
            bts=affmenu(modecl,tx,ty,mode,nbb,nbj,dif,affbords,affquadr,tmin,keysp,tps,palierpoints,paliertaille,nbteams,teamsp)
            needtoaff=False
        for event in pygame.event.get():
            if event.type==QUIT: exit()
            elif event.type==KEYDOWN:
                if event.key==K_q: exit()
            elif event.type==MOUSEBUTTONUP:
                needtoaff=True
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
                        elif di==13:
                            keysp[0]-=1
                            if keysp[0]<0: keysp[0]=len(pkeys)-1
                        elif di==14:
                            keysp[0]+=1
                            if keysp[0]>len(pkeys)-1: keysp[0]=0
                        elif di==15:
                            keysp[1]-=1
                            if keysp[1]<0: keysp[1]=len(pkeys)-1
                        elif di==16:
                            keysp[1]+=1
                            if keysp[1]>len(pkeys)-1: keysp[1]=0
                        elif di==17:
                            keysp[2]-=1
                            if keysp[2]<0: keysp[2]=len(pkeys)-1
                        elif di==18:
                            keysp[2]+=1
                            if keysp[2]>len(pkeys)-1: keysp[2]=0
                        elif di==19:
                            keysp[3]-=1
                            if keysp[3]<0: keysp[3]=len(pkeys)-1
                        elif di==20:
                            keysp[3]+=1
                            if keysp[3]>len(pkeys)-1: keysp[3]=0
                        elif di==21:
                            teamsp[0]+=1
                            if teamsp[0]>nbteams-1: teamsp[0]=0
                        elif di==22:
                            teamsp[1]+=1
                            if teamsp[1]>nbteams-1: teamsp[1]=0
                        elif di==23:
                            teamsp[2]+=1
                            if teamsp[2]>nbteams-1: teamsp[2]=0
                        elif di==24:
                            teamsp[3]+=1
                            if teamsp[3]>nbteams-1: teamsp[3]=0
                        elif di==25:
                            mode+=1
                            if mode==len(gamemodes): mode=0
                        elif di==26:
                            if nbteams > 2 : nbteams-=1
                        elif di==27:
                            if nbteams < 4 : nbteams+=1
                        elif di==28:
                            if tps > 60 : tps-=60
                        elif di==29:
                            if tps < 600 : tps+=60
                        elif di==30:
                            if paliertaille > 30 : paliertaille-=5
                        elif di==31:
                            if paliertaille < 100 : paliertaille+=5
                        elif di==32:
                            if palierpoints > 10000 : palierpoints-=1000
                        elif di==33:
                            if palierpoints < 100000 : palierpoints+=1000
                        elif di==34:
                            modecl+=1
                            if modecl==len(colormodes): modecl=0
                            
                            
                        
    if encourp:
        men=game(modecl,tx,ty,mode,nbb,nbj,dif,affbords,affquadr,tmin,keysp,tps,palierpoints,paliertaille,nbteams,teamsp)
        if men: menu()
    


menu()

