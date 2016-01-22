#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals
)

import numpy as np
import pandas as pd
import Quandl
import os
from sqlalchemy import sqlalchemy  # from flask.ext.


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

    def load(ticker):
        """Load data from Quandl into a dataframe, modify column names and
        check for non-numeric values."""
        # Grab the Quandl token
        token = os.environ.get('QUANDL_TOKEN')
        if token is None:
            token = input("Enter Quandl token: ")
        # Call Quandl module, trim input by default from 1990 forward
        df = Quandl.get(ticker, authtoken=token, trim_start='1990-01-01')
        # Get the column labels
        old_columns = list(df.columns.values)
        # Use the ticker symbol as our new prefix
        ticker_tag = ticker.split('_')[-1] + '_'
        # Drop spaces and concatenate
        new_labels = [ticker_tag + i.replace(' ', '') for i in old_columns]
        # Create a dictionary of old and new column labels
        new_columns = dict(zip(old_columns, new_labels))
        # Rename the columns using our dictionary
        df = df.rename(columns=new_columns)
        nulls = df[~df.applymap(np.isreal).all(1)]
        # Check for non-numeric values
        if len(nulls) > 0:
            raise ValueError('Dataframe contains non-numeric values')
        row_count = len(df)
        print('%d rows loaded into dataframe.' % row_count)
        return df

    def sma(df, column, period, **kwargs):
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
        if 'label' in kwargs:
            column_label = kwargs['label'] + '_' + str(period) + '-day'
        else:
            column_label = 'SMA_' + column + '_' + str(period) + '-day'
        df[column_label] = pd.stats.moments.rolling_mean(df[column], period)
        return df

    def diff(df, column_a, column_b, **kwargs):
        """Creates a new column from the differnce of column_a and column_b,
        as column_a minus column_b."""
        column_a_suffix = column_a.split('_')[-1]
        column_b_suffix = column_b.split('_')[-1]
        column_prefix = "_".join(column_b.split('_')[0:2])
        if 'label' in kwargs:
            column_label = kwargs['label']
        else:
            column_label = 'Delta_' + column_prefix + '_' + column_a_suffix + '_' + column_b_suffix
        df[column_label] = df[column_a] - df[column_b]
        return df

    def flag_swings(df, column, period, **kwargs):
        """Given a dataframe and column and a minimum sequence period
        for the same sign, the function returns: "1" for upward swings,
        "-1" for downward swings, or "0" if niether condition is met."""
        if 'label' in kwargs:
            # Append custom label with period days
            column_label = kwargs['label'] + '_' + str(period) + '-day'
        else:
            column_label = str(period) + '-day_SwingFlag_' + column
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

        df[column_label] = [flagger(n, p, r, s, period) for n, p, r, s in zip(tmp['sign-0'], tmp['sign-1'], tmp['sum-shift'], tmp['sum'])]
        return df

    def x_days(df):
        """Add a column with a descending counter."""
        df['x-day'] = ['x-' + str(i) for i in range(len(df) - 1, -1, -1)]
        return df

    def x_transpose(df):
        """Transpose the dataframe and set the x-days as the column labels."""
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
