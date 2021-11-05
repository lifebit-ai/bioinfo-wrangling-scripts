library(data.table)
library(dplyr)
library(tidyverse)


female_cohort = fread('mounted-data/female_cohort.csv')
head(female_cohort)

create_gwas_bc_cohort <- function(phenotype_df,n_cases_controls_to_match=1000) {
    phenotype_df <- phenotype_df %>% filter(Platekey-0.0 != NA)
    bc_cases <- phenotype_df %>%
                filter(Cancer_Disease_Type-0.0 == 'BREAST' | Cancer_Disease_Type-0.1 == 'BREAST' | Cancer_Disease_Type-0.2 == 'BREAST') %>% 
                mutate(breast_cancer = 1)
    
    controls <- phenotype_df %>%
                filter(Cancer_Disease_Type-0.0 == NA | Cancer_Disease_Type-0.1 == NA | Cancer_Disease_Type-0.2 == NA) %>% 
                mutate(breast_cancer = 0)

    cc_cohort = pd.concat([bc_cases.head(n_cases_controls_to_match), controls.head(n_cases_controls_to_match)])
    cc_cohort.columns = cc_cohort.columns.str.split('-').str[0]
    cc_cohort['year_of_consent'] = cc_cohort['Date_Of_Consent'].str.split('-').str[0]
    cc_cohort['year_of_consent'] = cc_cohort['year_of_consent'].astype(int)
    cc_cohort['age'] = cc_cohort['year_of_consent'] - cc_cohort['Year_Of_Birth']
    cc_cohort = cc_cohort.rename(columns={'Participant_Phenotypic_Sex':'sex','Platekey':'IID'})
    cc_cohort['FID'] = cc_cohort['IID']
    cc_cohort = cc_cohort[['FID','IID','sex','age','breast_cancer']]
    
    return cc_cohort
}
  
  
df = create_gwas_bc_cohort(female_cohort)

df.to_csv('gwas_cohort_pheno_covariates.tsv',sep='\t',index=False)
