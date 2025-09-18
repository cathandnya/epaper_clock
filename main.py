from ntp import get_ntp_time
from wifi import connect_wifi

from config import WIFI_SSID, WIFI_PASSWORD

from Pico_ePaper_3_7 import EPD_3in7
import utime
# main.py
# Raspberry Pi Pico + ePaper アナログ時計 メインプログラム

def main():
    # Wi-Fi接続
    if not connect_wifi(WIFI_SSID, WIFI_PASSWORD):
        return
    # e-Paper初期化
    epd = EPD_3in7()
    epd.EPD_3IN7_1Gray_init()  # 1Grayモードに切り替え
    center_x = epd.width // 2
    # 時計を上部に配置
    clock_center_y = epd.height // 2 - 60
    radius = min(center_x, clock_center_y) - 20
    # 最初にNTPで時刻取得（起動時のみ）
    t = get_ntp_time()
    if t is None:
        t = (0, 0, 0, 0, 0, 0, 0, 0, 0)
    hour = t[3]
    minute = t[4]
    second = t[5]
    from draw import draw_screen

    prev_time = utime.time()
    while True:
        now = utime.time()
        # ローカル時刻を経過秒数で加算
        elapsed = now - prev_time
        prev_time = now
        second += elapsed
        while second >= 60:
            second -= 60
            minute += 1
        while minute >= 60:
            minute -= 60
            hour += 1
        while hour >= 24:
            hour -= 24

        # 毎分0秒で画面描画・部分更新
        start_draw = utime.time()  # 描画開始時刻
        draw_screen(
            epd.image1Gray,
            hour,
            minute,
            int(second),
            t,
            center_x,
            clock_center_y,
            radius,
            epd.black,
            epd.height,
        )
        epd.EPD_3IN7_1Gray_Display_Part(epd.buffer_1Gray)  # 部分更新

        # 49分または00:00になったらNTPで時刻補正
        if int(minute) == 49 or (int(hour) == 0 and int(minute) == 0):
            ntp_t = get_ntp_time()
            if ntp_t is not None:
                t = ntp_t
                hour = t[3]
                minute = t[4]
                second = t[5]
                prev_time = utime.time()  # NTP取得後の基準時刻を補正

        end_draw = utime.time()  # 描画終了時刻
        # 描画＋NTP取得にかかった時間分だけsleepを調整
        wait = 60 - int(second) - int(end_draw - start_draw)
        if wait < 1:
            wait = 1
        utime.sleep(wait)


if __name__ == "__main__":
    main()
