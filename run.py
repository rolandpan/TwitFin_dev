# To run this example in your terminal follow the README.rst for
# getting started, then run: python examples.py

from twitfin import twitfin, read_csv, db_connection, read_sql
from twitfin import load, long_sma, short_sma, diff, macd, flag_swings, sign_sequence


def main(*args, **kwargs):
    """A collection of twitfin functions to be executed as a complete workflow."""

    # Load Quandl data into a dataframe
    df = load()
    # print(df.tail())  # Inspect the loaded data via terminal output

    # Add a columns with long and short simple moving average columns
    df = long_sma(df, 'Close')
    print('* Added column: ' + list(df.columns.values)[-1:][0])
    df = short_sma(df, 'Close')
    print('* Added column: ' + list(df.columns.values)[-1:][0])

    # Add a column with the MACD from the long and short simple moving average columns
    sma_columns = list(df.columns.values)[-2:]
    df = diff(df, sma_columns[0], sma_columns[1], label='MACD_Close')
    print('* Added column: ' + list(df.columns.values)[-1:][0])

    # Add a column with a SMA of the last MACD column
    macd_column = list(df.columns.values)[-1:][0]
    df = macd(df, macd_column, label='SMA_' + macd_column)
    print('* Added column: ' + list(df.columns.values)[-1:][0])

    # Add a column with a MACD the last two columns
    macd_sma_columns = list(df.columns.values)[-2:]
    df = diff(df, macd_sma_columns[0], macd_sma_columns[1])
    print('* Added column: ' + list(df.columns.values)[-1:][0])

    # Add a column that flags the crossovers or sign swings over a given period
    delta_column = list(df.columns.values)[-1:][0]
    df = flag_swings(df, delta_column)
    print('* Added column: ' + list(df.columns.values)[-1:][0])
    df = sign_sequence(df, delta_column)
    print('* Added column: ' + list(df.columns.values)[-1:][0])

    print('\n')
    print('* Current columns: ' + str(list(df.columns.values)))
    print('\n')
    del_columns = raw_input("Enter the names of columns to delete (seperated by commas): ")
    if del_columns:
        for i in del_columns.split():
            if i in list(df.columns.values):
                df.drop(i, axis=1, inplace=True)

    file_name = raw_input("Enter the file name to save as a csv: ")
    file_name = file_name.split('/')[-1]

    print('\n')
    print('* Columns: ' + str(list(df.columns.values)))

    # Execute example IO utilities
    # To write data to csv
    df.to_csv('data/' + file_name + '.csv')
    # print('Modified dataframe saved to: data/standard-example.csv')
    print('\nFile saved. See TwitFin_dev/data/' + file_name + '.csv')
    print('\n')

if __name__ == "__main__":
    # Run all the functions in main()
    df = main()
