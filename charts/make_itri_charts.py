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
