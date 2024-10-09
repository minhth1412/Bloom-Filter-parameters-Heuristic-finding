import random
import math
import time
import hashlib
from typing import Tuple
import pandas as pd

def prob_fp(k, q, N):
    """
    This function calculate and return: (1 - (1 - 1/q)^kN)^k
    
    , which is the probability of False-positive
    """
    return (1 - ((1 - 1/q)**(k*N)))**k
   
def generate_random_key(vec_key):
    """This function generate a random name with characters in alphabet, and the key size is random from 1 to 3 
    Returns:
        key: string type, a random key
    """
    while True:
        # Continue the random key generation until the key is not in the loop. In fact, this will run 
        key_length = random.randint(1, 7)       # Choose 7 because most of the keys is 8-digits numbers.
        key = ''.join(random.choices('0123456789', k=key_length))
        
        if key not in vec_key:
            break
    
    return key

def h(s, i, q):
    """
    This function is used to hash the input string S into hash function h_k.
    The input parameters are:
    - s: the input string to be hashed.
    - i: the index of hash function.
    - q: the size of Bloom Filter array.
    
    This function return the i_th hash value.
    """
    # Init for imported dataset, hash function is defined by myself.
    if i % 3 == 0:
        modified_string = s + str(i)
    elif i % 3 == 1:
        modified_string = str(i) + s
    else:
        modified_string = s[:len(s)//2] + str(i) + s[len(s)//2:]
                
    # Encode the modified string to bytes
    byte_string = modified_string.encode()
                
    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256()
                
    # Update the hash object with the byte string
    sha256_hash.update(byte_string)
                
    # Get the hexadecimal digest of the hash
    hex_digest = sha256_hash.hexdigest()
                
    res = int(hex_digest, 16) % q
                
    return res
        
def set_to_bloom(k, q, d):
    """
    This function is used to set the Bloom Filter array with the input string S.
    The input parameters are:
    - k: the number of hash functions.
    - q: the size of Bloom Filter array.
    - d: the set represent for dv that need to be inserted into Bloom Filter set
    """
    
    bloom = [0]*q
    # S = "".join(d)      
    # Set the Bloom Filter array with k hash values of S
    for S in d:
        for i in range(k):
            ind = h(S, i + 1, q)
            # print(f"Hash value for {S} with k = {i+1}: {ind}")
            bloom[ind] = 1
    
    return bloom

def check(bloom, key, k, q):
    """This function is to check that key is in the BF set or not"""
    for i in range(k):
        ind = h(key, i + 1, q)
        # print(f"Hash value for {S} with k = {i+1}: {ind}")
        if bloom[ind] == 0:
            return False
        
    return True

def update_optimal_q_k(
    fp: float, measured_time: float, q: int, k: int, 
    fp_result: float, time_result: float, q_res: int, k_res: int
) -> Tuple[float, float, int, int]:
    # Update optimal q, optimal k base on fp and time measured
    if fp_result == 1.0 and time_result == 0.0 and q_res == k_res and q_res == 0:
        return fp, measured_time, q, k
    elif fp_result > fp:
        return fp, measured_time, q, k
    elif fp_result == fp and time_result > measured_time:
        return fp, measured_time, q, k
    return fp_result, time_result, q_res, k_res
    
# # min_total_fp, min_running_time, ret_q, ret_k = update_optimal_q_k(total_false_positive, loop_time, q_star, k_star, min_total_fp, min_running_time, ret_q, ret_k)

#     if min_total_fp > total_false_positive:
#         min_running_time = loop_time
#         min_total_fp = total_false_positive
#         ret_q = q_star
#         ret_k = k_star
#     elif min_total_fp == total_false_positive:
#         if min_running_time > loop_time:
#             min_running_time = loop_time
#             ret_q = q_star
#             ret_k = k_star
# # general_fp_rate, general_avg_detected_time, general_optimal_q, general_optimal_k = update_optimal_q_k(mx_fp_rate, avg_detected_time, avg_optimal_q, avg_optimal_k, general_fp_rate, general_avg_detected_time, general_optimal_q, general_optimal_k)
#     if general_fp_rate > mx_fp_rate:
#         general_fp_rate = mx_fp_rate
#         general_optimal_q = avg_optimal_q
#         general_optimal_k = avg_optimal_k
#         general_avg_detected_time = avg_detected_time
#     elif general_fp_rate == mx_fp_rate:
#         if general_avg_detected_time > avg_detected_time:
#             general_optimal_q = avg_optimal_q
#             general_optimal_k = avg_optimal_k
#             general_avg_detected_time = avg_detected_time
    

def find_q_k_with_db(q, k, Dv):
    """
    This function calculates the optimized (q, k) for Bloom Filter, based on result from theory and the database for checking.
    Input includes:
    - q: The amount of bits represent for Bloom Filter array.
    - k: The amount of hash functions in Bloom Filter (h_1, h_2,...,h_k)
    - Dv: The dictionary that each value set has share the same key as value in database, 
         where each element in that set value is unique key
    
    The function returns the fixed optimal q and k that fit the current database.
    """
    # Initialize the parameters
    delta = 5   # This will be use for checking q', k' around q, k.
    min_total_fp = 1    # Save the minimum fp_rate calculated from each loop with each (q, k)
    ret_q = q   # the optimal_q for return
    ret_k = k   # the optimal_k for return
    
    # To avoid q_star have negative value, use these variables to make adjustment in below loop
    min_range_q = ret_q - delta
    
    # Because the range start from 1 for q, we pass 
    if min_range_q < 0:
        min_range_q = delta - q
    elif min_range_q == 0:
        min_range_q = min_range_q + 1
    else:
        min_range_q = 0
    # Detect q_star range, or detect [q_left, q_right)
    q_left = q - delta + min_range_q    # inclusive
    q_right = q + delta + min_range_q + 1   # exclusive
        
    # Detect k_star range, or detect [k_left, k_right)
    k_left = 2
    k_right = 13
    # If k < 6, the k_left will have negative numbers that will cause error.
    # So, we need to adjust the range of k_star.
    # If k = 6, or k - delta = 1, the bloom filter is just like a normal hash function.
    # The value k = 2 is the default value. So we just check if k > 7 or not to have the right adjustments.
    if (k > 7):
        k_left = k - delta          # k_left is inclusive
        k_right = k + delta + 1     # k_right is exclusive
    
    # Create variable for compare time running of each loop with (q_star, k_star), whenever both fp_rate results measured of 2 loops are the same.
    min_running_time = 0.0

    # Heuristic loop for each pair (q_star, k_star)
    for k_star in range(k_left, k_right):
        for q_star in range(q_left, q_right):
            
            loop_start = time.time()
            total_false_positive = 0.000
            for i in Dv:
                count = 0
                # Create bloom with (q_star, k_star)
                bloom = set_to_bloom(k_star, q_star, Dv[i])
                for _ in range(1000):
                    # We need a random key that is not in dataset, and check how many times the bloom filter return True for each random key
                    # In current loop, the key must not in Dv[i].
                    random_key = generate_random_key(list(Dv[i]))
                    
                    
                    # Compare the matching of random_key existence in both bloom of Dv and current Dv
                    # In details, to check false positive case, we check if random_key is not in current vec_key (which is checked when create random_key).
                    # And on the other hand, we need to check if the bloom return True for that random_key. It is counted as 1 false positive result.
                    if check(bloom, random_key, k_star, q_star) == True:
                        count += 1
                        
                # Update the total false-positive results that we have found
                false_positive = count/1000
                total_false_positive += false_positive
            loop_end = time.time()
            loop_time = loop_end - loop_start
            
            # Update optimal q and k
            min_total_fp, min_running_time, ret_q, ret_k = update_optimal_q_k(total_false_positive, loop_time, q_star, k_star, min_total_fp, min_running_time, ret_q, ret_k)
            
    # print(f"minimum total fp: {min_total_fp}")
    return min_total_fp, ret_q, ret_k
                    
def create_Dv(db):
    D = {0:[]}
    for i in db:
        if db[i] in D:
            D[db[i]] = D[db[i]] + [i]
        else:
            D[db[i]] = [i]
        D[0] = D[0] + [i]
    # for i in D:
    #     print(f"Records with value {i}: {D[i]}")
    return D

def read_db(num_rows):
    """
    This function is used to read the database.
    The database is a dictionary with unique keys and following values:
    """
    # Currently in this function, we use a static database for testing.
    # Later, we can replace this function with a function to read the database from a file.
    # db = {'a': 10, 'b': 10, 'c': 20, 'd': 15, 'e': 10, 'f': 15, 'g': 20}
    
    # --------------------- Data imported-----------------
    # Define the range of rows to import (100 to 300, inclusive)
    # The range can be modified for other tests
    # Random start_row from 1 to 100000
    start_row = random.randint(1, 150000 - num_rows)
    # start_row = 1
    # # calculate end_row
    # end_row = start_row + num_rows - 1


    # Calculate the number of rows to import

    # Read the specified range of rows from the CSV file, and put it in dataframe
    df = pd.read_csv('Crimes_-_2001_to_Present.csv', skiprows=range(1, start_row), nrows=num_rows)

    # Specify the columns you want to use as the dictionary's keys and values
    key_column = 'ID'
    value_column = 'District'

    # Convert the specified columns into a dictionary
    db = df.set_index(key_column)[value_column].to_dict()
    
    # Convert the set key from int into string
    db = {str(k): v for k, v in db.items()}
    
    # Create keys set for testing purpose
    key_set = set(df[key_column].astype(str))
    
    return key_set, db

if __name__ == "__main__":
    # Variable for measuring the time run total source
    timeStart = time.time()
    
    # Create variable for saving running results
    data = {
            'N records': [], # This is total records read from database, which is a blocks of continous rows that are choosed randomly
            'Baseline q': [], # Which is equal N * k (k is chosen from 1 to 10), which is the base for calculating the optimal q
            'fp_rate': [],
            'optimal_q': [],    # Optimal size of Bloom's array that found out
            'optimal_k': [],    # Optimal amount of hash functions that found out
            'detected time(s)': []
    }
    data1 = {
            'N records': [], # This is total records read from database, which is a blocks of continous rows that are choosed randomly
            'max_fp_rate': [],  # This will receive the max value of fp_rate in the results with same N records.
            'avg_optimal_q': [],    # Optimal size of Bloom's array that is average results of 100 times running with same N records
            'avg_optimal_k': [],    # Optimal amount of hash functions that is average results of 100 times running with same N records
            'avg_detected time(s)': []
    }
    
    ln2 = math.log(2)
    # Loop for testing with different amount of data (1000 rows, 2000 rows,..., 10000 rows)
    for j in range(1, 11, 1):
        # item_counts is the amount of data that extracted from database
        item_counts = j * 1000
        
        # Create variable that calculate final average result for the best case
        general_fp_rate = 1.0       # We need smaller fp_rate when compare 2 mx_fp_rate of 2 cases with same N records
        general_optimal_q = 0
        general_optimal_k = 0
        general_avg_detected_time = 0.0
        
        # N = 25      # Since the range of district in real dataset has maximum equals 25
        # desired_fp = 0.01 
        # min_prob_fp, optimal_q, optimal_k = find_q_k_with_theory(item_counts, desired_fp)
        for x in range(1, 16, 1):     # Modify the D_2 upperbound: N * x ~ item_counts * x, as know as baseline q
            q_base = item_counts * x
            k_base = int(math.ceil(x * ln2))
            vec_key, db = read_db(item_counts)
            print(f"q and k found with theory: (q, k) = ({q_base}, {k_base})")
            
            mx_fp_rate = 0.0       # We need the bigger fp_rate when comes to compare 2 min_fp
            avg_optimal_q = 0.0
            avg_optimal_k = 0.0
            avg_detected_time = 0.0
                
            # Create Dv set 
            Dv = create_Dv(db)
            for qq in range(10):
                
                # Variable initialization
                avg_min_fp = 0
                avg_q = 0
                avg_k = 0
                avg_cost = 0
                    
                # Start the timer
                start_time = time.time()
                print(f"Loop number {j * x * (qq + 1)}....", end="")
                min_fp, optimal_q, optimal_k = find_q_k_with_db(q_base, k_base, Dv)
                # Stop the timer
                end_time = time.time()
                print("finished")
                # Calculate the elapsed time
                elapsed_time = end_time - start_time
                
                data['N records'].append(item_counts)
                data['Baseline q'].append(item_counts * x)
                data['fp_rate'].append(min_fp)
                data['optimal_q'].append(optimal_q)
                data['optimal_k'].append(optimal_k)
                data['detected time(s)'].append(elapsed_time)
                
                if mx_fp_rate < min_fp:
                    mx_fp_rate = min_fp
                avg_optimal_q += optimal_q
                avg_optimal_k += optimal_k
                avg_detected_time += elapsed_time
            
            avg_optimal_q /= 10.0
            avg_optimal_k /= 10.0
            avg_detected_time /= 10.0
            
            # Calculate the best (q,k) with fp_rate and time_measured of case N records
            general_fp_rate, general_avg_detected_time, general_optimal_q, general_optimal_k = update_optimal_q_k(
                mx_fp_rate, avg_detected_time, avg_optimal_q, avg_optimal_k, general_fp_rate, general_avg_detected_time, general_optimal_q, general_optimal_k)
            
        
        data1['N records'].append(item_counts)
        data1['max_fp_rate'].append(general_fp_rate)
        data1['avg_optimal_q'].append(general_optimal_q)
        data1['avg_optimal_k'].append(general_optimal_k)
        data1['avg_detected time(s)'].append(general_avg_detected_time)
            
        
    df = pd.DataFrame(data)
    df1 = pd.DataFrame(data1)
        
    # excel_file = 'test_result_hardcode_with_n_equals_' + str(item_counts) + '.xlsx'
    excel_file = 'BF_parameters_heuristic_in_details.xlsx'
    excel_file_1 = 'BF_parameters_heuristic_in_general.xlsx'
        
    df.to_excel(excel_file, index=False)
    df1.to_excel(excel_file_1, index=False)
        
    print(f"Data testing exported to {excel_file} and {excel_file_1}")
    timeEnd = time.time()
    print(f"Total execution time: {timeEnd-timeStart} seconds")