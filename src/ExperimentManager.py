from concurrent.futures import ProcessPoolExecutor, as_completed
from threading import Lock
from datetime import datetime
from typing import Callable
from itertools import product
import logging
import pandas as pd
import json
import time
import os

class ExperimentManager:
    __out_dir: str
    __var: dict
    __runner: Callable
    __config: dict
    __cases: pd.DataFrame

    def __init__(self, args, runner, resume=False):
        """
        Inicializa o gerenciador de experimentos

        Parameters
        ----------
        out_dir : str
            Diretório de destino.
        var : dict
            Dicionário com as variáveis a serem testadas como chaves e os
            possíveis valores em uma lista.
        runner : Callable
            Experimento individual.
        config : TYPE, optional
            Parâmetros fixos para todos os experimentos realizados.
        """
        self.__out_dir = "simResults_" + args.out_dir
        with open(args.parameters) as json_file:
            self.__parameters = json.load(json_file)
        self.__config = self.__parameters["config"]
        self.__var = self.__parameters["var"]
        
        self.__runner = runner
        self.lock = Lock()
        
        if not resume:
            os.makedirs(self.__out_dir)
            with open(os.path.join(self.__out_dir, "parameters.json"), "w") as file:
                json.dump({"var": self.__var, "config": self.__config}, file)
            
            products = list(product(*self.__var.values()))
            self.__cases = pd.DataFrame(products, columns=self.__var.keys())
            self.__cases.to_csv(os.path.join(self.__out_dir, "cases.csv"))
            
            self.__completed = pd.DataFrame(None, columns=self.__var.keys())
            self.__completed["time"] = None
            self.__completed.to_csv(os.path.join(self.__out_dir, "completed.csv"))
        else:
            self.__cases = pd.read_csv(os.path.join(self.__out_dir, "cases.csv"), index_col=0)
            self.__completed = pd.read_csv(os.path.join(self.__out_dir, "completed.csv"), index_col=0)

    @property
    def out_dir(self):
        return self.__out_dir

    @property
    def command(self):
        return self.__config["cmd"]

    @property
    def input_file_name(self):
        return self.__config["inp_file"]

    def run(self, max_workers: int = None):
        """
        Roda os experimentos em parelelo

        Parameters
        ----------
        max_workers : int, optional
            número máximo de simulações em paralelo
        """
        logging.basicConfig(filename=os.path.join(self.__out_dir, "log.txt"), 
                            level=logging.DEBUG)
        logging.info('Starting experiment')
        
        cases_idx = self.__cases.index
        completed_idx = self.__completed.index
        path = os.path.join(self.__out_dir, "results")
        os.makedirs(path, exist_ok=True)
        
        self.__completed_file = open(os.path.join(self.__out_dir, "completed.csv"), "a")
        with ProcessPoolExecutor(max_workers=max_workers) as e:
            for idx in cases_idx:
                print(idx)
                if idx not in completed_idx:
                    print("calling")
                    f = e.submit(self.__runner, 
                                 os.path.join(path, str(idx)),
                                 **self.__cases.loc[idx].to_dict(),
                                 **self.__config)
                    f.add_done_callback(lambda fut, i=idx: self.__callback(fut, i))
                    logging.info('Running %i' %(idx))
        self.__completed_file.close()
        
    def __callback (self, future, idx):
        logging.info('%i ended' %(idx))
        tmp_df = self.__cases.loc[[idx]]
        tmp_df["time"] = datetime.now()
        tmp_txt = tmp_df.to_csv(header=False)
        with self.lock:
            self.__completed.append(tmp_df)
            self.__completed_file.write(tmp_txt)
            self.__completed_file.flush()

if __name__ == '__main__':
    def task(path, a, b):
        print("%i+%i começando" %(a, b))
        time.sleep(a+b)
        print("%i+%i terminando" %(a, b))
        print(path)
        with open(path+".txt", "w") as file:
            file.write(str(a+b))
        
    ex = ExperimentManager("test", {"a": [2, 4, 6], "b": [0, 1]}, task)
    ex.run()