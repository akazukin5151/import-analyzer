# Python import analyzer

Analyse imports in a given path with `.py` files

**Terminology**
* Dependents of x = Modules that import in x
* Dependencies of x = Modules that x imports

Roughly equal to the following manual steps:

1. `pyreverse koneko/*.py -o png`
2. Count the type of each arrow in each module box:
    * Dependents = imported by another module (arrow pointing towards box): +1
    * Dependencies = imports another module (arrow pointing away from box): -1
3. Score = sum
5. Proportion = dependents / abs(dependencies + dependents)

* Larger score means it is a dependency of other modules more
    * "A dependency of a lot of modules"
* Smaller score means it depends on other modules more
    * "Depends on a lot of modules"
* High proportion means most connections to other modules are its dependents
* Low proportion means most connections to other modules are its dependencies

# Example

Example output in stdout for [koneko](https://github.com/twenty5151/koneko), using panda's `to_markdown()` method:

|                 |   Dependents |   Dependencies |   Score |   Proportion |
|:----------------|-------------:|---------------:|--------:|-------------:|
| pure.py         |           10 |              0 |      10 |          100 |
| colors.py       |            2 |              0 |       2 |          100 |
| __init__.py     |           14 |              0 |      14 |          100 |
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
| __main__.py     |            0 |              5 |      -5 |            0 |
