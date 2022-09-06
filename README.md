# Bird Simulator

* `simulator.py` - Simulating the flight of the bird, given a policy or human player.

* `bird.py` - Configures a Bird object.

* `genetic_algorithm.py` - Train Bird to fly as high a possible using Genetic Algorithm.

* `qlearning.py` - Train Bird to fly as high a possible using QLearning Algorithm.

## Install Requirements:
```bash
pip3 install -r requirments.txt
```

## CLI Manual
```
python3 cli.py --help
______ _         _   _____ _
| ___ (_)       | | /  ___(_)
| |_/ /_ _ __ __| | \ `--. _ _ __ ___
| ___ \ | '__/ _` |  `--. \ | '_ ` _ \
| |_/ / | | | (_| | /\__/ / | | | | | |
\____/|_|_|  \__,_| \____/|_|_| |_| |_|

Bird-Sim is a program that simulates a bird flight

usage: cli.py [-h] [--version] [--loglevel LOGLEVEL] {train,play,policy}

positional arguments:
  {train,play,policy}
    train              train the bird
    play               play an interactive game
    policy             show policy

optional arguments:
  -h, --help           show this help message and exit
  --version            show program's version number and exit
  --loglevel LOGLEVEL  set logging level

usage: cli.py train [-h] [--gui] [--save_proc] [--to_visualize [TO_VISUALIZE]] {GA,QL} ...

positional arguments:
  {GA,QL}
    GA                  train using Genetic Algorithm
    QL                  train using QLearning algorithm

optional arguments:
  -h, --help            show this help message and exit
  --gui, -g             activate gui {default=False}
  --save_proc, -o       save process {default=False}
  --to_visualize [TO_VISUALIZE], -v [TO_VISUALIZE]
                        visualize current policy every v iterations {default=10}

usage: cli.py play [-h]

optional arguments:
  -h, --help  show this help message and exit

usage: cli.py policy [-h] <policy file>

positional arguments:
  <policy file>  path to .policy input file

optional arguments:
  -h, --help     show this help message and exit
```

* Saved results of the algorithms can be found under `out` dir