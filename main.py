from ntp import get_ntp_time
from wifi import connect_wifi
from draw import draw_clock

from config import WIFI_SSID, WIFI_PASSWORD

from Pico_ePaper_3_7 import EPD_3in7
import framebuf2 as framebuf
import utime
# main.py
# Raspberry Pi Pico + ePaper アナログ時計 メインプログラム

def main():
    # Wi-Fi接続
    if not connect_wifi(WIFI_SSID, WIFI_PASSWORD):
        return
    epd = EPD_3in7()
    epd.EPD_3IN7_1Gray_init()  # 1Grayモードに切り替え
    center_x = epd.width // 2
    # 時計を上部に配置
    clock_center_y = epd.height // 2 - 60
    radius = min(center_x, clock_center_y) - 20
    # 最初にNTPで時刻取得
    t = get_ntp_time()
    if t is None:
        t = (0, 0, 0, 0, 0, 0, 0, 0, 0)
    hour = t[3]
    minute = t[4]
    second = t[5]
    last_ntp = utime.time()
    from draw import draw_screen

    prev_time = utime.time()
    prev_minute = None
    while True:
        now = utime.time()
        # 60分ごとにNTP参照
        if now - last_ntp >= 3600:
            ntp_t = get_ntp_time()
            if ntp_t is not None:
                t = ntp_t
                hour = t[3]
                minute = t[4]
                second = t[5]
            last_ntp = now
            prev_time = now
        else:
            # 実際の経過秒数でローカル時刻を加算
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
        # 分が変わった時だけ描画・更新
        if prev_minute != int(minute):
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
            prev_minute = int(minute)
        utime.sleep(1)


if __name__ == "__main__":
    main()
