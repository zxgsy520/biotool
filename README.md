# biotool
Bioinformatics analysis tool

## Requirements
* [Python](https://www.python.org/)
* Three-party python package
  * [pysam](https://pypi.org/project/pysam/)
  * [matplotlib](https://matplotlib.org/)
  * [numpy](https://numpy.org/doc/stable/index.html)
## Installation
```
git clone https://github.com/zxgsy520/biotool.git
cd  biotool/bin
chmod 755 *
```
or
```
wget -c https://github.com/zxgsy520/biotool/archive/refs/heads/main.zip
unzip main.zip

```
## Options and usage
### Predict telomere
```
python find_telomeres.py genome.fasta >telomere.txt
```
