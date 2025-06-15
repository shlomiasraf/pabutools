import os
import time
import pandas as pd

from pabutools.rules.gpseq import gpseq
from pabutools.rules.phragmen import sequential_phragmen
from experiments_csv.load import load_instance_and_profile_from_csv_file

# Path to the directory containing experiment CSV files
EXPERIMENTS_DIR = "experiments_csv"

def run_comparison_on_instance(instance, profile, experiment_name):
    """
    Runs both GPseq and Phragmen algorithms on a given instance and profile,
    and returns the results including execution time and selected projects.
    """
    results = []

    for algorithm_name, algorithm_function in [
        ("GPseq", gpseq),
        ("Phragmen", sequential_phragmen)
    ]:
        start_time = time.time()
        result = algorithm_function(instance, profile)
        elapsed_time = round(time.time() - start_time, 6)

        results.append({
            "experiment": experiment_name,
            "algorithm": algorithm_name,
            "selected_projects": ",".join(p.name for p in result),
            "num_selected": len(result),
            "execution_time_sec": elapsed_time
        })

    return results

def main():
    all_results = []

    for filename in os.listdir(EXPERIMENTS_DIR):
        if not filename.endswith(".csv"):
            continue

        path = os.path.join(EXPERIMENTS_DIR, filename)

        try:
            instance, profile = load_instance_and_profile_from_csv_file(path)
            experiment_results = run_comparison_on_instance(instance, profile, filename)
            all_results.extend(experiment_results)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    # Save results to CSV
    df = pd.DataFrame(all_results)
    df.to_csv("comparison_all_experiments.csv", index=False)
    print("✅ Results saved to 'comparison_all_experiments.csv'")
    print(df)

if __name__ == "__main__":
    main()
