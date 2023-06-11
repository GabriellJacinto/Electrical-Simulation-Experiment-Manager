import pandas as pd
import itertools
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
    def join_all_spctre(directory, input_file_name):
        cases = pd.read_csv(os.path.join(directory, "cases.csv"), index_col=0)
        dfs = []
        for i in cases.index:
            process_dir = os.path.join(directory, "results", str(i), "{}.raw".format(input_file_name)) #essa solução é bem mais ou menos, ela necessita que as pastas dentro de results tenham esse pk inteiro
            results_dir = os.path.join(directory, "results", str(i)) 

            mc = CSVmanager.load_results_files_spectre(process_dir)
            for col in cases.columns:
                mc[col] = cases[col].loc[i]
            prefix = "{}.mt".format(input_file_name)
            for f in os.listdir(results_dir):
                if f.startswith(prefix):
                    with open(os.path.join(results_dir, f), 'r') as file:
                        lines = file.readlines()[2:]
                    # Step 1: process the list to remove unwanted characters or lines
                    lines = [line.split() for line in lines] 
                    flattened_list = list(itertools.chain(*lines))
                    # Step 2: finds "alter#", which is assumed to always be the last column
                    alter_idx = (flattened_list.index("alter#"))
                    headers, raw_data = flattened_list[:alter_idx+1], flattened_list[alter_idx+1:] 
                    # Step 3: groups the data according to the number of columns
                    m=len(headers)
                    grouped_data = [raw_data[i:i+m] for i in range(0, len(raw_data), m)] 
                    data = pd.DataFrame(grouped_data, columns=headers)
                    dfs.append(pd.concat([mc, data], axis=1))
        pd.concat(dfs, ignore_index=True).to_csv(os.path.join(directory,"all_results_{}.csv".format(input_file_name)))

    @staticmethod
    def load_results_files_spectre(directory):
        file = [f for f in os.listdir(directory) if f.endswith(".mcdata")][0]
        
        mc = pd.read_csv(os.path.join(directory, file), sep="\t", header=None)         
        col = mc.columns
        mc = mc.drop(columns=col[-1])
        rename = {}

        # Alters the name of the varibilty parameters columns
        for i in range(len(col)-1):
            rename[col[i]] = col[i+1]

        return mc.rename(rename, axis=1)

if __name__ == '__main__':
    #CSVmanager.join_all_spctre("../sample_results/NOT", "not")
    
    sim_type = input("What type of simulation files (spectre or hspice)? => ")
    dir = input("What's the directory name? => ")
    if sim_type == "hspice": 
        CSVmanager.join_all_hspice(dir)
    elif sim_type == "spectre":
        file_name = input("What's the name of the simulation script? ")
        CSVmanager.join_all_spctre(dir, file_name)