# The Computational Quest for Precision in Leukemia Diagnosis

## 🎯 Mission: Precision in Blood Cancer Diagnosis

The term "__leukemia__" covers a spectrum of devastating blood cancers, but not all leukemias are the same. Misclassification leads to missed treatment windows and poor patient outcomes.

This project, developed for the __Programming for Bioinformatics__ course, tackles this critical challenge head-on. Using machine learning and public genomic data (gene expression profiles from the GSE13164 dataset) to build a robust, data-driven classifier.

The Goal: To accurately distinguish and predict the __four major leukemia subtypes__ based on their molecular signatures.
| Leukemia Sub-type | Abbreviation |
| :---: | :---: |
| Acute Lymphoblastic Leukemia | ALL |
| Acute Myeloid Leukemia | AML |
| Chronic Lymphocytic Leukemia | CLL |
| Chronic Myeloid Leukemia | CML |—.


## 🛠️ The Pipeline: From Raw Data to Diagnostic Model

This repository contains the complete pipeline for multi-class classification:

1. __Data Wrangling__ : Cleaning and preprocessing raw microarray data.
> data_wrangling.py
> output file: GSE13164_cleaned_features.csv & GSE13164_cleaned_labels.csv

2. __Exploratory Data Analysis__ : Identifying key genes showing differential expression across subtypes.

3. __Feature Selection__ : Reducing the feature space to a high-impact biomarker panel.

4. __Model Developmen__t & Evaluation : Training and optimizing classifiers (e.g., Random Forest, Logistic Regression) using rigorous cross-validation to achieve high prediction accuracy.

## 🎓 Course Context
__Group 12__ : SECB3203_25261 Programming for Bioinformatics 

| Name | Matric Number | Email |
|:---:|:---:|:---:|
| NGU YU LING | A23CS0149 | nguyuling@gmail.com |