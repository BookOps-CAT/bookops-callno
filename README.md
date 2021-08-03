[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# bookops-callno

Python library for creation of BPL and NYPl branch call numbers based on bibliographic and order data.

Requires Python 3.8 and up. 

## Version
> 0.1.0

## Installation
Install via pip:
```bash
python -m pip install git+https://github.com/BookOps-CAT/bookops-callno
```

## Work notes
### Stage 1
+ Support for e-resouce call number creation for both systems
+ BPL & NYPL call numbers constructed for given call# pattern: pic, fic, dewey, dewey + subject, biography (print material only)
### Stage 2
+ Validation of given call# pattern
+ "auto" for given call# pattern (best choice)
+ Expand to visual materials
### Stage 3
+ Expand to other non-print material types (readalongs, audio, etc.)