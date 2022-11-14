from blankly import CoinbasePro
import datetime

exchange = CoinbasePro()
interface = exchange.get_interface()
ticker = []
volatility = []
duration = 20
epoch_end = datetime.datetime.today().timestamp()
epoch_start = epoch_end - (86400 * duration)

print('From', datetime.datetime.fromtimestamp(epoch_start),
      'to', datetime.datetime.fromtimestamp(epoch_end))

for dataPoint in interface.get_products():
    data = dataPoint['exchange_specific']
    coin = dataPoint['symbol']

    if data['status'] == 'online' and data['trading_disabled'] == False:
        ticker.append(coin)

for symbol in ticker:
    N = 0
    Nperc = 0
    x = 0
    metrics = interface.get_product_history(symbol, epoch_start, epoch_end, resolution='1d')

    # calculate ATR based on viewed duration
    if len(metrics) != 0:
        for j in range(len(metrics)):
            N = N + float(metrics.high[j]) - float(metrics.low[j])

        # convert from scientific notation
        N = str(('%.17f' % (N / len(metrics))).rstrip('0').rstrip('.'))
        for j in range(len(N)):
            if (N[j].__contains__('.') or N[j].__contains__('0')) == False and x == 0:
                x = j + 4
        N = N[0:x].rstrip('0').rstrip('.')
        Nperc = str(round((float(N) / metrics.close[len(metrics)-1]) * 100, 2))

        volatility.append(symbol + ' ' + N + ' ' + Nperc)
print(volatility)
