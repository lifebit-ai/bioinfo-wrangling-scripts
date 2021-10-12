import pandas as pd
import numpy as np

# +
samples = pd.read_csv('phewas_samples.txt',sep='\t',names=['id'])

codes = ['A01.0','A06.1','A15']
code_counts = pd.concat([samples]*2, ignore_index=True)
np.random.seed(123)
code_counts['code'] = np.random.choice(codes, size=len(code_counts))
code_counts['count'] = 1
code_counts.to_csv('icd_code_counts.csv',sep=',',index=False)
# -

#id,code,count
#1,A01.0,3
#1,A0.6.1,3
#1,A15,3,3

cb_export_df = pd.read_csv('mounted-data/test_phewas_cohort.csv')

cb_export_df.head()

cb_export_melt=pd.melt(cb_export_df,id_vars=['Platekey-0.0'],var_name='metrics', value_name='values')


cb_export_melt = cb_export_melt[]

cb_export_melt = cb_export_melt[~cb_export_melt['values'].isna()]

len(cb_export_melt)

cb_export_melt[cb_export_melt['metrics']!='i']

temp = cb_export_melt[(cb_export_melt['metrics'].str.contains('Diag')) & (cb_export_melt['values'].str.contains('A16'))]

len(temp)

temp = temp[~temp['Platekey-0.0'].isna()]

len(temp)

temp.head()

temp['values']=temp['values'].str[:-1] + '.' + temp['values'].str[-1]

temp.head()

temp.groupby(["Platekey-0.0"]).count().sort_values(["values"], ascending=False)

temp['count'] = temp.groupby(['Platekey-0.0'])['values'].transform('count')

temp.head()

temp = temp.rename(columns={''})
