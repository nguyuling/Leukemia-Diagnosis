import GEOparse
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

# --- 2.1 Importing Dataset ---

# Define the GEO Accession ID
GSE_ID = "GSE13164"
DATA_DIR = "./data" 

def load_and_preprocess_geo(gse_id):
    
    print(f"Downloading and parsing GEO series: {gse_id}. This may take a few minutes...")
    
    # 1. Download and Parse GEO Data
    try: 
        gse = GEOparse.get_GEO(geo=gse_id, destdir=DATA_DIR, silent=True)
    except Exception as e:
        print(f"Error downloading/parsing {gse_id}. Check network connection or GEO ID: {e}")
        return None, None, None
    # Get the platform ID (GPL) used by this series for probe-to-gene mapping
    platform_id = list(gse.gpls.keys())[0]
    
    # 2. Extract Expression Data (Features)
    expression_df = gse.pivot_samples('VALUE')
    # Ensure all values are numeric and handle any non-numeric placeholders
    expression_df = expression_df.apply(pd.to_numeric, errors='coerce').fillna(0)
    print(f"Raw Expression Data Shape (Probes x Samples): {expression_df.shape}")
    
    # 3. Extract Sample Metadata (Labels)
    metadata_list = []
    for name, gsm in gse.gsms.items():
        characteristics = gsm.metadata.get('characteristics_ch1', [])
        # We search for the classification/subtype, typically labeled 'leukemia subtype' or 'diagnosis'.
        sample_type = next((c.split(': ')[1].strip() for c in characteristics if c.startswith('leukemia subtype:')), None)
        if sample_type is None:
             sample_type = next((c.split(': ')[1].strip() for c in characteristics if c.startswith('diagnosis:')), 'Unknown')
        
        metadata_list.append({
            'Sample_ID': name,
            'Raw_Type': sample_type
        })
    metadata_df = pd.DataFrame(metadata_list)
    return expression_df, metadata_df, gse.gpls[platform_id].table

# --- 2.2 Data Wrangling ---

def clean_and_encode_labels(metadata_df, expression_df):
    
    print("\n--- 2.2 Data Wrangling: Label Cleaning and Encoding ---")
    
    # 1. Standardize and Map Sample Types based on the four target subtypes:
    def standardize_type(raw_type):
        if raw_type is None:
            return 'UNKNOWN'
        
        raw_type = raw_type.lower().strip()
        
        # Acute Lymphoblastic Leukemia (ALL)
        if 'all' in raw_type or 't-all' in raw_type or 'b-all' in raw_type:
            return 'ALL'
        # Acute Myeloid Leukemia (AML)
        elif 'aml' in raw_type:
            return 'AML'
        # Chronic Lymphocytic Leukemia (CLL)
        elif 'cll' in raw_type:
            return 'CLL'
        # Chronic Myeloid Leukemia (CML)
        elif 'cml' in raw_type:
            return 'CML'
        
        # Filter out anything else (e.g., Normal/Control, MDS, specific unclassified subtypes)
        return 'UNKNOWN'

    metadata_df['Leukemia_Type'] = metadata_df['Raw_Type'].apply(standardize_type)
    
    # 2. Filter out unwanted classes (UNKNOWN)
    target_classes = ['ALL', 'AML', 'CLL', 'CML']
    filtered_metadata = metadata_df[metadata_df['Leukemia_Type'].isin(target_classes)].copy()
    
    # 3. Create a unified list of samples present in both metadata and expression data
    shared_samples = list(set(filtered_metadata['Sample_ID']) & set(expression_df.columns))
    # Filter both dataframes to only include the shared, target samples
    filtered_metadata = filtered_metadata[filtered_metadata['Sample_ID'].isin(shared_samples)].set_index('Sample_ID')
    target_expression = expression_df[shared_samples]
    # Transpose the expression data so Samples are rows and Probes are columns
    target_expression = target_expression.T
    
    # 4. Numerical Encoding of Labels
    le = LabelEncoder()
    # Fit the encoder to the expected target classes to maintain consistent mapping
    le.fit(target_classes)
    filtered_metadata['Target_Code'] = le.transform(filtered_metadata['Leukemia_Type'])
    # Create the final Master DataFrame
    master_df = target_expression.merge(filtered_metadata['Target_Code'], 
                                        left_index=True, 
                                        right_index=True)
    
    class_map = dict(zip(le.classes_, le.transform(le.classes_)))
    
    print(f"Filtered Sample Count: {master_df.shape[0]}")
    print(f"Final Class Distribution:\n{filtered_metadata['Leukemia_Type'].value_counts()}")
    print(f"Class Mapping: {class_map}")
    
    return master_df, class_map

def map_probes_to_genes(master_df, platform_df):
    
    print("\n--- 2.2 Data Wrangling: Probe-to-Gene Mapping ---")
    
    # 1. Extract mapping information from the platform file
    probe_map = platform_df[['ID', 'Gene Symbol']].copy()
    probe_map = probe_map.dropna(subset=['Gene Symbol'])
    
    # 2. Handle multiple gene symbols per probe (use the first one) and clean symbols
    probe_map['Gene Symbol'] = probe_map['Gene Symbol'].apply(lambda x: str(x).split(' /// ')[0].strip())
    
    # 3. Filter expression data to only include probes we can map
    expression_columns = master_df.columns[:-1] # All columns except the last (Target_Code)
    
    # Create a temporary expression DataFrame using the index/columns from the master_df
    temp_expression = master_df.iloc[:, :-1].T # Transpose back to (Probes x Samples)
    temp_expression = temp_expression.merge(probe_map, 
                                            left_index=True, 
                                            right_on='ID', 
                                            how='inner')
    
    # Set the new index to Gene Symbol and drop the old probe ID
    temp_expression = temp_expression.set_index('Gene Symbol').drop(columns=['ID'])
    
    # 4. Handle multiple probes mapping to the same Gene Symbol by averaging their expression
    gene_expression_df = temp_expression.groupby(level=0).mean().T # Transpose back to (Samples x Genes)

    # 5. Re-attach the Target_Code column
    final_df = gene_expression_df.merge(master_df['Target_Code'], 
                                        left_index=True, 
                                        right_index=True)

    print(f"Gene-level Expression Data Shape (Samples x Genes): {final_df.shape}")
    print(f"Number of Genes after mapping: {final_df.shape[1] - 1}")
    
    return final_df


# --- EXECUTION ---

# 1. Load and extract data
raw_expression, raw_metadata, platform_data = load_and_preprocess_geo(GSE_ID)

if raw_expression is not None and platform_data is not None:
    # 2. Clean labels and filter samples
    master_df_probes, class_map = clean_and_encode_labels(raw_metadata, raw_expression)

    # 3. Map probes to genes and aggregate
    final_leukemia_df = map_probes_to_genes(master_df_probes, platform_data)
    
    # Display final results
    print("\n--- Final Cleaned DataFrame (Samples x Genes + Target) ---")
    print(final_leukemia_df.head())
    print("\nNext step: Exploratory Data Analysis (EDA) and Feature Selection (Task 3 & 4).")
else:
    print("\nData loading failed. Please check the GEO ID and network connection.")