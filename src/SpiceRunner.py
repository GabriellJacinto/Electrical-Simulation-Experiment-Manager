import os

def run(out_path: str, inp_file: str, copy: list = [], cmd = None, **kwargs):
    os.mkdir(out_path)
    create_config_file(out_path, cmd=cmd, **kwargs)
    for file_path in copy+[inp_file]:
        file = os.path.join(out_path, os.path.split(file_path)[1])
        os.system('cp "%s" "%s"' %(file_path, file))
    if cmd == 'hspice':
        os.system('hspice -i "%s" -o "%s"' %(file, out_path))
    elif cmd == 'spectre':
        os.system('spectre -outdir "%s" "%s"' %(out_path, file))

def create_config_file(path: str, temp=None, cmd=None, **kwargs):
    with open(os.path.join(path, "config.cir"), "w") as file:
        if temp != None:
            file.write(".temp")
            if isinstance(temp, list):
                for t in temp:
                    file.write(" %s" %(str(t)))
            else:
                file.write(" %s" %(str(temp)))
            file.write("\n")
        if cmd == "spectre":
            file.write("simulator lang=spectre\n")
            for variable, value in kwargs.items():
                file.write("parameters %s = %s\n" %(variable, str(value)))
        elif cmd == "hspice":
            for variable, value in kwargs.items():
                file.write(".param %s = %s\n" %(variable, str(value)))
        else:
            raise KeyError(cmd)

if __name__ == '__main__':
    os.mkdir("test")
    run("test/", "inverter.sp", copy=["../lib/FET_TT.pm"], temp=[0, 50], 
        vss         = 0,  
        number_fins = 1,
        cmd         = "spectre")
"""
    f = e.submit(self.__runner, 
                os.path.join(path, str(idx)),
                **self.__cases.loc[idx].to_dict(),
                **self.__config)
"""