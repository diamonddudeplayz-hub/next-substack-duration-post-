def dcf(fcf1,g1,years,g_term,r):
    pv=0.0;fcf=fcf1;peryr=[]
    for t in range(1,years+1):
        if t>1:fcf*=(1+g1)
        d=fcf/((1+r)**t);pv+=d;peryr.append(d)
    tv=fcf*(1+g_term)/(r-g_term);pvtv=tv/((1+r)**years)
    return pv+pvtv,pvtv

def line(name,g1,gt):
    r=0.09
    tot,pvtv=dcf(1,g1,10,gt,r)
    tot2,_=dcf(1,g1,10,gt,r+0.01)
    print(f"{name:9s} g1={g1*100:>3.0f}% gterm={gt*100:>3.1f}%  P/FCF={tot:5.1f}x  val>yr10={pvtv/tot*100:3.0f}%  dV/+100bp={ (tot2-tot)/tot*100:6.1f}%")

print("A) same terminal growth (3%)")
line("Value",0.03,0.03); line("Growth",0.15,0.03)
print("\nB) differentiated terminal growth (more realistic)")
line("Value",0.03,0.02); line("Growth",0.15,0.045)

print("\nC) where timing really bites: multiple's share of a 3-yr return")
# buy multiple M0, exit M1 after n yrs, cashflow CAGR g
def decomp(name,M0,M1,g,n):
    total=((M1/M0)*(1+g)**n)**(1/n)-1
    mult_cagr=(M1/M0)**(1/n)-1
    print(f"{name:10s} {M0:.1f}x->{M1:.1f}x over {n}y, cf g={g*100:.0f}%: total~{total*100:4.1f}%/yr, of which multiple re-rate ~{mult_cagr*100:4.1f}%/yr ({mult_cagr/total*100:3.0f}% of return)")
decomp("Itron-like",15.6,25.0,0.07,3)
decomp("Cheniere-like",10.4,11.5,0.06,3)

print("\nD) cost of a 20% worse entry vs missing a one-time 50% re-rate (per yr, over hold)")
for n in [3,5,7]:
    drag=(0.8)**(1/n)-1
    miss=(1/1.5)**(1/n)-1
    print(f" hold {n}y: 20% worse entry = {drag*100:5.1f}%/yr drag;  missing +50% re-rate = {miss*100:5.1f}%/yr")
