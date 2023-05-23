import argparse

from src.ExperimentManager import ExperimentManager
from src.CSVmanager import CSVmanager
import src.HspiceRunner as HspiceRunner

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spice Simulation Manager")
    parser.add_argument('-o', dest='out_dir', required=True, help="Complete output path for results")
    parser.add_argument('-p', dest='parameters', required=True, help="Json file containing two dictionaties: config (configurations for the spice script and its path) and var (values that will be permutated during simulation)")

    args = parser.parse_args()

    experiment = ExperimentManager(args, HspiceRunner.run)
    experiment.run(max_workers=6)

    CSVmanager.join_all(args.out_dir) 