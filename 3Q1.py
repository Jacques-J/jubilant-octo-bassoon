import threading
import time
import random

# Constants
NUM_PHILOSOPHERS = 4
NUM_FORKS = 4
EATING_TIME_RANGE = (10, 40)
THINKING_TIME = 10
WAIT_TIME_RANGE = (50, 100)

# Mutex locks for forks
fork_locks = [threading.Lock() for _ in range(NUM_FORKS)]

# Shared file for logging
log_file = open('philosophers.log', 'w')


class Philosopher(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.index = index
        self.left_fork_index = index
        self.right_fork_index = (index + 1) % NUM_FORKS
        self.hungry_time = 0
        self.eating_time = 0
        self.thinking_time = 0

    def run(self):
        global log_file

        # Run for 60 seconds
        start_time = time.time()
        while time.time() - start_time < 60:
            self.think()
            self.pickup_left_fork()
            self.pickup_right_fork()
            self.eat()
            self.putdown_forks()

        # Log statistics
        log_file.write(f"Philosopher {self.index} - Hungry: {self.hungry_time}s, Eating: {self.eating_time}s, Thinking: {self.thinking_time}s\n")

    def think(self):
        time.sleep(THINKING_TIME)
        self.thinking_time += THINKING_TIME

    def pickup_left_fork(self):
        fork = fork_locks[self.left_fork_index]
        while not fork.acquire(timeout=random.uniform(*WAIT_TIME_RANGE) / 1000):
            self.hungry_time += random.uniform(*WAIT_TIME_RANGE) / 1000

    def pickup_right_fork(self):
        fork = fork_locks[self.right_fork_index]
        while not fork.acquire(timeout=random.uniform(*WAIT_TIME_RANGE) / 1000):
            fork_locks[self.left_fork_index].release()
            self.hungry_time += random.uniform(*WAIT_TIME_RANGE) / 1000
            self.pickup_left_fork()

    def eat(self):
        time.sleep(random.uniform(*EATING_TIME_RANGE) / 1000)
        self.eating_time += random.uniform(*EATING_TIME_RANGE) / 1000

    def putdown_forks(self):
        fork_locks[self.left_fork_index].release()
        fork_locks[self.right_fork_index].release()


# Create philosopher threads
philosophers = [Philosopher(i) for i in range(NUM_PHILOSOPHERS)]

# Start philosopher threads
for philosopher in philosophers:
    philosopher.start()

# Wait for philosopher threads to finish
for philosopher in philosophers:
    philosopher.join()

# Calculate and print average times
total_hungry_time = sum([philosopher.hungry_time for philosopher in philosophers])
total_eating_time = sum([philosopher.eating_time for philosopher in philosophers])
total_thinking_time = sum([philosopher.thinking_time for philosopher in philosophers])
num_philosophers = len(philosophers)

avg_hungry_time = total_hungry_time / num_philosophers
avg_eating_time = total_eating_time / num_philosophers
avg_thinking_time = total_thinking_time / num_philosophers

print(f"Average hungry time: {avg_hungry_time:.2f}s")
print(f"Average eating time: {avg_eating_time:.2f}s")
print(f"Average thinking time: {avg_thinking_time:.2f}s")
