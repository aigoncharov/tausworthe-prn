# tausworthe-prn

Tausworthe pseudo-random number generator.

## System requirements:

- Ubuntu 21.04
- Python 3.9.5
- pip 20.3.4 

## Installation

`pip install -r requirements.txt`

## Running

`python ./main.py`

## Supported commands

### generate

Prints a sequence of Unif(0, 1) pseudo-random numbers.

### test

Generates a sequence of Unif(0, 1) pseudo-random numbers. Runs goodness-of-fit and independence tests. Prints a scatter graph with (U(i), U(i+1)) number pairs. Generates Nor(0, 1) deviates using Box-Muller method. Prints histograms for Z1 and Z2.