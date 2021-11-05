# ## Phenotype data wrangling script
#
# Purpose: Wrangles data exported from Cohort Browser.
# Performs:
# - Assigns cases to participants with BREAST cancer type 
# - Assigns control to participants with no recorded cancer type 
# - Creates a matched case-control cohort (1000 cases and 1000 controls)
# - Derives age at recruitment

import pandas as pd
pd.options.mode.chained_assignment = None

female_cohort = pd.read_csv('../../mounted-data/female_cohort.csv')
female_cohort.head()


def create_gwas_bc_cohort(phenotype_df,n_cases_controls_to_match=1000):
    phenotype_df = phenotype_df[~female_cohort['Platekey-0.0'].isna()]
    bc_cases = phenotype_df[(phenotype_df['Cancer_Disease_Type-0.0']=='BREAST') | (phenotype_df['Cancer_Disease_Type-0.1']=='BREAST') | (phenotype_df['Cancer_Disease_Type-0.2']=='BREAST')]
    bc_cases['breast_cancer'] = 1
    controls = phenotype_df[(phenotype_df['Cancer_Disease_Type-0.0'].isna()) & (phenotype_df['Cancer_Disease_Type-0.1'].isna()) & (phenotype_df['Cancer_Disease_Type-0.2'].isna())]
    controls['breast_cancer'] = 0
    cc_cohort = pd.concat([bc_cases.head(n_cases_controls_to_match), controls.head(n_cases_controls_to_match)])
    cc_cohort.columns = cc_cohort.columns.str.split('-').str[0]
    cc_cohort['year_of_consent'] = cc_cohort['Date_Of_Consent'].str.split('-').str[0]
    cc_cohort['year_of_consent'] = cc_cohort['year_of_consent'].astype(int)
    cc_cohort['age'] = cc_cohort['year_of_consent'] - cc_cohort['Year_Of_Birth']
    cc_cohort = cc_cohort.rename(columns={'Platekey':'IID'})
    cc_cohort['FID'] = cc_cohort['IID']
    cc_cohort = cc_cohort[['FID','IID','age','breast_cancer']]
    
    return cc_cohort


df = create_gwas_bc_cohort(female_cohort)

df.head()

df.to_csv('../../gwas_cohort_pheno_covariates.tsv',sep='\t',index=False)
