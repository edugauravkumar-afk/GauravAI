import math, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F="fonts/"  # folder holding the downloaded .ttf files
OUT="channel-assets/"
def font(name,size,wght=None):
    f=ImageFont.truetype(F+name,size)
    if wght is not None:
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f
def center_text(d,cx,y,text,f,fill,spacing=0):
    if spacing:
        w=sum(d.textlength(c,font=f) for c in text)+spacing*(len(text)-1); x=cx-w/2
        for c in text: d.text((x,y),c,font=f,fill=fill); x+=d.textlength(c,font=f)+spacing
        return w
    w=d.textlength(text,font=f); d.text((cx-w/2,y),text,font=f,fill=fill); return w
def vgrad(W,H,top,bot):
    img=Image.new("RGB",(W,H),top); px=img.load()
    for y in range(H):
        t=y/(H-1); c=tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3))
        for x in range(W): px[x,y]=c
    return img
def hexc(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
BW,BH=2560,1440; SAFE_W,SAFE_H=1546,423; SY0=(BH-SAFE_H)//2

# ---------- 1. Desk on Autopilot ----------
NAVY=hexc("0E1726"); NAVY2=hexc("16233A"); MINT=hexc("3DDC97"); WHITE=(255,255,255); SOFT=hexc("A9B7CC")
def toggle(d,cx,cy,w,h,on=True):
    r=h//2
    d.rounded_rectangle([cx-w//2,cy-h//2,cx+w//2,cy+h//2],radius=r,fill=MINT if on else SOFT)
    kx=cx+w//2-r if on else cx-w//2+r
    m=int(h*0.12)
    d.ellipse([kx-r+m,cy-r+m,kx+r-m,cy+r-m],fill=WHITE)
# profile
im=Image.new("RGB",(800,800),NAVY); d=ImageDraw.Draw(im)
d.ellipse([60,60,740,740],fill=NAVY2)
toggle(d,400,360,420,220)
center_text(d,400,505,"AUTOPILOT",font("PublicSans[wght].ttf",54,800),SOFT,spacing=6)
im.save(OUT+"desk-on-autopilot/profile-800.png")
# banner
im=vgrad(BW,BH,NAVY,NAVY2); d=ImageDraw.Draw(im)
for x in range(0,BW,64):
    for y in range(0,BH,64): d.ellipse([x-2,y-2,x+2,y+2],fill=(30,45,70))
tf=font("ArchivoBlack-Regular.ttf",104); sf=font("PublicSans[wght].ttf",42,600)
T="Desk on Autopilot"; S="Your admin, on autopilot. One real build every week."
tw=max(d.textlength(T,font=tf),d.textlength(S,font=sf)); iw=260; gap=60
gx=(BW-(iw+gap+tw))/2
toggle(d,int(gx+iw/2),BH//2,iw,140)
tx=gx+iw+gap
d.text((tx,BH//2-112),T,font=tf,fill=WHITE)
d.text((tx,BH//2+26),S,font=sf,fill=MINT)
im.save(OUT+"desk-on-autopilot/banner-2560x1440.png",optimize=True)

# ---------- 2. Gold and Ruin ----------
INK=hexc("120E0B"); INK2=hexc("231912"); GOLD=hexc("C9A44C"); GOLD_D=hexc("8C6E2A"); GOLD_L=hexc("E8CD7E"); CREAM=hexc("EFE6D2")
def coin(d,cx,cy,R,crack=True):
    d.ellipse([cx-R,cy-R,cx+R,cy+R],fill=GOLD_D)
    d.ellipse([cx-R+14,cy-R+14,cx+R-14,cy+R-14],fill=GOLD)
    d.ellipse([cx-R+44,cy-R+44,cx+R-44,cy+R-44],outline=GOLD_D,width=8)
    for i in range(48):
        a=2*math.pi*i/48; r1=R-26; r2=R-36
        d.line([cx+r1*math.cos(a),cy+r1*math.sin(a),cx+r2*math.cos(a),cy+r2*math.sin(a)],fill=GOLD_D,width=4)
    g=font("Cinzel[wght].ttf",int(R*0.95),800)
    w=d.textlength("G",font=g); bb=d.textbbox((0,0),"G",font=g)
    d.text((cx-w/2+4,cy-(bb[1]+bb[3])/2+4),"G",font=g,fill=GOLD_D)
    d.text((cx-w/2,cy-(bb[1]+bb[3])/2),"G",font=g,fill=GOLD_L)
    if crack:
        pts=[(cx+R*0.15,cy-R-5),(cx-R*0.05,cy-R*0.45),(cx+R*0.18,cy-R*0.15),(cx-R*0.12,cy+R*0.2),(cx+R*0.1,cy+R*0.5),(cx-R*0.08,cy+R+5)]
        left=[(x-10,y) for x,y in pts]; right=[(x+10,y) for x,y in reversed(pts)]
        d.polygon(left+right,fill=INK)
im=Image.new("RGB",(800,800),INK); d=ImageDraw.Draw(im)
coin(d,400,400,300)
im.save(OUT+"gold-and-ruin/profile-800.png")
im=vgrad(BW,BH,INK2,INK); 
glow=Image.new("L",(BW,BH),0); gd=ImageDraw.Draw(glow); gd.ellipse([BW//2-900,BH//2-380,BW//2+900,BH//2+380],fill=70)
glow=glow.filter(ImageFilter.GaussianBlur(160)); im=Image.composite(Image.new("RGB",(BW,BH),hexc("5A4220")),im,glow)
d=ImageDraw.Draw(im)
tf=font("Cinzel[wght].ttf",132,800); sf=font("CormorantGaramond-Italic[wght].ttf",60,500)
w=center_text(d,BW//2,BH//2-150,"GOLD AND RUIN",tf,GOLD,spacing=14)
y=BH//2+30
d.line([BW//2-w/2,y,BW//2-140,y],fill=GOLD_D,width=3); d.line([BW//2+140,y,BW//2+w/2,y],fill=GOLD_D,width=3)
d.polygon([(BW//2,y-14),(BW//2+14,y),(BW//2,y+14),(BW//2-14,y)],fill=GOLD)
center_text(d,BW//2,BH//2+62,"How fortunes were made, and how empires lost them.",sf,CREAM)
im.save(OUT+"gold-and-ruin/banner-2560x1440.png",optimize=True)

# ---------- 3. Twist of Myth ----------
INDIGO=hexc("1B1638"); TEAL=hexc("0F3B44"); AMBER=hexc("F2B35E"); PARCH=hexc("F3E9D2")
def stars(d,W,H,n,seed,box=None):
    rnd=random.Random(seed)
    for _ in range(n):
        x=rnd.randrange(W); y=rnd.randrange(H); r=rnd.choice([1,1,2,2,3])
        d.ellipse([x-r,y-r,x+r,y+r],fill=(235,225,200))
def spiral(d,cx,cy,turns,maxr,width,col):
    pts=[]; N=600
    for i in range(N+1):
        t=i/N; a=t*turns*2*math.pi; r=maxr*t
        pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
    d.line(pts,fill=col,width=width,joint="curve")
im=vgrad(800,800,INDIGO,TEAL); d=ImageDraw.Draw(im); stars(d,800,800,60,3)
spiral(d,400,400,3.2,250,26,AMBER)
d.ellipse([388,388,412,412],fill=PARCH)
im.save(OUT+"twist-of-myth/profile-800.png")
im=vgrad(BW,BH,INDIGO,TEAL); d=ImageDraw.Draw(im); stars(d,BW,BH,380,7)
tf=font("IMFeENrm28P.ttf",150); sf=font("IMFeENit28P.ttf",58)
T="Twist of Myth"; S="Old myths and legends, retold with a twist."
tw=max(d.textlength(T,font=tf),d.textlength(S,font=sf)); iw=280; gap=70
gx=(BW-(iw+gap+tw))/2
spiral(d,int(gx+iw/2),BH//2,2.6,iw//2,16,AMBER)
tx=gx+iw+gap
d.text((tx,BH//2-150),T,font=tf,fill=PARCH)
d.text((tx,BH//2+30),S,font=sf,fill=AMBER)
im.save(OUT+"twist-of-myth/banner-2560x1440.png",optimize=True)

# ---------- preview sheet for checking ----------
prev=Image.new("RGB",(1600,1500),(240,240,240))
y=10
for ch in ["desk-on-autopilot","gold-and-ruin","twist-of-myth"]:
    b=Image.open(OUT+ch+"/banner-2560x1440.png").resize((1280,720)); p=Image.open(OUT+ch+"/profile-800.png").resize((300,300))
    mask=Image.new("L",(300,300),0); ImageDraw.Draw(mask).ellipse([0,0,300,300],fill=255)
    bb=b.crop((0,(720-SAFE_H//2*1)//2 - 0, 1280, (720-SAFE_H//2)//2 + SAFE_H//2))
    prev.paste(b.crop((0,250,1280,470)),(10,y)); prev.paste(p,(1295,y-40 if y>10 else y),mask)
    d=ImageDraw.Draw(prev); 
    y+=490
prev=prev.crop((0,0,1600,y))
prev.save("preview.png")
print("done")
