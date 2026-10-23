import pandas as pd, numpy as np
ENTRY={'ITRI':92.74,'ADBE':274.14,'NVDA':179.78,'LNG':272.03}
FILES={'ITRI':'itri 5y (1).xlsx','ADBE':'adbe 5y.xlsx','LNG':'lng 5y (1).xlsx','NVDA':'nvda 5y.xlsx'}
def load(f):
    df=pd.read_excel(f, sheet_name='Table Data')
    df.columns=['Date','Px']
    df=df[pd.to_datetime(df['Date'],errors='coerce').notna()].copy()
    df['Date']=pd.to_datetime(df['Date']); df['Px']=pd.to_numeric(df['Px'],errors='coerce')
    return df.dropna().sort_values('Date').reset_index(drop=True)

series={k:load(v) for k,v in FILES.items()}
print("POSITION SCORECARD (current = last close 2026-10-22)")
print(f"{'name':5s} {'entry':>8s} {'current':>8s} {'ret%':>7s}  {'5y low':>8s} {'5y high':>8s}")
for k,df in series.items():
    cur=df['Px'].iloc[-1]; e=ENTRY[k]
    print(f"{k:5s} {e:8.2f} {cur:8.2f} {(cur/e-1)*100:7.1f}  {df['Px'].min():8.2f} {df['Px'].max():8.2f}")

print("\n200-WEEK MA (weekly resample; MA needs 200 wks ~3.85y of the 5y file)")
for k,df in series.items():
    w=df.set_index('Date')['Px'].resample('W-FRI').last().dropna()
    ma=w.rolling(200).mean()
    cur=w.iloc[-1]; curma=ma.iloc[-1]
    avail=ma.notna().sum()
    # weeks price below MA in available window
    sub=(w[ma.notna()]<ma[ma.notna()]).mean()*100
    print(f"{k:5s} price {cur:7.2f}  200wMA {curma:7.2f}  price/MA {(cur/curma-1)*100:+6.1f}%  (MA exists {avail} wks; price<MA {sub:.0f}% of them)")

print("\nDRAWDOWN & VOL (full 5y, daily)")
for k,df in series.items():
    px=df['Px']; dd=(px/px.cummax()-1).min()*100
    ret=px.pct_change().dropna(); 
    downside=ret[ret<0].std()*np.sqrt(252)*100
    print(f"{k:5s} maxDD {dd:7.1f}%  ann.vol {ret.std()*np.sqrt(252)*100:5.1f}%  downside.dev {downside:5.1f}%")

print("\nFORWARD 1Y (252d) RETURN DISPERSION over 5y  (how much entry DATE mattered)")
for k,df in series.items():
    px=df['Px'].values
    fwd=[(px[i+252]/px[i]-1)*100 for i in range(len(px)-252)]
    fwd=np.array(fwd)
    print(f"{k:5s} n={len(fwd)}  min {fwd.min():6.0f}%  p25 {np.percentile(fwd,25):6.0f}%  median {np.median(fwd):6.0f}%  p75 {np.percentile(fwd,75):6.0f}%  max {fwd.max():6.0f}%  std {fwd.std():5.0f}")

# rate beta: monthly stock ret vs change in 10y
tr=load('us 10y last 5y.xlsx').rename(columns={'Px':'y10'})
tr=tr.set_index('Date')['y10']
print("\nRATE BETA: regress monthly stock return on monthly change in 10Y (bp). beta = % per +100bp")
for k,df in series.items():
    m=df.set_index('Date')['Px'].resample('MS').last()
    d=pd.concat([m.pct_change(), tr.diff()],axis=1).dropna()
    d.columns=['r','dy']
    if len(d)>10:
        b=np.polyfit(d['dy'], d['r'], 1)[0]*100*100  # per +1.00 (100bp) -> %
        corr=d['r'].corr(d['dy'])
        print(f"{k:5s} n={len(d)}  beta {b:+6.1f}% per +100bp   corr {corr:+.2f}")
