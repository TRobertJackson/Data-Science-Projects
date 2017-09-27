# loading packages
import numpy as np
import pandas as pd
import datetime

def prepare_data():
    print("Started preparing data...")
    sale_df = load_sale_df()
    store_df = load_store_df()
    sale_df = prepare_sale_df(sale_df)
    sale_record_count_df = create_record_count_df(sale_df)
    master_df = prepare_master_df(sale_df, store_df, sale_record_count_df)
    print("Finished preparinig data.")

    return master_df

def load_sale_df():
    sale_df = pd.read_csv("data/train.csv",
                    low_memory = False,
                    dtype={'Store': np.int64,
                           'DayOfWeek': 'category',
                           'Sales':np.int64,
                           'Customers':np.int64,
                           'Open':np.int8,
                           'Promo':np.int8,
                           'StateHoliday':'category',
                           'SchoolHoliday':np.int8},
                   index_col='Date')
    print("  Sale data loaded.")
    return sale_df

def load_store_df():
    store_df = pd.read_csv("data/store.csv",
                   dtype={'Store':np.int64,
                          'StoreType':'category',
                          'Assortment':'category',
                          'Promo2':np.int8,
                         })
    print("  Store data loaded.")
    return store_df

def prepare_sale_df(sale_df):
    print("  Started preparing sale dataframe...")
    sale_df.sort_index(inplace = True)
    print("    Dataframe sorted by date.")

    sale_df.reset_index(inplace=True)
    print("    Indices reset for dataframe.")

    sale_df['Date'] = pd.to_datetime(sale_df['Date'])
    print("    Converted type of 'Date' from int to datetime.")

    print("    Made dummy variables for 'StateHoliday'.")
    sale_df = pd.get_dummies(sale_df, columns=['StateHoliday'], drop_first = True)

    print("    Creating columns of 'year', 'month', and 'week'...")
    sale_df['year'] = sale_df['Date'].apply(lambda x: x.year)
    sale_df['month'] = sale_df['Date'].apply(lambda x: x.month)
    sale_df['week'] = sale_df['Date'].apply(lambda x: x.month)
    print("    Created columns of 'year', 'month', and 'week'.")

    print("  Finished preparing sale dataframe.")
    return sale_df

def create_record_count_df(sale_df):
    sale_record_number_df = pd.DataFrame(sale_df.groupby('Store')['Sales'].count())
    sale_record_number_df.rename(columns = {'Sales': 'sale_record_number'}, inplace = True)
    sale_record_number_df.reset_index(inplace = True)
    print("  Created sale record count df.")

    return sale_record_number_df

def prepare_master_df(sale_df, store_df, sale_record_count_df):
    print("  Started preparing master dataframe...")
    master_df = pd.merge(sale_df, sale_record_count_df, on='Store', how='left')
    master_df = master_df[master_df.sale_record_number == 942]
    del master_df['sale_record_number']
    master_df.reset_index(inplace = True, drop=True)
    print("    Removed stores with missing records.")

    master_df = pd.merge(master_df, store_df, on='Store', how='left')
    print("    Merged sale_df with store_df.")

    master_df['promo2_open'] = 365 * (master_df.year - master_df.Promo2SinceYear) + 7 * (master_df.week - master_df.Promo2SinceWeek)
    master_df['promo2_open'] = master_df.promo2_open.apply(lambda x: 1 if x >= 0 else 0)
    print("    Added a column of promo2_open.")

    master_df['PromoInterval'] = master_df.PromoInterval.map({'Jan,Apr,Jul,Oct': 1, 'Feb,May,Aug,Nov': 2, 'Mar,Jun,Sept,Dec':3})
    master_df['promo2_stage'] = (master_df.month - master_df.PromoInterval)%3 + 1
    print("    Added a column of promo2_stage.")

    master_df['competitor_open'] = 12 * (master_df.year - master_df.CompetitionOpenSinceYear) + (master_df.month - master_df.CompetitionOpenSinceMonth)
    master_df['competitor_open'] = master_df.competitor_open.apply(lambda x: 0 if x < 0 else 1)
    print("    Added a column of competitor_open.")

    master_df.CompetitionDistance.fillna(758600, inplace=True)
    print("    Filled nan values for competition distance with 10 times of the max value.")

    master_df.promo2_stage.fillna(0, inplace = True)
    master_df = pd.get_dummies(master_df, columns=['promo2_stage'], drop_first=True)
    master_df.rename(columns = {'promo2_stage_1.0': 'promo2_stage_1', 'promo2_stage_2.0': 'promo2_stage_2', 'promo2_stage_3.0': 'promo2_stage_3'}, inplace=True)
    print("    Converted promo2_stage to dummy variables.")

    master_df.drop(['CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear', 'Promo2', 'Promo2SinceWeek', 'Promo2SinceYear', 'PromoInterval', 'promo2_open', 'week'], axis=1, inplace=True)
    print("    Dropped columns of 'CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear', 'Promo2', 'Promo2SinceWeek', 'Promo2SinceYear', 'PromoInterval', 'promo2_open', and 'week'.")

    master_df = pd.get_dummies(master_df, columns=['month', 'year', 'DayOfWeek', 'StoreType', 'Assortment'], drop_first=True)
    print("    Converted month, year, dayofweek, storetype and assortment to dummy variables.")

    master_df = master_df.sort_values(['Date', 'Store']).reset_index(drop = True)
    print("  Finished preparing master dataframe.")

    return master_df
