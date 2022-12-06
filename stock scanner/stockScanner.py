from os import getcwd
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
duration = 20
period = 365
epoch_end = datetime.datetime.today().timestamp() - (86400 / 24)
epoch_start = epoch_end - (86400 * period)
cwd = getcwd() + "\Logs"

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

with open(f'{cwd}\{datetime.date.today()}.txt', 'w', newline='') as logfile:
    datawriter = csv.writer(logfile)
    datawriter.writerow(['ticker,recent,change,atr$,atr%,volume,mean,devmean'])
    for ticker in tickers:
        prevClose = 0
        N = 0
        percN = 0
        highCount = 0
        lowCount = 0
        higherThan = 0
        lowerThan = 0
        bullbar = 0
        bearbar = 0
        percatr = 0
        devMean = 0
        h20 = False
        h50 = False
        l20 = False
        l50 = False

        # get stock information
        if not 'stockBlacklist.csv'.__contains__(ticker):
            metrics = interface.get_product_history(ticker, epoch_start, epoch_end, resolution='1d')
        # with open('metrics.csv', 'w', newline='') as csvmetrics:

        if duration >= len(metrics) <= 50 or len(metrics) == 0:
            blacklist.append(ticker)
            continue

        metriclen = len(metrics) - 1
        mhigh = metrics.high
        mopen = metrics.open
        mclose = metrics.close
        mlow = metrics.low
        mvolume = metrics.volume
        mtime = metrics.time
        avgVolume = round(sum(mvolume) / len(metrics), 0)
        meanClose = sum(mclose) / metriclen

        if avgVolume < 500000:
            blacklist.append(ticker)
            continue

        # calculate ATR, new high/low, check for ii, oi, ioi
        atr = round((sum(mhigh) - sum(mlow)) / len(metrics), 2)
        percatr = round(atr / mclose[metriclen] * 100, 2)

        # check for new high/low
        if max(mhigh[(metriclen - 20): len(metrics)]) == mhigh[metriclen]:
            # print('Higher than the past', duration, 'days')
            h20 = True
        if max(mhigh[(metriclen - 50): len(metrics)]) == mhigh[metriclen]:
            # print('Higher than the past', 50, 'days')
            h50 = True
        if min(mlow[(metriclen - 20): len(metrics)]) == mlow[metriclen]:
            # print('Lower than the past', duration, 'days')
            l20 = True
        if min(mlow[(metriclen - 50): len(metrics)]) == mlow[metriclen]:
            # print('Lower than the past', 50, 'days')
            l50 = True

        # iterate through all data for a given time frame for a single ticker
        for j in range(len(metrics)):
            # Calculate deviation from meanClose
            devMean = devMean + ((meanClose - mclose[j]) * (meanClose - mclose[j]))

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
            # check how many bars the high/low shadows
            if mclose[j] < mclose[metriclen]:
                # higherThan is number of days the current bar is higher than
                higherThan += 1
            if mclose[j] > mclose[metriclen]:
                # lowerThan is number of days the current bar is lower than
                lowerThan += 1

            # determine bear/bull bar
            if mclose[j] > mopen[j] and mhigh[j] - mlow[j] / mclose[j] - mopen[j] >= 0.5:  # bull bar
                # print("Bull bar", datetime.datetime.fromtimestamp(mtime[j]))
                bullbar += 1
            if mclose[j] < mopen[j] and mhigh[j] - mlow[j] / mopen[j] - mclose[j] >= 0.5:  # bear bar
                # print("Bear bar", datetime.datetime.fromtimestamp(mtime[j]))
                bearbar += 1
        devMean = round(devMean / metriclen, 2)
        logText = f'{ticker.upper()} ${mclose[metriclen]} {round(mclose[metriclen] - mclose[metriclen - 1], 2)} ${atr} {percatr}% {avgVolume} {h20} {h50} {l20} {l50}'
        datawriter.writerow([ticker.upper(), mclose[metriclen], round(mclose[metriclen] - mclose[metriclen - 1], 2), atr, percatr, avgVolume, h20, h50, l20, l50, devMean, (devMean - mclose[metriclen])])

with open(filenames[1], 'w', newline='') as csvfile:
    datawriter = csv.DictWriter(csvfile, fieldnames=['Ticker'])
    datawriter.writeheader()
    for ticker in blacklist:
        datawriter.writerow({'Ticker': ticker})
