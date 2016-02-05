#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# change log:
# 2016-02-04 - RP
#    altered functions: load(), long and short_sma() etc., enabled passing args w/o prompts
#    in sign_sequence: got rid of consolidation to single column

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals
)

import numpy as np
import pandas as pd
import Quandl
import os
# from sqlalchemy import sqlalchemy  # from flask.ext.


class twitfin(object):
    """This is a description of the class."""

    #: An example class variable.
    aClassVariable = True

    def __init__(self, argumentName, anOptionalArg=None):
        """Initialization method.
        :param argumentName: an example argument.
        :type argumentName: string
        :param anOptionalArg: an optional argument.
        :type anOptionalArg: string
        :returns: New instance of :class:`twitfin`
        :rtype: twitfin
        """

        self.instanceVariable1 = argumentName

        if self.aClassVariable:
            print('Hello')

        if anOptionalArg:
            print('anOptionalArg: %s' % anOptionalArg)


def load(*args, **kwargs):
    """Load data from Quandl into a dataframe, modify column names and
    check for non-numeric values."""
    # Grab the Quandl token
    # token = os.environ.get('QUANDL_TOKEN')
    # if token is None:
    
    if 'token' in kwargs:
        token = kwargs['token']
    else:
        token = raw_input("Enter Quandl token: ")
    
    if 'ticker' in kwargs:
        ticker = kwargs['ticker']
    else:
        ticker = raw_input("Enter Quandl ticker symbol (or hit Enter for default of YAHOO/INDEX_GSPC): ")
    
    if len(ticker) < 1:
        ticker = 'YAHOO/INDEX_GSPC'
    print(ticker)
    
    if 'start_date' in kwargs:
        start_date = kwargs['start_date']
    else:
        start_date = raw_input("Enter start date as YYYY-MM-DD (or hit ENTER for default of 1990-01-01): ")
    
    if len(start_date) < 1:
        start_date = '1990-01-01'
    print(start_date)
    
    # Call Quandl module, trim input by default from 1990 forward
    print('Pulling Quandl data...')
    df = Quandl.get(ticker, authtoken=token, trim_start=start_date)
    # Get the column labels
    # old_columns = list(df.columns.values)
    # Use the ticker symbol as our new prefix
    # ticker_tag = ticker.split('_')[-1] + '_'
    # Drop spaces and concatenate
    # new_labels = [ticker_tag + i.replace(' ', '') for i in old_columns]
    # Create a dictionary of old and new column labels
    # new_columns = dict(zip(old_columns, new_labels))
    # Rename the columns using our dictionary
    # df = df.rename(columns=new_columns)
    nulls = df[~df.applymap(np.isreal).all(1)]
    # Check for non-numeric values
    if len(nulls) > 0:
        raise ValueError('Dataframe contains non-numeric values')
    row_count = len(df)
    print('%d rows loaded into dataframe.' % row_count)
    return df

def long_sma(df, column, *args, **kwargs):
    """Given a dataframe, a column name and a period the function
    returns a dataframe with new column with a simple moving average
    for the period."""
    ### SMA function parameters
    # 1st parameter: target dataframe
    # 2nd parameter: target column
    # 3rd parameter: the period for the moving average
    # 4th paramter, optional: supply a label to be appended with period info,
    # for example df = twitfin.sma(df, 'GSPC_Close', 20, label='Close')
    # will result in a column label of 'Close_20-day'.
    # The default label is constructed as follows:
    # SMA_{ target column }_{ period }-day
    
    if 'period' in kwargs:
        period = kwargs['period']
    else:
        period = int(raw_input("Enter the period in days for the long SMA: "))
    # to add: default period = 26
    
    if 'label' in kwargs:
        column_label = kwargs['label'] + '_' + str(period) + '-day'
    else:
        column_label = 'SMA_' + column + '_' + str(period) + '-day'
    df[column_label] = pd.stats.moments.rolling_mean(df[column], period)
    return df

