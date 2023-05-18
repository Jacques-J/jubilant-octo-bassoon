import re
import threading
from queue import Queue
import time
start_time = time.time()

def count_word_lengths(file_path, queue):
    word_counts = {}

    with open(file_path, 'r') as file:
        for line in file:
            # Remove non-alphanumeric characters except for - and _
            line = re.sub(r'[^A-Za-z0-9-_ ]', ' ', line)
            words = line.split()

            for word in words:
                length = len(word)
                queue.put(length)

    queue.put(None)  # Signal the end of processing

def update_word_counts(queue, word_counts):
    while True:
        length = queue.get()
        if length is None:
            break

        with lock:
            word_counts[length] = word_counts.get(length, 0) + 1

if __name__ == '__main__':
    file_path = 'sample.txt'  # Path to the sample text file

    word_counts = {}
    lock = threading.Lock()
    queue = Queue()

    # Create and start the counting thread
    counting_thread = threading.Thread(target=count_word_lengths, args=(file_path, queue))
    counting_thread.start()

    # Create and start the updating thread
    updating_thread = threading.Thread(target=update_word_counts, args=(queue, word_counts))
    updating_thread.start()

    # Wait for both threads to finish
    counting_thread.join()
    updating_thread.join()

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