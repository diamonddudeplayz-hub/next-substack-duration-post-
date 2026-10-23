"""House-style charts for Post 2. Run: python3 charts/make_charts.py
Outputs PNGs into charts/. Matches Post 1 look: navy + orange, clean grid."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

# --- house palette ---
NAVY = "#1b3a5b"
ORANGE = "#d8732a"
SLATE = "#8a9bb0"
INK = "#1a1a1a"
GRID = "#d9dee6"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "axes.edgecolor": "#cfd6df",
    "axes.linewidth": 1.0,
    "figure.dpi": 160,
})

# --- data: daily closes, Oct 2026 (Yahoo Finance) ---
dates = ["Oct 1","Oct 2","Oct 5","Oct 6","Oct 7","Oct 8","Oct 9",
         "Oct 12","Oct 13","Oct 14","Oct 15","Oct 16"]
nvda = [230.86,233.95,238.90,239.24,237.47,230.48,229.28,226.32,228.52,221.30,217.23,214.13]
crwv = [88.57,89.62,87.39,91.72,88.45,81.58,82.08,80.26,77.81,65.78,69.69,61.39]
nbis = [232.28,242.81,232.57,249.87,237.15,219.71,221.07,210.06,206.86,186.01,188.41,165.47]

base = 4  # index to Oct 7 = 100
def idx(series):
    b = series[base]
    return [100.0 * v / b for v in series]

ni, ci, bi = idx(nvda), idx(crwv), idx(nbis)
x = list(range(len(dates)))

fig, ax = plt.subplots(figsize=(8.6, 5.2))

ax.axhline(100, color=GRID, lw=1, zorder=1)
ax.plot(x, ci, color=ORANGE, lw=2.4, zorder=3)
ax.plot(x, bi, color=SLATE, lw=2.4, zorder=3)
ax.plot(x, ni, color=NAVY, lw=2.8, zorder=4)

# Oct 7 reference marker
ax.axvline(base, color=GRID, lw=1, ls=(0, (3, 3)), zorder=1)
ax.annotate("Oct 7 = 100", xy=(base, 108.5), xytext=(base + 0.1, 108.5),
            fontsize=10, color="#7a7a7a", va="center")

# direct end labels
def endlabel(series_idx, name, color, dy=0):
    ax.scatter([x[-1]], [series_idx[-1]], color=color, s=26, zorder=5)
    pct = series_idx[-1] - 100
    ax.annotate(f"{name}  {pct:+.0f}%", xy=(x[-1], series_idx[-1]),
                xytext=(x[-1] + 0.18, series_idx[-1] + dy),
                color=color, fontsize=11.5, fontweight="bold", va="center")

endlabel(ni, "NVIDIA", NAVY, dy=1.8)
endlabel(ci, "CoreWeave", ORANGE, dy=-0.4)
endlabel(bi, "Nebius", SLATE, dy=1.2)

ax.set_xticks(x)
ax.set_xticklabels(dates, fontsize=9.5, color="#555")
ax.set_ylim(66, 110)
ax.set_yticks([70, 80, 90, 100, 110])
ax.set_yticklabels(["70", "80", "90", "100", "110"], color="#555")
ax.set_ylabel("Indexed to Oct 7, 2026 = 100", fontsize=10.5, color="#555")

for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
ax.set_xlim(-0.3, len(dates) + 2.6)

fig.suptitle("The order of damage: NVIDIA fell last, and least",
             fontsize=15.5, fontweight="bold", color=INK, x=0.085, ha="left", y=0.965)
fig.text(0.085, 0.875,
         "Share prices since the October 8 selloff. The lessors fell about three times as far as the chipmaker.",
         fontsize=10.8, color="#666", va="bottom")

fig.text(0.085, 0.015,
         "Daily closing prices, October 1–16, 2026. Source: Yahoo Finance.",
         fontsize=9, color="#888", style="italic")

fig.subplots_adjust(left=0.085, right=0.9, top=0.80, bottom=0.11)
out = "charts/order-of-damage.png"
fig.savefig(out, facecolor="white")
print("wrote", out)


# ======================================================================
# C1: NVIDIA revenue per gigawatt, by chip generation
# Proves "the old chip falling in rent is just a sale of the next one."
# Source: NVIDIA roadmap / non-deal roadshow deck, Sep 2026.
# ======================================================================
gens = ["Hopper", "Blackwell", "Rubin", "Feynman"]
pergw = [18, 25, 40, 60]
gcolors = [SLATE, NAVY, NAVY, ORANGE]  # Feynman (roadmap) in orange

fig, ax = plt.subplots(figsize=(8.6, 5.2))
ax.bar(range(4), pergw, color=gcolors, width=0.62, zorder=3)
for i, v in enumerate(pergw):
    ax.annotate(f"${v}B", (i, v), xytext=(0, 6), textcoords="offset points",
                ha="center", fontweight="bold", color=INK, fontsize=13)

ax.set_xticks(range(4))
ax.set_xticklabels(["Hopper", "Blackwell", "Rubin", "Feynman\n(roadmap)"],
                   fontsize=11.5, color="#444")
ax.set_ylim(0, 70)
ax.set_yticks([0, 20, 40, 60])
ax.set_yticklabels(["0", "$20B", "$40B", "$60B"], color="#555")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)

fig.suptitle("Every upgrade sells for more",
             fontsize=15.5, fontweight="bold", color=INK, x=0.085, ha="left", y=0.965)
fig.text(0.085, 0.875,
         "NVIDIA's revenue per gigawatt, by generation. It pays only if each one earns more per megawatt.",
         fontsize=10.6, color="#666", va="bottom")
fig.text(0.085, 0.02,
         "Revenue per gigawatt of deployed compute. Source: NVIDIA roadmap / non-deal roadshow deck, Sep 2026.",
         fontsize=9, color="#888", style="italic")
fig.subplots_adjust(left=0.085, right=0.95, top=0.80, bottom=0.155)
out = "charts/revenue-per-gw.png"
fig.savefig(out, facecolor="white")
print("wrote", out)


# ======================================================================
# C3: CoreWeave debt stack, by type and cost
# Debunks "the whole company yields 16%." Source: CoreWeave Q2 FY26 10-Q, Note 10.
# ======================================================================
LIGHT = "#b9c4d2"
rows = [
    ("Secured term loans (DDTLs)", 14, "~10%", NAVY),
    ("Unsecured senior notes",     10, "10% coupon, ~16% now", ORANGE),
    ("Convertibles",                7, "2%", LIGHT),
    ("Equipment financing",         5, "~11%", SLATE),
]
labels = [r[0] for r in rows]
amounts = [r[1] for r in rows]
rates = [r[2] for r in rows]
bcolors = [r[3] for r in rows]
y = list(range(len(rows)))[::-1]  # first row on top

fig, ax = plt.subplots(figsize=(9.2, 5.0))
ax.barh(y, amounts, color=bcolors, height=0.62, zorder=3)
# amount in bold + rate underneath, both to the right of the bar.
# the unsecured row (the viral 16%) gets its rate in bold orange so the
# number ties to its bar by colour and position, no clutter on the bar.
for i, (yi, amt, rate) in enumerate(zip(y, amounts, rates)):
    is_viral = (i == 1)
    ax.annotate(f"${amt}B", (amt, yi), xytext=(8, 0), textcoords="offset points",
                va="center", ha="left", fontweight="bold", color=INK, fontsize=12.5)
    ax.annotate(f"at {rate}", (amt, yi), xytext=(8, -14), textcoords="offset points",
                va="center", ha="left",
                color=ORANGE if is_viral else "#777",
                fontweight="bold" if is_viral else "normal",
                fontsize=9.8 if is_viral else 9.2)

# one quiet orange kicker in the whitespace beside the viral bar
ax.annotate("the number that went viral", xy=(10.4, y[1] + 0.34),
            va="center", ha="left", color=ORANGE, fontsize=9.3, style="italic")

ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=11, color="#333")
ax.set_xlim(0, 19)
ax.set_xticks([0, 5, 10, 15])
ax.set_xticklabels(["0", "$5B", "$10B", "$15B"], color="#555")
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.grid(axis="x", color=GRID, lw=0.8, zorder=0)

fig.suptitle("The viral 16% is one slice, not the company",
             fontsize=15.5, fontweight="bold", color=INK, x=0.03, ha="left", y=0.965)
fig.text(0.03, 0.875,
         "CoreWeave's ~$36B of debt, its largest facilities by type and cost. The blended effective rate is about 8%, not 16%.",
         fontsize=10.6, color="#666", va="bottom")
fig.text(0.03, 0.015,
         "Principal outstanding as of June 30, 2026. Source: CoreWeave Q2 FY26 10-Q, Note 10.",
         fontsize=9, color="#888", style="italic")
fig.subplots_adjust(left=0.28, right=0.96, top=0.80, bottom=0.12)
out = "charts/coreweave-debt-stack.png"
fig.savefig(out, facecolor="white")
print("wrote", out)
