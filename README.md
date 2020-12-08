# Stock Market Infromation System with Anlysis
Running server.py with Python3 in SSH
Visit [The website](http://34.75.51.10:8111)

# Introduction
The idea of this project is to make a stock data and information vending system.
The system connects between the investors and the stock market data and information.
In this system, the investors will have broad access to various stock datasets, including its historical trading data, its fundamental data released by financial reports,
and its profile information about the company’s background. The investor will also have a glance at the major exectuves and their information.
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
