import ntptime
import utime

def get_ntp_time():
    ntptime.host = 'ntp.nict.jp'  # 日本のNTPサーバー（NICT公式）
    try:
        ntptime.settime()
        t = utime.localtime()
        # JST（UTC+9）補正
        t = utime.localtime(utime.mktime(t) + 9 * 3600)
        return t
    except Exception as e:
        print("NTP取得失敗:", e)
        return None
