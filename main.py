import argparse

from src.ExperimentManager import ExperimentManager
from src.CSVmanager import CSVmanager
import src.SpiceRunner as SpiceRunner

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spice Simulation Manager")
    parser.add_argument('-o', dest='out_dir', required=True, help="Complete output path for results")
    parser.add_argument('-p', dest='parameters', required=True, help="Json file containing two dictionaties: config (configurations for the spice script and its path) and var (values that will be permutated during simulation)")
    parser.add_argument('-w', dest='max_workers', required=False, help="Maximum number of parallel simulations", default=6)

    args = parser.parse_args()

    experiment = ExperimentManager(args, SpiceRunner.run)
    experiment.run(max_workers=args.max_workers)
    
    if experiment.command == "hspice": 
        CSVmanager.join_all_hspice(experiment.out_dir)
    elif experiment.command == "spectre":
        CSVmanager.join_all_spctre(experiment.out_dir, experiment.input_file_name)