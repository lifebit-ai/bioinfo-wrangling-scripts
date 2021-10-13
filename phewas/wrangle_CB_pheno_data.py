# ## PheWAS: wrangling of phenotypic data from Cohort Browser

# ### Import libraries

import pandas as pd
import numpy as np


# ### Load in Cohort Browser exported .csv file

cb_export_df = pd.read_csv('mounted-data/test_phewas_cohort.csv')
#cb_export_df.head()

# ### Function to wrangle exported Cohort Browser data to get ICD-10 counts per individual

def create_icd_counts_df(cb_export_df):
    cb_export_melt=pd.melt(cb_export_df,id_vars=['Platekey-0.0'],var_name='metrics', value_name='values')
    cb_export_melt = cb_export_melt[~cb_export_melt['values'].isna()]
    temp = cb_export_melt[cb_export_melt['metrics'].str.contains('Diag')]
    temp = temp[~temp['Platekey-0.0'].isna()]
    temp['values']=temp['values'].str[:-1] + '.' + temp['values'].str[-1]
    temp['count'] = temp.groupby(['Platekey-0.0'])['values'].transform('count')
    temp['count'] = 3
    temp = temp.rename(columns={'Platekey-0.0':'id','values':'code'})
    temp = temp[~temp['id'].isna()]
    return temp[['id','code','count']]


icd_code_counts_df = create_icd_counts_df(cb_export_df)

# ### Write out .csv file containing ICD10 counts

icd_code_counts_df.to_csv('phewas_icd_code_counts.csv',index=False)

# ### Write out a list of samples to use in pheWAS

icd_code_counts_df[['id']].to_csv('phewas_samples.txt',index=False, header=None)
