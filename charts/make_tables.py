"""House-style data tables (navy header bar, like the forward-multiples tables)."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
plt.rcParams.update({"font.family":"DejaVu Sans","figure.dpi":160})
NAVY="#1b3a5b"; HDR="#2b4a6b"; INK="#1a1a1a"; ZEBRA="#eef2f6"; RULE="#d9dee6"

def table(fname,title,cols,aligns,widths,rows,source,cw=9.0):
    n=len(rows); rows_total=2+n
    fig_h=0.5*rows_total+1.0
    fig,ax=plt.subplots(figsize=(cw,fig_h)); ax.axis("off")
    ax.set_xlim(0,1); ax.set_ylim(0,1)
    xs=[sum(widths[:i]) for i in range(len(widths))]
    band=0.82/rows_total; top=0.96
    def cellx(a,w,x): return x+(0.012 if a=="left" else (w-0.012 if a=="right" else w/2))
    # title band
    y_t=top-band
    ax.add_patch(Rectangle((0,y_t),1,band,color=NAVY,ec="none"))
    ax.text(0.012,y_t+band/2,title,color="white",fontsize=12.5,fontweight="bold",va="center",ha="left")
    # header band
    y_h=y_t-band
    ax.add_patch(Rectangle((0,y_h),1,band,color=HDR,ec="none"))
    for name,a,w,x in zip(cols,aligns,widths,xs):
        ax.text(cellx(a,w,x),y_h+band/2,name,color="white",fontsize=10.2,fontweight="bold",va="center",ha=a)
    # data rows
    for r,row in enumerate(rows):
        yr=y_h-(r+1)*band
        if r%2==1: ax.add_patch(Rectangle((0,yr),1,band,color=ZEBRA,ec="none"))
        ax.plot([0,1],[yr,yr],color=RULE,lw=0.8)
        for c,(val,a,w,x) in enumerate(zip(row,aligns,widths,xs)):
            ax.text(cellx(a,w,x),yr+band/2,val,color=INK,fontsize=10.4,
                    fontweight="bold" if c==0 else "normal",va="center",ha=a)
    ybot=y_h-n*band
    ax.plot([0,1],[ybot,ybot],color=NAVY,lw=1.4)
    ax.text(0.0,ybot-0.045,source,color="#888",fontsize=8.0,style="italic",va="top",ha="left")
    fig.subplots_adjust(left=0.02,right=0.98,top=0.995,bottom=0.01)
    fig.savefig(f"charts/{fname}",facecolor="white"); print("wrote",fname)

table("table-dispersion.png","One-Year Return by Entry Date, Five Years",
      ["Name","Worst 1-yr","Median","Best 1-yr","Spread (σ)"],
      ["left","right","right","right","right"],[0.34,0.17,0.15,0.17,0.17],
      [["Cheniere (LNG)","−20%","+13%","+72%","18"],
       ["Itron (ITRI)","−45%","+22%","+99%","33"],
       ["Adobe (ADBE)","−58%","−21%","+105%","38"],
       ["NVIDIA (NVDA)","−55%","+62%","+305%","91"]],
      "Every trading day Oct 2021–Oct 2025 taken as an entry, held one year. Spread is the standard deviation of those outcomes. Source: LSEG daily closes; author's calculations.")

table("table-betas.png","Sensitivity to the 10-Year Yield",
      ["Name","Move per +1 point in the 10-year","R²"],
      ["left","right","right"],[0.46,0.38,0.16],
      [["Cheniere (LNG)","−1.6%","0.00"],
       ["Itron (ITRI)","−10.6%","0.08"],
       ["Adobe (ADBE)","−15.7%","0.16"],
       ["NVIDIA (NVDA)","−16.2%","0.10"]],
      "60-month regression of monthly returns on the monthly change in the 10-year yield, Oct 2021–Oct 2026. Source: LSEG; author's calculations.",cw=8.0)
