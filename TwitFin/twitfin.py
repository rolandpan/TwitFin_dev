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
        """Load data from Quandl into a dataframe, modify
        column names and check for non-numeric values."""
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

    def read_csv(filename, *args, **kwargs):
        return pd.read_csv(filename, *args)

    def read_sql(table, db, *args, **kwargs):
         return pd.read_sql(table, db, *args, **kwargs)

    def db_connection(uri):
        return sqlalchemy.create_engine(uri)
