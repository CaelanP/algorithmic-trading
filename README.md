# piggy-backer
Pull from a PDF that has been made publicly available for the STOCK act for politicians making transactions over $1000 in stocks and mimic their trades, or a couple of them.
Find the name(s) of those of interest and find what stock they have traded for.
Copy the action that has taken place and send a trade request automatically to an online broker.  
This is the form for proceeding with getting the public information. 
https://ethics.od.nih.gov/oge-form-201  
This one seems better and more direct of a purpose of what is required.
https://efdsearch.senate.gov/search/  
This outlines the purpose of it
https://www.doi.gov/sites/doi.gov/files/migrated/ethics/forms/upload/stock_act_summary_5_22_2017.pdf  

Potential data sets to pull from:  
Stocks  
Finviz provides information for float, short float and short float ratio https://finviz.com/screener.ashx?v=111&ft=4
Options  
Python end of the day options information https://thetadata-api.github.io/PythonAPI/tutorials/  
Seems like websockets or something, pulls data from a site and gets the information in a series of queries https://polygon.io/docs/options/getting-started  
CBOE Historical Options Data has provides a downloadable CSV file of a selected period https://www.cboe.com/us/options/market_statistics/daily/ https://www.cboe.com/us/options/market_statistics/historical_data/  
