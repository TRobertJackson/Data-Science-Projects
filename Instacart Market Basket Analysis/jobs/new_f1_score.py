def new_f1_score(df):
    import pandas as pd
    import numpy as np
    TNdf = pd.DataFrame(df[(df.y == 0) & (df.XGB_pred_y == 0)].groupby('user_id')['product_id'].nunique())
    TNdf.rename(columns = {'product_id': 'TN'}, inplace = True)
    TNdf.reset_index(inplace = True)

    TPdf = pd.DataFrame(df[(df.y == 1) & (df.XGB_pred_y == 1)].groupby('user_id')['product_id'].nunique())
    TPdf.rename(columns = {'product_id': 'TP'}, inplace = True)
    TPdf.reset_index(inplace = True)
    
    FNdf = pd.DataFrame(df[(df.y == 1) & (df.XGB_pred_y == 0)].groupby('user_id')['product_id'].nunique())
    FNdf.rename(columns = {'product_id': 'FN'}, inplace = True)
    FNdf.reset_index(inplace = True)

    FPdf = pd.DataFrame(df[(df.y == 0) & (df.XGB_pred_y == 1)].groupby('user_id')['product_id'].nunique())
    FPdf.rename(columns = {'product_id': 'FP'}, inplace = True)
    FPdf.reset_index(inplace = True)

    matrix_df = pd.merge(TNdf, TPdf, on = 'user_id', how = 'outer')
    matrix_df = pd.merge(matrix_df, FNdf, on = 'user_id', how = 'outer')
    matrix_df = pd.merge(matrix_df, FPdf, on = 'user_id', how = 'outer')

    matrix_df.fillna(0, inplace = True)
    matrix_df['precision'] = matrix_df.TP / (matrix_df.FP + matrix_df.TP)
    matrix_df['recall'] = matrix_df.TP / (matrix_df.FN + matrix_df.TP)
    matrix_df['f1'] = 2*matrix_df.TP / (2*matrix_df.TP+matrix_df.FP+matrix_df.FN)
    matrix_df.fillna(1, inplace = True)
    return matrix_df.f1.mean()
