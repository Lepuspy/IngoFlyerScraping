#-*-coding:utf-8-*-
import numbers
#pip install が必要なモジュール
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

"""InagoFlyer Sell & Buy Volume 取得モジュール"""


__author__ = "Lepus <Twitter @lepus_py>"
__version__ = "2.0"
__date__    = "2018/05/25"



options = Options()
#ヘッドレスモード等オプション設定
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')


class InagoFlyer:
		
	def __init__(self):
		#chrome.exe を同じディレクトリへ置くこと
		self.Driver = webdriver.Chrome(chrome_options=options)
		self.Now = 20
		self.BuyVolume = 0
		self.SellVolume = 0	
		self.Merit = None
		self.__Connection()

	def __Connection(self):
		"""
		Action:
			InagoFlyerに接続する
		
		Raises:
			RuntimeError:
				InagoFlyer接続失敗
				サウンドミュート失敗
		"""

		try:
			self.Driver.get("https://inagoflyer.appspot.com/btcmac")
		except:
			raise RuntimeError("Inago Flyer に接続できません")
		#音をミュートに
		try:
			volume=self.Driver.find_element_by_id('sound')
			volume.click()
		except:
			raise RuntimeError("音をミュートに出来ません")

	def AvgChange(self, AvgTime):
		"""
		Action:
			Buy & Sellボリュームの平均秒数変更

		Parameters:
			AvgTime: Number
				floatで指定されても整数に直す

		Raises:
			ValueError:
				AvgTime が 10 ～ 60 の範囲外で設定された
			TypeError:
				AvgTime が 文字で入力された

		"""
		if isinstance(AvgTime, numbers.Number):
			AvgTime = int(AvgTime)
			if self.Now != AvgTime:
				if 10 <= AvgTime <= 60:
					bs_ave = self.Driver.find_element_by_id("measurementTime")
					bs_ave.clear()
					bs_ave.send_keys(AvgTime)
					print("イナゴ平均秒数を変更しました 平均{}秒".format(AvgTime))
					self.Now = AvgTime
				else:
					raise ValueError("現在 平均{}秒\n10-60の間に設定して下さい".format(self.Now))	
		else:
			raise TypeError("AvgTimeは数値で指定して下さい")

	def VolumeGet(self, Threshold=0, Difference=0):
		"""
		Action:
			InagoFlyerのSell & Buy Volume取得
			while True: 等でループ推奨
			約0.88秒毎に更新?
		
		Parameters:
			Threshold: Number
				指定値以下のVolume の場合 Merit を "Volume is Low" とする
			Difference: Number
				Sell Buy Volume の差が指定値以下の場合 "Even" とする
		
		Raises:
			TypeError:
				引数が数値以外で設定された
		"""
		if isinstance(Threshold, numbers.Number) and isinstance(Difference, numbers.Number):
			self.SellVolume = float(self.Driver.find_element_by_id("sellVolumePerMeasurementTime").text)

			self.BuyVolume = float(self.Driver.find_element_by_id("buyVolumePerMeasurementTime").text)

			if self.BuyVolume < Threshold and self.SellVolume < Threshold:
				self.Merit = "Volume is Low"

			elif abs(self.BuyVolume - self.SellVolume) < Difference:
				self.Merit = "Even"

			elif self.BuyVolume > self.SellVolume:
				self.Merit = "Buy"

			elif self.BuyVolume < self.SellVolume:
				self.Merit = "Sell"

			return {"Sell":self.SellVolume,"Buy":self.BuyVolume,"Merit":self.Merit}
		else:
			TypeError("Threshold, Difference は数値で指定して下さい")

if __name__ == '__main__':
	import time
	inago = InagoFlyer()
	while True:
		inago.VolumeGet()
		print(inago.BuyVolume)
		print(inago.SellVolume)
		time.sleep(1)

	