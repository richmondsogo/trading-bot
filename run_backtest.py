import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

data = pd.read_csv("btc_data_reordered.csv", parse_dates=True, index_col="Date")

split = int(len(data) * 0.8)

backtest_data = data.iloc[:split]
forward_data = data.iloc[split:]


class SMAStrategy(Strategy):
    def init(self):
        self.sma1 = self.I(SMA, self.data.Close, 10)
        self.sma2 = self.I(SMA, self.data.Close, 20)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy()
        elif crossover(self.sma2, self.sma1):
            self.sell()


if __name__ == "__main__":
    bt = Backtest(backtest_data, SMAStrategy, cash=10000, commission=0.0025)
    stats = bt.run()
    print(stats)
    stats.to_csv("backtest_stats.csv")

    bt_forward = Backtest(forward_data, SMAStrategy, cash=10000, commission=0.0025)
    forward_stats = bt_forward.run()
    print(forward_stats)
    forward_stats.to_csv("forward_results.csv")
