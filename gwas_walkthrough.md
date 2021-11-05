# GWAS walkthrough

This document outlines steps for creating a case-control breast cancer cohort in Cohort Browser, wrangling phenotypic data in a jupyter session and triggering a GWAS job supplying created files as parameter inputs.

## 1. Initiating a Jupyter session
You can start a new jupyter session by clicking on the bottom **Jupyter Notebooks** tab on left-side bar. This will direct you to a page with existing jupyter notebooks in that workspace. You can start a new jupyter session by clicking on the green "New Analysis" button in the top right.

You can rename the name of the session (New Session by default) by clicking on pencil icon and supplying desired name. Each jupyter notebook belongs to a project - you can either initiate a session in an existing project (available via dropdown) or create a new project by clicking "New" button under "Select a project" section.

Next, you can select the instance and amount of storage required for your jupyter session. Here, we will use c5.xlarge instance with default 500GB storage.

You can set up additional time and cost limits for the session, if preferred. 

You are now ready to start the session! Please click blue "Create" button in the top right corner of the page.

It will take 2-4 mins for the spin up the selected instance and initiate a jupyter session.

## 2. Creating a cohort in Cohort Browser

You can navigate to Cohort Browser by clicking on the second bottom **Cohort Browser v2** tab on left-side bar. This will direct you to a page with existing cohorts present in the workspace. You can create a new jupyter session by clicking on the green "New Cohort" button in the top right. Please give it a name and an optional description and click "Save".

An example we use here is a case-control breast cancer cohort. First, let's select female participants to retain in the cohort of interest. Click on the green plus "Add filters" icon which will display a search bar for querying phenotypes available in the data for filtering. Search "phenotypic sex" in the search bar and select the first result. Click on the blue "Add as filter" button to add this field as a filter.

You will see a pop-up confirming that the filter has been added. Under "Phenotypes" section, you can select female participants by clicking on "F" horizontal bar. Once it has been highlighted, please click on blue "Apply" button on right hand side under "Cohort Query". The filter has been successfully applied if you can see the total number of selected participants at the top of the page changing to reflect the number of participants in selected subset.

You can now select desired columns for phenotype and covariate information. Under "Participants Data" section, select "Manage Columns". Please click on the icon with a tick and a number 6, and deselect the default columns. You can add preferred columns by querying fields in the search bar. The columns of interest for this example are:

- Platekey (search 'platekey' and select the third result)
- Year of birth (search 'year of birth' and select the second result)
- Date of consent (search 'date of consent' and select the first result)
- Cancer disease type (search 'cancer disease type' and select the first result)

You can now close "Participants table columns" window. You will now see the selected fields present under "Participants Data" section.

Please click on "Export participants data" button on the right. Select "Download or Export to dataset" in the dropdown, create a name for exported dataset and select "All data" under "Data Selection". Under "Action", select "Export to dataset or folder" and choose location for the exported files. You can create a new dataset location under Data & Results by clicking on the green "+" icon. Once you've navigated to the desired output location, click on "Export to current folder".

A pop-up notification will notify you that the files have been successfully exported.

## 3. Wrangling phenotypic data exported from Cohort Browser

You can use a wrangling script in this repo (`gwas/create_gwas_cohort.py`) to generate a file containing phenotype and covariates in a format suitable for GWAS pipeline.
The script:
    - Assigns cases to participants with BREAST cancer type
    - Assigns control to participants with no recorded cancer type
    - Derives age at recruitment
    - Generates a file containing phenotype of interest and covariates

Click "Save" in the top right of page with running jupyter session to save the output file.

## 4. Supplying parameter inputs and triggering a GWAS pipeline job

You now have everything you need to submit a GWAS job! You can navigate to Jobs by clicking on the **Jobs** tab on left-side bar. This will direct you to a page with existing jobs present in the workspace. You can create a new job by clicking on the green "New" button with the rocket icon in the top right. You will be redirected to "Run New Analysis" page - click "New" button to import the gwas pipeline anew. Next, click on the green Nextflow logo and input the URL of a GWAS pipeline (https://github.com/lifebit-ai/gwas), provide a name and click "Next". The following page will allow you to supply parameter inputs. Necessary parameters are:

`--trait_type`: binary
`--pheno_data`: This should point to the pheno + covariates file generated in the first step. It will be saved under "Project Results" -> project_name -> jupyter_session_name and can be linked using the blue database button.
`--input_folder_location`: s3 link to vcf files - this will be provided in the workshop.
`--number_of_files_to_process`: 3
`--file_pattern`: pattern of filenames of VCFs and their indices
`--phenotype_colname`: breast_cancer

In the dropdown on the right, please select "gwas" - this will use "gwas" git tag of the pipeline to run the analysis.

Select "Next" - you will be prompted to select an instance and set up cost limit, if preferred. You also have the option to make the job "Resumable" which caches the output of successfully executed processes of a pipeline.

Click "Run Job" to start your analysis!

It will take 2-4 mins for the spin up the selected instance and initialize the job.
















