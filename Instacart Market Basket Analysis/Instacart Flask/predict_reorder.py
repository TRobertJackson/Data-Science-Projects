import numpy as np
import pandas as pd
import pickle
from xgboost import XGBClassifier
from sklearn.externals import joblib

def predict_reorder(user_id, product_id):
    orders = pd.read_csv('data/orders.csv', dtype = {
    'order_id': np.uint32,
    'user_id' :np.uint32,
    'eval_set': 'category',
    'order_number': np.uint16,
    'order_dow': np.uint16,
    'order_hour_of_day': np.uint8,
    'days_since_prior_order': np.float32},
                     usecols=['order_id', 'user_id', 'eval_set', 'order_number', 'order_dow', 'order_hour_of_day', 'days_since_prior_order'])

    user_info = pickle.load(open('data/user_info.p', 'rb'))
    product_info = pickle.load(open('data/product_info.p', 'rb'))
    user_product_info = pickle.load(open('data/user_product_info.p', 'rb'))
    aisle_info = pickle.load(open('data/aisle_info.p', 'rb'))
    department_info = pickle.load(open('data/department_info.p', 'rb'))
    pred_model = joblib.load('Predict_funtion.p')

    user_id = int(user_id)
    product_id = int(product_id)

    df = pd.merge(user_product_info[(user_product_info.user_id == user_id) & (user_product_info.product_id == product_id)], user_info, on = 'user_id', how = 'left')
    if df.empty:
        return ("User {0} hasn't bought product {1} before, we're not sure if he/she will buy it.".format(user_id, product_id))
    df = pd.merge(df, product_info, on = 'product_id', how = 'left')
    df = pd.merge(df, aisle_info, on = 'aisle_id', how = 'left', suffixes=('', '_y'))
    df.drop('department_id_y', axis = 1, inplace=True)
    df = pd.merge(df, department_info, on = 'department_id', how = 'left', suffixes=('', '_y'))
    df = pd.merge(df, orders, on='user_id', how = 'left')
    cols = ['user_product_last_purchase_day', 'user_product_reorder_ratio', 'user_history', 'days_since_prior_order', 'product_reorder_user_ratio', 'product_reorder_ratio', 'user_product_order_num', 'user_product_order_interval_mean', 'product_order_interval_mean', 'user_product_order_interval_std', 'product_user_num', 'product_reorder_num', 'product_add_to_cart_order_mean', 'product_reorder_user_num', 'user_order_interval_mean', 'user_product_add_order_mean', 'user_order_num', 'user_product_rank', 'product_order_interval_std', 'product_order_num', 'aisle_user_reorder_ratio', 'user_basket_size_std', 'user_order_interval_std', 'aisle_prod_reorder_num_std', 'aisle_reorder_ratio', 'aisle_prod_order_interval_mean_mean', 'aisle_prod_order_interval_mean_std', 'department_prod_order_num_sum', 'user_product_add_order_std', 'eval_set', 'user_id', 'product_id']
    X = df[cols].iloc[-1:,:]
    X = X.drop(['eval_set', 'user_id', 'product_id'], axis = 1)
    y = pred_model.predict_proba(X)
    if (y[:,1:] > 0.197):
        return("Yes, user {0} will buy product {1} in his/her next order.".format(user_id, product_id))
    else:
        return("No, user {0} won't buy product {1} in his/her next order.".format(user_id, product_id))
