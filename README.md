# Stock Simulator

This project is a Python/Flask application, utilized with Javascript front end, SQL databases and HTML design to create a web-app that can functionally buy and sell stocks. The web-app uses the yfinance libraries to retrieve live, real-time and accurate data about stocks.
I keep track of a user's initial $5,000 balance, and then every transaction (buy/sell) they make with respect to any stock. Utilizing this information such as purchase price, quantity bought and the ticker, I keep track of a user's portfolio.
A user can see their total % increase, as well as % increases for each individual stocks.

The future goals of this project are to implement AI trading strategies to see which one can product the most profit over a period of time and identify trends/analysis. Stay Tuned.This project is a Python/Flask application, utilized with Javascript front end, SQL databases and HTML design to create a web-app that can functionally buy and sell stocks. The web-app uses the yfinance libraries to retrieve live, real-time and accurate data about stocks. I keep track of a user's initial $5,000 balance, and then every transaction (buy/sell) they make with respect to any stock. Utilizing this information such as purchase price, quantity bought and the ticker, I keep track of a user's portfolio. A user can see their total % increase, as well as % increases for each individual stocks. The future goals of this project are to implement AI trading strategies to see which one can product the most profit over a period of time and identify trends/analysis. Stay Tuned.

Skills: Full-Stack Development · Python · Flask · JavaScript · HTML · SQL

## Login Page
Utilizing Flask Login Manager, I am able to host different users, storing each of them and their username, email, encrypted password, profile pic, etc. into the mySQL database. User's can then access their profile page to edit any of this information and update it accordingly.

## Transactions & Stock Info
The user can scroll through a chart accessed from mySQL database including all of the transactions they have ever made in this web app, for any stock.

Addtionally, using Plotly, Javascript and SocketIO, I have accessed the yfinance data to plot the stock history for different time periods, and socketIO allows it to continuously fetch and update the page to ensure the user is always seeing the most accurate data.

## Web-App Home Page
The home page shows the user's name, their profile picture, the amount they have invested in total, what their investments are currently worth, finally with a big highlight on the overall % change in the portfolio
