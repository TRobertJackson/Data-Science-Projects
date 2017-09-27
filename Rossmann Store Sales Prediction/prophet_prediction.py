# loading packages
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import warnings

from fbprophet import Prophet


def make_holidays(df):
    '''
    function to make holiday dataframe for facebook prophet model.
    '''
    closed = pd.DataFrame({
      'holiday': 'closed',
      'ds': pd.to_datetime(df[df.Open == 0].ds),
      'lower_window': 0, # these help us specify spillover into previous and future days
      'upper_window': 1,
    })

    promos = pd.DataFrame({
      'holiday': 'promo',
      'ds': pd.to_datetime(df[df.Promo == 1].ds),
      'lower_window': 0, # these help us specify spillover into previous and future days
      'upper_window': 1,
    })

    school_holidays = pd.DataFrame({
      'holiday': 'school_holiday',
      'ds': pd.to_datetime(df[df.SchoolHoliday == 1].ds),
      'lower_window': 0,
      'upper_window': 1,
    })

    state_holiday_a = pd.DataFrame({
      'holiday': 'state_holiday_a',
      'ds': pd.to_datetime(df[df.StateHoliday_a == 1].ds),
      'lower_window': 0,
      'upper_window': 1,
    })

    state_holiday_b = pd.DataFrame({
      'holiday': 'state_holiday_b',
      'ds': pd.to_datetime(df[df.StateHoliday_b == 1].ds),
      'lower_window': 0,
      'upper_window': 1,
    })

    state_holiday_c = pd.DataFrame({
      'holiday': 'state_holiday_c',
      'ds': pd.to_datetime(df[df.StateHoliday_c == 1].ds),
      'lower_window': 0,
      'upper_window': 1,
    })

    if df.competitor_open.nunique() == 2:
        competitor_open = pd.DataFrame({
          'holiday': 'competitor_open',
          'ds': pd.to_datetime(df[df.competitor_open == 1].ds),
          'lower_window': 0,
          'upper_window': 1,
        })
    else:
        competitor_open = pd.DataFrame()

    promo2_stage_1 = pd.DataFrame({
      'holiday': 'promo2_stage_1',
      'ds': pd.to_datetime(df[df.promo2_stage_1 == 1].ds),
      'lower_window': 0,
      'upper_window': 1,
    })

    promo2_stage_2 = pd.DataFrame({
      'holiday': 'promo2_stage_2',
      'ds': pd.to_datetime(df[df.promo2_stage_2 == 1].ds),
      'lower_window': 0,
      'upper_window': 1,
    })

    promo2_stage_3 = pd.DataFrame({
      'holiday': 'promo2_stage_3',
      'ds': pd.to_datetime(df[df.promo2_stage_3 == 1].ds),
      'lower_window': 0,
      'upper_window': 1,
    })

    holidays = pd.concat((closed, promos, school_holidays, state_holiday_a, state_holiday_b, state_holiday_c, competitor_open, promo2_stage_1, promo2_stage_2, promo2_stage_3))

    return holidays

def prophet_predict_store(master_df, store, traindate):
    '''
    function to build facebook prophet model for a specif store
    '''
    #meke store dataframe
    store_df = master_df[master_df.Store == store]

    #change the column name of predicted values to be 'y', the column name of date to be 'ds', as required by facebook prophet model
    store_df.rename(columns = {'Sales': 'y', 'Date': 'ds'}, inplace = True)
    store_df.reset_index(inplace=True, drop=True)

    #make holiday dataframe for facebook prophet model
    holidays = make_holidays(store_df)

    #train facebook prophet model
    prophet_model = Prophet(holidays=holidays, daily_seasonality=False)
    prophet_model.fit(store_df[store_df.ds <= traindate])

    #forecast sales using facebook prophet model
    forecast = prophet_model.predict(store_df)
    forecast['y'] = store_df['y']
    forecast['Store'] = store_df['Store']
    forecast['Date'] = store_df['ds']

    predict_columns = list(set(forecast).difference(set(master_df.columns).union(set(['ds', 'y']))))
    #when the store is closed, set all the components of forecasts to be 0.
    forecast.loc[forecast.y == 0, predict_columns] = 0

    return forecast, prophet_model

def prophet_predict_all(master_df, traindate):
    '''
    function to build one facebook prophet model for each store.
    '''
    store_list = master_df.Store.unique()
    store_list.sort()
    predict_df = pd.DataFrame()

    print("Started Prophet predictions...")
    print("  predicted for store", end=": ")
    for store in store_list:
        print("{}".format(store), end=", ")
        forecast, prophet_model = prophet_predict_store(master_df, store, traindate)
        predict_df = pd.concat([predict_df, forecast], axis=0)
        predict_df.reset_index(drop = True, inplace = True)
    print("\nFinished Prophet predictions.")

    return predict_df
