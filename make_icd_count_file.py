import pandas as pd
import numpy as np
samples = pd.read_csv('all_samples.txt',sep='\t',names=['id'])

codes = ['A01.0','A06.1','A15']
code_counts = pd.concat([samples]*2, ignore_index=True)
#np.random.seed(123)
code_counts['code'] = np.random.choice(codes, size=len(code_counts))
code_counts['count'] = 3
code_counts.to_csv('random_code_counts.csv',sep=',',index=False)
