# Knowledge-Base-Inference-Checker
A knowledge Base Inference Checker in python using UBCSAT solver for windows and picosat for linux

# Depencencies
* python 
* UBCSAT if you use windows and picosat for linux

# HOW TO RUN IT

## Solvers
### Windows
To run the script on windows you'll need the UBCSAT solver. You can download it [http://ubcsat.dtompkins.com/](here).
After downloading it just place the exe in the project root

### Linux
On linux just install the solver picosat
```bash
sudo apt install picosat
```

## Run the scripts

Just need to run `main.py`

```bash
python3 main.py -linux -litteral "-5 7 5 7 7 3 0" -file uf20-01.cnf
```

### Arguements

The script take 4 arguments:
* -file to specify the path (absolute or relative) to our knowladge base, by default the knowladge base will be exemple1.cnf in the project root. Exemple : -file exemple2.cnf
* -litteral to input the literals to infere (in str format), Exemple : (-litteral "-3 5 0")
* -windows to specify to the script to run UBSCAT as a solver on windows
* -linux to specify to the script to run picoasta as a solver on linux
