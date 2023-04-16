# Replication Package for Automatic Identification of Self-Admitted Technical Debt from Four Different Sources

##### Authors: Yikun Li, Mohamed Soliman, Paris Avgeriou


## Description of This Study

Technical debt refers to taking shortcuts to achieve short-term goals while sacrificing the long-term maintainability and evolvability of software systems. A large part of technical debt is explicitly reported by the developers themselves; this is commonly referred to as Self-Admitted Technical Debt or SATD. Previous work has focused on identifying SATD from source code comments and issue trackers. However, there are no approaches available for automatically identifying SATD from other sources such as commit messages and pull requests, or by combining multiple sources. Therefore, we propose and evaluate an approach for automated SATD identification that integrates four sources: source code comments, commit messages, pull requests, and issue tracking systems. 
Our findings show that our approach outperforms baseline approaches and achieves an average F1-score of 0.611 when detecting four types of SATD (i.e., code/design debt, requirement debt, documentation debt, and test debt) from the four aforementioned sources. Thereafter, we analyze 23.6M code comments, 1.3M commit messages, 3.7M issue sections, and 1.7M pull request sections to characterize SATD in 103 open-source projects. Furthermore, we investigate the SATD keywords and relations between SATD in different sources. The findings indicate, among others, that: 1) SATD is evenly spread among all sources; 2) issues and pull requests are the two most similar sources regarding the number of shared SATD keywords, followed by commit messages, and then followed by code comments; 3) there are four kinds of relations between SATD items in the different sources.


## Structure of the Replication Package

We have assembled a replication package that includes a **comprehensive SATD dataset**, comprised of 5,000 commit messages and 5,000 pull request sections gathered from 103 Apache open-source projects. Each entry is labeled as either non-SATD or with a specific type of SATD. Additionally, the package contains the **trained SATD detector** model to facilitate further research and analysis.

```
├── LICENSE
├── README.md
├── SATD Detector
│   ├── requirements.txt
│   └── satd_detector.py
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


## Getting Started With SATD Detector

### Requirements

- fasttext
- nltk
- torch


### Identifying SATD

1. Download the model weight and word embedding files from [LINK](https://doi.org/10.5281/zenodo.6783762).
2. Unzip the fasttext_word_embeddings.bin.zip file.
3. Replace the file path with the real path and run the following command:

```bash
python satd_detector.py 
  --embed-vectors "{PATH}/fasttext_issue_300.bin"
  --snapshot "{PATH}/satd_detector.pt"
```


### Example Output

```
Source type: code_comment
Text: TODO: support multiple signers
Predicted result: requirement-debt

Source type: code_comment
Text: TODO: please add some javadoc
Predicted result: documentation-debt

Source type: code_comment
Text: TODO: lack of tests
Predicted result: test-debt

Source type: issue
Text: I would like to remove this as its no longer needed.
Predicted result: code|design-debt

Source type: issue
Text: to make their code more readable. I would like to see something like this in the API.
Predicted result: code|design-debt

Source type: issue
Text: To experiment with transfer learning, we first combine all the issue sections
Predicted result: non-SATD

Source type: issue
Text: We need to update this documentation
Predicted result: documentation-debt

Source type: issue
Text: There are unimplemented requirements
Predicted result: requirement-debt

Source type: issue
Text: This is a good patch
Predicted result: non-SATD

Source type: commit_message
Text: Get rid of some superfluous informational messages
Predicted result: code|design-debt

Source type: commit_message
Text: fix bugs in SystemML - removed XXX
Predicted result: non-SATD

Source type: commit_message
Text: fix typo in error message
Predicted result: documentation-debt

Source type: pull_request
Text: nit: use local variable if possible
Predicted result: code|design-debt

Source type: pull_request
Text: Use the Python Postinstall implementation by default
Predicted result: non-SATD
```


## Paper

Latest version available on [arXiv](https://arxiv.org/abs/2202.02387)

If you use this dataset to support your research and publish a paper, we encourage you to cite the following paper in your publication:

```
@article{li2023automatic,
  author = {Li, Yikun and Soliman, Mohamed and Avgeriou, Paris},
  title = {Automatic identification of self-admitted technical debt from four different sources},
  journal = {Empirical Software Engineering},
  year = 2023,
  month = {Apr},
  day = 15,
  volume = 28,
  number = 65,
  issn = {1573-7616},
  doi = {10.1007/s10664-023-10297-9},
}
```


## Contact

- Please use the following email addresses if you have questions:
    - :email: <yikun.li@rug.nl>
