from blankly import Alpaca
import csv

a = Alpaca()
interface = a.interface
active_assets = interface.get_products()
stockTicker = []
cryptoTicker = []
arrays = [stockTicker, cryptoTicker]


def contains_number(row):
    for i in range(len(row)):
        if row[i].isdigit() or row.lower().__contains__("delisted"):
            return True


def update_tickers(filename):
    for asset in active_assets:
        if asset['exchange_specific']['class'] == 'us_equity':
            stockTicker.append(asset['symbol'])
        if asset['exchange_specific']['class'] == 'crypto':
            cryptoTicker.append(asset['symbol'])
    for array in arrays:
        array.sort(key=str.upper)

    for file in filename:
        ticker_array = arrays[filename.index(file)]
        with open(file, 'w', newline='') as csvfile:
            datawriter = csv.DictWriter(csvfile, fieldnames=['Ticker'])
            datawriter.writeheader()
            for line in ticker_array:
                if not contains_number(line):
                    datawriter.writerow({'Ticker': line})


# https://www.tradingview.com/widget/, https://www.tradingview.com/widget/advanced-chart/
# https://developer.interactsoftware.com/docs/embedding-tradingview-widgets
def update_html(ticker_list):
    with open("stockViewer.html", 'w', newline='') as textfile:
        textfile.write('<!DOCTYPE html>\n'
                       '<html lang="en">\n'
                       '<head>\n'
                       '  <meta charset="UTF-8">\n'
                       '  <title>Potential Trades</title>\n'
                       '</head>\n'
                       '<body>\n')
        for ticker in ticker_list:
            textfile.write('<div class="tradingview-widget-container">\n'
                           f'  <div id="{ticker_list.index(ticker)}" style="width: 100%;height: 500px;"></div>"\n'
                           '  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>\n'
                           '  <script type="text/javascript">\n'
                           '  new TradingView.widget(\n'
                           '  {\n'
                           '  "autosize": true,\n'
                           f'  "symbol": "{ticker}",\n'
                           '  "range": "3M",\n'
                           '  "timezone": "Etc/UTC",\n'
                           '  "theme": "dark",\n'
                           '  "style": "1",\n'
                           '  "locale": "en",\n'
                           '  "toolbar_bg": "#f1f3f6",\n'
                           '  "hide_top_toolbar": false,\n'
                           '  "enable_publishing": false,\n'
                           '  "allow_symbol_change": true,\n'
                           '  "save_image": false,\n'
                           f'  "container_id": "{ticker_list.index(ticker)}"\n'
                           '  }\n'
                           '  );\n'
                           '</script>\n'
                           '</div>')
        textfile.write('</body>\n'
                       '<div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/"'
                       'rel="noopener" target="_blank"><span class="blue-text">Charting</span></a> by '
                       'TradingView</div>\n'
                       '</html>')
