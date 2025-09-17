# epaper.py
# WaveShare 3.7inch e-Paper用制御モジュール
# 参考: https://github.com/waveshareteam/Pico_ePaper_Code/

import machine
import time

# ピン定義（例: Pico用）
EPD_RST_PIN = 12
EPD_DC_PIN  = 8
EPD_CS_PIN  = 9
EPD_CLK_PIN = 10
EPD_DIN_PIN = 11
EPD_BUSY_PIN = 13

class EPD:
    def draw_rect(self, x0, y0, x1, y1, color=0):
        # (x0, y0)から(x1, y1)までの矩形を描画
        buf = bytearray([0xFF] * (self.WIDTH * self.HEIGHT // 8))
        for y in range(y0, y1):
            for x in range(x0, x1):
                self._set_pixel(buf, x, y, color)
        self._display_buffer(buf)
        print(f"矩形描画: ({x0},{y0})-({x1},{y1})")
    def __init__(self):
        self.rst = machine.Pin(EPD_RST_PIN, machine.Pin.OUT)
        self.dc  = machine.Pin(EPD_DC_PIN, machine.Pin.OUT)
        self.cs  = machine.Pin(EPD_CS_PIN, machine.Pin.OUT)
        self.clk = machine.Pin(EPD_CLK_PIN, machine.Pin.OUT)
        self.din = machine.Pin(EPD_DIN_PIN, machine.Pin.OUT)
        self.busy = machine.Pin(EPD_BUSY_PIN, machine.Pin.IN)
        self.spi = machine.SPI(0, baudrate=2000000, polarity=0, phase=0)

    def reset(self):
        self.rst.value(1)
        time.sleep_ms(200)
        self.rst.value(0)
        time.sleep_ms(2)
        self.rst.value(1)
        time.sleep_ms(200)

    def send_command(self, command):
        self.dc.value(0)
        self.cs.value(0)
        self.spi.write(bytearray([command]))
        self.cs.value(1)

    def send_data(self, data):
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(bytearray([data]))
        self.cs.value(1)

    def wait_until_idle(self):
        while self.busy.value() == 1:
            time.sleep_ms(100)

    def init(self):
        self.reset()
        # EPD_3IN7_Init (公式サンプルそのまま)
        self.send_command(0x01)
        self.send_data(0x03)
        self.send_data(0x00)
        self.send_data(0x2B)
        self.send_data(0x2B)
        self.send_data(0x09)
        self.send_command(0x06)
        self.send_data(0x17)
        self.send_data(0x17)
        self.send_data(0x17)
        self.send_command(0x04)
        self.wait_until_idle()
        self.send_command(0x00)
        self.send_data(0x3F)
        self.send_command(0x30)
        self.send_data(0x3C)
        self.send_command(0x61)
        self.send_data(0x01)
        self.send_data(0xE0)
        self.send_data(0x01)
        self.send_data(0x18)
        self.send_command(0x82)
        self.send_data(0x12)
        self.send_command(0x50)
        self.send_data(0x97)
        self.send_command(0x60)
        self.send_data(0x22)
        self.send_command(0x65)
        self.send_data(0x00)
        self.wait_until_idle()

    def clear(self):
        # EPD_3IN7_Clear (公式サンプルそのまま)
        buf = bytearray([0xFF] * (self.WIDTH * self.HEIGHT // 8))
        self.send_command(0x10)
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(buf)
        self.cs.value(1)
        self.send_command(0x13)
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(buf)
        self.cs.value(1)
        self.send_command(0x12)
        self.wait_until_idle()
        print("画面クリア（白塗り）")

    def _display_buffer(self, buf):
        # EPD_3IN7_Display (公式サンプルそのまま)
        self.send_command(0x13)
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(buf)
        self.cs.value(1)
        self.send_command(0x12)
        self.wait_until_idle()



    # 3.7inch e-Paperの解像度
    WIDTH = 480
    HEIGHT = 280


    def draw_dot(self):
        # 画面中央に黒点を描画
        buf = bytearray([0xFF] * (self.WIDTH * self.HEIGHT // 8))
        x = self.WIDTH // 2
        y = self.HEIGHT // 2
        self._set_pixel(buf, x, y, 0)  # 0:黒, 1:白
        self._display_buffer(buf)
        print("中央に黒点を描画")

    def _set_pixel(self, buf, x, y, color):
        # 1bitカラー（黒:0, 白:1）
        if x < 0 or x >= self.WIDTH or y < 0 or y >= self.HEIGHT:
            return
        idx = x + y * self.WIDTH
        byte_idx = idx // 8
        bit_idx = 7 - (idx % 8)
        if color:
            buf[byte_idx] |= (1 << bit_idx)
        else:
            buf[byte_idx] &= ~(1 << bit_idx)

    def _display_buffer(self, buf):
        # バッファをePaperに送信（公式サンプルのDisplay関数相当）
        # 1. データ送信コマンド
        self.send_command(0x24)  # RAM write
        # 2. バッファ送信
        self.dc.value(1)
        self.cs.value(0)
        self.spi.write(buf)
        self.cs.value(1)
        # 3. 更新コマンド
        self.send_command(0x22)  # Display Update Control
        self.send_data(0xC7)     # Enable clock, enable CP
        self.send_command(0x20)  # Master Activation
        self.wait_until_idle()


    def display_text(self, text):
        # 画面にテキストを表示する（簡易例）
        # 公式サンプルのdraw_string関数などを参考
        # ここでは仮の処理
        print("表示: ", text)
        # 実際はバッファに描画してからePaperに送信

    def display_clock(self, t):
        # TODO: アナログ時計描画処理
        pass
