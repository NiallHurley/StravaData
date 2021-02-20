
# https://medium.com/@alexander.mueller/rolling-aggregations-on-time-series-data-with-pandas-80dee5893f9
# https://realpython.com/pandas-groupby/

#%%
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
#plt.style.use('seaborn-poster')
# bigger plot elements suitable for giving talks
sns.set_context("talk")


rawdf = pd.read_csv('strava_activities_full.csv')
rawdf['date']=pd.to_datetime(rawdf.start_date_local)
rawdf.sort_values(by=['date'], inplace=True)
rawdf.set_index('date',inplace=True)
print(f'Loaded {len(rawdf)} rows from db')
#%%
df = rawdf.loc[rawdf['type']=='Run']
df['time'] = df.index.time
df['dt']=df.index.date
df.index = pd.to_datetime(df['dt'])
#df.set_index('dt',inplace=True)
df['Rolling'] = df.rolling('7D').distance.sum()

print(f'There are {len(df)} run activities')

#%%
def rolling_avgs_plot(df):    
    # set figure size
    plt.figure(figsize=(16,9))
    df['Rolling7D'] = df.rolling('7D').distance.sum()
    df['Rolling7Dsmoothed'] = df.rolling(7).Rolling7D.mean()
    # Time series plot with Seaborn lineplot() with label
    sns.lineplot(x="dt",y="distance",
                label="Daily", data=df,marker='.',
                ci=None,alpha=.2)
    # 7-day rolling average Time series plot with Seaborn lineplot() with label
    sns.lineplot(x="dt",y="Rolling7D",
                label="7-day distance",
                data=df, marker = '.',dashes = True,
                ci=None,alpha=.3)
    sns.lineplot(x="dt",y="Rolling7Dsmoothed",
                label="7-day smoothed",
                data=df, marker = 'o',dashes = True,
                ci=None,alpha=.9)

    # set axis labels
    plt.xlabel("Date", size=14)
    plt.ylabel("Distance (m)", size=14)
    #plt.gca().set_xticklabels(plt.gca().get_xticklabels(),rotation=90)
    plt.setp(plt.gca().get_xticklabels(), rotation=90)
    plt.title(f"Smoothed 7 day distance")
    # save image as PNG file
    plt.savefig("Strava_Distance_and_7Day_distance.png",
                       format='png',
                       dpi=150)
rolling_avgs_plot(df)
#%%

#%%


def stacked_grouped_hist(tmpdf,x_var,group_var,bins = 10, cmapname='ocean'):
    xlabeltxt = x_var
    xlabelttxt = '7 day distance (m)'
    df_agg = tmpdf.loc[:, [x_var, groupby_var]].groupby(groupby_var)
    vals = [tmpdf[x_var].values.tolist() for i, tmpdf in df_agg]

    # Draw
    plt.figure(figsize=(16,9))
    colormp = plt.cm.get_cmap('ocean')
    colors = [colormp(i/float(len(vals)-1)) for i in range(len(vals))]
    n, bins, patches = plt.hist(vals, bins=bins, stacked=True, density=False, color=colors[:len(vals)])

    # Decoration
    plt.legend({group:col for group, col in zip(np.unique(tmpdf[groupby_var]).tolist(), colors[:len(vals)])})
    plt.title(f"Stacked Histogram of ${x_var}$ colored by ${groupby_var}$", fontsize=22)
    plt.xlabel(xlabeltxt)
    plt.ylabel("Frequency")
    #plt.xticks(ticks=bins, labels=np.unique(tmpdf[x_var]).tolist(), rotation=90, horizontalalignment='left')    
    fig = plt.gcf()
    fig.savefig(f"Strava_Histogram_of_{x_var}_colored_by_{groupby_var}.png",                    format='png',bbox_inches='tight',dpi=150)


x_var = 'Rolling'
groupby_var = 'Year'
bins = 'auto'
df['Year'] = [x.year for x in df['dt']]
stacked_grouped_hist(df,x_var,groupby_var,bins)

