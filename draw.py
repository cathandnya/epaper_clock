import framebuf2 as framebuf
# draw.py
# アナログ時計描画用モジュール（時計・針・数字・目盛りの描画関数を提供）

import math


def draw_screen(
    fb, hour, minute, second, date_tuple, center_x, clock_center_y, radius, color, screen_height
):
    # 画面を白でクリア
    fb.fill(1)
    # 上部にアナログ時計を描画
    draw_clock(fb, hour, minute, second, center_x, clock_center_y, radius, color)
    # 下部に日付と時刻（分まで）を大きく表示
    yearstr = "{:04}".format(date_tuple[0])
    datestr = "{:02}/{:02}".format(date_tuple[1], date_tuple[2])
    timestr = "{:02}:{:02}".format(hour, minute)
    # 日付（下部中央）
    fb.large_text(yearstr, center_x - 50, screen_height - 140, 2, color, 90)
    fb.large_text(datestr, center_x - 80, screen_height - 140, 2, color, 90)
    # 時刻（下部中央）
    fb.large_text(timestr, center_x - 110, screen_height - 140, 2, color, 90)


def draw_thick_line(fb, x0, y0, x1, y1, width, color):
    # 線分(x0,y0)-(x1,y1)を指定した太さで描画
    dx = x1 - x0
    dy = y1 - y0
    length = math.sqrt(dx*dx + dy*dy)
    if length == 0:
        return
    # 垂直方向ベクトル
    nx = -dy / length
    ny = dx / length
    for w in range(-width//2, width//2+1):
        sx0 = int(x0 + nx * w)
        sy0 = int(y0 + ny * w)
        sx1 = int(x1 + nx * w)
        sy1 = int(y1 + ny * w)
        fb.line(sx0, sy0, sx1, sy1, color)

    # アナログ時計描画
    # fb: framebufオブジェクト, hour, minute, second: int, center_x, center_y, radius: int, color: 描画色


def draw_clock(
    fb: framebuf.FrameBuffer, hour, minute, second, center_x, center_y, radius, color
):
    # 12, 3, 6, 9の数字を大きく描画（拡大文字）
    num_list = [(12, 0), (3, 90), (6, 180), (9, 270)]
    num_radius = radius - 12
    num_angle_set = set([0, 90, 180, 270])
    # 12, 3, 6, 9の数字（8倍サイズで描画）
    for num, deg in num_list:
        rad = math.radians(deg)
        x = int(center_x + num_radius * math.cos(rad))
        y = int(center_y + num_radius * math.sin(rad))
        if num == 12:
            fb.large_text(str(num), x - 16, y - 28, 4, color, 90)  # 2文字分左にずらす
        else:
            fb.large_text(str(num), x - 16, y - 16, 4, color, 90)
    # 12時間の目盛り（数字位置は除外、短い線）
    offsets = [0, 1]
    for h in range(12):
        angle_deg = h * 30
        if angle_deg in num_angle_set:
            continue  # 12,3,6,9の位置は目盛り描画しない
        angle = math.radians(angle_deg)
        for off in offsets:
            outer_x = int(center_x + (radius + off) * math.cos(angle))
            outer_y = int(center_y + (radius + off) * math.sin(angle))
            inner_x = int(center_x + (radius - 10 + off) * math.cos(angle))
            inner_y = int(center_y + (radius - 10 + off) * math.sin(angle))
            fb.line(inner_x, inner_y, outer_x, outer_y, color)
    # 時針（太い線で描画、長さは半径の0.5倍）
    hour_angle = math.radians((hour % 12 + minute / 60) * 30)
    hour_length = int(radius * 0.5)
    hour_x = int(center_x + hour_length * math.cos(hour_angle))
    hour_y = int(center_y + hour_length * math.sin(hour_angle))
    draw_thick_line(fb, center_x, center_y, hour_x, hour_y, 4, color)
    # 分針（太さ3、長さは半径の0.6倍）
    minute_angle = math.radians(minute * 6)
    minute_length = int(radius * 0.6)
    minute_x = int(center_x + minute_length * math.cos(minute_angle))
    minute_y = int(center_y + minute_length * math.sin(minute_angle))
    draw_thick_line(fb, center_x, center_y, minute_x, minute_y, 3, color)
    # 秒針（細い線、長さは半径の0.8倍）
    second_angle = math.radians(second * 6)
    second_length = int(radius * 0.8)
    second_x = int(center_x + second_length * math.cos(second_angle))
    second_y = int(center_y + second_length * math.sin(second_angle))
    draw_thick_line(fb, center_x, center_y, second_x, second_y, 1, color)
