import pandas as pd, numpy as np
FILES={'ITRI':'itri 5y (1).xlsx','ADBE':'adbe 5y.xlsx','LNG':'lng 5y (1).xlsx','NVDA':'nvda 5y.xlsx'}
def load(f):
    df=pd.read_excel(f,sheet_name='Table Data'); df.columns=['Date','Px']
    df=df[pd.to_datetime(df['Date'],errors='coerce').notna()].copy()
    df['Date']=pd.to_datetime(df['Date']); df['Px']=pd.to_numeric(df['Px'],errors='coerce')
    return df.dropna().sort_values('Date').reset_index(drop=True)
# 10Y monthly
t=load('us 10y last 5y.xlsx').rename(columns={'Px':'y10'})
t['M']=t['Date'].dt.to_period('M'); t=t.set_index('M')['y10'].sort_index()
d10=(t.diff()).rename('d10Y_pts')   # month-over-month change in points (1.0 = 100bp)
# stock monthly returns (month-end close)
mret={}
for k,f in FILES.items():
    s=load(f).set_index('Date')['Px'].resample('ME').last()
    s.index=s.index.to_period('M')
    mret[k]=s.pct_change().rename(k)
tab=pd.concat([d10]+[mret[k] for k in FILES],axis=1).dropna()
# regression per name
print("n months:",len(tab))
rows=[]
for k in FILES:
    x=tab['d10Y_pts'].values; yv=tab[k].values
    b,a=np.polyfit(x,yv,1)
    r=np.corrcoef(x,yv)[0,1]
    beta_pct=b*100      # % return per +1.00 (100bp)
    rows.append((k,beta_pct,r**2,r))
    print(f"{k:5s} beta={beta_pct:+6.1f}% per +100bp   R2={r**2:.3f}  corr={r:+.2f}")
# write workbook
out=tab.copy()
for k in FILES: out[k]=(out[k]*100).round(2)   # returns as %
out['d10Y_pts']=out['d10Y_pts'].round(3)
out.index=out.index.astype(str)
summ=pd.DataFrame(rows,columns=['Name','beta_%_per_+100bp','R2','corr']).round(3)
with pd.ExcelWriter('analysis/rate_regression.xlsx') as xl:
    out.to_excel(xl,sheet_name='monthly_data')
    summ.to_excel(xl,sheet_name='regression_summary',index=False)
print("wrote analysis/rate_regression.xlsx")
print(summ.to_string(index=False))
