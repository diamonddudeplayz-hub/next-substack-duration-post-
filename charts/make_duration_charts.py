"""Duration/entry-timing post charts. House style from Post 1/2.
Run: python3 charts/make_duration_charts.py"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd, numpy as np

NAVY="#1b3a5b"; ORANGE="#d8732a"; SLATE="#8a9bb0"; INK="#1a1a1a"; GRID="#d9dee6"; LIGHT="#b9c4d2"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":12,
    "axes.edgecolor":"#cfd6df","axes.linewidth":1.0,"figure.dpi":160})

def load(f):
    df=pd.read_excel(f,sheet_name='Table Data'); df.columns=['Date','Px']
    df=df[pd.to_datetime(df['Date'],errors='coerce').notna()].copy()
    df['Date']=pd.to_datetime(df['Date']); df['Px']=pd.to_numeric(df['Px'],errors='coerce')
    return df.dropna().sort_values('Date').reset_index(drop=True)

# ---------- Chart 1: 1-year outcome dispersion by name (HERO) ----------
# worst, median, best, std  (from price_analysis.py)
rows=[("NVIDIA (NVDA)",-55,62,305,ORANGE),
      ("Adobe (ADBE)", -58,-21,105,NAVY),
      ("Itron (ITRI)", -45,22,99,NAVY),
      ("Cheniere (LNG)",-20,13,72,NAVY)]
y=list(range(len(rows)))[::-1]
fig,ax=plt.subplots(figsize=(9.6,5.4))
ax.axvline(0,color="#c7c7c7",lw=1,zorder=1)
for yi,(name,wlo,med,whi,col) in zip(y,rows):
    ax.plot([wlo,whi],[yi,yi],color=col,lw=8.5,solid_capstyle="round",alpha=0.9,zorder=3)
    ax.scatter([med],[yi],color="white",edgecolor=col,s=90,lw=2.5,zorder=4)
    ax.annotate(f"{wlo:+d}%",(wlo,yi),xytext=(-11,0),textcoords="offset points",va="center",ha="right",color="#666",fontsize=10.5)
    ax.annotate(f"{whi:+d}%",(whi,yi),xytext=(12,0),textcoords="offset points",va="center",ha="left",fontweight="bold",color=INK,fontsize=11.5)
# one 'median' callout on the top row so the ring is unambiguous
ax.annotate("median",(62,y[0]),xytext=(0,-15),textcoords="offset points",ha="center",va="top",fontsize=9,color="#9a9a9a")
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows],fontsize=12,color="#2b2b2b")
ax.set_xlim(-98,345); ax.set_xticks([-50,0,50,100,150,200,250,300])
ax.set_xticklabels(["-50%","0","+50%","+100%","+150%","+200%","+250%","+300%"],color="#666",fontsize=9.5)
ax.set_ylim(-0.6,3.7)
for s in ["top","right","left"]: ax.spines[s].set_visible(False)
ax.tick_params(axis="y",length=0); ax.grid(axis="x",color=GRID,lw=0.8,zorder=0)
fig.suptitle("Entry date decided five times as much on NVIDIA as on Cheniere",
    fontsize=15,fontweight="bold",color=INK,x=0.02,ha="left",y=0.965)
fig.text(0.02,0.875,"One-year returns by entry day over five years. Each bar runs from the worst to the best outcome; the ring is the median.",
    fontsize=10.6,color="#666",va="bottom")
fig.text(0.02,0.015,"Every trading day Oct 2021–Oct 2025 as an entry, held one year. Source: LSEG daily closes; author's calculations.",
    fontsize=9,color="#888",style="italic")
fig.subplots_adjust(left=0.175,right=0.95,top=0.80,bottom=0.11)
fig.savefig("charts/entry-dispersion.png",facecolor="white"); print("wrote charts/entry-dispersion.png")

# ---------- Chart 2: Itron price vs 200-week line, annotated ----------
itri=load("itri 5y (1).xlsx")
w=itri.set_index('Date')['Px'].resample('W-FRI').last()
ma=w.rolling(200).mean()
ma_d=ma.reindex(itri['Date'].values,method='ffill').values  # 200w MA aligned to daily
d=itri.copy(); d['ma']=ma_d
d=d[d['Date']>=pd.Timestamp('2025-04-01')].reset_index(drop=True)
x=range(len(d))
fig,ax=plt.subplots(figsize=(9.2,5.2))
ax.plot(x,d['ma'],color=SLATE,lw=2.0,ls=(0,(4,3)),zorder=2,label="200-week line")
ax.plot(x,d['Px'],color=NAVY,lw=2.4,zorder=3,label="ITRI")
def mark(date,txt,dy,col=INK,ha="center",dx=0):
    i=(d['Date']-pd.Timestamp(date)).abs().idxmin(); px=d['Px'].iloc[i]
    ax.scatter([i],[px],color=col,s=30,zorder=5)
    ax.annotate(txt,(i,px),xytext=(dx,dy),textcoords="offset points",ha=ha,fontsize=9.6,color=col,
        fontweight="bold",va="bottom" if dy>0 else "top")
mark('2026-07-27',"pre-print $84.78",-14,"#888")
mark('2026-07-28',"+26% on the Q2 beat,\n$107 intraday",16,ORANGE)
mark('2026-10-22',"now\n$88.17",2,NAVY,ha="left",dx=10)
# inline 200-week label on the dashed line, mid-chart
li=int(len(d)*0.42)
ax.annotate("200-week line",(li,d['ma'].iloc[li]),xytext=(0,-16),textcoords="offset points",color=SLATE,fontsize=10,fontweight="bold",ha="center",va="top")
# x ticks monthly-ish
ticks=[i for i in range(0,len(d),42)]
ax.set_xticks(ticks); ax.set_xticklabels([d['Date'].iloc[i].strftime("%b %y") for i in ticks],fontsize=9,color="#555")
ax.set_ylim(60,145); ax.set_yticks([60,80,100,120,140]); ax.set_yticklabels(["$60","$80","$100","$120","$140"],color="#555")
ax.set_xlim(-3,len(d)+30)
for s in ["top","right"]: ax.spines[s].set_visible(False)
ax.grid(axis="y",color=GRID,lw=0.8,zorder=0)
fig.suptitle("Itron repriced the earnings, not the business",
    fontsize=15.5,fontweight="bold",color=INK,x=0.065,ha="left",y=0.965)
fig.text(0.065,0.875,"The 26% pop on the Q2 print has fully faded. The stock sits back on its 200-week line, with the re-rate still ahead.",
    fontsize=10.6,color="#666",va="bottom")
fig.text(0.065,0.015,"Daily closes and 200-week moving average, Apr 2025–Oct 2026. Source: LSEG; author's calculations.",
    fontsize=9,color="#888",style="italic")
fig.subplots_adjust(left=0.075,right=0.91,top=0.80,bottom=0.11)
fig.savefig("charts/itron-200week.png",facecolor="white"); print("wrote charts/itron-200week.png")

# ---------- Chart 3: the duration / entry-timing spectrum ----------
# names placed by |rate beta| (resilience). Gold is the conceptual far end.
pts=[("Cheniere\n(LNG)",1.6,18,NAVY,'up'),
     ("Itron\n(ITRI)",10.6,33,NAVY,'up'),
     ("Adobe\n(ADBE)",15.7,38,SLATE,'down'),
     ("NVIDIA\n(NVDA)",16.2,91,ORANGE,'up')]
fig,ax=plt.subplots(figsize=(10.2,5.1))
# baseline arrow
ax.annotate("",xy=(20.8,0),xytext=(-0.6,0),
    arrowprops=dict(arrowstyle="-|>",color="#9aa6b4",lw=2.2))
for name,bx,sd,col,side in pts:
    ax.scatter([bx],[0],s=150,color=col,zorder=5,edgecolor="white",lw=1.5)
    if side=='up':
        ax.annotate(name,(bx,0),xytext=(0,30),textcoords="offset points",ha="center",va="bottom",
            fontsize=11.5,fontweight="bold",color=INK)
        ax.annotate(f"β −{bx:.1f}%   σ {sd}",(bx,0),xytext=(0,16),textcoords="offset points",
            ha="center",va="bottom",fontsize=9,color="#777")
    else:
        ax.annotate(name,(bx,0),xytext=(0,-34),textcoords="offset points",ha="center",va="top",
            fontsize=11.5,fontweight="bold",color=INK)
        ax.annotate(f"β −{bx:.1f}%   σ {sd}",(bx,0),xytext=(0,-18),textcoords="offset points",
            ha="center",va="top",fontsize=9,color="#777")
# gold note: it is off this axis, not at the end of it
ax.text(0.985,0.60,"Gold sits off this axis:\nno cash flows, no multiple",transform=ax.transAxes,
    ha="right",va="top",fontsize=9,color="#b08a2e",style="italic")
# pole labels, pinned to the bottom corners so they clear the markers
ax.text(0.015,0.03,"COMMITTED CASH\nrate-resilient · timing is noise",transform=ax.transAxes,
    ha="left",va="bottom",fontsize=9.5,color=NAVY,fontweight="bold")
ax.text(0.985,0.03,"DISCRETIONARY MULTIPLE\nrate-sensitive · timing is the trade",transform=ax.transAxes,
    ha="right",va="bottom",fontsize=9.5,color=ORANGE,fontweight="bold")
ax.set_xlim(-1.5,22); ax.set_ylim(-1.7,1.0)
ax.axis("off")
fig.suptitle("The entry decides the most where the return rides on the multiple",
    fontsize=15,fontweight="bold",color=INK,x=0.03,ha="left",y=0.96)
fig.text(0.03,0.855,"Each name placed by how hard it moves with the ten-year yield (β per +100bp). σ is the spread of one-year outcomes by entry date.",
    fontsize=10.4,color="#666",va="bottom")
fig.text(0.03,0.02,"Rate betas (β per +100bp) from a 60-month regression of monthly returns on the change in the 10-year. Source: LSEG; author's calculations.",
    fontsize=9,color="#888",style="italic")
fig.subplots_adjust(left=0.03,right=0.97,top=0.76,bottom=0.12)
fig.savefig("charts/duration-spectrum.png",facecolor="white"); print("wrote charts/duration-spectrum.png")
