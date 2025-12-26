from Bio import Entrez 
import pandas as pd
import re

# Define your search term 
search_term = "cystic fibrosis"
 
# Perform the search 
handle = Entrez.esearch(db="gene", term=search_term, retmax=3)
record = Entrez.read(handle) 
handle.close() 
print("\n") 
 
# Get the list of Gene IDs from the search results 
gene_ids = record["IdList"] 
 
# Retrieve gene information for all search results 
gene_information = [] 
for gene_id in gene_ids: 
    handle = Entrez.efetch(db="gene", id=gene_id, 
rettype="gb", retmode="text") 
    gene_info = handle.read() 
    handle.close() 
    gene_information.append(gene_info) 
 
# Extract gene symbol, other aliases, and ID
table_data = []
for gene_info in gene_information:
    # Extract gene symbol
    symbol_match = re.search(r'^\d+\.\s+(\S+)', gene_info, re.MULTILINE)
    symbol = symbol_match.group(1) if symbol_match else "N/A"
    
    # Extract other aliases
    aliases_match = re.search(r'Other Aliases:\s*(.+?)(?:\n|$)', gene_info)
    aliases = aliases_match.group(1).strip() if aliases_match else "N/A"
    
    # Extract ID
    id_match = re.search(r'ID:\s*(\d+)', gene_info)
    gene_id = id_match.group(1) if id_match else "N/A"
    
    table_data.append([symbol, aliases, gene_id])

# Create and display pandas DataFrame
df = pd.DataFrame(table_data, columns=["Gene Symbol", "Other Aliases", "ID"])
print(f"Gene search results for: {search_term}\n")
print(df.to_string(index=False))