import pandas as pd
import json
import os

class CSVmanager():
    @staticmethod
    def join_all_hspice(directory):
        cases = pd.read_csv(os.path.join(directory, "cases.csv"), index_col=0)
        dfs = []
        for i in cases.index:
            cur_dir = os.path.join(directory, "results", str(i))
            mc, prefix = CSVmanager.load_results_files_hspice(cur_dir)
            for col in cases.columns:
                mc[col] = cases[col].loc[i]
            prefix += ".mt"
            for f in os.listdir(cur_dir):
                if f.startswith(prefix):
                    data = pd.read_csv(os.path.join(cur_dir, f), index_col=0, skiprows=4)
                    data = data.drop(columns=data.columns[-1])
                    dfs.append(pd.concat([mc, data], axis=1))
        pd.concat(dfs, ignore_index=True).to_csv("all_results.csv")
    
    @staticmethod
    def load_results_files_hspice(directory):
        file = [f for f in os.listdir(directory) if f.endswith(".mc0.csv")][0]
        mc = pd.read_csv(os.path.join(directory, file), index_col=0, skiprows=26)
        col = mc.columns
        mc = mc.drop(columns=col[-1])
        rename = {}
        for i in range(len(col)-1):
            rename[col[i]] = col[i+1]
        return (mc.rename(rename, axis=1), file.split('.')[0])
    
    @staticmethod
    def join_all_spctre(directory):
        cases = pd.read_csv(os.path.join(directory, "cases.csv"), index_col=0)
        dfs = []
        for i in cases.index:
            cur_dir = os.path.join(directory, "results", str(i)) #esssa solução é bem mais ou menos, ela necessita que as pastas dentro de results tenham esse pk inteiro
            
            mc, prefix = CSVmanager.load_results_files_spectre(cur_dir)
            for col in cases.columns:
                mc[col] = cases[col].loc[i]
            prefix += ".mt"
            for f in os.listdir(cur_dir):
                if f.startswith(prefix):
                    data = pd.read_csv(os.path.join(cur_dir, f), index_col=0, skiprows=4)
                    data = data.drop(columns=data.columns[-1])
                    dfs.append(pd.concat([mc, data], axis=1))
        
        pd.concat(dfs, ignore_index=True).to_csv("all_results.csv")

    @staticmethod
    def load_results_files_spectre(directory):
        file = [f for f in os.listdir(directory) if f.endswith(".mcdata")][0]
        
        mc = pd.read_csv(os.path.join(directory, file), sep="\t", header=None)         
        col = mc.columns
        mc = mc.drop(columns=col[-1])
        rename = {}
        for i in range(len(col)-1):
            rename[col[i]] = col[i+1]

        return (mc.rename(rename, axis=1), file.split('.')[0])

if __name__ == '__main__':
    sim_type = input("What type of simulation files (spectre or hspice)? => ")
    dir = input("What's the directory name? => ")
    if sim_type == "hspice": 
        CSVmanager.join_all_hspice(dir)
    elif sim_type == "spectre":
        CSVmanager.join_all_spctre(dir)