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
rows=[("NVIDIA (NVDA)",-55,62,305,91,ORANGE),
      ("Adobe (ADBE)", -58,-21,105,38,NAVY),
      ("Itron (ITRI)", -45,22,99,33,NAVY),
      ("Cheniere (LNG)",-20,13,72,18,NAVY)]
y=list(range(len(rows)))[::-1]
fig,ax=plt.subplots(figsize=(9.2,5.2))
ax.axvline(0,color="#b9b9b9",lw=1,zorder=1)
for yi,(name,wlo,med,whi,sd,col) in zip(y,rows):
    ax.plot([wlo,whi],[yi,yi],color=col,lw=7,solid_capstyle="round",alpha=0.85,zorder=3)
    ax.scatter([med],[yi],color="white",edgecolor=col,s=70,lw=2.2,zorder=4)
    ax.annotate(f"{wlo:+d}%",(wlo,yi),xytext=(1,-12),textcoords="offset points",va="top",ha="left",color="#888",fontsize=9.3)
    ax.annotate(f"{whi:+d}%",(whi,yi),xytext=(9,0),textcoords="offset points",va="center",ha="left",fontweight="bold",color=INK,fontsize=10.5)
    ax.annotate(f"σ {sd}",(whi,yi),xytext=(9,-13),textcoords="offset points",va="center",ha="left",color=col if col==ORANGE else "#888",fontweight="bold" if col==ORANGE else "normal",fontsize=9.3)
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows],fontsize=11.5,color="#333")
ax.set_xlim(-75,330); ax.set_xticks([-50,0,50,100,150,200,250,300])
ax.set_xticklabels(["-50%","0","+50%","+100%","+150%","+200%","+250%","+300%"],color="#555",fontsize=9.5)
for s in ["top","right","left"]: ax.spines[s].set_visible(False)
ax.tick_params(axis="y",length=0); ax.grid(axis="x",color=GRID,lw=0.8,zorder=0)
fig.suptitle("Entry date decided five times as much on NVIDIA as on Cheniere",
    fontsize=15,fontweight="bold",color=INK,x=0.02,ha="left",y=0.965)
fig.text(0.02,0.875,"Spread of one-year returns by entry day, last five years. Each bar runs worst to best; the ring is the median.",
    fontsize=10.6,color="#666",va="bottom")
fig.text(0.02,0.015,"Every trading day Oct 2021–Oct 2025 as an entry, held one year. Source: LSEG daily closes; author's calculations.",
    fontsize=9,color="#888",style="italic")
fig.subplots_adjust(left=0.165,right=0.93,top=0.80,bottom=0.11)
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
