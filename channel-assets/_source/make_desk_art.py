import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F="fonts/"; OUT="/home/user/GauravAI/channel-assets/desk-on-autopilot/"
def font(name,size,w=None):
    f=ImageFont.truetype(F+name,size)
    if w is not None:
        try: f.set_variation_by_axes([w])
        except Exception: pass
    return f
NAVY=(14,23,38); NAVY2=(22,35,58); MINT=(61,220,151); MINT_D=(26,120,85); WHITE=(255,255,255); SOFT=(169,183,204); LINE=(38,54,82)
TAG="Automate the tasks you hate. No code, no hype."

def base(W,H):
    img=Image.new("RGB",(W,H),NAVY); px=img.load()
    for y in range(H):
        for x in range(0,W):
            t=(x/W*0.6+y/H*0.4)
            px[x,y]=tuple(int(NAVY[i]+(NAVY2[i]-NAVY[i])*t) for i in range(3))
    return img

def node_graph(d,W,H,seed,alpha_lines=LINE,alpha_dots=(60,82,118),accent_every=7):
    rnd=random.Random(seed); pts=[]
    cols=12; rows=7
    for r in range(rows):
        for c in range(cols):
            x=int((c+0.5)*W/cols+rnd.uniform(-40,40)); y=int((r+0.5)*H/rows+rnd.uniform(-40,40)); pts.append((x,y))
    for i,(x,y) in enumerate(pts):
        for j in (i+1,i+cols):
            if j<len(pts) and rnd.random()<0.55:
                d.line([pts[i],pts[j]],fill=alpha_lines,width=2)
    for i,(x,y) in enumerate(pts):
        r=5 if i%accent_every else 7
        col=MINT_D if i%accent_every==0 else alpha_dots
        d.ellipse([x-r,y-r,x+r,y+r],fill=col)

def glow(img,cx,cy,rx,ry,strength=90,color=MINT):
    m=Image.new("L",img.size,0); ImageDraw.Draw(m).ellipse([cx-rx,cy-ry,cx+rx,cy+ry],fill=strength)
    m=m.filter(ImageFilter.GaussianBlur(rx/2))
    return Image.composite(Image.new("RGB",img.size,color),img,m)

def toggle(d,cx,cy,w,h):
    r=h//2
    d.rounded_rectangle([cx-w//2+6,cy-h//2+10,cx+w//2+6,cy+h//2+10],radius=r,fill=(8,14,24))  # shadow
    d.rounded_rectangle([cx-w//2,cy-h//2,cx+w//2,cy+h//2],radius=r,fill=MINT)
    kx=cx+w//2-r; m=int(h*0.12)
    d.ellipse([kx-r+m+4,cy-r+m+6,kx+r-m+4,cy+r-m+6],fill=(30,150,100))
    d.ellipse([kx-r+m,cy-r+m,kx+r-m,cy+r-m],fill=WHITE)
    # "ON" tick inside knob
    d.line([(kx-14,cy+2),(kx-4,cy+12),(kx+16,cy-10)],fill=MINT,width=8,joint="curve")

def pill(d,x,y,text,f,fg=MINT,bg=(20,60,48)):
    w=d.textlength(text,font=f); h=f.size+18
    d.rounded_rectangle([x,y,x+w+36,y+h],radius=h//2,fill=bg,outline=MINT_D,width=2)
    d.text((x+18,y+8),text,font=f,fill=fg)
    return w+36

# ---------- YouTube banner 2560x1440 ----------
W,H=2560,1440
img=base(W,H); d=ImageDraw.Draw(img)
node_graph(d,W,H,11)
img=glow(img,int(W*0.33),H//2,520,300,70)
d=ImageDraw.Draw(img)
tf=font("ArchivoBlack-Regular.ttf",112); sf=font("PublicSans[wght].ttf",44,600); pf=font("PublicSans[wght].ttf",26,700)
T="Desk on Autopilot"
tw=d.textlength(T,font=tf); sw=d.textlength(TAG,font=sf)
iw=250; gap=64; block=iw+gap+max(tw,sw)
gx=(W-block)/2
toggle(d,int(gx+iw/2),H//2-10,iw,136)
tx=gx+iw+gap
d.text((tx+4,H//2-126+4),T,font=tf,fill=(6,10,18))
d.text((tx,H//2-126),T,font=tf,fill=WHITE)
d.text((tx,H//2+22),TAG,font=sf,fill=MINT)
# pills row under tagline
px=tx; py=H//2+96
for t in ["n8n","Google Sheets","AI","Free templates"]:
    px+=pill(d,px,py,t,pf)+14
img.save(OUT+"banner-2560x1440.png",optimize=True)

# ---------- profile 800 ----------
im=base(800,800); d=ImageDraw.Draw(im)
node_graph(d,800,800,5,accent_every=5)
im=glow(im,400,380,300,300,80); d=ImageDraw.Draw(im)
d.ellipse([70,70,730,730],fill=NAVY2,outline=MINT_D,width=6)
toggle(d,400,370,400,210)
f=font("PublicSans[wght].ttf",52,800)
t="AUTOPILOT"; w=sum(d.textlength(c,font=f) for c in t)+7*(len(t)-1); x=400-w/2
for c in t: d.text((x,515),c,font=f,fill=SOFT); x+=d.textlength(c,font=f)+7
im.save(OUT+"profile-800.png")
im.resize((150,150),Image.LANCZOS).save(OUT+"watermark-150.png")

# ---------- LinkedIn cover 2256x382 and 1536x768 ----------
for (cw,chh,name,tsize,ssize,iw,gap) in [(2256,382,"linkedin-cover-2256x382.jpg",96,38,210,56),(1536,768,"linkedin-cover-1536x768.jpg",92,36,200,52)]:
    im=base(cw,chh); d=ImageDraw.Draw(im); node_graph(d,cw,chh,3)
    im=glow(im,int(cw*0.3),chh//2,int(cw*0.18),chh//2,70); d=ImageDraw.Draw(im)
    tf=font("ArchivoBlack-Regular.ttf",tsize); sf=font("PublicSans[wght].ttf",ssize,600)
    tw=d.textlength(T,font=tf); sw=d.textlength(TAG,font=sf); block=iw+gap+max(tw,sw); gx=(cw-block)/2
    toggle(d,int(gx+iw/2),chh//2,iw,int(iw*0.54))
    tx=gx+iw+gap; ty=chh//2-tsize-8
    d.text((tx+3,ty+3),T,font=tf,fill=(6,10,18)); d.text((tx,ty),T,font=tf,fill=WHITE)
    d.text((tx,chh//2+10),TAG,font=sf,fill=MINT)
    im.save(OUT+name,quality=92)
im=Image.open(OUT+"profile-800.png").resize((400,400),Image.LANCZOS); im.save(OUT+"linkedin-logo-400.png")
print("done")
