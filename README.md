# Bentley Ottman Algorithm

*First year Java project at Ensimag - Grenoble INP - 2016*

![100_lines](https://i.imgur.com/eXdf4dr.png)

Implementation of the [Bentley-Ottman algorithm](https://en.wikipedia.org/wiki/Bentley–Ottmann_algorithm).
> The Bentley–Ottmann algorithm is a sweep line algorithm for listing all crossings in a set of line segments.

## Usage

```sh
./bo.py -h
usage: bo.py [-h] [-s] [-t] [-l] filepaths [filepaths ...]

List all crossings in a set of line segments using the Bentley–Ottmann algorithm.

positional arguments:
  filepaths   filepaths of the .bo files to analyse

optional arguments:
  -h, --help  show this help message and exit
  -s          save the results as svg in ./outputs
  -t          tycat the results
  -l          add results to a log.csv file
```

## Use example

```sh
./bo.py -s -l ./tests/simple.bo

    Running Bentley Ottmann on simple ...

    [=========================] 100%

    Unique intersections          :   1
    Crossings within segments     :   2
    Runtime for Bentley Ottmann   :   0m 0.0008020401000976562s


    Running naive algorithm on simple ...

    [=========================] 100%


    Runtime for naive algorithm   :   0m 9.799003601074219e-05s

```

### Performance

Comparison with a naive algorithm (see `naive.py`) on 200 random lines:

![200_lines_with_crossings](https://i.imgur.com/kxirU2w.png)
