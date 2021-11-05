# ## Phenotype data wrangling script
#
# Purpose: Wrangles data exported from Cohort Browser.
# Performs:
# - Assigns cases to participants with BREAST cancer type 
# - Assigns control to participants with no recorded cancer type 
# - Creates a matched case-control cohort (1000 cases and 1000 controls)
# - Derives age at recruitment

suppressMessages(library(tidyverse))

input_file = "../../mounted-data/female_cohort.csv"
female_cohort = readr::read_csv(input_file, na = c('', 'NA'))

# Remove rows without platekeys
t2 = female_cohort %>% dplyr::filter(!is.na(`Platekey-0.0`)) %>% unite( contains('Cancer_Disease_Type'), col = 'CANCERS', sep = ',')
t3 <- separate(data = t2, col = `Date_Of_Consent-0.0`, into = c("year_of_consent", "month_of_consent","day_of_consent"), sep = "-")
t3$year_of_consent <- as.numeric(t3$year_of_consent)
t3$`Year_Of_Birth-0.0` <- as.numeric(t3$`Year_Of_Birth-0.0`)
t4 = t3 %>% mutate( breast_cancer = ifelse(grepl("BREAST", CANCERS), 1, 0), age=as.numeric(year_of_consent)-as.numeric(`Year_Of_Birth-0.0`))
t5 = t4 %>% select(FID='Platekey-0.0', IID='Platekey-0.0', age, breast_cancer)

write_tsv(file="../../gwas_cohort_pheno_covariates.tsv", x=t5)
