import base64
import time
import win32api
import win32gui
import win32ui
import win32con
import win32print
from ctypes import windll
from PIL import Image
import tkinter as tk
import threading as th
import os
import dhash
import tailCoin
import headCoin

# num = 0
w = 0
h = 0
head_coin_sum = 0
tail_coin_sum = 0
desktop_global_resize_w_zoom = 0
desktop_global_resize_h_zoom = 0
is_head = False
is_head_time = 0
root = tk.Tk()
show_text = tk.StringVar()


# 得到游戏界面截图
def get_window_screen_shot_image(hwnd: int):
    global w, h, desktop_global_resize_h_zoom, desktop_global_resize_w_zoom
    # global num
    app = win32gui.GetWindowText(hwnd)
    # 无法找到游戏进程,不进行操作
    if not hwnd or hwnd <= 0 or len(app) == 0:
        return False
    is_iconic = win32gui.IsIconic(hwnd)
    # 游戏处于最小化窗口状态, 无法获取屏幕图像, 不执行操作
    if is_iconic:
        return False

    left, top, right, bot = win32gui.GetClientRect(hwnd)

    w = right - left
    h = bot - top

    # 获取屏幕未缩放分辨率
    hDc = win32gui.GetDC(0)

    _screen_w = win32print.GetDeviceCaps(hDc, win32con.DESKTOPHORZRES)
    _screen_h = win32print.GetDeviceCaps(hDc, win32con.DESKTOPVERTRES)

    _current_screen_w = win32api.GetSystemMetrics(0)
    _current_screen_h = win32api.GetSystemMetrics(1)

    desktop_global_resize_w_zoom = _screen_w / _current_screen_w
    desktop_global_resize_h_zoom = _screen_h / _current_screen_h

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, int(w * desktop_global_resize_w_zoom), int(h * desktop_global_resize_h_zoom))

    saveDC.SelectObject(saveBitMap)

    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
    # saveBitMap.SaveBitmapFile(saveDC, "img_MasterDuel" + str(num) + ".png")

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result != 1:
        return False
    else:
        # num += 1
        return im


# 找到游戏程序
def find_master_duel(program_name):
    hwnd = win32gui.FindWindow(None, program_name)
    return hwnd


# 截取游戏抛硬币时的部分界面
def cut_master_duel_coin_message_image(hwnd):
    global w, h, desktop_global_resize_h_zoom, desktop_global_resize_w_zoom
    # global num
    img = get_window_screen_shot_image(hwnd)
    if not img:
        return False
    box = (
        int(w * desktop_global_resize_w_zoom / 2 - w * desktop_global_resize_w_zoom / 16),
        int(h * desktop_global_resize_h_zoom / 2 - h * desktop_global_resize_h_zoom / 9),
        int(w * desktop_global_resize_w_zoom / 2 + w * desktop_global_resize_w_zoom / 16),
        int(h * desktop_global_resize_h_zoom / 2 + h * desktop_global_resize_h_zoom / 9)
    )
    img = img.crop(box)
    # img.show()
    # img.save("img_MasterDuel" + str(num) + ".png")
    # num += 1
    return img


# 得到拿来对比是否相似的汉明值
def get_hamming_dist(str1, str2):
    assert len(str1) == len(str2)
    return sum([ch1 != ch2 for ch1, ch2 in zip(str1, str2)])


# 得到dhash值
def get_dhash(img):
    row, col = dhash.dhash_row_col(img)
    img_dhash = dhash.format_hex(row, col)
    return img_dhash


# 得到本地图片的dhash值
def get_coin_message_dhash(coin):
    img = Image.open(coin)
    head_coin_dhash = get_dhash(img)
    return head_coin_dhash


# 和赢硬币对比是否相似
def judge_head_coin_message(message):
    if message >= 0.92:
        return True
    return False


# 和输硬币对比是否相似
def judge_tail_coin_message(message):
    if message >= 0.92:
        return True
    return False


