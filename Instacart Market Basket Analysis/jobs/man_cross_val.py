def man_cross_val(train_df, learning_rate=0.2, max_depth=6, n_estimators=100, gamma=0, min_child_weight=1, subsample=1):
    import pandas as pd
    import numpy as np
    from xgboost import XGBClassifier
    from sklearn.model_selection import train_test_split, cross_val_score, learning_curve, KFold, GridSearchCV, GroupKFold
    info_columns = ['user_id', 'product_id', 'product_name', 'aisle_id', 'department_id', 'aisle', 'department', 'order_id', 'eval_set', 'add_to_cart_order', 'y', 'order_hour_group', 'order_dow', 'order_hour_of_day']
    X = train_df.drop(info_columns, axis = 1)
    y = train_df.y
    kf = GroupKFold(n_splits=5)
    final_df = pd.DataFrame()
    for i, (train_index, test_index) in enumerate(kf.split(train_df, groups=train_df['user_id'].values)):
        xgb_model = XGBClassifier(learning_rate=learning_rate, max_depth=max_depth, n_estimators=n_estimators, gamma=gamma, min_child_weight=min_child_weight, subsample=subsample)
        xgb_fit = xgb_model.fit(X.iloc[train_index], y.iloc[train_index])
        result = xgb_fit.predict_proba(X.iloc[test_index])
        new_df = train_df.iloc[test_index][['y', 'user_id', 'product_id']]
        new_df['True'] = result[:, 1:]
        new_df['set'] = i
        final_df = pd.concat([final_df, new_df])
    return final_df
