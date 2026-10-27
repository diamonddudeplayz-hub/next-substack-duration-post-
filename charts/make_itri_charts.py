"""House-style charts for the Itron Q3 2026 post. Navy + orange, clean grid.
Matches make_charts.py conventions. Run: python3 charts/make_itri_charts.py"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

NAVY="#1b3a5b"; ORANGE="#d8732a"; SLATE="#8a9bb0"; INK="#1a1a1a"; GRID="#d9dee6"; LIGHT="#b9c4d2"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":12,
    "axes.edgecolor":"#cfd6df","axes.linewidth":1.0,"figure.dpi":160})

# --- data: Itron inventory components + product revenue, $M (10-Q/10-K) ---
q    = ["1Q24","2Q24","3Q24","4Q24","1Q25","2Q25","3Q25","4Q25","1Q26","2Q26","3Q26"]
rawm = [205.9,210.4,195.0,199.0,205.9,222.6,199.5,184.7,184.1,200.4,229.5]
fg   = [ 54.6, 47.3, 66.4, 55.1, 59.6, 45.2, 40.6, 44.6, 44.1, 45.4, 37.1]
prod = [527.8,532.9,538.2,532.4,523.1,517.2,494.3,474.3,477.8,453.5,489.0]
x=list(range(len(q)))

fig,ax1=plt.subplots(figsize=(8.9,5.3))
ax2=ax1.twinx()
# product revenue first (context), muted, on right axis
ax2.plot(x,prod,color=SLATE,lw=2.2,ls=(0,(4,3)),zorder=2)
# inventory lines on left axis
ax1.plot(x,rawm,color=NAVY,lw=2.8,zorder=4)
ax1.plot(x,fg,color=ORANGE,lw=2.6,zorder=4)

def endlab(ax,series,color,text,dy=0,bold=True):
    ax.scatter([x[-1]],[series[-1]],color=color,s=26,zorder=5)
    ax.annotate(text,xy=(x[-1],series[-1]),xytext=(x[-1]+0.15,series[-1]+dy),
                color=color,fontsize=11,fontweight="bold" if bold else "normal",va="center")
endlab(ax1,rawm,NAVY,"Raw materials\n$229M",dy=14)
endlab(ax1,fg,ORANGE,"Finished goods\n$37M",dy=-16)
endlab(ax2,prod,SLATE,"Product\nrevenue $489M",dy=0,bold=False)

ax1.set_ylim(0,250); ax1.set_yticks([0,50,100,150,200,250])
ax1.set_yticklabels(["0","$50M","$100M","$150M","$200M","$250M"],color="#555")
ax1.set_ylabel("Inventory",fontsize=10.5,color="#555")
ax2.set_ylim(380,580); ax2.set_yticks([400,450,500,550])
ax2.set_yticklabels(["$400M","$450M","$500M","$550M"],color=SLATE)
ax1.set_xticks(x); ax1.set_xticklabels(q,fontsize=9.3,color="#555")
ax1.set_xlim(-0.3,len(q)+2.2)

for s in ["top"]: ax1.spines[s].set_visible(False); ax2.spines[s].set_visible(False)
ax1.spines["right"].set_visible(False)
ax2.spines["right"].set_color(SLATE)
ax1.grid(axis="y",color=GRID,lw=0.8,zorder=0)

fig.suptitle("Components in, finished goods out",fontsize=15.5,fontweight="bold",
             color=INK,x=0.085,ha="left",y=0.965)
fig.text(0.085,0.875,"Raw materials at a two-year high against sales, finished goods at a two-year low, as revenue turns up.",
         fontsize=10.5,color="#666",va="bottom")
fig.text(0.085,0.015,"Itron inventory components and product revenue, $M, 1Q24-3Q26. Source: Itron 10-Q and 10-K filings.",
         fontsize=9,color="#888",style="italic")
fig.subplots_adjust(left=0.10,right=0.84,top=0.80,bottom=0.11)
out="charts/itri-inventory.png"; fig.savefig(out,facecolor="white"); print("wrote",out)


# ======================================================================
# ARR build + YoY growth
# ======================================================================
fig,ax=plt.subplots(figsize=(8.6,5.2))
qa=["4Q25","1Q26","2Q26","3Q26"]; arr=[368,414,417,423]; yoy=[20,28,21,25]
colors=[NAVY,NAVY,NAVY,ORANGE]
xa=range(len(qa))
ax.bar(xa,arr,color=colors,width=0.6,zorder=3)
for i,(v,g) in enumerate(zip(arr,yoy)):
    ax.annotate(f"${v}M",(i,v),xytext=(0,6),textcoords="offset points",ha="center",
                fontweight="bold",color=INK,fontsize=12)
    ax.annotate(f"+{g}% YoY",(i,v/2),ha="center",va="center",color="white",fontsize=10.5,fontweight="bold")
ax.set_xticks(list(xa)); ax.set_xticklabels(qa,fontsize=10.5,color="#444")
ax.set_ylim(0,470); ax.set_yticks([0,100,200,300,400]); ax.set_yticklabels(["0","$100M","$200M","$300M","$400M"],color="#555")
for s in ["top","right"]: ax.spines[s].set_visible(False)
ax.grid(axis="y",color=GRID,lw=0.8,zorder=0)
fig.suptitle("ARR reaccelerated after the Q2 scare",fontsize=15.5,fontweight="bold",color=INK,x=0.085,ha="left",y=0.965)
fig.text(0.085,0.875,"Annual recurring revenue, with year-over-year growth. Q2's slip to 21% from 28% did not become a trend.",fontsize=10.5,color="#666",va="bottom")
fig.text(0.085,0.015,"Itron reported ARR, 4Q25-3Q26. Source: Itron earnings releases.",fontsize=9,color="#888",style="italic")
fig.subplots_adjust(left=0.085,right=0.95,top=0.80,bottom=0.10)
fig.savefig("charts/itri-arr-build.png",facecolor="white"); print("wrote charts/itri-arr-build.png")

# ======================================================================
# EPS: consensus vs actual, 2026 (the serial beats)
# ======================================================================
fig,ax=plt.subplots(figsize=(8.6,5.2))
qe=["Q1 2026","Q2 2026","Q3 2026"]; cons=[1.25,1.29,1.56]; act=[1.49,1.59,1.94]
beat=[round((a/c-1)*100) for a,c in zip(act,cons)]
xe=range(len(qe)); w=0.36
ax.bar([i-w/2 for i in xe],cons,width=w,color=SLATE,zorder=3,label="Consensus (mean)")
ax.bar([i+w/2 for i in xe],act,width=w,color=NAVY,zorder=3,label="Reported")
for i in xe:
    ax.annotate(f"${cons[i]:.2f}",(i-w/2,cons[i]),xytext=(0,4),textcoords="offset points",ha="center",color="#555",fontsize=10)
    ax.annotate(f"${act[i]:.2f}",(i+w/2,act[i]),xytext=(0,4),textcoords="offset points",ha="center",fontweight="bold",color=INK,fontsize=10.5)
    ax.annotate(f"+{beat[i]}%",(i,max(act[i],cons[i])+0.14),ha="center",color=ORANGE,fontsize=10.5,fontweight="bold")
ax.set_xticks(list(xe)); ax.set_xticklabels(qe,fontsize=10.5,color="#444")
ax.set_ylim(0,2.25); ax.set_yticks([0,0.5,1.0,1.5,2.0]); ax.set_yticklabels(["0","$0.50","$1.00","$1.50","$2.00"],color="#555")
for s in ["top","right"]: ax.spines[s].set_visible(False)
ax.grid(axis="y",color=GRID,lw=0.8,zorder=0)
ax.legend(loc="upper left",fontsize=10,framealpha=0.9)
fig.suptitle("Analysts have under-forecast Itron every quarter of 2026",fontsize=15,fontweight="bold",color=INK,x=0.085,ha="left",y=0.965)
fig.text(0.085,0.875,"Non-GAAP EPS, consensus mean versus reported. The misses did not shrink as the year went on.",fontsize=10.5,color="#666",va="bottom")
fig.text(0.085,0.015,"Consensus from LSEG; reported from Itron earnings releases, 2026.",fontsize=9,color="#888",style="italic")
fig.subplots_adjust(left=0.085,right=0.95,top=0.80,bottom=0.10)
fig.savefig("charts/itri-eps-beats.png",facecolor="white"); print("wrote charts/itri-eps-beats.png")


# ======================================================================
# Non-GAAP EPS year-over-year bridge (waterfall)
# ======================================================================
fig,ax=plt.subplots(figsize=(8.6,5.2))
labs=["Q3 2025","Operating\nincome","Interest\nincome","Tax &\nshare count","Q3 2026"]
# bottoms / heights / colors for a waterfall
bottoms=[0,1.54,1.78,1.78,0]
heights=[1.54,0.38,0.14,0.16,1.94]
cols=[NAVY,SLATE,ORANGE,SLATE,NAVY]
txt=["$1.54","+$0.38","−$0.14","+$0.16","$1.94"]
xb=range(5)
ax.bar(xb,heights,bottom=bottoms,color=cols,width=0.62,zorder=3)
# connector lines
tops=[1.54,1.92,1.78,1.94]
for i in range(4):
    ax.plot([i+0.31,i+1-0.31],[tops[i],tops[i]],color="#b9c4d2",lw=1,zorder=2)
for i,(b,h,t) in enumerate(zip(bottoms,heights,txt)):
    y=b+h+0.03 if i in (0,1,3,4) else b-0.09
    va="bottom" if i in (0,1,3,4) else "top"
    col=ORANGE if i==2 else INK
    ax.annotate(t,(i, (b+h+0.03) if i!=2 else (b-0.02)),ha="center",va="bottom" if i!=2 else "top",
                fontweight="bold",color=col,fontsize=11.5)
ax.set_xticks(list(xb)); ax.set_xticklabels(labs,fontsize=10,color="#444")
ax.set_ylim(0,2.15); ax.set_yticks([0,0.5,1.0,1.5,2.0]); ax.set_yticklabels(["0","$0.50","$1.00","$1.50","$2.00"],color="#555")
for s in ["top","right"]: ax.spines[s].set_visible(False)
ax.grid(axis="y",color=GRID,lw=0.8,zorder=0)
fig.suptitle("The operating line did the work; interest income was the drag",fontsize=14.5,fontweight="bold",color=INK,x=0.085,ha="left",y=0.965)
fig.text(0.085,0.875,"Non-GAAP EPS year-over-year bridge. Interest income fell because the cash went to software acquisitions.",fontsize=10.5,color="#666",va="bottom")
fig.text(0.085,0.015,"Source: Itron Q3 2026 earnings presentation, slide 10.",fontsize=9,color="#888",style="italic")
fig.subplots_adjust(left=0.085,right=0.95,top=0.80,bottom=0.12)
fig.savefig("charts/itri-eps-bridge.png",facecolor="white"); print("wrote charts/itri-eps-bridge.png")
