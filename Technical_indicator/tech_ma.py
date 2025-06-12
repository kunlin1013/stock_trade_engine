import pandas as pd

def simple_moving_average(close: pd.Series, period: int = 20) -> pd.DataFrame:
    """
    計算簡單移動平均（SMA）

    參數:
        close (pd.Series): 收盤價序列
		period (int): 移動平均期數（預設為20）

    回傳:
        pd.DataFrame: 包含以下欄位的資料表
			- sma: 簡單移動平均線
    """
    sma = close.rolling(window=period).mean()

    return pd.DataFrame({
        'sma': sma
    })
