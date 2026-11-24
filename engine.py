import sys
W=[];TT={};U=[];Q='abcdefgh';R='12345678'
D=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
J=[(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
N=[0]*64;K=[0]*64;PA=[[0]*64,[0]*64];RY=[]
for s in range(64):
 f,r=s&7,s>>3;q=[]
 for a,b in D:
  x,y=f+a,r+b;t=[]
  while 0<=x<8 and 0<=y<8:t+=[y*8+x];x+=a;y+=b
  q+=[t]
 RY+=[q];K[s]=sum(1<<u[0]for u in q if u)
 PA[0][s]=sum(1<<u[0]for u in q[4::2]if u);PA[1][s]=sum(1<<u[0]for u in q[5::2]if u)
 N[s]=sum(1<<((r+b)*8+f+a)for a,b in J if 0<=f+a<8 and 0<=r+b<8)
for p in range(6):
 t=[]
 for s in range(64):
  f,r=s&7,s>>3;c=6-min(f,7-f)-min(r,7-r)
  t+=[(r*4+c*2+100,c*4+310,c*3+322,c*2+496+12*(r==6),c*2+896,20-c*4)[p]]
 W+=[t]
BB=[0]*12;T=0;C=0;E=-1;CM=[15]*64
CM[0]=13;CM[7]=14;CM[56]=7;CM[63]=11
def init(f='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -'):
 global T,C,E
 p=f.split();BB[:]=[0]*12;C=0;E=-1;U.clear();TT.clear();T=p[1]=='b';r=7;x=0
 for c in p[0]:
  if c=='/':r-=1;x=0
  elif c>'9':BB['PNBRQKpnbrqk'.index(c)]|=1<<(r*8+x);x+=1
  else:x+=int(c)
 for c in p[2]:
  if c in'KQkq':C|=1<<'KQkq'.find(c)
 if p[3]!='-':E='abcdefgh'.index(p[3][0])+8*int(p[3][1])-8
def oc():return sum(BB)
def sl(s,o,d):
 a=0
 for i in d:
  for t in RY[s][i]:
   a|=1<<t
   if o>>t&1:break
 return a
def aof(p,s,o):
 if p==1 or p==5:return(N,K)[p==5][s]
 return sl(s,o,((4,5,6,7),(0,1,2,3),(0,1,2,3,4,5,6,7))[p-2])
def bad(s,e):
 o=oc();b=e*6
 if N[s]&BB[b+1]or K[s]&BB[b+5]or PA[e^1][s]&BB[b]:return 1
 x=aof(2,s,o);y=aof(3,s,o)
 return x&(BB[b+2]|BB[b+4])or y&(BB[b+3]|BB[b+4])
def chk(c):
 k=BB[c*6+5]
 return k and bad(k.bit_length()-1,c^1)
def gen():
 M=[];o=oc();c=T;e=c*6;me=sum(BB[e:e+6])
 en=o^me;d=8-16*c;b=BB[e]
 while b:
  l=b&-b;b^=l;s=l.bit_length()-1;r=s>>3;t=s+d
  if t>=0 and not o>>t&1:
   if r==6-5*c:
    M+=[s|t<<6|q<<12 for q in(1,2,3,4)]
   else:
    M.append(s|t<<6)
    if r==1+5*c and not o>>(s+2*d)&1:M.append(s|(s+2*d)<<6)
  a=PA[c][s]&en
  while a:
   l=a&-a;a^=l;t=l.bit_length()-1
   if t>>3==7-7*c:
    M+=[s|t<<6|q<<12 for q in(1,2,3,4)]
   else:M.append(s|t<<6)
  if E>=0 and PA[c][s]>>E&1:M.append(s|E<<6)
 for p in range(1,6):
  b=BB[e+p]
  while b:
   l=b&-b;b^=l;s=l.bit_length()-1;q=aof(p,s,o)&~me
   while q:
    l=q&-q;q^=l;M.append(s|(l.bit_length()-1)<<6)
  if p==5 and not bad(s,c^1):
   h=56*c
   if C>>2*c&1 and not o>>h+5&3 and not bad(h+5,c^1):M.append(h+4|h+6<<6)
   if C>>2*c&2 and not o>>h+1&7 and not bad(h+3,c^1):M.append(h+4|h+2<<6)
 return M
def do(m):
 global T,C,E
 U.append((BB[:],T,C,E))
 f=m&63;t=m>>6&63;pr=m>>12;c=T;e=c*6;o=oc();p=0
 while not BB[e+p]>>f&1:p+=1
 BB[e+p]^=1<<f
 if o>>t&1:
  for i in range(e^6,e^6+6):
   if BB[i]>>t&1:BB[i]^=1<<t
 elif p==0 and t&7!=f&7:BB[(c^1)*6]^=1<<(t-8+16*c)
 if p==5 and abs(t-f)==2:
  a,b=(f+3,f+1)if t>f else(f-4,f-1)
  BB[e+3]^=1<<a|1<<b
 BB[e+(pr or p)]|=1<<t
 if p==5:C&=~(3<<2*c)
 C&=CM[f]&CM[t]
 E=(f+t)//2 if p==0 and abs(t-f)==16 else -1
 T^=1
def undo():
 global T,C,E
 BB[:],T,C,E=U.pop()
def ev():
 s=0
 for i in range(12):
  b=BB[i];g=1 if i<6 else -1
  while b:
   l=b&-b;b^=l;q=l.bit_length()-1
   s+=g*W[i%6][q^56 if g<0 else q]
 return s-2*s*T
def ky():return(tuple(BB),T,C,E)
def s(d,a,b):
 k=ky();g=TT.get(k);bm=g[3]if g else 0
 if g and g[0]>=d and(g[2]==0 or g[2]<0 and g[1]<=a or g[2]>0 and g[1]>=b):return g[1]
 if d<1:return ev()
 o=oc();ms=gen();ms.sort(key=lambda m:-99*(m==bm)-13*((BB[3]|BB[4]|BB[9]|BB[10])>>(m>>6&63)&1)-5*(o>>(m>>6&63)&1))
 bb=-99999;oa=a;f=0
 for m in ms:
  do(m)
  if chk(T^1):undo();continue
  f=1;v=-s(d-1,-b,-a);undo()
  if v>bb:bb=v;bm=m
  if v>a:
   a=v
   if a>=b:break
 if not f:return -99999 if chk(T) else 0
 TT[k]=(d,bb,(bb>=b)-(bb<=oa),bm)
 return bb
def st(m):
 return Q[m&7]+R[m>>3&7]+Q[m>>6&7]+R[m>>9&7]+('','n','b','r','q')[m>>12]
def go(d):
 m=0
 for i in range(d):
  v=s(i+1,-32000,32000);m=TT.get(ky(),(0,0,0,0))[3]or m;print(i+1,v,st(m))
 print('bestmove',st(m))
init()
if __name__=='__main__':
 if len(sys.argv)>2:init(sys.argv[2])
 go(int(sys.argv[1])if len(sys.argv)>1 else 5)