# 对比的代码
def comparison_coin():
    global tail_coin_sum, head_coin_sum, show_text, is_head, is_head_time
    # global num
    hwnd = find_master_duel("masterduel")
    coin = cut_master_duel_coin_message_image(hwnd)
    # num += 1
    if not coin:
        start()
    else:
        message = 1 - get_hamming_dist(get_coin_message_dhash("./headCoin.png"), get_dhash(coin)) * 1. / (32 * 32 / 4)
        # if is_head is True:
        #     print("赢   ", message, end="\t")
        if judge_head_coin_message(message) and is_head is False:
            is_head_time = time.time() + 4
            time.sleep(1)
            is_head = True
        elif judge_head_coin_message(message) and is_head is True:
            is_head = False
            head_coin_sum += 1
            text_str = "赢硬币:" + str(head_coin_sum) + "    输硬币:" + str(tail_coin_sum)
            show_text.set(text_str)
            time.sleep(8)
        elif is_head is True:
            message = 1 - get_hamming_dist(get_coin_message_dhash("./tailCoin.png"), get_dhash(coin)) * 1. / (32 * 32 / 4)
            # print("输   ", message)
            if judge_tail_coin_message(message):
                is_head = False
                tail_coin_sum += 1
                text_str = "赢硬币:" + str(head_coin_sum) + "    输硬币:" + str(tail_coin_sum)
                show_text.set(text_str)
                time.sleep(8)
            else:
                is_head_time_now = time.time()
                if is_head_time_now >= is_head_time:
                    is_head = False
                    is_head_time = 0
        start()


# 增加一次赢硬币的按钮事件
def head_coin_add():
    global tail_coin_sum, head_coin_sum, show_text
    head_coin_sum += 1
    text_str = "赢硬币:" + str(head_coin_sum) + "    输硬币:" + str(tail_coin_sum)
    show_text.set(text_str)


# 减少一次赢硬币的按钮事件
def head_coin_minus():
    global tail_coin_sum, head_coin_sum, show_text
    if head_coin_sum - 1 >= 0:
        head_coin_sum -= 1
        text_str = "赢硬币:" + str(head_coin_sum) + "    输硬币:" + str(tail_coin_sum)
        show_text.set(text_str)


# 增加一次输硬币的按钮事件
def tail_coin_add():
    global tail_coin_sum, head_coin_sum, show_text
    tail_coin_sum += 1
    text_str = "赢硬币:" + str(head_coin_sum) + "    输硬币:" + str(tail_coin_sum)
    show_text.set(text_str)


# 减少一次输硬币的按钮事件
def tail_coin_minus():
    global tail_coin_sum, head_coin_sum, show_text
    if tail_coin_sum - 1 >= 0:
        tail_coin_sum -= 1
        text_str = "赢硬币:" + str(head_coin_sum) + "    输硬币:" + str(tail_coin_sum)
        show_text.set(text_str)


# GUI
def tk_gui():
    global root, show_text
    text_str = "赢硬币:0    输硬币:0"
    root.title("硬币统计")
    show_text.set(text_str)

    lb = tk.Label(root, textvariable=show_text, font=('Arial', 11))
    lb.grid(row=0, column=0, columnspan=6)

    lb1 = tk.Label(root, textvariable="")
    lb1.grid(row=1, column=0, columnspan=6)

    head_coin_add_button = tk.Button(root, text='赢硬币+1', command=head_coin_add)
    head_coin_add_button.grid(row=2, column=0)

    tail_coin_add_button = tk.Button(root, text='输硬币+1', command=tail_coin_add)
    tail_coin_add_button.grid(row=2, column=1)

    head_coin_minus_button = tk.Button(root, text='赢硬币 -1', command=head_coin_minus)
    head_coin_minus_button.grid(row=3, column=0)

    tail_coin_minus_button = tk.Button(root, text='输硬币 -1', command=tail_coin_minus)
    tail_coin_minus_button.grid(row=3, column=1)

    root.geometry("240x115+1+1")
    root.attributes('-topmost', 'true')
    root.mainloop()


# 启动
def start():
    p = th.Timer(0.05, comparison_coin)
    p.setDaemon(True)
    p.start()


if __name__ == '__main__':
    with open(r'./headCoin.png', 'wb') as f:
        f.write(base64.b64decode(headCoin.true))
    with open(r'./tailCoin.png', 'wb') as f:
        f.write(base64.b64decode(tailCoin.false))
    start()
    tk_gui()
    os.remove('./headCoin.png')
    os.remove('./tailCoin.png')
