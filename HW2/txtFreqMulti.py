import re
import multiprocessing
import time
start_time = time.time()

def count_word_lengths(file_path, word_lengths):
    with open(file_path, 'r') as file:
        for line in file:
            # Remove non-alphanumeric characters except for - and _
            line = re.sub(r'[^A-Za-z0-9-_ ]', ' ', line)
            words = line.split()

            for word in words:
                length = len(word)
                word_lengths.append(length)

def update_word_counts(word_lengths, word_counts):
    for length in word_lengths:
        with lock:
            word_counts[length] = word_counts.get(length, 0) + 1

if __name__ == '__main__':
    file_path = 'sample.txt'  # Path to the sample text file

    manager = multiprocessing.Manager()
    word_lengths = manager.list()
    word_counts = manager.dict()
    lock = multiprocessing.Lock()

    # Create and start the file I/O process
    io_process = multiprocessing.Process(target=count_word_lengths, args=(file_path, word_lengths))
    io_process.start()

    # Create and start the word counting processes
    counting_process1 = multiprocessing.Process(target=update_word_counts, args=(word_lengths[:len(word_lengths)//2], word_counts))
    counting_process2 = multiprocessing.Process(target=update_word_counts, args=(word_lengths[len(word_lengths)//2:], word_counts))
    counting_process1.start()
    counting_process2.start()

    # Wait for the file I/O process to finish
    io_process.join()

    # Wait for the word counting processes to finish
    counting_process1.join()
    counting_process2.join()

    # Print the word frequencies
    max_length = max(word_counts.keys())
    max_count = max(word_counts.values())

    print("Word Length\tFrequency")
    print("-------------------------")
    for length in range(1, max_length + 1):
        count = word_counts.get(length, 0)
        frequency = count / max_count * 100 if max_count != 0 else 0
        print(f"{length}\t\t{frequency:.2f}%")

end_time = time.time()
print ("This took %.2f seconds" % (end_time - start_time))
