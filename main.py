import json,os,sys,urllib.request
E=os.environ["MAKEFUN_ENV_URL"]
V=dict(P=100,N=320,B=330,R=500,Q=900,K=20000,p=-100,n=-320,b=-330,r=-500,q=-900,k=-20000)
P=[0]*16+[10,10,20,30,30,20,10,10,5,5,10,25,25,10,5,5,0,0,0,20,20,0,0,0]+[0]*24
N=[-50,-40,-30,-30,-30,-30,-40,-50,-40,-20,0,0,0,0,-20,-40,-30,0,10,15,15,10,0,-30,-30,5,15,20,20,15,5,-30,-30,0,15,20,20,15,0,-30,-30,5,10,15,15,10,5,-30,-40,-20,0,5,5,0,-20,-40,-50,-40,-30,-30,-30,-30,-40,-50]
B=[-20,-10,-10,-10,-10,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,10,10,5,0,-10,-10,5,5,10,10,5,5,-10,-10,0,10,10,10,10,0,-10,-10,10,10,10,10,10,10,-10,-10,5,0,0,0,0,5,-10,-20,-10,-10,-10,-10,-10,-10,-20]
R=[0]*8+[5,10,10,10,10,10,10,5]+[-5,0,0,0,0,0,0,-5]*4+[0,0,0,5,5,0,0,0]
Q=[-20,-10,-10,-5,-5,-10,-10,-20,-10,0,0,0,0,0,0,-10,-10,0,5,5,5,5,0,-10,-5,0,5,5,5,5,0,-5,0,0,5,5,5,5,0,-5,-10,5,5,5,5,5,0,-10,-10,0,5,0,0,0,0,-10,-20,-10,-10,-5,-5,-10,-10,-20]
K=[20,30,10,0,0,10,30,20,20,20,0,0,0,0,20,20]+[-20]*48
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
def pst(c,i):
 t=T.get(c.upper())
 if not t:return 0
 r,f=divmod(i,8);idx=(7-r)*8+f if c.islower() else r*8+f
 return t[idx]*(1 if c.isupper() else -1)
def evaluate(b,side):
 s=0
 for i,c in enumerate(b):
  if c:s+=V[c]+pst(c,i)
 return s if side=="w" else -s
N_DIR=(-17,-15,-10,-6,6,10,15,17);B_DIR=(-9,-7,7,9);R_DIR=(-8,-1,1,8);K_DIR=(-9,-8,-7,-1,1,7,8,9)
def on(i):return 0<=i<64
def gen(b,side):
 moves=[];w=side=="w"
 for i,c in enumerate(b):
  if not c or c.isupper()!=w:continue
  t=c.upper()
  if t=="P":
   d=-8 if w else 8;to=i+d
   if on(to) and not b[to]:
    if (w and to<8) or (not w and to>=56):
     for p in "qrbn":moves.append((i,to,p))
    else:moves.append((i,to,None))
    if (w and 48<=i<56) or (not w and 8<=i<16):
     to2=i+2*d
     if on(to2) and not b[to2]:moves.append((i,to2,None))
   for dd in (-1,1):
    to=i+d+dd
    if on(to) and b[to] and b[to].isupper()!=w:
     if (w and to<8) or (not w and to>=56):
      for p in "qrbn":moves.append((i,to,p))
     else:moves.append((i,to,None))
  elif t=="N":
   for d in N_DIR:
    to=i+d
    if on(to) and abs((to%8)-(i%8))<=2 and (not b[to] or b[to].isupper()!=w):moves.append((i,to,None))
  elif t in "BRQ":
   dirs=B_DIR if t=="B" else R_DIR if t=="R" else B_DIR+R_DIR
   for d in dirs:
    to=i+d
    while on(to) and abs((to%8)-(i%8))<8:
     if b[to]:
      if b[to].isupper()!=w:moves.append((i,to,None))
      break
     moves.append((i,to,None));to+=d
  elif t=="K":
   for d in K_DIR:
    to=i+d
    if on(to) and abs((to%8)-(i%8))<=1 and (not b[to] or b[to].isupper()!=w):moves.append((i,to,None))
 return moves
def apply(b,m):
 nb=b[:];fr,to,pr=m;p=nb[fr];nb[fr]=None
 if pr:p=pr.upper() if p.isupper() else pr
 nb[to]=p;return nb
def uci(m):
 fr,to,pr=m;s=chr(97+fr%8)+str(8-fr//8)+chr(97+to%8)+str(8-to//8)
 return s+pr if pr else s
def ab(b,side,d,a,be):
 if d<=0:return evaluate(b,side)
 ms=gen(b,side)
 if not ms:return evaluate(b,side)
 best=-10**9
 for m in ms:
  v=-ab(apply(b,m),"b" if side=="w" else "w",d-1,-be,-a)
  if v>best:best=v
  if best>a:a=best
  if a>=be:break
 return best
def choose(fen,legal,side):
 b=parse(fen);root=[]
 for u in legal:
  fr=(8-int(u[1]))*8+(ord(u[0])-97);to=(8-int(u[3]))*8+(ord(u[2])-97)
  pr=u[4] if len(u)>4 else None;root.append((fr,to,pr))
 if not root:return legal[0]
 best=None;bv=-10**9
 for m in root:
  v=-ab(apply(b,m),"b" if side=="w" else "w",1,-10**9,10**9)
  if v>bv:bv=v;best=m
 return uci(best) if best else legal[0]
def main():
 while 1:
  g=post("/game",{})
  if g.get("status")=="done":return
  while g.get("status")=="your_move":
   m=choose(g["fen"],g["legal_moves"],g["colour"][0])
   g=post("/move",{"game":g["game"],"move":m})
main()
