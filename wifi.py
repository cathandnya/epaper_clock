# wifi.py
# Raspberry Pi Pico W用 Wi-Fi接続ユーティリティ

import network
import utime

def connect_wifi(ssid, password, timeout=30):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print("Wi-Fi接続中...")
    for _ in range(timeout):
        if wlan.isconnected():
            print("Wi-Fi接続成功")
            return True
        utime.sleep(1)
    print("Wi-Fi接続失敗")
    return False
