import time
from experiments_csv.load import load_instance_and_profile_from_csv_file
from pabutools.rules.gpseq import gpseq

instance, profile = load_instance_and_profile_from_csv_file("experiments_csv/big_input.csv")

start = time.perf_counter()
gpseq(instance, profile)
end = time.perf_counter()

print(f"⏱ GPseq runtime BEFORE optimization: {end - start:.6f} seconds")
