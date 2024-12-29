# Altmetric-Spider

## 1. Introduction

根据论文DOI爬取对应基本信息和[Altmetrics](https://www.altmetric.com/)指标。

## 2. Environment 

Python=3.8+

## 3. Structure

- `get_paper_info.py`：爬取论文基本信息
  - doi, detail_url, ass

- `get_paper_ass.py`：爬取论文altmetrics信息
  - doi, news, blogs, policy, twitter,  patent, weibo, facebook, wikipedia,  googleplus, reddit, video,  dimensions_citation, mendeley, citeulike


## 4. Usage

1. 整理要爬取的论文doi存入paper_doi.csv
2. 运行`get_paper_info.py`爬取论文基本信息。
3. 运行`get_paper_ass.py`爬取论文altmetrics信息。

## 5. Contact

Created by [OxCsea](https://github.com/OxCsea) - feel free to reach out!

> https://t.me/magic_Cxsea