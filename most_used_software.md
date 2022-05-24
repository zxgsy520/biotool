软件安装方法1：conda create --prefix=/Work/pipeline/software/meta/platon/v1.6 -c conda-forge -c bioconda -c defaults platon=1.6 #使用conda安装，prefix指定安装路径，这样可以构建独立的环境。
软件安装方法1：conda env create --prefix=/Work/pipeline/software/meta/MitoFlex/v0.2.9 --file environment.yml

|软件|分类|软件链接|文章链接|说明|
|----|----|----|----|----|
|platon|质粒预测|[https://github.com/oschwengers/platon](https://github.com/oschwengers/platon)|https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7660248/|通过验证，如果是比较新的质粒可能预测不出来，整体上效果还可以|
|sortmerna|从宏转录组数据中过滤 rRNA|https://github.com/biocore/sortmerna|https://pubmed.ncbi.nlm.nih.gov/23071270/||
|AGORA|根据近源物种注释线粒体|https://bigdata.dongguk.edu/gene_project/AGORA/|https://pubmed.ncbi.nlm.nih.gov/29617954/|在线|
|MitoZ|根据近源物种注释动物线粒体|https://github.com/linzhi2013/MitoZ|https://pubmed.ncbi.nlm.nih.gov/30864657/|部分物种效果不理想|
|mitos2|动物线粒体注释|http://mitos2.bioinf.uni-leipzig.de/index.py||注释动物线粒体还可以|
|pLannotate|工程质粒注释软件|http://plannotate.barricklab.org/|https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8262757/|在线|
|MEANGS|动物线粒体组装软件|https://github.com/YanCCscu/meangs|https://pubmed.ncbi.nlm.nih.gov/34941991/|通过测试组装效果很差，组装时间很长，没有我开发的好|
|MitoFlex|动物线粒体组装|https://github.com/Prunoideae/MitoFlex|https://pubmed.ncbi.nlm.nih.gov/33605414/|未测试，底层使用megahit组装，可能适合从宏基因组中组装出线粒体|


