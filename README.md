# Replication Package for Automatic Identification of Self-Admitted Technical Debt from Four Different Sources

##### Authors: Yikun Li, Mohamed Soliman, Paris Avgeriou

## Description of this study:

Technical debt refers to taking shortcuts to achieve short-term goals while sacrificing the long-term maintainability and evolvability of software systems. A large part of technical debt is explicitly reported by the developers themselves; this is commonly referred to as Self-Admitted Technical Debt or SATD. Previous work has focused on identifying SATD from source code comments and issue trackers. However, there are no approaches available for automatically identifying SATD from other sources such as commit messages and pull requests, or by combining multiple sources. Therefore, we propose and evaluate an approach for automated SATD identification that integrates four sources: source code comments, commit messages, pull requests, and issue tracking systems. 
Our findings show that our approach outperforms baseline approaches and achieves an average F1-score of 0.611 when detecting four types of SATD (i.e., code/design debt, requirement debt, documentation debt, and test debt) from the four aforementioned sources. Thereafter, we analyze 23.6M code comments, 1.3M commit messages, 3.7M issue sections, and 1.7M pull request sections to characterize SATD in 103 open-source projects. Furthermore, we investigate the SATD keywords and relations between SATD in different sources. The findings indicate, among others, that: 1) SATD is evenly spread among all sources; 2) issues and pull requests are the two most similar sources regarding the number of shared SATD keywords, followed by commit messages, and then followed by code comments; 3) there are four kinds of relations between SATD items in the different sources.


## Structure of the replication package:

We created a SATD dataset containing 5,000 commit messages and 5,000 pull request sections from 103 Apache open-source projects.
Each item is tagged as non-SATD or different types of SATD.

```
├── LICENSE
├── README.md
├── SATD Keyowrds
│   ├── SATD Keyowrds for different types of SATD
│   │   ├── Keywords for code or design debt.txt
│   │   ├── Keywords for documentation debt.txt
│   │   ├── Keywords for requirement debt.txt
│   │   └── Keywords for test debt.txt
│   └── SATD Keywords for different sources
│       ├── Keywords for code comments.txt
│       ├── Keywords for commit messages.txt
│       ├── Keywords for issues.txt
│       └── Keywords for pull requests.txt
├── satd-dataset-code_comments.csv
├── satd-dataset-commit_messages.csv
├── satd-dataset-issues.csv
└── satd-dataset-pull_requests.csv
```


## Paper

Latest version available on [arXiv](https://arxiv.org/abs/2202.02387)

If you publish a paper where this dataset helps your research, we encourage you to cite the following paper in your publication:

```
@misc{https://doi.org/10.48550/arxiv.2202.02387,
  doi = {10.48550/ARXIV.2202.02387},
  url = {https://arxiv.org/abs/2202.02387},
  author = {Li, Yikun and Soliman, Mohamed and Avgeriou, Paris},
  keywords = {Software Engineering (cs.SE), Artificial Intelligence (cs.AI), FOS: Computer and information sciences, FOS: Computer and information sciences},
  title = {Automatic Identification of Self-Admitted Technical Debt from Four Different Sources},
  publisher = {arXiv},
  year = {2022},
  copyright = {arXiv.org perpetual, non-exclusive license}
}
```

## Contact

- Please use the following email addresses if you have questions:
    - :email: <yikun.li@rug.nl>