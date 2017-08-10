from get_traindf import get_traindf
from opt_threshold import opt_threshold
from man_cross_val import man_cross_val
import numpy as np
def xgb_para_opt(learning_rate=0.2, max_depth=6, n_estimators=100, gamma=0, min_child_weight=1, subsample=1, threshold=np.arange(0.1,0.3,0.001)):
    return opt_threshold(man_cross_val(get_traindf(), learning_rate=learning_rate, max_depth=max_depth, n_estimators=n_estimators, gamma=gamma, min_child_weight=min_child_weight, subsample=subsample), threshold_list=threshold_list)
