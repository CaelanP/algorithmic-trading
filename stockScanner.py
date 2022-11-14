from blankly import Alpaca
import csv, datetime, getTickers

exchange = Alpaca()
interface = exchange.get_interface()
filenames = ['stockTickers.csv', 'stockBlacklist.csv']
tickers = []
blacklist = []
variables = [tickers, blacklist]
tickerLow = []
tickerHigh = []
duration = 21
epoch_end = datetime.datetime.today().timestamp() - (86400 / 24)
epoch_start = epoch_end - (86400 * duration)


# update tickers with class us_equity
getTickers.update_tickers(filenames)


def csv_reader(filename, lists):
    # for each item in the amount of things in filename
    for i in range(len(filename)):
        with open(filename[i], 'r') as csvfile:
            datareader = csv.reader(csvfile)
            for row in datareader:
                if row[0] == 'Ticker':
                    continue
                lists[i].append(row[0])


csv_reader(filenames, variables)

print('From', datetime.datetime.fromtimestamp(epoch_start),
      'to', datetime.datetime.fromtimestamp(epoch_end), "\n", len(tickers), "stocks")

for ticker in tickers:
    prevClose = 0
    N = 0
    percN = 0
    highCount = 0
    lowCount = 0
    higherThan = 0
    lowerThan = 0

    # get stock information
    if not 'stockBlacklist.csv'.__contains__(ticker):
        metrics = interface.get_product_history(ticker, epoch_start, epoch_end, resolution='1d')
    # with open('metrics.csv', 'w', newline='') as csvmetrics:
    mhigh = metrics.high
    mopen = metrics.open
    mclose = metrics.close
    mlow = metrics.low
    mvolume = metrics.volume
    mtime = metrics.time

    if len(metrics) == 0:
        blacklist.append(ticker)
        continue

    avgVolume = round(sum(mvolume) / len(metrics), 0)
    if avgVolume < 500000:
        blacklist.append(ticker)
        continue

    # calculate ATR, new high/low, check for ii, oi, ioi
    print(), print(ticker.upper(), mclose[len(metrics) - 1])

    # check for new high/low
    if max(mhigh) == mhigh[len(metrics) - 1]:
        print('New high in the past', len(metrics), 'days')
    if min(mlow) == mlow[len(metrics) - 1]:
        print('New low in the past', len(metrics), 'days')

    # iterate through all data for a given time frame for a single ticker
    for j in range(len(metrics)):
        # Check for consecutive day high or low
        if (mclose[j] < prevClose) and (j < len(metrics)):
            lowCount += 1
        elif (mclose[j] > prevClose) and (j < len(metrics) and prevClose != 0):
            highCount += 1
        else:
            if lowCount == len(metrics):
                tickerLow.append(ticker)
            elif highCount == len(metrics):
                tickerHigh.append(ticker)
        prevClose = mclose[j]

        # determine bear/bull bar
        if mhigh[j] >= mclose[j] > mopen[j]:  # bull bar
            print("Bull bar", datetime.datetime.fromtimestamp(mtime[j]))

            # if (0.8 > ((high[j] - close[j]) / (open[j] - low[j])) < 1.2 and (
            #        (close[j] - open[j]) / (high[j] - low[j])) < 0.33) or (
            #        high[j] - close[j] == 0 and open[j] - low[j] != 0):
            #    print("Bull doji on", datetime.datetime.fromtimestamp(time[j]))
        if mlow[j] <= mclose[j] < mopen[j]:  # bear bar
            print("Bear bar", datetime.datetime.fromtimestamp(mtime[j]))

            # if 0.8 > ((high[j] - open[j]) / (close[j] - low[j])) < 1.2 and (
            #        (open[j] - close[j]) / (high[j] - low[j])) < 0.33:
            #    print("Bear doji on", datetime.datetime.fromtimestamp(time[j]))

        # check how many bars the high/low shadows
        if mclose[j] < mclose[len(metrics) - 1]:
            # higherThan is number of days the current bar is higher than
            higherThan += 1
        if mclose[j] > mclose[len(metrics) - 1]:
            # lowerThan is number of days the current bar is lower than
            lowerThan += 1

        # stock/volume volatility and percent volatility
        N = N + float(mhigh[j]) - float(mlow[j])

    N = round(N / len(metrics), 3)
    percN = round(N / mclose[len(metrics) - 1] * 100, 2)

    print("Volatility $", N, "%",  percN)
    print("Average Volume", avgVolume, higherThan, highCount, lowCount)
    # print("Stock: ", ticker[i], "\n", "Lower: ", lowCount, low, "\n",
    # "Higher: ", highCount, high, "\n", "Volatility: ", N, hlDiff)
# implement a plotter, matplitlib

for ticker in blacklist:
    with open('blacklist.csv', 'w', newline='') as csvfile:
        datawriter = csv.writer(csvfile)
        for t in datawriter:
            row = t
            datawriter.writerow([row])
