"""
    Name: NGU YU LING
    MATRIC NO. A23CS0149
"""

#! Q1: DNA Complement + Base Count
def dna_summary(seq):
    # Clean the input: remove spaces and convert to uppercase
    cleaned_seq = seq.replace(" ", "").upper()
    
    # Count A, T, C, G
    count_A = cleaned_seq.count('A')
    count_T = cleaned_seq.count('T')
    count_C = cleaned_seq.count('C')
    count_G = cleaned_seq.count('G')
    
    # Create complement mapping
    complement_map = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    
    # Produce complement sequence
    complement_seq = ''.join(complement_map.get(base, '') for base in cleaned_seq)
    
    # Print counts
    print(f"Counts: A={count_A}, T={count_T}, G={count_G}, C={count_C}")
    
    # Return complement sequence
    return complement_seq

#! Q2: K-mer Frequency Analysis
def kmer_count(seq, k):
    # Clean the input: remove spaces and convert to uppercase
    cleaned_seq = seq.replace(" ", "").upper()
    
    # Check if k is valid
    if k <= 0 or k > len(cleaned_seq):
        print(f"Error: k must be between 1 and {len(cleaned_seq)}")
        return None, 0
    
    # Extract all k-mers using sliding window
    kmers = []
    for i in range(len(cleaned_seq) - k + 1):
        kmer = cleaned_seq[i:i+k]
        kmers.append(kmer)
    
    # Count frequency of each k-mer using dictionary
    kmer_dict = {}
    for kmer in kmers:
        kmer_dict[kmer] = kmer_dict.get(kmer, 0) + 1
    
    # Find the most frequent k-mer
    if not kmer_dict:
        print(f"No k-mers found for k={k}")
        return None, 0
    
    most_frequent_kmer = max(kmer_dict, key=lambda x: kmer_dict[x])
    max_count = kmer_dict[most_frequent_kmer]
    
    # Print results
    print(f"K-mers extracted (k={k}): {', '.join(kmers)}")
    print(f"K-mer frequencies: {kmer_dict}")
    print(f"Most frequent k-mer: {most_frequent_kmer} ({max_count})")
    
    return most_frequent_kmer, max_count


#! Function calling
if __name__ == "__main__":
    # Test Q1
    print("\n--- Q1: DNA COMPLEMENT + BASE COUNT ---")
    
    print("\nTest 1:")
    test_seq_1 = "a t g c C a"
    print(f"Input: '{test_seq_1}'")
    complement_1 = dna_summary(test_seq_1)
    print(f"Complement: {complement_1}")
    
    print("\nTest 2:")
    test_seq_2 = "ACGTACGT"
    print(f"Input: '{test_seq_2}'")
    complement_2 = dna_summary(test_seq_2)
    print(f"Complement: {complement_2}")
    
    print("\nTest 3:")
    test_seq_3 = "A T T A C G C G"
    print(f"Input: '{test_seq_3}'")
    complement_3 = dna_summary(test_seq_3)
    print(f"Complement: {complement_3}")
    
    # Test Q2
    print("\n--- Q2: K-MER FREQUENCY ANALYSIS ---")
    
    print("\nTest 1:")
    test_seq_q2_1 = "ATATAT"
    k_1 = 2
    print(f"Input: seq='{test_seq_q2_1}', k={k_1}")
    most_freq_1, count_1 = kmer_count(test_seq_q2_1, k_1)
    
    print("\nTest 2:")
    test_seq_q2_2 = "A A C G T A C G T"
    k_2 = 3
    print(f"Input: seq='{test_seq_q2_2}', k={k_2}")
    most_freq_2, count_2 = kmer_count(test_seq_q2_2, k_2)
    
    print("\nTest 3:")
    test_seq_q2_3 = "AAAA"
    k_3 = 2
    print(f"Input: seq='{test_seq_q2_3}', k={k_3}")
    most_freq_3, count_3 = kmer_count(test_seq_q2_3, k_3)