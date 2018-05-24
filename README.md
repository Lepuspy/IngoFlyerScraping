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

while True:
  inago.VolumeGet()
  print(inago.BuyVolume)
  print(inago.SellVolume)
  time.sleep(1)
```
