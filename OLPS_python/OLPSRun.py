#This is the main interface
import numpy as np
import pandas as pd
from pandas.tseries.offsets import *
from datetime import datetime, date
import matplotlib.pyplot as plt
import BenchMarkStrategy as bms
import OLPSResult as olps
from varname import nameof
import copy
from xone import calendar

#create a DatetimeIndex with all trading days from start_date to end_date
def business_dates(start_date:str, end_date:str):
    us_cal = calendar.USTradingCalendar()
    kw = dict(start=start_date, end=end_date)
    return pd.bdate_range(**kw).drop(us_cal.holidays(**kw))

#modify the index column of the given dataframes to be a time series(DatetimeIndex object)
def add_time(df:pd.DataFrame, start_date, end_date):
    num_rows = df.shape[0]
    time_col = business_dates(start_date, end_date)
    df.index = time_col[:num_rows]
#all-in-one function, compare multiple strategies on the same dataset
def compare_strats(strats:list, df:pd.DataFrame, df_name = "", print_option=True, plot_option=True):
    results = []
    for s in strats:
        s_result = s.run(df)
        results.append(copy.copy(s_result))
        if print_option:
            print("{} Strategy on {} dataset{}{}".format(s.name(),df_name, "\n", s_result.__str__()))
    if plot_option:
        labels = [type(s).__name__ for s in strats]
        olps.olps_plot(results, labels=labels, title = df_name)

if __name__ == "__main__":
    # load data
    # df_nyseo = pd.read_excel("Datasets/nyse-o.xlsx")
    # df_nysen = pd.read_excel("Datasets/nyse-n.xlsx")
    # df_tse = pd.read_excel("Datasets/tse.xlsx")
    df_sp500 = pd.read_excel("Datasets/sp500.xlsx")
    # df_msci = pd.read_excel("Datasets/msci.xlsx")
    # df_djia = pd.read_excel("Datasets/djia.xlsx")

    # #add time column as index
    # add_time(df_nyseo, "1962-07-03", "1984-12-31")
    # add_time(df_nysen, "1985-01-01", "2010-06-30")
    # add_time(df_tse, "1994-01-04", "1998-12-31")
    add_time(df_sp500, "1998-01-02", "2003-01-31")
    # add_time(df_msci, "2006-04-01", "2010-03-31")
    # add_time(df_djia, "2001-01-14", "2003-01-14")

    df_name = "SP500"
    strats = [bms.BAH(stock='Bank of America Corporation (107 Bil)'), bms.BS(), bms.UCRP(), bms.BCRP()]
    compare_strats(strats, df_sp500, df_name=df_name, print_option=True,plot_option=True )
