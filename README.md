# Amazon Reviews

An aspect based sentiment analysis on Amazon reviews using ASUM and JST models.

## Dataset

The analysis focuses on a subset of Amazon product reviews, specifically in the "Computer Internal Components"
subcategory. You can access the data at https://nijianmo.github.io/amazon/index.html.

> Jianmo Ni, Jiacheng Li, Julian McAuley Empirical Methods in Natural Language Processing (EMNLP), 2019

## Models

The model executables are generated from the following projects:

- [https://yohanjo.github.io/research/WSDM11/index.html](https://yohanjo.github.io/research/WSDM11/index.html)
- [https://github.com/saiteki-kai/JST](https://github.com/saiteki-kai/JST)

> Yohan Jo and Alice Oh, Aspect and Sentiment Unification Model for Online Review Analysis, In Proceedings of the 4th
> ACM International Conference on Web Search and Data Mining (WSDM), 2011

> Lin, C., He, Y., Everson, R. and Reuger, S. Weakly-supervised Joint Sentiment-Topic Detection from Text, IEEE
> Transactions on Knowledge and Data Engineering (TKDE), 2011

The processing only includes English reviews, which are identified using
the [fastText](https://fasttext.cc/docs/en/language-identification.html) model.

> A. Joulin, E. Grave, P. Bojanowski, T. Mikolov, Bag of Tricks for Efficient Text Classification, 2016

## Setup

Create a virtual environment

```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

Install the dependencies

```bash
pip install -r requirements.txt
```

Install the "reviews" package

```bash
pip install -e .
```

Download the dataset consisting of reviews and metadata from the Electronics category in the `./data/raw/` folder.

Run the following scripts to filter the products metadata by the category "Computer Internal Components" and 
then obtain the corresponding subset of reviews

```bash
python scripts/filter-metadata.py
python scripts/filter-reviews.py 
```

Download the project in the root folder and generate the executable for JST

```bash
cd JST/Debug
make
mv jst ../../bin/
```

Download the project in the root folder and generate the executable for ASUM

```bash
cd ASUM/ASUM
jar cf ASUM.jar 
mv ASUM.jar ../../bin/
```

Execute the notebooks to perform the processing and the analysis.

```
./notebooks
    01_clean.ipynb       # Data cleaning
    02_analysis.ipynb    # Exploratory data analysis
    03_processing.ipynb  # Text processing
    04_jst.ipynb         # JST traning and performance
    05_asum.ipynb        # ASUM traning and performance
    06_results.ipynb     # Results and comparison of the models
```

Launch the dashboard
```bash
python dashboard/run.py
```
