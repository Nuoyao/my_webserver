
The database used in Part3 is the same as that in Part2.  
Team member: Nuoyao Yang (ny2033)
Account: ny2303  
Key: 9414  
URL: http://34.75.51.10:8111  
The parts in Part1 are all implemented except that the ticker data (ask and bid) as an attribute of the stock are deleted and replaced by market cap attribute beacause I can not get free access to the real-time ticker data in the real world.  
New features: Add the Key Executives for the investors for reference. Add the analysis toolkit with some interesting queries used in this part.   
Two of the web pages that require the most interesting database operations:  
1. analysis web page in this project 
I corporated the information from the company profiles, fundamental data available from company's financial reports, and the secondary-market trading data to reproduce the indicators that are meaningful for the real-world investors. One the two queries drag data from stock and fundamental entities to compute the sum of the market caps of all the stocks with positive revunue and profit in each sector with more than one stock in our databse. Another one utilized real-world trading data to compute maximum daily percentage increment of the each stock and its correlating trading day in a specific time reange. 
2. Google Map developed by Google
in terms of what the pages are used for,
Google map depicts the map for the user with each location spot connecting to more areas of data sets. For example, when the user selects a restaurant in Google Map, the website pulls the specific pjhone number, address, sector of this business, etc. (attributes) from the datavase. Furthermore, it also depicts the correlatd comments for this restuarants, which consist of text comment, star tatings, and the time stamp of each visit. In addition, Google Map also returns the similar businesses around the restarurant you select, which group the entities in the restuarant sector and implement recommendation system to rank the results. I believe it's innovative and interesting because it's useful for our life and meaningful in terms of the business. 

# Stock Market Infromation System with Anlysis
Running server.py with Python3 in SSH
Visit [The website](http://34.75.51.10:8111)

# Introduction
The idea of this project is to make a stock data and information vending system.
The system connects between the investors and the stock market data and information.
In this system, the investors will have broad access to various stock datasets, 
including its historical trading data, its fundamental data released by financial reports,
and its profile information about the company’s background. 
The investor will also have a glance at the major exectuves and their information.
With this system, the investor will have an understanding of the enterprise’s market prospect to assist his or her investment decision.

Data Source: Yahoo Finance, Bloomberg

# Functions 
Click "Go to the analysis toolkit!" to check analysis results. 
You will find that 2 processing results are displayed.

ANALYSIS 1. For each stock sector with more than one stock, we compute the sum of market cap of all the stocks with positive revunue and profit in this sector, and also their average profit margin.  
ANALYSIS 2. Return the maximum daily percentage increment of the each stock, and this day, in last October.   
Click the Profile ID,	Historical Data, and Fundamental Information to check the related information of each stock. 

# Software
Python 3.8.1
sqlalchemy
flask
