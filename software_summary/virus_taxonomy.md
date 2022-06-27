软件安装方法1：conda create --prefix=/Work/pipeline/software/meta/platon/v1.6 -c conda-forge -c bioconda -c defaults platon=1.6 #使用conda安装，prefix指定安装路径，这样可以构建独立的环境。

软件安装方法1：conda env create --prefix=/Work/pipeline/software/meta/MitoFlex/v0.2.9 --file environment.yml

|软件|分类|软件链接|文章链接|说明|
|----|----|----|----|----|
|PhaGCN|病毒快速分类|[https://github.com/KennthShang/PhaGCN2.0](https://github.com/KennthShang/PhaGCN2.0)|https://www.researchsquare.com/article/rs-1658089/v1|软件不能多线程，且只能在安装路径下运行，注释不到种属|
|vpf-tools|病毒分类注释|[https://github.com/biocom-uib/vpf-tools](https://github.com/biocom-uib/vpf-tools)|https://pubmed.ncbi.nlm.nih.gov/33471063/||
