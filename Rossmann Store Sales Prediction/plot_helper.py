import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

def plot_fb_prophet_forecast(df, startdate, traindate):
    '''
    function to plot facebook prophet sales forecasting results
    '''
    fig, ax = plt.subplots(figsize=(16,5))
    #plot ovserved values
    ax.plot_date(df[df.Date > startdate].Date, df[df.Date > startdate].Sales, fmt='-', label='observed')

    #plot predicted values
    ax.plot_date(df[df.Date > traindate].Date, df[df.Date > traindate].yhat, fmt='-', label='predicted')

    #set x range and y range
    ax.set_xlim([startdate, datetime.datetime.strptime('2015-08-01', "%Y-%m-%d")])
    ax.set_ylim([-500, df[df.Date > startdate].yhat.max()*1.2])

    #set number of yticks
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(6))

    #set position of legend
    plt.legend(loc = 'upper right', bbox_to_anchor=(1.16, 1), fontsize=20)

    #set xticks, yticks, title, xlable and ylabel
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.title('Facebook Prophet Sales Forecasts for Store {}'.format(df.Store[0]), y = 1.08)
    plt.xlabel('Date', fontsize=24)
    plt.ylabel('Sales', fontsize=24)

    fig.tight_layout();

    return

def plot_fb_prophet_breakdown(df, startdate):
    '''
    function to plot the breakdown of the components from facebook prophet sales forecasting.
    '''
    #store number
    store = df.Store[0]

    #get maximum y value
    yhat_max = df[df.ds > startdate].yhat.max()

    #make frames for stacked bar plot
    if 'competitor_open_pre' in df.columns:
        df = df[df.ds > startdate][['ds', 'trend', 'yearly', 'weekly', 'promo', 'school_holiday', 'state_holiday_a', 'state_holiday_b', 'state_holiday_c', 'competitor_open']]
    else:
        df = df[df.ds > startdate][['ds', 'trend', 'yearly', 'weekly', 'promo', 'school_holiday', 'state_holiday_a', 'state_holiday_b', 'state_holiday_c']]
    df['ds'] = df.ds.apply(lambda x: x.strftime("%Y-%m-%d"))
    df.reset_index(inplace=True, drop = True)
    df.set_index('ds', inplace = True)

    #set colors for stacked bar plot
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c','#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    #plot stacked bar plot
    ax = df.plot(kind='bar', stacked=True, figsize=(16,6), width = 0.7, color = colors)

    #set legend positions
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='upper right',  bbox_to_anchor=(1.2, 1), fontsize=18)

    #set xticks
    ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5))
    ax.xaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1))
    for tick in ax.get_xticklabels():
        tick.set_rotation(0)

    #set yticks
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(8))
    ax.set_ylim([-3000, yhat_max*1.1])

    #set xticks, yticks, title, xlable and ylabel
    plt.title('Facebook Prophet Sales Forecasts Breakdown for Store {}'.format(store), y =1.08)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.xlabel('Date', fontsize=24)
    plt.ylabel('Sales', fontsize=24)
    plt.tight_layout()

    return

def plot_xgb_forecast(df, store, startdate, traindate):
    '''
    function to plot xgboost sales forecasting results
    '''
    fig, ax = plt.subplots(figsize=(16,5))
    ax.plot_date(df[(df.Store == store) & (df.Date > startdate)].Date, df[(df.Store == store) &(df.Date > startdate)].Sales, fmt='-', color = '#1f77b4', label = 'observed')
    ax.plot_date(df[(df.Store == store) & (df.Date > traindate)].Date, df[(df.Store == store) &(df.Date > traindate)].new_sales, fmt='-', color = '#2ca02c', label = 'predicted')

    #set x range and y range
    ax.set_xlim([startdate, datetime.datetime.strptime('2015-08-01', "%Y-%m-%d")])
    ax.set_ylim([-500, df[(df.Store == store) & (df.Date > startdate)].new_sales.max()*1.2])

    #set number of yticks
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(6))

    #set position of legend
    plt.legend(loc = 'upper right', bbox_to_anchor=(1.16, 1), fontsize=20)

    #set xticks, yticks, title, xlable and ylabel
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.title('XGBoost Sales Forecasts for Store {}'.format(store), y = 1.08)
    plt.xlabel('Date', fontsize=24)
    plt.ylabel('Sales', fontsize=24)

    fig.tight_layout();

    return

