import pandas as pd

def read_csv(file_path, delimiter='|'):
    return pd.read_csv(file_path, delimiter=delimiter, skiprows=1)

def compare_csv(doc1_path, doc2_path, threshold=0.05, delimiter='|'):
    doc1 = read_csv(doc1_path, delimiter)
    doc2 = read_csv(doc2_path, delimiter)

    # Combine the first two columns to create a key
    doc1['key'] = doc1.iloc[:, 0].astype(str) + '_' + doc1.iloc[:, 1].astype(str)
    doc2['key'] = doc2.iloc[:, 0].astype(str) + '_' + doc2.iloc[:, 1].astype(str)

    # Set the key as index
    doc1.set_index('key', inplace=True)
    doc2.set_index('key', inplace=True)

    # Find common keys
    common_keys = doc1.index.intersection(doc2.index)

    # Compare the values in the 7th and 8th columns
    results = []
    for key in common_keys:
        value1_7th = doc1.loc[key].iloc[6]
        value2_7th = doc2.loc[key].iloc[6]
        value1_8th = doc1.loc[key].iloc[7]
        value2_8th = doc2.loc[key].iloc[7]

        # Calculate the percentage difference
        diff_7th = abs(value1_7th - value2_7th) / value1_7th if value1_7th != 0 else float('inf')
        diff_8th = abs(value1_8th - value2_8th) / value1_8th if value1_8th != 0 else float('inf')

        # Check if the difference exceeds the threshold
        if diff_7th > threshold:
            results.append(f"Key: {key} - 7th column value differs by more than {threshold*100}% (Original: {value1_7th}, New: {value2_7th})")
        if diff_8th > threshold:
            results.append(f"Key: {key} - 8th column value differs by more than {threshold*100}% (Original: {value1_8th}, New: {value2_8th})")

    return results

if __name__ == "__main__":
    doc1_path = "path/to/doc1.csv"
    doc2_path = "path/to/doc2.csv"
    threshold = 0.05  # 5%

    differences = compare_csv(doc1_path, doc2_path, threshold)

    for diff in differences:
        print(diff)
