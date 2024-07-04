import pandas as pd
import yfinance as yf
import time

# CSVファイルの読み込み
file_path = r'C:\Users\とも\Desktop\kabuka\jpx_nikkei_index_400_weight_jp.csv'
jpx_nikkei_index400 = pd.read_csv(file_path, encoding='shift_jis')



# コードから小数点を削除し、シンボルリストを作成
jpx_nikkei_index400['コード'] = jpx_nikkei_index400['コード'].astype(str).str.replace('.0', '', regex=False)
jpx_nikkei_index400['コード'] = jpx_nikkei_index400['コード'].apply(lambda x: x.zfill(4))
symbols = jpx_nikkei_index400['コード'].astype(str) + '.T'  # TSEのシンボル形式に合わせて修正

# 株価データの取得関数
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="5y")  # 直近5年間のデータを取得
    return hist

# 条件に基づく銘柄の選定
selected_stocks = []
failed_symbols = []

for symbol in symbols:
    try:
        stock_data = get_stock_data(symbol)
        if stock_data.empty or 'Close' not in stock_data.columns:
            failed_symbols.append(symbol)
            continue

       

        current_price = stock_data['Close'].iloc[-1]
        if 3000 <= current_price <= 8000:  # 株価範囲の条件
            

            # 最高値更新のチェック
            max_price_5y = stock_data['Close'].max()
            if current_price >= max_price_5y:
                print(f"{symbol}: 株価範囲と最高値更新の両方の条件を満たす ({current_price} >= {max_price_5y})")
                selected_stocks.append((symbol, jpx_nikkei_index400[jpx_nikkei_index400['コード'] == symbol.split('.')[0]]['銘柄名'].values[0]))
    except Exception as e:
        print(f"Error retrieving stock data for {symbol}: {e}")
        failed_symbols.append(symbol)
        continue

    time.sleep(2)  # APIのレート制限を避けるためのウェイト

print("\n選定された銘柄:")
for stock in selected_stocks:
    print(f"証券コード: {stock[0]}, 会社名: {stock[1]}")

print("\nデータが取得できなかった銘柄:")
print(failed_symbols)
