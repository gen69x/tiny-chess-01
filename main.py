import json,os,time,urllib.request
E=os.environ["MAKEFUN_ENV_URL"]
V=dict(P=100,N=320,B=330,R=500,Q=900,K=20000,p=-100,n=-320,b=-330,r=-500,q=-900,k=-20000)
P=[0]*8+[50]*8+[10,10,20,30,30,20,10,10,5,5,10,25,25,10,5,5,0,0,0,20,20,0,0,0,5,-5,-10,0,0,-10,-5,5,5,10,10,-20,-20,10,10,5]+[0]*8
N=[-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,0,0,0,-20,-40,-30,0,10,15,15,10,0,-30,-30,5,15,20,20,15,5,-30,-30,0,15,20,20,15,0,-30,-30,5,10,15,15,10,5,-30,-40,-20,0,5,5,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50]
B=[-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,10,10,5,0,-10,-10,5,5,10,10,5,5,-10,-10,0,10,10,10,10,0,-10,-10,10,10,10,10,10,10,-10,-10,5,0,0,0,0,5,-10,-20,-10,-10,-10,-10,-10,-10,-20]
R=[0]*8+[5,10,10,10,10,10,10,5]+[-5,0,0,0,0,0,0,-5]*4+[0,0,0,5,5,0,0,0]
Q=[-20,-10,-10,-5,-5,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,5,5,5,0,-10,-5,0,5,5,5,5,0,-5,0,0,5,5,5,5,0,-5,-10,5,5,5,5,5,0,-10,-10,0,5,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20]
K=[-30,-40,-40,-50,-50,-40,-40,-30]*4+[-20,-30,-30,-40,-40,-30,-30,-20,-10,-20,-20,-20,-20,-20,-20,-10,20,20,0,0,0,0,20,20,20,30,10,0,0,10,30,20]
KE=[-50,-40,-30,-20,-20,-30,-40,-50,-30,-20,-10,0,0,-10,-20,-30,-30,-10,20,30,30,20,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,30,40,40,30,-10,-30,-30,-10,20,30,30,20,-10,-30,-30,-30,0,0,0,0,-30,-30,-50,-30,-30,-30,-30,-30,-30,-50]
T=dict(P=P,N=N,B=B,R=R,Q=Q,K=K)
def post(p,b):
 r=urllib.request.Request(E+p,data=json.dumps(b).encode(),headers={"content-type":"application/json"})
 with urllib.request.urlopen(r,timeout=9)as x:return json.load(x)
def parse(fen):
 b=[None]*64;i=0
 for c in fen.split()[0]:
  if c=="/":continue
  if c.isdigit():i+=int(c)
  else:b[i]=c;i+=1
 return b
def ev(b,w):
 s=0;eg=sum(1 for c in b if c and c.upper() in "QRBN")<=4
 for i,c in enumerate(b):
  if c:
   u=c.upper();t=KE if(u=="K"and eg)else T[u]
   r,f=divmod(i,8);idx=r*8+f if c.isupper()else(7-r)*8+f
   s+=V[c]+(t[idx]if c.isupper()else-t[idx])
 return s if w else-s
ND=(-17,-15,-10,-6,6,10,15,17);BD=(-9,-7,7,9);RD=(-8,-1,1,8);KD=BD+RD
def gen(b,w,caps=0):
 ms=[]
 for i,c in enumerate(b):
  if not c or c.isupper()!=w:continue
  t=c.upper();f=i%8
  if t=="P":
   d=-8 if w else 8;to=i+d
   if not caps and 0<=to<64 and not b[to]:
    if(w and to<8)or(not w and to>=56):
     for p in"qrbn":ms.append((i,to,p))
    else:ms.append((i,to,None))
    if((w and 48<=i<56)or(not w and 8<=i<16))and not b[i+2*d]:ms.append((i,i+2*d,None))
   for dd in(-1,1):
    if 0<=f+dd<8:
     to=i+d+dd
     if 0<=to<64 and b[to]and b[to].isupper()!=w:
      if(w and to<8)or(not w and to>=56):
       for p in"qrbn":ms.append((i,to,p))
      else:ms.append((i,to,None))
  elif t=="N":
   for d in ND:
    to=i+d
    if 0<=to<64 and abs(to%8-f)<=2 and(not b[to]or b[to].isupper()!=w)and(not caps or b[to]):ms.append((i,to,None))
  elif t in"BRQ":
   for d in(BD if t=="B"else RD if t=="R"else KD):
    p=i;to=i+d
    while 0<=to<64 and abs(to%8-p%8)<=1:
     if b[to]:
      if b[to].isupper()!=w:ms.append((i,to,None))
      break
     if not caps:ms.append((i,to,None))
     p=to;to+=d
  else:
   for d in KD:
    to=i+d
    if 0<=to<64 and abs(to%8-f)<=1 and(not b[to]or b[to].isupper()!=w)and(not caps or b[to]):ms.append((i,to,None))
 return ms
def mk(b,m):
 nb=b[:];fr,to,pr=m;p=nb[fr];nb[fr]=None
 if pr:p=pr.upper()if p.isupper()else pr
 nb[to]=p;return nb
def order(b,ms):
 return sorted(ms,key=lambda m:(10*abs(V[b[m[1]]])-abs(V[b[m[0]]])if b[m[1]]else 0)+(800 if m[2]=="q"else 0),reverse=True)
def qs(b,w,a,be,dl):
 sp=ev(b,w)
 if sp>=be:return be
 if sp>a:a=sp
 if time.time()>dl:return a
 for m in order(b,gen(b,w,1)):
  if b[m[1]]and b[m[1]].upper()=="K":return 19000
  v=-qs(mk(b,m),not w,-be,-a,dl)
  if v>=be:return be
  if v>a:a=v
 return a
def ab(b,w,d,a,be,dl):
 if d<=0:return qs(b,w,a,be,dl)
 if time.time()>dl:return ev(b,w)
 ms=order(b,gen(b,w))
 if not ms:return ev(b,w)
 best=-10**9
 for m in ms:
  if b[m[1]]and b[m[1]].upper()=="K":return 19000+d
  v=-ab(mk(b,m),not w,d-1,-be,-a,dl)
  if v>best:best=v
  if best>a:a=best
  if a>=be:break
 return best
def uci(m):
 fr,to,pr=m;return chr(97+fr%8)+str(8-fr//8)+chr(97+to%8)+str(8-to//8)+(pr or"")
def choose(fen,legal,w):
 b=parse(fen)
 root=[((8-int(u[1]))*8+ord(u[0])-97,(8-int(u[3]))*8+ord(u[2])-97,u[4]if len(u)>4 else None)for u in legal]
 if len(root)==1:return legal[0]
 dl=time.time()+1.2;best=root[0]
 for d in range(1,7):
  if time.time()>dl:break
  cb=None;bv=-10**9;a=-10**9;ok=1
  for m in order(b,root):
   if b[m[1]]and b[m[1]].upper()=="K":return uci(m)
   v=-ab(mk(b,m),not w,d-1,-10**9,-a,dl)
   if time.time()>dl and d>1:ok=0;break
   if v>bv:bv=v;cb=m
   if bv>a:a=bv
  if ok and cb:best=cb
  if bv>18000:break
 return uci(best)
def main():
 while 1:
  g=post("/game",{})
  if g.get("status")=="done":return
  while g.get("status")=="your_move":
   m=choose(g["fen"],g["legal_moves"],g["colour"][0]=="w")
   g=post("/move",{"game":g["game"],"move":m})
main()
