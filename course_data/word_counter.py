import pandas as pd
from collections import Counter

def word_frequency(series):
    word_count = Counter()
    for entry in series:
        words = entry.split()
        word_count.update(words)
    frequency_series = pd.Series(word_count)
    filtered_series = frequency_series[frequency_series >= 100].sort_values(ascending=False)

    return filtered_series

# Example usage:
data = pd.read_csv('combined_courses_preprocessed.csv')['Description Preprocessed'].dropna()
freq = word_frequency(data)
pd.set_option('display.max_rows', None)
print(freq)
