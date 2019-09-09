# Import packages and load file
import pandas as pd
import pandasql as ps
pysql = lambda q: ps.sqldf(q, globals())

file = 'Adops & Data Scientist Sample Data.xlsx'

# Load file
xls = pd.ExcelFile(file)

# Check if file loaded properly
print(xls.sheet_names)

# Load data to dataframe
df_analytics = xls.parse('Q1 Analytics', skiprows = 0)

# First look at data
print(df_analytics.head())
print(df_analytics.shape)

df_analytics_BDV = df_analytics[df_analytics['country_id'] == "BDV"]

print(df_analytics_BDV.head())
print(df_analytics_BDV.shape)

# Unique site_id for BDV
set_siteId_BDV = df_analytics_BDV['site_id'].unique()
print(set_siteId_BDV)

#For each site_id, number of unique user_id's in 844 rows.
for sid in set_siteId_BDV:
    print(sid, df_analytics_BDV[df_analytics_BDV['site_id'] == sid]['user_id'].unique().shape)
    
# Data between 2019-02-03 00:00:00 and 2019-02-04 23:59:59
df_analytics_timeslice = df_analytics[(df_analytics['ts'] >= '2019-02-03 00:00:00') & (df_analytics['ts'] <= '2019-02-04 23:59:59')] 

# Unique site_id for original dataset
set_siteId = df_analytics['site_id'].unique()
print(set_siteId)

# Sites visited more than 10 times
for sid in set_siteId:
    df_site_visitFreq = df_analytics_timeslice[df_analytics_timeslice['site_id'] == sid].groupby('user_id').count()['site_id'].reset_index(name="count")   
    print(sid) 
    print(df_site_visitFreq[df_site_visitFreq['count'] >= 10])

q1 = """SELECT * FROM df_analytics where user_id == 'LC3561' """
q2 = """SELECT * from (SELECT site_id, user_id, max(ts) FROM df_analytics GROUP BY user_id) where user_id == 'LC3561'"""
q3 = """SELECT site_id, user_id, max(ts) FROM df_analytics GROUP BY user_id"""

# Query: All sites, based on metric of last visited site
q4 = """SELECT site_id, COUNT(user_id) AS total_users FROM (SELECT site_id, user_id, MAX(ts) FROM df_analytics GROUP BY user_id) GROUP BY site_id ORDER BY total_users DESC"""

df1 = pysql(q1)
df2 = pysql(q2)
df3 = pysql(q4)

# All sites, based on metric of last visited site
print(df3)
df3.shape

# Top 3 sites, based on metric of last visited site
print(df3[:3])

q_firstsite = """SELECT user_id, site_id AS site_id_first, min(ts) AS first_visit_ts FROM df_analytics GROUP BY user_id"""
q_lastsite = """SELECT user_id, site_id AS site_id_last, max(ts) AS last_visit_ts FROM df_analytics GROUP BY user_id"""
q5_check = """SELECT * FROM df_analytics where user_id == 'LC06C3' """

df_firstsite = pysql(q_firstsite)
df_lastsite = pysql(q_lastsite)
df3 = pysql(q5_check)
q_sitevisits_firstlast = """SELECT df_firstsite.user_id, df_firstsite.site_id_first, df_lastsite.site_id_last, df_firstsite.first_visit_ts, df_lastsite.last_visit_ts FROM df_firstsite INNER JOIN df_lastsite ON df_firstsite.user_id = df_lastsite.user_id"""
df_sitevisits_firstlast = pysql(q_sitevisits_firstlast)
df_sitevisits_firstlast['same_site_firstlast'] = (df_sitevisits_firstlast['site_id_first'] == df_sitevisits_firstlast['site_id_last'])
# All sites, based on metric of last visited site
print(df_firstsite.head())
print(df_firstsite.shape)

print(df_lastsite.head())
print(df_lastsite.shape)

print(df_sitevisits_firstlast.head())
print(df_sitevisits_firstlast.shape)

print(df_sitevisits_firstlast[df_sitevisits_firstlast['same_site_firstlast'] == True].shape)

