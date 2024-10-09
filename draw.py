import pandas as pd
import matplotlib.pyplot as plt

# This file is use for other purpose, that is checking time between Bloom Filter using FP-rate = 0.01, and parameters that is
# calculated from Test_bloom_variable.py file. The numbers below, each of them is the average result, which is calculated from 100 results
# with the same conditions.

# 4 data below are the results of other work that is further from BF scope, and have nothing to notice on this work. You can know that
# that other work support a query which can return boolean value. And base on the FP-rate, the result returned may be wrong. (The bigger
# FP-rate, the more wrong result returned). The time of each function is calculated by the average time of 100 results.

# Plot 4.2: Chart that show runtime of functions that use Bloom Filter with FP-rate = 0.01, and return true for the query.
data_4_2 = {
    'N': [250, 500, 750, 1000, 1250, 1500, 1750, 2000],
    'commit_4_2': [50.2087, 95.6459, 130.6562, 169.9348, 214.7093, 256.7218, 289.7610, 337.1503],
    'generate_proof_4_2': [6.9067, 13.2527, 18.1590, 23.5217, 28.9882, 34.7959, 40.7629, 46.7266],
    'verification_4_2': [107.8411, 105.7711, 107.6122, 111.2974, 109.2190, 112.3603, 122.9812, 128.4400],
    'execution_time_4_2': [404.8523, 771.2792, 1157.0934, 1537.6996, 1927.0494, 2331.3802, 2629.2623, 3104.8206]
}

# Plot 4.4: Chart that show runtime of funtions that use Bloom Filter with parameters from this work, and return true for the query.
data_4_4 = {
    'N': [250, 500, 750, 1000, 1250, 1500, 1750, 2000],
    'commit_4_4': [36.1799, 69.0325, 98.3444, 133.2830, 170.1691, 178.4985, 176.9156, 223.7173],
    'generate_proof_4_4': [1.4220, 4.1896, 4.2616, 8.2417, 10.5786, 10.7284, 10.8700, 13.2595],
    'verification_4_4': [68.9108, 77.6504, 81.2333, 81.8836, 93.7301, 107.8836, 82.8215, 90.1038],
    'execution_time_4_4': [267.1072, 545.8248, 804.7239, 1204.7347, 1501.5904, 1534.1482, 1590.5207, 1994.4261]
}

# Plot 4.3: Chart that show runtime of functions that use Bloom Filter with FP-rate = 0.01, and return false for the query.
data_4_3 = {
    'N': [250, 500, 750, 1000, 1250, 1500, 1750, 2000],
    'commit_4_3': [48.5605, 94.0926, 128.0318, 163.2266, 211.2313, 242.1553, 299.7898, 350.3360],
    'generate_proof_4_3': [6.8388, 12.9620, 18.2114, 22.9553, 28.7146, 33.6467, 41.8854, 44.1231],
    'verification_4_3': [97.0775, 106.3600, 107.3400, 107.4904, 106.7949, 107.6639, 112.5151, 113.6594],
    'execution_time_4_3': [404.1362, 724.0072, 1150.5271, 1623.4981, 1936.6037, 2206.7247, 2789.8722, 3102.3089]
}

# Plot 4.5: Chart that show runtime of funtions that use Bloom Filter with parameters from this work, and return false for the query.
data_4_5 = {
    'N': [250, 500, 750, 1000, 1250, 1500, 1750, 2000],
    'commit_4_5': [47.6849, 30.9004, 115.1021, 156.7491, 189.6461, 168.1094, 248.9460, 263.9163],
    'generate_proof_4_5': [2.0185, 1.9390, 4.5428, 9.2853, 11.8501, 10.0709, 15.4187, 15.8775],
    'verification_4_5': [90.4846, 80.3414, 87.0920, 119.7157, 96.0746, 88.7939, 112.1339, 112.2152],
    'execution_time_4_5': [362.8521, 224.3038, 903.3621, 1387.5186, 1542.4667, 1559.4922, 2256.8272, 2373.8093]
}

# Change data into DataFrame
df_4_2 = pd.DataFrame(data_4_2)
df_4_4 = pd.DataFrame(data_4_4)
df_4_3 = pd.DataFrame(data_4_3)
df_4_5 = pd.DataFrame(data_4_5)

