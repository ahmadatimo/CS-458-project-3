import os
import subprocess

# List of test files to run
test_files = ["test1.py", "test2.py", "test3.py", "test4.py", "test5.py"]

for test_file in test_files:
    print(f"Running {test_file}...")
    subprocess.run(["python", test_file])
    print(f"Finished {test_file}\n")