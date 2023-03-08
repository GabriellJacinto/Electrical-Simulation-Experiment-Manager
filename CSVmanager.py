import pandas as pd
import json
import os

class CSVmanager():
    @staticmethod
    def join_all(directory):
        cases = pd.read_csv(os.path.join(directory, "cases.csv"), index_col=0)
        dfs = []
        for i in cases.index:
            cur_dir = os.path.join(directory, "results", str(i))
            mc, prefix = CSVmanager.load_mc(cur_dir)
            for col in cases.columns:
                mc[col] = cases[col].loc[i]
            prefix += ".mt"
            for f in os.listdir(cur_dir):
                if f.startswith(prefix):
                    data = pd.read_csv(os.path.join(cur_dir, f), index_col=0, skiprows=4)
                    data = data.drop(columns=data.columns[-1])
                    dfs.append(pd.concat([mc, data], axis=1))
        pd.concat(dfs, ignore_index=True).to_csv(os.path.join(directory, "results", "all.csv"))
    
    @staticmethod
    def load_mc(directory):
        file = [f for f in os.listdir(directory) if f.endswith(".mc0.csv")][0]
        mc = pd.read_csv(os.path.join(directory, file), index_col=0, skiprows=26)
        col = mc.columns
        mc = mc.drop(columns=col[-1])
        rename = {}
        for i in range(len(col)-1):
            rename[col[i]] = col[i+1]
        return (mc.rename(rename, axis=1), file.split('.')[0])
        
if __name__ == '__main__':
    CSVmanager.join_all("NAND2_40") 