# epaper_clock

[![YouTube](https://github.com/user-attachments/assets/06d7e8c2-3079-4c59-b125-572584ffa07e)](https://youtu.be/7izADfk7rCI?si=zEewazNPbxkOBeJJ)

## 概要
Raspberry Pi Pico WH（ピンヘッダ付き）＋WaveShare 3.7inch e-Paperディスプレイでアナログ時計を作成します。
NTPで正確な時刻を取得し、時計表示に反映します。

## 構成ファイル
主な構成ファイル：
- main.py：時計のメインプログラム
- config.py：Wi-Fi設定
- draw.py：時計・画面描画
- framebuf2.py：FrameBuffer拡張
- Pico_ePaper_3_7.py：e-Paper制御
- ntp.py：NTP時刻取得
- wifi.py：Wi-Fi接続
- README.md：使い方や配線図など

## 環境設定
### config.py
- Wi-FiのSSIDとパスワードを編集してください（例：WIFI_SSID, WIFI_PASSWORD）
### framebuf2.py
- 必ずプロジェクト直下に配置してください（importエラー防止のため）
- 取得元: https://github.com/peter-l5/framebuf2

### Pico_ePaper_3_7.py
- 必ずプロジェクト直下に配置してください（importエラー防止のため）
- 取得元: https://github.com/waveshareteam/Pico_ePaper_Code/blob/main/python/Pico-ePaper-3.7.py

## 使い方
1. MicroPythonファームウェアをRaspberry Pi Pico Wに書き込み
2. 必要なライブラリ・ファイル（main.py, Pico_ePaper_3_7.py, draw.py, ntp.py, wifi.py, framebuf2.py）をampy等で転送


3. main.pyを実行（例: `ampy --port /dev/tty.usbmodemXXXXXX run main.py`）
4. NTPで時刻取得し、e-Paperにアナログ時計＋日付・時刻を表示

## 参考
- ePaperサンプル: https://github.com/waveshareteam/Pico_ePaper_Code/
