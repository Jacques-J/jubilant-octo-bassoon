import threading
import time
import random

# Constants
NUM_PHILOSOPHERS = 4
EATING_TIME_RANGE = (10, 40)
THINKING_TIME = 10
SIMULATION_TIME = 60

# Mutex locks for forks
fork_locks = [threading.Lock() for _ in range(NUM_PHILOSOPHERS)]

# Shared file for logging
log_file = open('philosophers.log', 'w')

# Variables for tracking times
hungry_times = [0] * NUM_PHILOSOPHERS
eating_times = [0] * NUM_PHILOSOPHERS
thinking_times = [0] * NUM_PHILOSOPHERS


class Philosopher(threading.Thread):
    def __init__(self, index):
        threading.Thread.__init__(self)
        self.index = index
        self.left_fork_index = index
        self.right_fork_index = (index + 1) % NUM_PHILOSOPHERS

    def run(self):
        global log_file, hungry_times, eating_times, thinking_times

        # Run for the specified simulation time
        start_time = time.time()
        while time.time() - start_time < SIMULATION_TIME:
            self.think()
            self.pickup_left_fork()
            self.pickup_right_fork()
            self.eat()
            self.putdown_forks()

        # Log statistics
        log_file.write(f"Philosopher {self.index} - Hungry: {hungry_times[self.index]}s, Eating: {eating_times[self.index]}s, Thinking: {thinking_times[self.index]}s\n")

    def think(self):
        time.sleep(THINKING_TIME)
        thinking_times[self.index] += THINKING_TIME

    def pickup_left_fork(self):
        fork = fork_locks[self.left_fork_index]
        fork.acquire()

    def pickup_right_fork(self):
        fork = fork_locks[self.right_fork_index]
        fork.acquire()

    def eat(self):
        eating_time = random.uniform(*EATING_TIME_RANGE) / 1000
        time.sleep(eating_time)
        eating_times[self.index] += eating_time

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
total_hungry_time = sum(hungry_times)
total_eating_time = sum(eating_times)
total_thinking_time = sum(thinking_times)

avg_hungry_time = total_hungry_time / NUM_PHILOSOPHERS
avg_eating_time = total_eating_time / NUM_PHILOSOPHERS
avg_thinking_time = total_thinking_time / NUM_PHILOSOPHERS

print(f"Average hungry time: {avg_hungry_time:.2f}s")
print(f"Average eating time: {avg_eating_time:.2f}s")
print(f"Average thinking time: {avg_thinking_time:.2f}s")
