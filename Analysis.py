import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from datetime import datetime


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



### 3. how many unique writers post tweets each day?

#copying the original dataframe
twt_u=twt.copy()

#converting the post date column from Unix time to datetime
##twt_u['post_date']=twt_u['post_date'].apply(lambda x: datetime.utcfromtimestamp(x).strftime('%Y-%m-%d'))

###above code equivalent to 
twt_u['post_date'] = dt.datetime(1970,1,1) + pd.to_timedelta(twt_u['post_date'],'s')
twt_u['post_date'] = twt_u['post_date'].dt.date

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
