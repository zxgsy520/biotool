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
## Use biotool
```
./biotool -h
usage: biotool [-h] {fq2fa,seqsplit,sort_genome} ...

name:
biotool：Commonly used processing tools for biological information

URL：https://github.com/zxgsy520/biotool

version: 1.1.0
contact:  Xingguo Zhang <invicoun@foxmail.com>        

optional arguments:
  -h, --help            show this help message and exit

command:
  {fq2fa,seqsplit,sort_genome}
    fq2fa               fastq to fasta    #将fastq文件转化为fasta文件
    seqsplit            Split files by a specific size.  #对fasta或者fastq文件按大小进行拆分
    sort_genome         Sort and rename the genome.   #对基因组进行排序，将序列转化为大写，并且根据排序结果重新命名

```

### Predict telomere  #预测端粒
```
python find_telomeres.py genome.fasta >telomere.txt
```
