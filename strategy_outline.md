# Strategy Outline

## Strategy Name
Simple Moving Average Crossover

## Asset
BTC-USD

## Timeframe
1D (daily candles)

## Data Source
Yahoo Finance

## Entry Rules
- Buy when 20-day MA crosses above 50-day MA
- Only enter if no open position

## Exit Rules
- Sell when 20-day MA crosses below 50-day MA

## Risk Management
- Risk 2% of capital per trade
- No leverage

## Backtesting Plan
- Backtest from 2018 to present
- Measure:
    - CAGR
    - Max Drawdown
    - Sharpe Ratio