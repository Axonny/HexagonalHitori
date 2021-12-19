# HexagonalHitori

## Solver
```
usage: main.py [-h] [-c COUNT] [-s SUM] filename

positional arguments:
  filename              Path to file

options:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Find n solves. Default is all
  -s SUM, --sum SUM     Limit on the amount per line. Default is no limit
```

## Generator
```
usage: generator.py [-h] [-s SIZE] filename

positional arguments:
  filename              Path to output file

options:
  -h, --help            show this help message and exit
  -s SIZE, --size SIZE  Generate SxS field. size must be in [3, 8]. Default is 3
```