import pandas as pd
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG


class DummyStrategy(Strategy):
    def init(self):
        pass

    def next(self):
        pass


if __name__ == "__main__":
    bt = Backtest(GOOG, DummyStrategy, cash=10000, commission=0.0025)

    stats = bt.run()
    print(stats)
    stats.to_csv("backtest_stats.csv")
