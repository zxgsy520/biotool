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

version: 1.2.4
contact:  Xingguo Zhang <invicoun@foxmail.com>        

optional arguments:
  -h, --help            show this help message and exit

command:
  {fq2fa,seqsplit,sort_genome,look_alnfa}
    stats               simple statistics of FASTA/Q files #对序列进行统计（fasta, fastq, fasta.gz, fastq.gz）。
    stat_ngs            Statistics of NGS sequencing data #统计二代测试数据。
    fq2fa               fastq to fasta #将fastq文件转化为fasta文件。
    fa2fq               fasta to fastq #将fasta文件转化为fastq文件(质量值是假的，为了方便一些软件只支持fastq格式输入)。
    sort_genome         Sort and rename the genome.  #对基因组进行排序，将序列转化为大写，并且根据排序结果重新命名。
    rmdupid             Modify duplicate sequence id. #修改有重复id的序列名称。
    rename_fq           Rename the ID of the fatsq file. #删除指定序列。
    filter_seq          Filter sequence files based on length #根据长度过滤序列。
    find_telomere       Genome telomere prediction. #对基因进行端粒预测。
    seqsplit            Split files by a specific size. #对fasta或者fastq文件按大小进行拆分。
    merge_seq           Merge sequences. #合并多个序列，修改序列名字防止有重复的名字。
    greps               Extract specific lines of files based on keywords. #提供一个关键词的列表，通过关键词提取文件对应的行。
    cat                 Combine compressed and uncompressed files and strip empty lines. #合并普通文件和压缩文件，并将里面的空行去掉。
    makemd5             Generate MD5 values for files in the folder one by one. #对文件生产MD5验证码（如果是文件夹，就对文件夹里面的每一个文件都生产MD5验证码）。
    qdels               Kill tasks delivered by qsub based on keywords.  #根据关键词批量杀死qsub投的任务。
    look_alnfa          View multiple sequence alignment files. #将多序列比对后的文件用Excel表示，标记出差异的位置。
    copys_file          Copy a file to multiple paths. #批量修改文件前缀名称。
```

### Predict telomere（预测端粒）
```
./biotool.pyc find_telomere genome.fasta >telomere.txt  #所有系统
././biotool find_telomere genome.fasta >telomere.txt  #如果是linux系统
``` 
### Batch close tasks（批量关闭任务）
使用sge的服务器，批量杀死指定任务的插件。
```
biotool qdels -k evm_  #杀死说有“evm_”字符的任务
biotool qdels -k evm*A1 #支持字符串中间的通配符
``` 
