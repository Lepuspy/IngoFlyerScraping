# IngoFlyerScraping
InagoFlyerのSELL &amp; BUY Volumeを取得してくるコードです

WINDOWでのみ動作確認


必要なもの:
------------------------
https://sites.google.com/a/chromium.org/chromedriver/home



使い方:
-----------------------
chromedriver.exeをダウンロードしてきて同ディレクトリに置く  
適当にpip install　する

```python
import inago
import time

inago = inago.InagoFlyer()

for vol in inago.VolumeGet():
		print(vol)
    # >>>> {"Sell":54.2, "Buy": 150.1, "Merit": "Buy"}
		time.sleep(1)
```
