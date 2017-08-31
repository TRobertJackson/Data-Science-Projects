import numpy as np
learning_rate_list = np.arange(0.18,0.24,0.02)
max_depth_list = [9, 10, 11]
n_estimators_list = np.arange(100, 160,20)
gamma_list = [0, 0.05]
min_child_weight_list = [2, 4]
subsample_list = [1]
num = 1
for lr in learning_rate_list:
        for md in max_depth_list:
            for n in n_estimators_list:
                for g in gamma_list:
                    for w in min_child_weight_list:
                        for s in subsample_list:
                            fname = '{0}.py'.format(num)
                            with open(fname, 'w') as f:
                                f.write('from xgb_para_opt import xgb_para_opt\n')
                                f.write('lr = {0}\n'.format(lr))
                                f.write('md = {0}\n'.format(md))
                                f.write('n = {0}\n'.format(n))
                                f.write('g = {0}\n'.format(g))
                                f.write('w = {0}\n'.format(w))
                                f.write('s = {0}\n'.format(s))
                                f.write('\n')
                                f.write("with open('{0}_output.txt', 'w') as f:\n".format(num))
                                f.write("    f.write('{0} {1} {2} {3} {4} {5} {6}'.format(lr, md, n, g, w, s, xgb_para_opt(lr, md, n, g, w, s)))\n")
                                f.write("f.close()")
                            f.close()

                            sname = 'script{0}'.format(num)
                            with open(sname, 'w') as f:
                                f.write("#!/bin/bash\n")
                                f.write("#$ -M hma@nd.edu	 # Email address for job notification\n")
                                f.write("#$ -m abe		 # Send mail when job begins, ends and aborts\n")
                                f.write("#$ -q *@@crc_d12chas		 # Specify queue\n")
                                f.write("#$ -pe smp 1\n")
                                f.write("python {0}.py".format(num))
                            f.close()

                            num += 1
