# README: Web Scraping and Data Analysis with Scrapy

This guide walks you through setting up a virtual environment, creating a Scrapy project, running the web crawler to collect fire incident reports, and analyzing the data. Follow the steps below to get started.

## Table of Contents
1. [Configurations and Installations](#configurations-and-installations)
    1. [Select Interpreter](#select-interpreter)
    2. [Change Directory into Project Folder](#change-directory-into-project-folder)
    3. [Create a Virtual Environment](#create-a-virtual-environment)
    4. [Activate the Virtual Environment](#activate-the-virtual-environment)
    5. [Upgrade pip](#upgrade-pip)
    6. [Install Required Libraries](#install-required-libraries)
2. [Creating a Scrapy Project](#creating-a-scrapy-project)
    1. [Start Scrapy Project](#start-scrapy-project)
3. [Creating the Crawler Class](#creating-the-crawler-class)
    1. [XPath Explanation](#xpath-explanation)
    2. [Create a Spider](#create-a-spider)
4. [Running the Crawler](#running-the-crawler)
    1. [Run Combine](#run-combine)
    2. [Crawl the Webpage](#crawl-the-webpage)
    3. [Perform the Analysis](#perform-the-analysis)
5. [Conclusion](#conclusion)

## 1. Configurations and Installations

### 1.1 Select Interpreter
- Open VS Code.
    - On Windows: Press `Ctrl + Shift + P`
    - On Mac: Press `Cmd + Shift + P`
- Type: `Python: Select Interpreter`
- Choose your preferred interpreter (e.g., Python 3.11.9 64-bit (Microsoft Store)).

### 1.2 Change Directory into Project Folder
Change your directory into the project folder fire_incidents_exercise
```sh
cd 1_fire_incidents_exercise
```

### 1.3 Create a Virtual Environment
Create a virtual environment to manage your project's dependencies.
```sh
python -m venv venv
```

### 1.4 Activate the Virtual Environment
Activate the virtual environment to use the installed packages.

- On Windows:
    ```sh
    .\venv\Scripts\activate
    ```

- On Unix or MacOS:
    ```sh
    source venv/bin/activate
    ```

### 1.5 Upgrade pip
Upgrade pip to the latest version.
```sh
python -m pip install --upgrade pip
```

### 1.6 Install Required Libraries
Install the necessary libraries specified in the `requirements.txt` file.
```sh
pip install -r requirements.txt
```
If you encounter PowerShell permission issues on Windows, use:
```sh
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 2. Creating a Scrapy Project

### 2.1 Start Scrapy Project
Start a new Scrapy project with the name `fire_incidents`.
```sh
scrapy startproject fire_incidents
```
If you encounter PowerShell permission issues on Windows, use:
```sh
.\venv\Scripts\python.exe -m scrapy startproject fire_incidents
```

## 3. Creating the Crawler Class

### 3.1 XPath Explanation
The crawler retrieves information from the website using XPath expressions.

1. Open the Scrapy shell to test XPath on the fly:
    ```sh
    scrapy shell
    ```

2. Fetch the page:
    ```python
    r = scrapy.Request(url="https://fireandemergency.nz/incidents-and-news/incident-reports/")
    fetch(r)
    ```

3. Get the Central region div:
    ```python
    on_central_div = response.xpath("//div[@class='incidentreport__region'][h3[text()='Central']]")
    on_central_div
    ```

4. Get the first list element:
    ```python
    li = on_central_div.xpath(".//ul[@class='incidentreport__region__list']/li/a")[0]
    ```

5. Extract the href from the first list element:
    ```python
    li.xpath("@href").get()
    ```

6. Extract the text from the first list element:
    ```python
    li.xpath("text()").get().strip()
    ```

### 3.2 Create a Spider
Create a spider to crawl the web page.
```sh
cd fire_incidents
scrapy genspider incident_reports fireandemergency.nz/incidents-and-news/incident-reports
```
Check the `robots.txt` of the website to ensure you are allowed to crawl it:
- [https://fireandemergency.nz/robots.txt](https://fireandemergency.nz/robots.txt)

## 4. Running the Crawler

### 4.1 Run Combine
First, execute the `Main_1_ScrapyRunner.py`, followed by `Main_2_AnalyzeData.py`.
```sh
python Main_3_Combine.py
```

### 4.2 Crawl the Webpage
Run the spider to extract data and save it into a CSV file in the `data` folder.
```sh
cd path/to/your/root/directory
python Main_1_ScrapyRunner.py
```

### 4.3 Perform the Analysis
This script retrieves and analyzes the latest `day_of_week_incident_reports` CSV file to answer the following questions:

- How many incidents has the Stratford Brigade responded to in the last 7 days?
- How many medical incidents have been reported in the Central Region in the last 7 days?
- Where were the medical incidents reported in the last 7 days?

Run the analysis script:
```sh
python Main_2_AnalyzeData.py
```

## 5. Conclusion
By following the steps outlined in this README, you will be able to set up your environment, create and run a Scrapy project, and analyze fire incident report data effectively. This guide ensures that new users can easily make use of the provided Scrapy code.