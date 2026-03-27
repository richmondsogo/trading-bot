import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy


data = pd.read_csv("./data/btc_data_reordered.csv", parse_dates=["Date"], index_col="Date")
data = data.loc["2026-01-01":"2026-03-20"]  # Ensure we have the same date range as the original download

class OpeningRangeBreakout(Strategy):
    def init(self):
        self.opening_range_high = self.data.High.rolling(20).max()
        self.opening_range_low = self.data.Low.rolling(20).min()

    def next(self):
        print(self.data)

# # ── Indicator functions (plain named functions, no lambdas) ───────────────────


# def rolling_max(arr, n):
#     return pd.Series(arr).rolling(n).max().values


# def rolling_min(arr, n):
#     return pd.Series(arr).rolling(n).min().values


# def sma(arr, n):
#     return pd.Series(arr).rolling(n).mean().values


# def atr(high, low, close, n=14):
#     h = pd.Series(high)
#     l = pd.Series(low)
#     c = pd.Series(close)
#     prev_c = c.shift(1)
#     tr = pd.concat([h - l, (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
#     return tr.rolling(n).mean().values


# # ── Strategy ──────────────────────────────────────────────────────────────────


# class OpeningRangeBreakout(Strategy):
#     orb_window = 20
#     atr_period = 14
#     atr_stop_mult = 1.5
#     risk_reward = 2.0
#     risk_pct = 0.01
#     trend_sma_period = 50

#     def init(self):
#         self.orb_high = self.I(
#             rolling_max, self.data.High, self.orb_window, name="ORB High"
#         )
#         self.orb_low = self.I(
#             rolling_min, self.data.Low, self.orb_window, name="ORB Low"
#         )
#         self.trend = self.I(
#             sma, self.data.Close, self.trend_sma_period, name="Trend SMA"
#         )
#         self.atr_vals = self.I(
#             atr,
#             self.data.High,
#             self.data.Low,
#             self.data.Close,
#             self.atr_period,
#             name="ATR",
#         )

#     def next(self):
#         # Need at least 2 bars of indicator history to detect a cross
#         if len(self.data.Close) < 2:
#             return

#         price_now = self.data.Close[-1]
#         price_prev = self.data.Close[-2]
#         orb_hi_now = self.orb_high[-1]
#         orb_hi_prev = self.orb_high[-2]
#         orb_lo_now = self.orb_low[-1]
#         orb_lo_prev = self.orb_low[-2]
#         trend = self.trend[-1]
#         atr_v = self.atr_vals[-1]

#         # Skip until all indicators are warm
#         if any(
#             np.isnan(v)
#             for v in [orb_hi_now, orb_hi_prev, orb_lo_now, orb_lo_prev, trend, atr_v]
#         ):
#             return

#         # Manual crossover: price was BELOW the level last bar, ABOVE this bar
#         crossed_above_high = (price_prev <= orb_hi_prev) and (price_now > orb_hi_now)
#         crossed_below_low = (price_prev >= orb_lo_prev) and (price_now < orb_lo_now)

#         # ── LONG ──────────────────────────────────────────────────────────────
#         if crossed_above_high and price_now > trend:
#             if not self.position.is_long:
#                 stop = price_now - atr_v * self.atr_stop_mult
#                 target = price_now + atr_v * self.atr_stop_mult * self.risk_reward
#                 dist = price_now - stop
#                 if dist > 0:
#                     size = max(1, int((self.equity * self.risk_pct) / dist))
#                     self.buy(size=size, sl=stop, tp=target)

#         # ── SHORT ─────────────────────────────────────────────────────────────
#         elif crossed_below_low and price_now < trend:
#             if not self.position.is_short:
#                 stop = price_now + atr_v * self.atr_stop_mult
#                 target = price_now - atr_v * self.atr_stop_mult * self.risk_reward
#                 dist = stop - price_now
#                 if dist > 0:
#                     size = max(1, int((self.equity * self.risk_pct) / dist))
#                     self.sell(size=size, sl=stop, tp=target)


# # ── Run ───────────────────────────────────────────────────────────────────────

# bt = Backtest(
#     data, OpeningRangeBreakout, cash=10_000, commission=0.0025, exclusive_orders=True
# )
# stats = bt.run()
# print(stats)
# stats.to_csv("backtest_stats.csv")
# bt.plot()


# # ── Optimise (uncomment to run) ───────────────────────────────────────────────
# # opt = bt.optimize(
# #     orb_window       = range(10, 40, 5),
# #     atr_stop_mult    = [1.0, 1.5, 2.0, 2.5],
# #     risk_reward      = [1.5, 2.0, 2.5, 3.0],
# #     trend_sma_period = range(30, 100, 10),
# #     maximize         = "Sharpe Ratio",
# #     constraint       = lambda p: p.risk_reward > p.atr_stop_mult,
# # )
# # print(opt)
