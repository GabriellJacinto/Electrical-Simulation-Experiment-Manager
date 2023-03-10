from ExperimentManager import ExperimentManager
import HspiceRunner

var = {
    'load': ["1f", "4f", "8f", "16f"],
    'Vin': [0.6, 0.7, 0.8, 0.9],
    'pmosW': [7e-08, 1.4e-07, 2.1e-07],
    'nmosW': [7e-08, 1.4e-07, 2.1e-07, 2.8e-07, 3.4e-07, 4.2e-07]
}

config = {
    "passo": "0.01n",
    "t_pulse": "10n",
    "dl": "0.1p",
    'pmosL': "4e-08",
    'nmosL': "4e-08",
    "temp": [-25.0, 0.0, 25.0, 50.0, 75.0, 100.0],
    "inp_file": "Scripts/NAND2_var.cir", 
    "copy": ["Scripts/32nm_HPvar.pm"]
}

ex = ExperimentManager("NAND2_40", var, HspiceRunner.run, config)
ex.run(max_workers=6)