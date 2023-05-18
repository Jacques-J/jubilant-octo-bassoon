import re
import time
start_time = time.time()

def count_word_lengths(file_path):
    word_counts = {}

    with open(file_path, 'r') as file:
        for line in file:
            # Remove non-alphanumeric characters except for - and _
            line = re.sub(r'[^A-Za-z0-9-_ ]', ' ', line)
            words = line.split()

            for word in words:
                length = len(word)
                word_counts[length] = word_counts.get(length, 0) + 1

    return word_counts

def print_word_frequencies(word_counts):
    max_length = max(word_counts.keys())
    max_count = max(word_counts.values())

    print("Word Length\tFrequency")
    print("-------------------------")
    for length in range(1, max_length + 1):
        count = word_counts.get(length, 0)
        frequency = count / max_count * 100 if max_count != 0 else 0
        print(f"{length}\t\t{frequency:.2f}%")

if __name__ == '__main__':
    file_path = 'sample.txt'  # Path to the sample text file

    word_counts = count_word_lengths(file_path)
    print_word_frequencies(word_counts)
end_time = time.time()
print ("This took %.2f seconds" % (end_time - start_time))