def short_sma(df, column, *args, **kwargs):
    """Given a dataframe, a column name and a period the function
    returns a dataframe with new column with a simple moving average
    for the period."""
    
    if 'period' in kwargs:
        period = kwargs['period']
    else:
        period = int(raw_input("Enter the period in days for the short SMA: "))
        
    if 'label' in kwargs:
        column_label = kwargs['label'] + '_' + str(period) + '-day'
    else:
        column_label = 'SMA_' + column + '_' + str(period) + '-day'
    df[column_label] = pd.stats.moments.rolling_mean(df[column], period)
    return df

def diff(df, column_a, column_b, **kwargs):
    """Creates a new column from the differnce of column_a and column_b,
    as column_a minus column_b."""
    ### diff function parameters
    # 1st parameter: target dataframe
    # 2nd parameter: target column_a
    # 3rd parameter: target column_b
    # TODO: describe default label and custom label options
    column_a_suffix = column_a.split('_')[-1]
    column_b_suffix = column_b.split('_')[-1]
    column_prefix = "_".join(column_b.split('_')[0:2])
    if 'label' in kwargs:
        column_label = kwargs['label']
    else:
        column_label = 'Delta_' + column_prefix + '_' + column_a_suffix + '_' + column_b_suffix
    df[column_label] = df[column_a] - df[column_b]
    return df

def macd(df, column, *args, **kwargs):
    """Given a dataframe, a column name and a period the function
    returns a dataframe with new column with a simple moving average
    for the period."""
    
    if 'period' in kwargs:
        period = kwargs['period']
    else:
        period = int(raw_input("Enter the period in days for the SMA of the MACD: "))
        
    if 'label' in kwargs:
        column_label = kwargs['label'] + '_' + str(period) + '-day'
    else:
        column_label = 'SMA_' + column + '_' + str(period) + '-day'
    df[column_label] = pd.stats.moments.rolling_mean(df[column], period)
    return df

def flag_swings(df, column, *args, **kwargs):
    """Given a dataframe and column and a minimum sequence period
    for the same sign, the function returns: "1" for upward swings,
    "-1" for downward swings, or "0" if niether condition is met."""
    ### flag_swings function parameters
    # 1st parameter: target dataframe
    # 2nd parameter: target column
    # 3rd parameter: minimum swing period
    # TODO: describe default label and custom label options
    if 'period' in kwargs:
        period = kwargs['period']
    else:
        period = int(raw_input("Enter the period in days to flag swings: "))
    
    if 'label' in kwargs:
        # Append custom label with period days
        column_label = kwargs['label'] + '_' + str(period) + '-day'
    else:
        column_label = 'SwingFlag_' + str(period) + '-day'
    # Trim null value artifacts in SMA columns
    df = df.dropna()
    # Create a temporary dataframe
    tmp = df.copy()
    tmp['sum'] = 0
    # Determine the sign of each day and sum signs from prior days using the
    # "x-day" notation as "sign-'reference day'"
    tmp['sign-0'] = [1 if x >= 0 else -1 for x in df[column]]
    if period < 2:
        raise ValueError('The minimum swing period should be 2 days.')
    else:
        # Shift rows down for lateral comparison depending on period
        for i in range(1, period):
            label = 'sign-' + str(i)
            tmp[label] = tmp['sign-0'].shift(i)
            # The sum of consecutive signs agregates here
            tmp['sum'] = tmp['sum'] + tmp[label]

    # The we shift the sum signs by one to compare prior sequence history
    tmp['sum-shift'] = tmp['sum'].shift(1)

    def flagger(sign_now, sign_prior, sign_run, sign_sum, period):
        # flagger contains the logical for lateral comparison of time-shifted
        # sign data, agregations and time-shifted agregations
        if sign_now > sign_prior and abs(sign_run) >= period - 1 and sign_sum != 0:
            # Indicates a positive sign after a sufficient period of negative signs
            return 1  # Also referred to here as an upward swing or crossover
        else:
            if sign_now < sign_prior and abs(sign_run) >= period - 1 and sign_sum != 0:
                # Indicates a negative sign after a sufficient period of positive signs
                return -1  # Also referred to here as an downward swing or crossover
            else:
                # Otherwaise returning zero. Zero could still be a sign change
                # but prior minimum sign sequence period criteria was not met.
                return 0

    try:
        df = df.copy()
        df[column_label] = [flagger(n, p, r, s, period) for n, p, r, s in zip(tmp['sign-0'], tmp['sign-1'], tmp['sum-shift'], tmp['sum'])]
    except Exception as e:
        print(e)
        if e =='SettingWithCopyWarning':
            pass
    return df

