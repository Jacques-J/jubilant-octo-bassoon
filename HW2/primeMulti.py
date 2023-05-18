import math
import time
import multiprocessing
start_time = time.time()

def is_prime(n):
    if n < 2:
        return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False

    return True

def check_prime(number):
    
    if is_prime(number):
        print(f"{number} is prime")
    else:
        print(f"{number} is not prime")

if __name__ == '__main__':
    number = 69881631850817231  # Hardcoded number to check


    # Create a multiprocessing Pool with the number of available CPU cores
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    # Split the range of numbers into chunks
    #chunks = multiprocessing.cpu_count()

    # Distribute the work among processes
    #pool.map(check_prime, range(2, number + 1, chunks))

    result = pool.map(check_prime, [number]) [0]

    # Close the pool and wait for the processes to finish
    pool.close()
    pool.join()

end_time = time.time()
print ("This took %.2f seconds" % (end_time - start_time))