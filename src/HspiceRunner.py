import os
import logging

def run(out_path: str, inp_file: str, copy: list = [], cmd: str = 'hspice', **kwargs):
    os.mkdir(out_path)
    logging.info("starting " + out_path)
    create_config_file(out_path, **kwargs)
    for file_path in copy+[inp_file]:
        file = os.path.join(out_path, os.path.split(file_path)[1])
        os.system('cp "%s" "%s"' %(file_path, file))

    if cmd == 'hspice':
        os.system('hspice -i "%s" -o "%s"' %(file, out_path))
    elif cmd == 'spectre':
        os.system('spectre -outdir "%s" "%s"' %(out_path, file))

def create_config_file(path: str, temp=None, **kwargs):
    with open(os.path.join(path, "config.cir"), "w") as file:
        if temp != None:
            file.write(".temp")
            if isinstance(temp, list):
                for t in temp:
                    file.write(" %s" %(str(t)))
            else:
                file.write(" %s" %(str(temp)))
            file.write("\n")
    
        for variable, value in kwargs.items():
            file.write(".param %s = %s\n" %(variable, str(value)))
        
if __name__ == '__main__':
    os.mkdir("test")
    run("test/", "Scripts/NAND2_var.cir", copy=["Scripts/32nm_HPvar.pm"], temp=[0, 50], 
        passo    = '0.01n',
        t_pulse  = '10n',
        dl       = '0.1p',
        pmosL    = '32n',
        pmosW    = '64n',
        nmosL    = '32n',
        nmosW    = '64n',
        Vin      = '0.9',
        load     = '1f')
"""
    f = e.submit(self.__runner, 
                os.path.join(path, str(idx)),
                **self.__cases.loc[idx].to_dict(),
                **self.__config)
"""