def transpose_column(df, column, *args, **kwargs):
    """Given a dataframe and column, returns df with added columns
    of prior date data for the given period."""
    
    if 'period' in kwargs:
        period = kwargs['period']
    else:
        period = int(raw_input("Enter the days prior to list the signs: "))
        
    # Trim null value artifacts in SMA columns
    df = df.dropna()
    # Create a temporary dataframe
    tmp = df.copy()
    # Determine the sign of each day and sum signs from prior days using the
    # "x-day" notation
    label0 = column + '-0'
    tmp[label0] = df[column]
    
    # Shift rows down for lateral comparison depending on period
    for i in range(1, period):
        label = column +'-'+ str(i)
        tmp[label] = tmp[label0].shift(i)
    # get rid of NA rows
    tmp2 = tmp.ix[(period -1):]
    return tmp2


def sign_sequence(df, column, *args, **kwargs):
    """Given a dataframe and column, returns a column with a list
    of prior signs for the given period."""
    
    if 'period' in kwargs:
        period = kwargs['period']
    else:
        period = int(raw_input("Enter the days prior to list the signs: "))
        
    # prior_signs_label = 'SignSequence_' + str(period) + '-days'
    # Trim null value artifacts in SMA columns
    df = df.dropna()
    # Create a temporary dataframe
    tmp = df.copy()
    # Determine the sign of each day and sum signs from prior days using the
    # "x-day" notation as "sign-'reference day'"
    label0 = column + '_sign-0'
    tmp[label0] = ['1' if x >= 0 else '-1' for x in df[column]]
    # Shift rows down for lateral comparison depending on period
    # labels = ['sign-0']
    for i in range(1, period):
        label = column +'_sign-'+ str(i)
        # labels.append(label)
        tmp[label] = tmp[label0].shift(i)
    # get rid of NA rows
    tmp2 = tmp.ix[(period -1):]
    return tmp2
 
# Get rid of consolidation under one column    
#    df2 = df.ix[(period -1):]
#    labels = labels[::-1]
#    try:
#        df2 = df2.copy()
#        df2[prior_signs_label] = tmp2[labels].apply(lambda x: ','.join(x), axis=1)
#    except Exception as e:
#        print(e)
#        if e =='SettingWithCopyWarning':
#            pass
#    return df2

def x_days(df):
    """Add a column with a descending counter."""
    # One paramter: target dataframe
    df['x-day'] = ['x-' + str(i) for i in range(len(df) - 1, -1, -1)]
    return df

def x_transpose(df):
    """Transpose the dataframe and set the x-days as the column labels."""
    # One paramter: target dataframe, assumes an x-day column has been created
    df = df.set_index('x-day')
    df = df.transpose()
    pd.options.display.float_format = '{:.3f}'.format
    return df

def read_csv(filename, *args, **kwargs):
    """read_csv is a port of the Pandas read_csv module."""
    return pd.read_csv(filename, *args)

def read_sql(table, db, *args, **kwargs):
    """read_sql is a port of the Pandas read_sql module."""
    return pd.read_sql(table, db, *args, **kwargs)

def db_connection(uri):
    """db_connection is a port of the SQLAlchemy create_engine module."""
    return sqlalchemy.create_engine(uri)

# Execute example IO utilities
# To write data to csv
# df.to_csv('data/example.csv')
# print('Modified dataframe saved to: data/standard-example.csv')
# print('\nData saved.')

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
