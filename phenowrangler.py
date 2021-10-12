import pandas as pd
from datetime import date

df = pd.read_csv('mounted-data/tmp-5078qRqTJ608UR5.csv')
df['FID'] = df['i']
df['IID'] = df['i']

col_list = df.columns.to_list()
clean_col_list = [x.split('-')[0] for x in col_list]

df.columns = clean_col_list

df['Participant_phenotypic_sex'] = df['Participant_phenotypic_sex'].map({'M':1,'F':0})

df = df[~df['PC1_in_aggregate_VCF'].isna()]

def calculate_age(born):
  today = date.today()
  return today.year - born

df['age'] = df['Year_of_birth'].apply(calculate_age)
df = df.rename(columns={'Participant_phenotypic_sex':'sex'})
df.columns = [x.replace('_in_aggregate_VCF','') for x in df.columns]
column_headers = ['FID','IID','sex','age','PC1','PC2', 'PC3','PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9', 'PC10']
df = df.reindex(columns=column_headers)

df.to_csv('test_sex_as_pheno.phe',sep='\t',index=False)


