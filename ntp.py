import ntptime
import utime

def get_ntp_time():
    ntptime.host = 'ntp.nict.jp'  # 日本のNTPサーバー（NICT公式）
    try:
        ntptime.settime()
        t = utime.localtime()
        return t
    except Exception as e:
        print('NTP取得失敗:', e)
        return None
# ntp.py
# NTP時刻取得用モジュール

    # ...existing code...