# Create plots
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

# Comparison between Plot 4.2 and Plot 4.4  
axs[0, 0].plot(df_4_2['N'], df_4_2['commit_4_2'], label='Commit (4.2)', marker='o')
axs[0, 0].plot(df_4_4['N'], df_4_4['commit_4_4'], label='Commit (4.4)', marker='o')
axs[0, 0].set_title('Commit Time Comparison (4.2 vs 4.4)')
axs[0, 0].set_xlabel('N')
axs[0, 0].set_ylabel('Time (s)')
axs[0, 0].legend()

axs[0, 1].plot(df_4_2['N'], df_4_2['generate_proof_4_2'], label='Generate Proof (4.2)', marker='o')
axs[0, 1].plot(df_4_4['N'], df_4_4['generate_proof_4_4'], label='Generate Proof (4.4)', marker='o')
axs[0, 1].set_title('Generate Proof Time Comparison (4.2 vs 4.4)')
axs[0, 1].set_xlabel('N')
axs[0, 1].set_ylabel('Time (s)')
axs[0, 1].legend()

axs[1, 0].plot(df_4_2['N'], df_4_2['verification_4_2'], label='Verification (4.2)', marker='o')
axs[1, 0].plot(df_4_4['N'], df_4_4['verification_4_4'], label='Verification (4.4)', marker='o')
axs[1, 0].set_title('Verification Time Comparison (4.2 vs 4.4)')
axs[1, 0].set_xlabel('N')
axs[1, 0].set_ylabel('Time (ms)')
axs[1, 0].legend()

axs[1, 1].plot(df_4_2['N'], df_4_2['execution_time_4_2'], label='Execution Time (4.2)', marker='o')
axs[1, 1].plot(df_4_4['N'], df_4_4['execution_time_4_4'], label='Execution Time (4.4)', marker='o')
axs[1, 1].set_title('Execution Time Comparison (4.2 vs 4.4)')
axs[1, 1].set_xlabel('N')
axs[1, 1].set_ylabel('Time (s)')
axs[1, 1].legend()

plt.tight_layout()
plt.show()

# Comparison between Plot 4.2 and Plot 4.4 
fig, axs = plt.subplots(2, 2, figsize=(14, 10))

axs[0, 0].plot(df_4_3['N'], df_4_3['commit_4_3'], label='Commit (4.3)', marker='o')
axs[0, 0].plot(df_4_5['N'], df_4_5['commit_4_5'], label='Commit (4.5)', marker='o')
axs[0, 0].set_title('Commit Time Comparison (4.3 vs 4.5)')
axs[0, 0].set_xlabel('N')
axs[0, 0].set_ylabel('Time (s)')
axs[0, 0].legend()

axs[0, 1].plot(df_4_3['N'], df_4_3['generate_proof_4_3'], label='Generate Proof (4.3)', marker='o')
axs[0, 1].plot(df_4_5['N'], df_4_5['generate_proof_4_5'], label='Generate Proof (4.5)', marker='o')
axs[0, 1].set_title('Generate Proof Time Comparison (4.3 vs 4.5)')
axs[0, 1].set_xlabel('N')
axs[0, 1].set_ylabel('Time (s)')
axs[0, 1].legend()

axs[1, 0].plot(df_4_3['N'], df_4_3['verification_4_3'], label='Verification (4.3)', marker='o')
axs[1, 0].plot(df_4_5['N'], df_4_5['verification_4_5'], label='Verification (4.5)', marker='o')
axs[1, 0].set_title('Verification Time Comparison (4.3 vs 4.5)')
axs[1, 0].set_xlabel('N')
axs[1, 0].set_ylabel('Time (ms)')
axs[1, 0].legend()

axs[1, 1].plot(df_4_3['N'], df_4_3['execution_time_4_3'], label='Execution Time (4.3)', marker='o')
axs[1, 1].plot(df_4_5['N'], df_4_5['execution_time_4_5'], label='Execution Time (4.5)', marker='o')
axs[1, 1].set_title('Execution Time Comparison (4.3 vs 4.5)')
axs[1, 1].set_xlabel('N')
axs[1, 1].set_ylabel('Time (s)')
axs[1, 1].legend()

plt.tight_layout()
plt.show()
