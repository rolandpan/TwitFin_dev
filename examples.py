from twitfin import twitfin


# To load Quandl data into a dataframe run:
df = twitfin.load("YAHOO/INDEX_GSPC")
print(df.tail())
# Outputs: 6565 rows loaded into dataframe.

# To write data to csv
df.to_csv('data/gspc.csv')
print('\nData saved to data/gspc.csv')

# To read data from csv
df_test = twitfin.read_csv('data/gspc.csv')
df_test = df_test.set_index('Date')
print('\nData read from csv:')
print(df_test.tail())

# To write data to sql table
db = twitfin.db_connection('sqlite:///data/dev.db')
df.to_sql('gspc', db, if_exists='replace')
print('\nData saved to data/dev.db/gspc')

# To read data from sql table
df_test = twitfin.read_sql('gspc', db)
df_test = df_test.set_index('Date')
print('\nData read from sql:')
print(df_test.tail())
