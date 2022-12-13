import yfinance
import pandas_ta  #noqa

TICKER = 'AAPL'  # TODO: replace this with your own ticker
TRAIN_START_DATE = '2017-02-10'  # TODO: replace this with your own start date
TRAIN_END_DATE = '2017-12-31'  # TODO: replace this with your own end date
EVAL_START_DATE = '2018-01-01'  # TODO: replace this with your own end date
EVAL_END_DATE = '2022-12-12'  # TODO: replace this with your own end date

yf_ticker = yfinance.Ticker(ticker=TICKER)

df_training = yf_ticker.history(start=TRAIN_START_DATE, end=TRAIN_END_DATE, interval='60m')
print(df_training.head(5))
df_training.drop(['Dividends', 'Stock Splits'], axis=1, inplace=True)
df_training["Volume"] = df_training["Volume"].astype(int)
df_training.ta.log_return(append=True, length=16)
df_training.ta.rsi(append=True, length=14)
df_training.ta.macd(append=True, fast=12, slow=26)
df_training.to_csv('./tmp/data/training.csv', index=False)

df_evaluation = yf_ticker.history(start=EVAL_START_DATE, end=EVAL_END_DATE, interval='60m')
df_evaluation.drop(['Dividends', 'Stock Splits'], axis=1, inplace=True)
df_evaluation["Volume"] = df_evaluation["Volume"].astype(int)
df_evaluation.ta.log_return(append=True, length=16)
df_evaluation.ta.rsi(append=True, length=14)
df_evaluation.ta.macd(append=True, fast=12, slow=26)
df_evaluation.to_csv('./tmp/data/evaluation.csv', index=False)