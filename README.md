# YahooNewsScraper
YahooNewsをスクレイピングするスクリプトです

## requirement
 - Python(3.4 > ) 
 - BeautifulSoup
 - regex
 - boto

## what is this
Yahoo JapanのRSSを参考にリアルタイムで変化し続ける、ニュース記事を追いかけます
また、AWSのS3とともに連携できる機能もあり、S3に格納することで、ディスクがオーバーフローするリスクを低減します

## どういった用途に役に立つのか
- Yahooのニュースが影響を及ぼすと仮定できるKPIの予想（株、市場行動、etc）
- 時勢の変化の観測
- ニュース記事の機械学習的・統計的解析

## 実行
ローカルに保存する場合
```sh
$ python3 yahooNewsParserFromRSS.py -c 
```
S3に保存する場合
```sh
$ python3 yahooNewsParserFromRSS.py -c -s3
```
## ファイル構成
このようなディレクトリ構成になっている。
<p align="center">
  <img width="450" src="https://cloud.githubusercontent.com/assets/4949982/25940916/9b22beba-3672-11e7-9061-ab843a39bb3d.png">
</p>
<div align="center">図1. ファイルシステム構成図 </div>

## MITライセンス
どうぞ
