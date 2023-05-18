import math
import time
start_time = time.time()

def is_prime(n):
    if n < 2:
        return False

    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False

    return True

if __name__ == '__main__':
    number = 69881631850817231  # Hardcoded number to check

    if is_prime(number):
        print(f"{number} is prime")
    else:
        print(f"{number} is not prime")
end_time = time.time()
print ("This took %.2f seconds" % (end_time - start_time))
