# epaper_clock

## 概要
Raspberry Pi Pico WH（ピンヘッダ付き）＋WaveShare 3.7inch e-Paperディスプレイでアナログ時計を作成します。
NTPで正確な時刻を取得し、時計表示に反映します。

## 構成ファイル
- main.py：時計のメインプログラム
- epaper.py：ePaper制御用モジュール
- ntp.py：NTP時刻取得用モジュール
- README.md：使い方や配線図など

## 技術選択・方針
- MicroPython（Python）で開発
- 必要に応じてC言語にも挑戦

## 使い方
1. MicroPythonファームウェアをPicoに書き込み
2. 必要なライブラリを転送
3. main.pyを実行

## 参考
- ePaperサンプル: https://github.com/waveshareteam/Pico_ePaper_Code/
