# Electrical-Simulation-Experiment-Manager

<div align="center">

![PyPI](https://img.shields.io/pypi/v/customtkinter)
![PyPI - Downloads](https://img.shields.io/pypi/dm/customtkinter?color=green&label=downloads)
![Downloads](https://static.pepy.tech/personalized-badge/customtkinter?period=total&units=international_system&left_color=grey&right_color=green&left_text=downloads)
![Mozilla Add-on](https://img.shields.io/amo/dw/teste)
</div>

Python automation for electrical simulation with spectre and hspice

## 💻 Requirements

Before downloading, certify that you have the following requirements:
* You have the most recent version of `python`
* Your operating system is `Windows` or `Linux` based.

## 🚀 Installing

Run the following commands:

```
pip install -r requirements.txt
```

Lauching the application:

```
python3 main.py
```
## Current Version: 0.1

This software is on realese 0.1. The current version is capable of:

<details open>
<summary>Version 1.1.* Features</summary>

- [x] Execution by command line (see [Installation](#🚀-Installing))
- [ ] Update readme instructions.
- [x] Run Hspice files Manually
- [x] Run Spectre files Manually
- [x] Manage simulation files and compile in one csv
- [x] Run automatically to any type of simulation (either Hspice or Spectre)  
- [ ] Adicionar o comando '.option post = 2' e '.option measform = 3' nos scripts para hspice, talvez fazer um template seja interessante de manter no dir de sample_scripts
- [ ] Adicionar o número de sims Monte Carlo como variável nos scripts e no .json
- [ ] Refatorar o CSVManager para que ele possa refazer o layout do all_results.csv para as simulações spectre. São dois arquivos que precisam ser processados:
        - <\cellname>.mt0
        - <\cellname>.raw/mc1.process.mcdata
- [ ] Verificar se a criação do file config.cir está correto para as simulações spectre, creio que esteja no formato hspice ainda 
  
</details>


## 📝 License

See [License](LICENSE) for more information.

[⬆ Back to the top](#-Electrical-Simulation-Experiment-Manager)<br>
