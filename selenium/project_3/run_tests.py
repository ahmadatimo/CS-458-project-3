import os
import subprocess

# Automatically generate test file names from test1.py to test20.py
test_files = [f"test{i}.py" for i in range(1, 21)]

for test_file in test_files:
    print(f"Running {test_file}...")
    subprocess.run(["python3.10", test_file])
    print(f"Finished {test_file}\n")
