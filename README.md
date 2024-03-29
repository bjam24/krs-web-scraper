# KRS Web Scraper
This project is a part of bigger project called **Analysis of data from the National Court Register** implemented by a team of 3 students as a part of the Data Mining course at the AGH UST in 2023/2024.
Every team member had tasks to do. I was responsible for KRS data collection through the use of my programmed web scraper in Selenium.

## Analysis of data from the National Court Register (Krajowa Rada Sądownictwa in Polish)
### What is National Court Register (KRS) ?
**THIS SECTION IS UNDER CONSTRUCTION BECAUSE DESCRIBED PROJECT HAS NOT BEEN FINISHED YET**

<p align="center">
<img src="images/graph_org_rep_con.jpg" width="600"/>
</p>

## How does it work
1. Web scraper opens Rejestr.io | Wyszukiwarka danych z KRS website.
2. Because the complete list of valid KRS numbers is unknown to me, web scraper checks every single number from given interval by pasting it into the search bar on the website.

<p align="center">
<img src="images/krs_search.jpg" width="600"/>
</p>

3. Web scraper omits unused KRS numbers or KRS numbers of companies that no longer exist (removed website of a company). When program encounters website of existing company it scrapes company name and full names
   of board memebers.

<p align="center">
<img src="images/krs_example_representatives.jpg" width="600"/>
</p>

4. More of encountered profiles have their personal websites where person's connections with other organizations are visible. However sometimes such website do not exist. Particulay in situation when board member is
   not Polish citizen. Please remember this is not the rule. Web scraper handles missing websites and continues scraping useful information from available profiles.

<p align="center">
<img src="images/krs_example_connections.jpg" width="600"/>
</p>

5. Every profile has own website. On such website are visible all person's connections with organizations. Web scraper scrapes this data. Moreover it is able to scrape current organization name instead of old name of
   organziation. Some data is not visible for average human. There are information hideen in web site details such as KRS numbers of connected organizations from a list.

6. How data can be stored and what is chosen format? Well the purpose of **Analysis of data from the National Court Register** project is visualization of different personal connections among companies.
   Therefore scraped data must be stored in particular order. Below is proposed order of columns and data distribution in CSV file. Mentioned file is created and saved in the same folder in which web scraper is located.

## How to use web scraper
**THIS SECTION IS UNDER CONSTRUCTION**
## Future work
**THIS SECTION IS UNDER CONSTRUCTION**
## Data Source
- Rejestr.io | Wyszukiwarka danych z KRS https://rejestr.io/krs/

## Technology stack
- Python

- Selenium
