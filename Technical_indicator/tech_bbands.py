import pandas as pd
import yfinance as yf

def bbands(close: pd.Series, period: int = 20, times: float = 2.0) -> pd.DataFrame:
    """
    計算布林通道及相關指標

    參數:
        close (pd.Series): 收盤價序列
        period (int): 移動平均期數（通常為20）
        times (float): 標準差倍數（通常為2）

    回傳:
        pd.DataFrame: 包含以下欄位的布林通道指標資料表
            - bb_middle: 中軌線（middle band）：即移動平均線
            - bb_upper: 上軌線（upper band）：中軌 + N 倍標準差
            - bb_lower: 下軌線（lower band）：中軌 − N 倍標準差
            - bb_break_upper: 是否突破上軌，布林突破訊號（1表示突破，0表示未突破）
            - bb_break_lower: 是否跌破下軌，可能代表過度悲觀訊號（1表示跌破，0表示未跌破）
            - bb_bandwidth: 布林帶寬，衡量市場波動度，帶寬越大波動越劇烈
            - bb_percent_b: %b指標 = (收盤價 − 下軌) / (上軌 − 下軌)，判斷收盤價相對於布林帶的位置
    """

    # 計算中軌與標準差
    bb_middle = close.rolling(window=period, min_periods=period).mean()
    bb_std = close.rolling(window=period, min_periods=period).std()

    # 計算上軌與下軌
    bb_upper = bb_middle + times * bb_std
    bb_lower = bb_middle - times * bb_std

    # 判斷是否突破上軌 / 跌破下軌
    bb_break_upper = (close > bb_upper).astype(int)
    bb_break_lower = (close < bb_lower).astype(int)

    # 布林帶寬：衡量波動程度
    bb_bandwidth = (bb_upper - bb_lower) / bb_middle

    # %b指標：收盤價在布林帶中的位置比例
    bb_percent_b = (close - bb_lower) / (bb_upper - bb_lower)

    return pd.DataFrame({
        'bb_middle': bb_middle,             # 中軌（移動平均）
        'bb_upper': bb_upper,               # 上軌（中軌 + N倍標準差）
        'bb_lower': bb_lower,               # 下軌（中軌 - N倍標準差）
        'bb_break_upper': bb_break_upper,   # 是否突破上軌（1 or 0）
        'bb_break_lower': bb_break_lower,   # 是否跌破下軌（1 or 0）
        'bb_bandwidth': bb_bandwidth,       # 布林帶寬（反映波動性）
        'bb_percent_b': bb_percent_b        # %b值（相對位置）
    })


if __name__ == '__main__':
	stock = yf.Ticker("2330.TW")
	df = stock.history(start="2017-01-01", end="2021-02-02")

	# 計算布林通道指標
	bb_df = bbands(df['Close'])

	# 合併原始股價資料與布林指標
	df_combined = pd.concat([df, bb_df], axis=1)

	print(df_combined.tail())