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
下载之后给执行权限就可以使用（目前支持者linux系统），要在其他系统中使用可以直接运行脚本，但需要安装依赖。
## Options and usage
## Use biotool
```
./biotool -h
usage: biotool [-h] {fq2fa,seqsplit,sort_genome,look_alnfa} ...

name:
biotool：Commonly used processing tools for biological information

URL：https://github.com/zxgsy520/biotool

version: 1.2.3
contact:  Xingguo Zhang <invicoun@foxmail.com>        

optional arguments:
  -h, --help            show this help message and exit

command:
  {fq2fa,seqsplit,sort_genome,look_alnfa}
    stats               simple statistics of FASTA/Q files #对序列进行统计（fasta, fastq, fasta.gz, fastq.gz）
    fq2fa               fastq to fasta #将fastq文件转化为fasta文件
    seqsplit            Split files by a specific size. #对fasta或者fastq文件按大小进行拆分
    sort_genome         Sort and rename the genome. #对基因组进行排序，将序列转化为大写，并且根据排序结果重新命名
    look_alnfa          View multiple sequence alignment files. #将多序列比对后的文件用Excel表示，标记出差异的位置
 
```

### Predict telomere（预测端粒）
```
python find_telomeres.py genome.fasta >telomere.txt  #所有系统
./find_telomeres genome.fasta >telomere.txt  #如果是linux系统
``` 
### Batch close tasks（批量关闭任务）
使用sge的服务器，批量杀死指定任务的插件。
```
qdels -k evm_  #杀死说有“evm_”字符的任务
qdels -k evm*A1 #支持字符串中间的通配符
``` 