def plot_xgb_forecast_compare_competitor(df, no_competitor_df, store, startdate, traindate):
    '''
    function to plot the forecasts using xgboost with/without competitor info.
    '''
    fig, ax = plt.subplots(figsize=(16,5))
    ax.plot_date(df[(df.Store == store) & (df.Date > startdate)].Date, df[(df.Store == store) &(df.Date > startdate)].Sales, fmt='-', color = '#1f77b4', label = 'observed')
    ax.plot_date(df[(df.Store == store) & (df.Date > traindate)].Date, df[(df.Store == store) &(df.Date > traindate)].new_sales, fmt='-', color = '#2ca02c', label = 'predicted\nwith new\ncompetitor')
    ax.plot_date(no_competitor_df[(no_competitor_df.Store == store) & (no_competitor_df.Date > traindate)].Date, no_competitor_df[(no_competitor_df.Store == store) &(no_competitor_df.Date > traindate)].new_sales, fmt='-', color = '#ff7f0e', label = 'predicted\nwithout new\ncompetitor')

    #set x range and y range
    ax.set_xlim([startdate, datetime.datetime.strptime('2015-08-01', "%Y-%m-%d")])
    ax.set_ylim([-500, df[(df.Store == store) & (df.Date > startdate)].new_sales.max()*1.2])

    #set number of yticks
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(6))

    #set position of legend
    plt.legend(loc = 'upper right', bbox_to_anchor=(1.2, 1), fontsize=20)

    #set xticks, yticks, title, xlable and ylabel
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.title('XGBoost Sales Forecasts for Store {}'.format(store), y = 1.08)
    plt.xlabel('Date', fontsize=24)
    plt.ylabel('Sales', fontsize=24)

    fig.tight_layout();

    return

def plot_xgb_feature_importance(xgb_model, feature_num):
    '''
    function to plot the feature importances of xgboost.
    '''
    #set figure size to adjust for differnt feature number
    fig, ax = plt.subplots(figsize=(1+1.5*feature_num,4))

    #wrap up names for features
    feature_columns = ['Open', 'Promo', 'School Holiday',
           'StateHoliday a', 'StateHoliday b', 'StateHoliday c',
           'Competition\nDistance', 'promo2\nstage 1',
           'promo2\nstage 2', 'promo2\nstage 3', 'year\n2014', 'year\n2015',
           'DayOfWeek 2', 'DayOfWeek 3', 'DayOfWeek 4', 'DayOfWeek 5',
           'DayOfWeek 6', 'DayOfWeek 7', 'StoreType b', 'StoreType c',
           'StoreType d', 'Assortment b', 'Assortment c', 'month 2', 'month 3',
           'month 4', 'month 5', 'month 6', 'month 7', 'month 8', 'month 9',
           'month 10', 'month 11', 'month 12', 'sale\n1 day before',
           'sale\n2 day before', 'sale\n3 day before', 'sale\n4 day before', 'sale\n7 day before']

    #create feature importance dataframe based on xgboost model results
    feature_importance = pd.DataFrame(columns = ['feature', 'importance'])
    for index, importance in enumerate(xgb_model.feature_importances_):
        feature_importance.loc[index] = [feature_columns[index], importance]
    feature_importance.sort_values('importance', inplace = True, ascending = False)
    feature_importance.reset_index(drop = True, inplace = True)

    #plot important features in xgboost model
    matplotlib.rcParams.update({'font.size': 16})
    objects = feature_importance.feature[:feature_num]
    x_pos = np.arange(len(objects))
    performance = feature_importance.importance[:feature_num]

    plt.bar(x_pos, performance, align='center', alpha=0.7)
    plt.xticks(x_pos, objects)
    plt.ylabel('Importance')
    plt.title('Top {} Important Features'.format(feature_num))

    plt.show()

    return
