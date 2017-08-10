def get_traindf():
    import numpy as np
    import pandas as pd
    import pickle
    import random
    orders = pd.read_csv('data/orders.csv', dtype = {
    'order_id': np.uint32,
    'user_id' :np.uint32,
    'eval_set': 'category',
    'order_number': np.uint16,
    'order_dow': np.uint16,
    'order_hour_of_day': np.uint8,
    'days_since_prior_order': np.float32},
                     usecols=['order_id', 'user_id', 'eval_set', 'order_number', 'order_dow', 'order_hour_of_day', 'days_since_prior_order'])
    order_product_train = pd.read_csv('data/order_products__train.csv', dtype = {
    'order_id': np.uint32,
    'product_id': np.uint32,
    'add_to_cart_order': np.uint16,
    'reordered': np.uint16},
    usecols=['order_id', 'product_id', 'add_to_cart_order', 'reordered'])

    user_info = pickle.load(open('data/pickle_files/user_info.p', 'rb'))
    product_info = pickle.load(open('data/pickle_files/product_info.p', 'rb'))
    user_product_info = pickle.load(open('data/pickle_files/user_product_info.p', 'rb'))
    ordertime_info = pickle.load(open('data/pickle_files/ordertime_info.p', 'rb'))
    user_ordertime_info = pickle.load(open('data/pickle_files/user_ordertime_info.p', 'rb'))
    product_ordertime_info = pickle.load(open('data/pickle_files/product_ordertime_info.p', 'rb'))
    aisle_info = pickle.load(open('data/pickle_files/aisle_info.p', 'rb'))
    department_info = pickle.load(open('data/pickle_files/department_info.p', 'rb'))

    train_users = orders[orders.eval_set == 'train'].user_id
    train_df = pd.merge(user_product_info[user_product_info.user_id.isin(train_users)], user_info, on = 'user_id', how = 'left')
    train_df = pd.merge(train_df, product_info, on = 'product_id', how = 'left')
    train_df = pd.merge(train_df, aisle_info, on = 'aisle_id', how = 'left', suffixes=('', '_y'))
    train_df = pd.merge(train_df, department_info, on = 'department_id', how = 'left', suffixes=('', '_y'))
    train_df = pd.merge(train_df, orders[orders.eval_set == 'train'], on='user_id', how = 'left')
    train_df = pd.merge(train_df, order_product_train, on =['order_id', 'product_id'], how = 'left')
    train_df.reordered.fillna(0, inplace = True)
    train_df.rename(columns = {'reordered': 'y'}, inplace = True)
    hour_bins = [-1,2,6,10,14,18,22,25]
    hour_gourp_names = ['22-2-1', '3-6', '7-10', '11-14', '15-18', '19-22', '22-2']
    train_df['order_hour_group'] = pd.cut(train_df.order_hour_of_day, bins = hour_bins, labels=hour_gourp_names)
    train_df = pd.merge(train_df, ordertime_info, on = ['order_dow', 'order_hour_group'], how = 'left')
    train_df = pd.merge(train_df, user_ordertime_info, on = ['user_id', 'order_dow', 'order_hour_group'], how = 'left')
    train_df = pd.merge(train_df, product_ordertime_info, on = ['product_id', 'order_dow', 'order_hour_group'], how = 'left')
    train_df['user_ordertime_order_num'].fillna(0, inplace = True)
    train_df['product_ordertime_order_num'].fillna(0, inplace = True)
    train_df = pd.concat([train_df, pd.get_dummies(train_df['order_hour_group'])], axis = 1)
    train_df = pd.concat([train_df, pd.get_dummies(train_df['order_dow'], prefix='order_dow')], axis = 1)
    train_df['22-2'] = train_df['22-2-1'] + train_df['22-2']
    train_df = train_df.drop('22-2-1', axis = 1)
    print(train_df.columns)
    return train_df
