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
    while True:
        t = get_ntp_time()
        if t is None:
            t = (0,0,0,0,0,0,0,0,0)
        hour = t[3]
        minute = t[4]
        second = t[5]
        # 画面クリア
        epd.image1Gray.fill(epd.white)
        # アナログ時計（上部）
        draw_clock(epd.image1Gray, hour, minute, second, center_x, clock_center_y, radius, epd.black)
        # 下部に日付と時刻を大きく表示
        datestr = "{:04}/{:02}/{:02}".format(t[0], t[1], t[2])
        timestr = "{:02}:{:02}:{:02}".format(hour, minute, second)
        # 日付（下部中央）
        epd.image1Gray.large_text(datestr, center_x-90, epd.height-70, 2, epd.black)
        # 時刻（下部中央）
        epd.image1Gray.large_text(timestr, center_x-90, epd.height-40, 2, epd.black)
        epd.EPD_3IN7_1Gray_Display_Part(epd.buffer_1Gray)  # 部分更新
        utime.sleep(10)

if __name__ == "__main__":
    main()
