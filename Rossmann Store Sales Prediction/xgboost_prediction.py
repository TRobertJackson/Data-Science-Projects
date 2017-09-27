import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import warnings
from copy import deepcopy

from xgboost.sklearn import XGBRegressor

from performance_evaluation import *

def xgb_df_preparation(master_df, traindate):
    '''
    function to prepare dataframe for xgboost.
    '''

    print("Started xgb_df preparation...")

    xgb_df = deepcopy(master_df.sort_values(['Date', 'Store']).reset_index(drop = True))
    print("  changing competitor distance to a large number when the the competitor is not open...")
    xgb_df['CompetitionDistance'] = xgb_df.apply(lambda row: row['CompetitionDistance'] if row['competitor_open'] == 1 else 758600, axis=1)


    print("  adding features of the sales of previous days...")
    xgb_df['new_sales'] = xgb_df.apply(lambda row: row.Sales if ((row.year_2015 == 0 ) or (row.month_7 == 0)) else np.nan,axis=1)
    xgb_df['sale_1_day_before'] = xgb_df.groupby(['Store'])['new_sales'].shift(1)
    xgb_df['sale_2_day_before'] = xgb_df.groupby(['Store'])['new_sales'].shift(2)
    xgb_df['sale_3_day_before'] = xgb_df.groupby(['Store'])['new_sales'].shift(3)
    xgb_df['sale_4_day_before'] = xgb_df.groupby(['Store'])['new_sales'].shift(4)
    xgb_df['sale_7_day_before'] = xgb_df.groupby(['Store'])['new_sales'].shift(7)

    print("  droped first 7 rows because they lack the sales of previous days.")
    dropdate = datetime.datetime.strptime('2013-01-07', "%Y-%m-%d")
    xgb_df = xgb_df[xgb_df.Date > dropdate]

    print("Finished xgb_df preparation.")

    return xgb_df

def xgb_predict(xgb_df, traindate, n_estimators=50, max_depth=20, learning_rate=0.2, subsample=0.9):
    '''
    function to train xgboost model and forecast for future sales.
    '''

    print("Started Xgboost predictions...")

    feature_columns = ['Open', 'Promo', 'SchoolHoliday',
       'StateHoliday_a', 'StateHoliday_b', 'StateHoliday_c',
       'CompetitionDistance', 'promo2_stage_1',
       'promo2_stage_2', 'promo2_stage_3', 'year_2014', 'year_2015',
       'DayOfWeek_2', 'DayOfWeek_3', 'DayOfWeek_4', 'DayOfWeek_5',
       'DayOfWeek_6', 'DayOfWeek_7', 'StoreType_b', 'StoreType_c',
       'StoreType_d', 'Assortment_b', 'Assortment_c', 'month_2', 'month_3',
       'month_4', 'month_5', 'month_6', 'month_7', 'month_8', 'month_9',
       'month_10', 'month_11', 'month_12', 'sale_1_day_before',
       'sale_2_day_before', 'sale_3_day_before', 'sale_4_day_before', 'sale_7_day_before']

    X = xgb_df[xgb_df.Date <= traindate][feature_columns]
    y = xgb_df[xgb_df.Date <= traindate]['Sales']

    print("  training model on sales before traindate...")
    xgb_model = XGBRegressor(n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate, subsample=subsample, random_state=91817)
    xgb_model.fit(X, y)
    print("  finished training model.")

    print("  predicting for new dates...\n    ")

    xgb_forecast_df = deepcopy(xgb_df)
    date = traindate

    #forecast sales for every date in July, 2015
    for day in range(31):
        date += datetime.timedelta(days=1)
        print('day', day+1, end=", ")
        indices = xgb_forecast_df[xgb_forecast_df.Date == date].index

        #use forecasted sales on previous days as features for new date
        for i, df_index in enumerate(indices):
            xgb_forecast_df.set_value(df_index, 'sale_1_day_before', xgb_forecast_df.loc[df_index-934*1].new_sales)
            xgb_forecast_df.set_value(df_index, 'sale_2_day_before', xgb_forecast_df.loc[df_index-934*2].new_sales)
            xgb_forecast_df.set_value(df_index, 'sale_3_day_before', xgb_forecast_df.loc[df_index-934*3].new_sales)
            xgb_forecast_df.set_value(df_index, 'sale_4_day_before', xgb_forecast_df.loc[df_index-934*4].new_sales)
            xgb_forecast_df.set_value(df_index, 'sale_7_day_before', xgb_forecast_df.loc[df_index-934*7].new_sales)

        predicted_values = xgb_model.predict(xgb_forecast_df.loc[indices][feature_columns])

        #predict sales on new date
        for i, df_index in enumerate(indices):
            xgb_forecast_df.set_value(df_index, 'new_sales', predicted_values[i])

    print("\nFinished Xgboost predictions.")

    return xgb_forecast_df, xgb_model

def xgb_predict_no_competitor(xgb_df, xgb_model, traindate):
    '''
    function to forecast sales without competitor info using trained xgboost.
    '''

    print("Started Xgboost predictions without competitor info...")

    no_competitor_df = deepcopy(xgb_df)
    print("  chaning all competition distances to a large number by assuming all the competitor stores are very far away")
    #assume all the competitor stores are very far away
    no_competitor_df['CompetitionDistance'] = 758600

    feature_columns = ['Open', 'Promo', 'SchoolHoliday',
       'StateHoliday_a', 'StateHoliday_b', 'StateHoliday_c',
       'CompetitionDistance', 'promo2_stage_1',
       'promo2_stage_2', 'promo2_stage_3', 'year_2014', 'year_2015',
       'DayOfWeek_2', 'DayOfWeek_3', 'DayOfWeek_4', 'DayOfWeek_5',
       'DayOfWeek_6', 'DayOfWeek_7', 'StoreType_b', 'StoreType_c',
       'StoreType_d', 'Assortment_b', 'Assortment_c', 'month_2', 'month_3',
       'month_4', 'month_5', 'month_6', 'month_7', 'month_8', 'month_9',
       'month_10', 'month_11', 'month_12', 'sale_1_day_before',
       'sale_2_day_before', 'sale_3_day_before', 'sale_4_day_before', 'sale_7_day_before']

    print("  predicting for new dates...\n")
    date = traindate

    #forecast sales for every date in July, 2015 without competitor info
    for day in range(31):
        date += datetime.timedelta(days=1)
        print('day', day+1, end=", ")
        indices = no_competitor_df[no_competitor_df.Date == date].index
        #use forecasted sales on previous days as features for new date
        for i, df_index in enumerate(indices):
            no_competitor_df.set_value(df_index, 'sale_1_day_before', no_competitor_df.loc[df_index-934*1].new_sales)
            no_competitor_df.set_value(df_index, 'sale_2_day_before', no_competitor_df.loc[df_index-934*2].new_sales)
            no_competitor_df.set_value(df_index, 'sale_3_day_before', no_competitor_df.loc[df_index-934*3].new_sales)
            no_competitor_df.set_value(df_index, 'sale_4_day_before', no_competitor_df.loc[df_index-934*4].new_sales)
            no_competitor_df.set_value(df_index, 'sale_7_day_before', no_competitor_df.loc[df_index-934*7].new_sales)

        predicted_values = xgb_model.predict(no_competitor_df.loc[indices][feature_columns])

        #predict sales on new date
        for i, df_index in enumerate(indices):
            no_competitor_df.set_value(df_index, 'new_sales', predicted_values[i])

    print("\nFinished xgboost predictions without competitor info.")

    return no_competitor_df
