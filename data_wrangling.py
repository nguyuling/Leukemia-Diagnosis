import GEOparse
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import re 
import os 
from functools import reduce

# --- Configuration ---
# The target GEO Series ID for the MILE Study Stage 2
GSE_ID = "GSE13164" 
OUTPUT_CLEAN_DATA = "GSE13164_cleaned_features.csv"
OUTPUT_CLEAN_LABELS = "GSE13164_cleaned_labels.csv"

# The four target classes for the multi-class classification problem
TARGET_CLASSES = ['ALL', 'AML', 'CLL', 'CML']
FEATURE_IDENTIFIER = 'GB_ACC' # Using GenBank Accession as the reliable feature identifier

# --- 1. GEO Download, Parse, and Extraction ---

def load_and_preprocess_geo(gse_id):
    """
    Downloads, parses, and extracts expression and metadata by merging
    individual GSM sample files, which is robust against platform table formatting errors.
    
    Args:
        gse_id (str): The GEO Series (GSE) accession ID.
        
    Returns:
        tuple: (expression_df, metadata_df) - two Pandas DataFrames.
    """
    print(f"Downloading and parsing GEO series: {gse_id}. This may take a few minutes...")
    try:
        # Downloads the file if not already present, and parses it
        gse = GEOparse.get_GEO(geo=gse_id, destdir="./", silent=False)
    except Exception as e:
        print(f"Error downloading/parsing {gse_id}: {e}")
        return None, None

    platform_key = list(gse.gpls.keys())[0]
    gpl_table = gse.gpls[platform_key].table.copy()
    
    # --- 2. Data Wrangling: Label Extraction and Filtering (Pre-merge) ---
    print("\nStarting Label Extraction and Filtering...")
    
    metadata_list = []
    sample_dfs = []

    for name, gsm in gse.gsms.items():
        characteristics = ' '.join(gsm.metadata.get('characteristics_ch1', ['']))
        leukemia_type = None
        
        # Identify the leukemia type based on target classes
        for t_type in TARGET_CLASSES:
            if re.search(r'\b' + re.escape(t_type) + r'\b', characteristics, re.IGNORECASE):
                leukemia_type = t_type
                break

        # 2a. Only process samples belonging to our target classes
        if leukemia_type in TARGET_CLASSES:
            # Add sample info to metadata list
            metadata_list.append({'Sample_ID': name, 'Leukemia_Type': leukemia_type})
            
            # 2b. Extract expression data from the GSM's table
            gsm_df = gsm.table.copy()
            
            # Use 'ID_REF' as the joining key (Probe ID)
            if 'ID_REF' not in gsm_df.columns:
                print(f"Warning: GSM {name} missing 'ID_REF'. Skipping.")
                continue
            
            # Identify the expression value column. Typically the last non-ID column.
            # Using common names for signal/value
            value_col = next((col for col in gsm_df.columns if col.upper() in ['VALUE', 'LOG_RATIO', 'SIGNAL', 'AVG_SIGNAL', 'NORMALIZED_SIGNAL']), None)
            
            # Fallback: Assume the expression column is the last column after ID_REF
            if not value_col:
                non_id_cols = [c for c in gsm_df.columns if c != 'ID_REF']
                if non_id_cols:
                    value_col = non_id_cols[-1]
                else:
                    print(f"Warning: GSM {name} has no detectable value column. Skipping.")
                    continue

            # Select ID_REF and the value, then rename the value column to the sample name
            gsm_df = gsm_df[['ID_REF', value_col]].rename(columns={value_col: name})
            sample_dfs.append(gsm_df)

    metadata_df = pd.DataFrame(metadata_list)
    print(f"Samples identified and labeled: {len(sample_dfs)}.")
    
    if not sample_dfs:
        print("CRITICAL ERROR: No samples with identifiable labels or expression values were found.")
        return None, None

    # --- 3. Merging Sample DataFrames ---
    print("\nMerging individual sample expression tables...")
    
    # Merge all sample DataFrames based on 'ID_REF' (the probe ID)
    expression_data = reduce(lambda left, right: pd.merge(left, right, on='ID_REF', how='inner'), sample_dfs)
    expression_data = expression_data.set_index('ID_REF')
    
    print(f"Initial Merged Feature Matrix Shape (Probes x Samples): {expression_data.shape}")

    # --- 4. Probe Mapping and Aggregation ---
    print("\nStarting Probe Mapping and Aggregation using GPL table...")
    
    # 4a. Get the necessary columns from the GPL (Platform) annotation table
    annotation_cols = ['ID', FEATURE_IDENTIFIER]
    annotation_df = gpl_table[annotation_cols].rename(columns={'ID': 'ID_REF', FEATURE_IDENTIFIER: 'Feature_ID'})

    # Clean Feature IDs (GB_ACC)
    annotation_df.dropna(subset=['Feature_ID'], inplace=True)
    annotation_df = annotation_df[annotation_df['Feature_ID'].str.strip() != '---']
    annotation_df['Feature_ID'] = annotation_df['Feature_ID'].apply(lambda x: x.split(' // ')[0].strip())
    
    # Merge annotation with expression data
    merged_df = pd.merge(expression_data.reset_index(), annotation_df, on='ID_REF', how='inner')

    # Remove probes that didn't map to a valid Feature_ID
    merged_df.dropna(subset=['Feature_ID'], inplace=True)
    
    # Get the list of sample columns (all columns except ID_REF and Feature_ID)
    sample_cols = [col for col in merged_df.columns if col.startswith('GSM')]

    # 4b. Aggregate: Group by Feature ID (GB_ACC) and take the mean expression (O2)
    final_features_df = merged_df.groupby('Feature_ID')[sample_cols].mean()
    
    # Transpose the final data (Samples as Rows, Features/Accessions as Columns)
    final_features_df = final_features_df.T
    
    # --- 5. Final Data Alignment and Encoding ---

    # Ensure the metadata index aligns with the sample IDs found in the feature matrix
    metadata_df = metadata_df.set_index('Sample_ID').loc[final_features_df.index.tolist()].reset_index()

    # Encode the target labels (O2)
    le = LabelEncoder()
    metadata_df['Target_Code'] = le.fit_transform(metadata_df['Leukemia_Type'])

    # Final check
    print("\n--- Final Data Alignment ---")
    print(f"Final Feature Matrix Shape (Samples x Features): {final_features_df.shape}")
    print(f"Final Label Matrix Shape (Samples x Info): {metadata_df.shape}")
    print(f"Sample-wise alignment check (should be TRUE): {all(final_features_df.index == metadata_df['Sample_ID'])}")

    return final_features_df, metadata_df

# --- EXECUTION ---

# Create the data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

print("--- Starting O1: Data Collection & Wrangling (Python) ---")
# 1. Load, clean, and map the data
expression_data, metadata = load_and_preprocess_geo(GSE_ID)

if expression_data is not None and metadata is not None:
    # 2. Save the final products for the next step (EDA/Feature Selection)
    try:
        expression_data.to_csv(OUTPUT_CLEAN_DATA)
        metadata.to_csv(OUTPUT_CLEAN_LABELS, index=False)
        print(f"\nSUCCESS: Cleaned features saved to: {OUTPUT_CLEAN_DATA}")
        print(f"SUCCESS: Cleaned labels saved to: {OUTPUT_CLEAN_LABELS}")
    except Exception as e:
        print(f"Error saving data: {e}")

    print("\nData Wrangling (O1) is now complete. You can proceed to EDA and Feature Selection (O2/O3) in 'leukemia_eda_feature_selection.py'.")