# algorithmic trading
Pull from a PDF that has been made publicly available for the STOCK act for politicians making transactions over $1000 in stocks and mimic their trades, or a couple of them.
Find the name(s) of those of interest and find what stock they have traded for.
Copy the action that has taken place and send a trade request automatically to an online broker.  

Potential data sets to get public information regarding politicians:  
This is the form for proceeding with getting the public information. 
https://ethics.od.nih.gov/oge-form-201  
This one seems better and more direct of a purpose of what is required.
https://efdsearch.senate.gov/search/  
This outlines the purpose of it
https://www.doi.gov/sites/doi.gov/files/migrated/ethics/forms/upload/stock_act_summary_5_22_2017.pdf  

Potential data sets to pull stock/options from:  
Regarding both stocks and options, with Interactive Brokers it seems it can be setup to pull information from them, and I have access to read options contracts as well as permissions to trade stocks, need to update this link with something more informative but this is a rough idea https://www.interactivebrokers.com/en/?f=%2Fen%2Fsoftware%2Fhighlights%2FapiHighlights.php  
Can similarly get access to stocks and options through RBC's portal  
SEC open/available datasets/information https://www.sec.gov/data  
FINRA api documentation for getting information on equity (short interest and general information on shorting), fixed income, FIRNA content, firms, registration https://developer.finra.org/docs#query_api https://developer.finra.org/catalog#query-api and more in-depth information/resources for information https://www.finra.org/finra-data  
Stocks  
Finviz provides information for float, short float and short float ratio https://finviz.com/screener.ashx?v=111&ft=4 not sure what you wanted me to look at but this provides a good list of stocks being heavily shorted https://finviz.com/screener.ashx?v=152&f=sh_avgvol_o500,sh_relvol_o1.5,sh_short_o10&ft=4&o=-shortinterestshare  
Alpaca 200 api calls per minute https://alpaca.markets/docs/  
Interactive Brokers API: 50 api calls per second https://interactivebrokers.github.io/tws-api/index.html https://ibkr.info/article/1765  
Blankly https://docs.blankly.finance/  
Options  
Fees per contract(potentially proprietary): https://ibkr.info/article/1184  
Python end of the day options information https://thetadata-api.github.io/PythonAPI/tutorials/  
Seems like websockets or something, pulls data from a site and gets the information in a series of queries https://polygon.io/docs/options/getting-started  
CBOE Historical Options Data has provides a downloadable CSV file of a selected period https://www.cboe.com/us/options/market_statistics/daily/ https://www.cboe.com/us/options/market_statistics/historical_data/ https://www.cboe.com/us/options/market_data_services/  
ORATS is expensive but does a lot and provides some information for a single cost(?) https://www.orats.com/data-api/ https://www.orats.com/historical-quotes/
Historical option data is very expensive but seems in-depth, also provides example data to backtest on https://historicaloptiondata.com/  
A website that outlines how to calculate greeks for options, as well as has explanations ofr the roles each one servers https://www.macroption.com/option-greeks/  
Opening up an account lets us pull from this api for free https://documentation.tradier.com/brokerage-api  
I've seen stuff on referencing scrapping data from yahoo finance or using yfinance in python https://finance.yahoo.com/quote/AAPL/options?p=AAPL&straddle=false provides free information for options  
Someones free sql database they have exported option information to https://www.dolthub.com/repositories/post-no-preference/options/data/master/option_chain  
Interactive Brokers API: 50 api calls per second https://interactivebrokers.github.io/tws-api/index.html https://ibkr.info/article/1765  
