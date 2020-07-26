# Python import analyzer

> Analyse internal package imports in a given path with `.py` files

### Terminology
* Dependents of x = Modules that import in x
* Dependencies of x = Modules that x imports

### Example

**Columns**
* 'Dependents' (of module m in row x) = number of modules that import in m
* 'Dependencies' (of module m in row x) = number of modules that m imports
* 'Score' = 'Dependents' column minus 'Dependencies' column
* 'Proportion' = 'Dependents' column / ('Dependents' column + 'Dependencies' column) * 100

**What does the numbers mean?**
* A larger score means it is a dependency of other modules more
    * "A dependency of a lot of modules"
* A smaller score means it depends on other modules more
    * "Depends on a lot of modules"
* A high proportion means most connections to other modules are its dependents
* A low proportion means most connections to other modules are its dependencies

Example output for [koneko](https://github.com/twenty5151/koneko), using panda's `to_markdown()` method

|                 |   Dependents |   Dependencies |   Score |   Proportion |
|:----------------|-------------:|---------------:|--------:|-------------:|
| pure.py         |           10 |              0 |      10 |          100 |
| colors.py       |            2 |              0 |       2 |          100 |
| \_\_init\_\_.py |           14 |              0 |      14 |          100 |
| files.py        |            5 |              1 |       4 |           83 |
| printer.py      |            7 |              2 |       5 |           78 |
| utils.py        |            9 |              3 |       6 |           75 |
| config.py       |            5 |              2 |       3 |           71 |
| lscat.py        |            6 |              4 |       2 |           60 |
| api.py          |            3 |              3 |       0 |           50 |
| cli.py          |            2 |              3 |      -1 |           40 |
| prompt.py       |            3 |              5 |      -2 |           38 |
| picker.py       |            3 |              5 |      -2 |           38 |
| data.py         |            1 |              2 |      -1 |           33 |
| screens.py      |            2 |              4 |      -2 |           33 |
| download.py     |            2 |              4 |      -2 |           33 |
| lscat_prompt.py |            1 |              3 |      -2 |           25 |
| assistants.py   |            2 |              7 |      -5 |           22 |
| main.py         |            2 |              7 |      -5 |           22 |
| ui.py           |            2 |             12 |     -10 |           14 |
| lscat_app.py    |            1 |              7 |      -6 |           12 |
| \_\_main\_\_.py |            0 |              5 |      -5 |            0 |


## Installation & usage

1. Clone the repo and cd into it
2. `pip install -r requirements.txt`
3. `python imports.py -p {PATH_TO_FILES} -n {NAME_OF_PACKAGE}`
    * PATH_TO_FILES: the directory where your `.py` files are
    * NAME_OF_PACKAGE: usually the name of the above directory. Only the *internal* imports of your modules are analyzed, see `from {NAME_OF_PACKAGE} import ...`

## Todo

* Support `from . import ...`
* Recursive discovery of files (currently only works on a flat directory structure)

## Details

Roughly equal to the following manual steps:

1. `pyreverse koneko/*.py -o png`
2. Count the type of each arrow in each module box:
    * Dependents = imported by another module (arrow pointing towards box): +1
    * Dependencies = imports another module (arrow pointing away from box): -1
3. Score = sum
5. Proportion = dependents / abs(dependencies + dependents)
