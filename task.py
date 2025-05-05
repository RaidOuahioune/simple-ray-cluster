import ray
import time
import numpy as np
import os

# Connect to the Ray cluster - modified connection string
ray.init(address="ray://ray-head:10001", _redis_password=os.environ.get("REDISPASSWORD", "password"))

print("Connected to Ray cluster")
print(f"Ray cluster resources: {ray.cluster_resources()}")

# Define a regular Python function
def calculate_square(x):
    time.sleep(0.5)  # Simulate some work
    return x * x

# Turn the function into a Ray remote function using the decorator
@ray.remote
def calculate_square_remote(x):
    time.sleep(0.5)  # Simulate some work
    return x * x

# --- Sequential Execution (for comparison) ---
print("Starting sequential execution...")
start_time_seq = time.time()
results_seq = [calculate_square(i) for i in range(10)]
end_time_seq = time.time()
print(f"Sequential results: {results_seq}")
print(f"Sequential execution time: {end_time_seq - start_time_seq:.2f} seconds")
print("-" * 20)

# --- Parallel Execution with Ray ---
print("Starting Ray parallel execution...")
start_time_ray = time.time()
# Launch remote tasks. These calls return immediately with ObjectRefs (futures).
result_refs = [calculate_square_remote.remote(i) for i in range(10)]
# Retrieve the actual results from the ObjectRefs. This blocks until results are ready.
results_ray = ray.get(result_refs)
end_time_ray = time.time()
print(f"Ray results: {results_ray}")
print(f"Ray execution time: {end_time_ray - start_time_ray:.2f} seconds")
print("-" * 20)

assert results_seq == results_ray
print("Results verified.")

# Shutdown Ray connection
ray.shutdown()
print("Ray connection shut down.")