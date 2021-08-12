import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib as mpl


twt = pd.read_csv("Tweet.csv")
stk = pd.read_csv("CompanyValues.csv")
ct=pd.read_csv("Company_Tweet.csv")

twt.info()
stk.info()
ct.info()


##### Exploratory Analysis #####


### 1. does each tweet only mention one company?

#distinct counting the company symbol per tweet_id
ct['distinct_count']=ct.groupby('tweet_id')['ticker_symbol'].transform('nunique') 

#getting rid of the ticker_symbol column
ct_ut=ct.drop('ticker_symbol', axis=1) 

#getting rid of all duplicated values
ct_ut=ct_ut.drop_duplicates()

#sorting by the distinct count column
ct_ut=ct_ut.sort_values(by=['distinct_count'], ascending=False)
###there are tweet_id that are aligned to multiple companies. so tweet_id is not unique to company



### 2. how many individuals have posted these tweets
len(twt['writer'].drop_duplicates())



### 3a. how many unique writers post tweets each day?

#copying the original dataframe
twt_u=twt.rename(columns={'post_date':'post_datetime'})

#converting the post date column from Unix time to datetime
twt_u['post_datetime'] = dt.datetime(1970,1,1) + pd.to_timedelta(twt_u['post_datetime'],'s')

#want to have 2 column for date. one with time, one with time set at equal time so only the date is considered.

#twt_u['post_date'] = twt_u['post_date'].dt.date     this code change the datatype to str
###above code equivalent to 
##twt_u['post_date']=twt_u['post_date'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%Y-%m-%d'))
##same problem though. end datatype is str

#performance testing between .replace and .normalize. both functions set time at midnight
#start_time = time.time()
twt_u['post_date'] = twt_u['post_datetime'].apply(lambda x: x.replace(hour=0, minute=0, second=0, microsecond=0))
#print("--- %s seconds ---" % (time.time() - start_time))

##start_time = time.time()
##twt_u['post_date'] = twt_u['post_datetime'].apply(lambda x: x.normalize())
##print("--- %s seconds ---" % (time.time() - start_time))
# 24.7287 seconds (.replace) vs. 27.4480 seconds (.normalize)

#pivotting 'writer' distinct counts by year and month
twt_u_piv1=pd.pivot_table(twt_u, 
                          index=twt_u['post_date'].dt.month, 
                          columns=twt_u['post_date'].dt.year, 
                          values='writer', 
                          aggfunc=lambda x: len(x.unique()))
twt_u_piv1.index.rename('Month', inplace=True)
twt_u_piv1.columns.rename('Year', inplace=True)

##plotting
plot1=twt_u_piv1.plot(color=['#D6EAF8','#85C1E9','#3498DB','#2874A6','#C0392B'],
                linewidth=2,
                figsize=(20,12))
plt.ylabel('Distinct Number of Writers', labelpad=15)
plt.xlabel('Month', labelpad=15)
plt.title('How Many Distinct Number of Writers Posted Tweets Each Month Over the Years?', 
          fontdict={'size':25, 'weight':'bold'},
          pad=20)
plot1.yaxis.set_major_formatter(
    mpl.ticker.StrMethodFormatter('{x:,.0f}')) #y axis number format include commas
#plot1.figure

### 3b. when do most tweets get published through the day over the years?

#pivotting distinct count of tweets over hours of the day and years
twt_u_piv2=pd.pivot_table(twt_u, 
                          index=twt_u['post_datetime'].dt.hour, 
                          columns=twt_u['post_datetime'].dt.year, 
                          values='tweet_id', 
                          aggfunc=lambda x: len(x.unique()))
twt_u_piv2.index.rename('Month',inplace=True)#=['Month']
twt_u_piv2.columns.rename('Year', inplace=True)

##plotting
plot2=twt_u_piv2.plot.bar(color=['#D6EAF8','#85C1E9','#3498DB','#2874A6','#C0392B'],
                          figsize=(20,12),
                          width=0.9)
plt.ylabel('Distinct Number of Tweets', labelpad=15)
plt.xlabel('Hour', labelpad=15)
plt.title('Hourly Distribution of Tweet Counts Over the Years', 
          fontdict={'size':25, 'weight':'bold'},
          pad=20)
plot2.yaxis.set_major_formatter(
    mpl.ticker.StrMethodFormatter('{x:,.0f}')) #y axis number format include commas
















#########################Note#########################

twt_u_piv1.reset_index()






#distinct counting writer per day
twt_u['distinct_user_count']=twt_u.groupby('post_date')['writer'].transform('nunique')

#dropping all columns except post date and distinct user count columns
twt_u=twt_u[['post_date','distinct_user_count']]

#getting rid of all duplicated values
twt_u=twt_u.drop_duplicates()

#indexing the date for graphing
twt_u=twt_u.set_index('post_date')

#line graph x=post date, y=distinct user count
plt.plot(twt_u)

#histogram of the distinct user count
plt.hist(twt_u, bins=50)

##merging twt with company code
twt_m=twt.merge(ct,on='tweet_id',how='left')












##time unit conversion - posixct (seconds after 1970-01-01)
twt_m['post_date']=dt.datetime(1970,1,1)+pd.to_timedelta(twt_m['post_date'],'s')

##graphing
twt_m_piv=twt_m.pivot_table('tweet_id', 'post_date', 'ticker_symbol', aggfunc=pd.Series.nunique )
plt.plot(twt_m_piv.AAPL, color="red")
plt.plot(twt_m_piv.AMZN, color="yellow")
plt.plot(twt_m_piv.GOOG, color="orange")
plt.plot(twt_m_piv.GOOGL, color="green")
plt.plot(twt_m_piv.MSFT, color="blue")
plt.plot(twt_m_piv.TSLA, color="purple")




a=twt_m.head()

twt_m_piv=twt_m_piv.reset_index()






twt_m_piv.info()

plt.rcParams["figure.figsize"]=(20,12)
twt_m_piv.plot(kind='line',x='post_date',y='AAPL', linewidth=1)








ts=128410148
print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
ts.info()
