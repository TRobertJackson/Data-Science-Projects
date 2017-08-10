def opt_threshold(result_df, threshold_list=[0.2]):
    import pandas as pd
    import numpy as np
    from new_f1_score.py import new_f1_score
    threshold_opt = 0.2
    max_score = 0
    for threshold in threshold_list:
        scores = []
        bins = [0, threshold, 1]
        group_names = [0, 1]
        result_df['XGB_pred_y'] = pd.cut(result_df['True'], bins, labels=group_names).astype(np.float32)
        for i in range(5):
            scores.append(new_f1_score(result_df[result_df.set == i]))
        score = np.mean(scores)
        if score > max_score:
            max_score = score
            threshold_opt = threshold
    return max_score, threshold_opt
