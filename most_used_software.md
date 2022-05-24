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
|GetOrganelle|组装线粒体、叶绿体和ITs|https://github.com/Kinggerm/GetOrganelle|https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02153-6|有的物种组装的可以，有的组装的不好|
|badread|三代数据模拟软件|https://github.com/rrwick/Badread|||
|BMTagger|区分人类基因和微生物序列的软件|https://www.westgrid.ca/support/software/bmtagger|||
|ChewBBACA|核心基因分析软件|https://github.com/B-UMMI/chewBBACA|https://www.microbiologyresearch.org/content/journal/mgen/10.1099/mgen.0.000166||
|dram|宏病毒注释软件|https://github.com/WrightonLabCSU/DRAM|https://academic.oup.com/nar/article/48/16/8883/5884738||
|mob_suite|从细菌草图中获取质粒|https://github.com/phac-nml/mob-suite|https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7660255/||
|proovread|使用二代数据或者基因组数据矫正三代数据|https://github.com/BioInf-Wuerzburg/proovread|https://academic.oup.com/bioinformatics/article/30/21/3004/2422147||
|SortMeRNA|从宏基因组数据中过滤rRNA序列|https://github.com/biocore/sortmerna||
|PGA|叶绿体基因组注释|https://github.com/quxiaojian/PGA|https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6528300/||
|CPGAVAS2|质体注释软件| http://47.96.249.172:16019/analyzer/updateAnno|https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6602467/||
|MitoFinder|动物线粒体组装注释|https://github.com/RemiAllio/MitoFinder|https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7497042/||
