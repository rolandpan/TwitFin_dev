# To run this example in your terminal follow the README.rst for
# getting started, then run: python examples.py

from TwitFin import twitfin, read_csv, db_connection, read_sql


def main(*args, **kwargs):
    """A collection of TwitFin functions to be executed as a complete workflow."""

    # Load Quandl data into a dataframe
    df = twitfin.load("YAHOO/INDEX_GSPC")
    # print(df.tail())  # Inspect the loaded data via terminal output

    # Add a column with long and short simple moving average columns
    df = twitfin.sma(df, 'GSPC_Close', 20)
    df = twitfin.sma(df, 'GSPC_Close', 10)

    # Add a column with the MACD from the long and short simple moving average columns
    df = twitfin.diff(df, 'SMA_GSPC_Close_20-day', 'SMA_GSPC_Close_10-day', label='MACD_GSPC_Close')

    # Add a column with a SMA of the last MACD column
    df = twitfin.sma(df, 'MACD_GSPC_Close', 3, label='SMA_MACD_GSPC_Close')

    # Add a column with a MACD the last two columns
    df = twitfin.diff(df, 'MACD_GSPC_Close', 'SMA_MACD_GSPC_Close_3-day', label='MACD-Delta-3-day')

    # Add a column that flags the crossovers or sign swings over a given period
    df = twitfin.flag_swings(df, 'MACD-Delta-3-day', 3)

    # Add a column for x-day annotations
    df = twitfin.x_days(df)

    # Transpose the datframe and set the x-day row as our new column labels
    # df = twitfin.x_transpose(df)

    return df


if __name__ == "__main__":
    # Run all the functions in main()
    df = main()

    # Execute example IO utilities
    # To write data to csv
    df.to_csv('data/standard-example.csv')
    print('Modified dataframe saved to: data/standard-example.csv')
    # print('\nData saved to data/gspc.csv')

    # To read data from csv
    # df = read_csv('data/example.csv')
    # df = df.set_index('Date')
    # print('\nData read from csv:')
    # print(df_test.tail())

    # To write data to sql table
    # db = db_connection('sqlite:///data/dev.db')
    # df.to_sql('example', db, if_exists='replace')
    # print('\nData saved to data/dev.db/gspc')

    # To read data from sql table
    # df = read_sql('example', db)
    # df = df.set_index('Date')
    # print('\nData read from sql:')
    # print(df_test.tail())
