import os
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
import dhash
from configparser import ConfigParser
import webbrowser
import tailCoin
import headCoin
import base64

# num = 0
p = ""
w = 0
h = 0
head_coin_sum = 0
tail_coin_sum = 0
desktop_global_resize_w_zoom = 0
desktop_global_resize_h_zoom = 0
is_head = False
is_head_time = 0
head_coin_dhash = ""
tail_coin_dhash = ""
root = tk.Tk()
show_text = tk.StringVar()
conf = ConfigParser()
top_tk = 1
width_tk = 213
height_tk = 125
width_win = 1
height_win = 1
font_size = 9
lb = ""
head_coin_add_button = ""
tail_coin_add_button = ""
head_coin_minus_button = ""
tail_coin_minus_button = ""
top_button = ""
font_add_button = ""
font_minus_button = ""
bug_text = ""
bili_button = ""
github_button = ""


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
    coin_dhash = get_dhash(img)
    return coin_dhash


# 和硬币对比是否相似
def judge_coin_message(message):
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
        message = 1 - get_hamming_dist(head_coin_dhash, get_dhash(coin)) * 1. / (32 * 32 / 4)
        # if is_head is True:
        #     print("赢   ", message, end="\t")
        if judge_coin_message(message) and is_head is False:
            # print("开始识别：", end="\n")
            is_head_time = time.time() + 4
            time.sleep(1)
            is_head = True
        elif judge_coin_message(message) and is_head is True:
            # print("\n赢赢赢", end="\n\n")
            is_head = False
            head_coin_sum += 1
            text_str = "赢硬币:" + str(head_coin_sum) + "   输硬币:" + str(tail_coin_sum)
            show_text.set(text_str)
            time.sleep(5)
        elif is_head is True:
            message = 1 - get_hamming_dist(tail_coin_dhash, get_dhash(coin)) * 1. / (32 * 32 / 4)
            # print("输   ", message, end="\t")
            if judge_coin_message(message):
                # print("\n输输输", end="\n\n")
                is_head = False
                tail_coin_sum += 1
                text_str = "赢硬币:" + str(head_coin_sum) + "   输硬币:" + str(tail_coin_sum)
                show_text.set(text_str)
                time.sleep(5)
            else:
                is_head_time_now = time.time()
                if is_head_time_now >= is_head_time:
                    is_head = False
                    is_head_time = 0
        start()


# 增加一次赢硬币的按钮
def head_coin_add():
    global head_coin_sum
    head_coin_sum += 1
    text_str = "赢硬币:" + str(head_coin_sum) + "   输硬币:" + str(tail_coin_sum)
    show_text.set(text_str)


# 减少一次赢硬币的按钮
def head_coin_minus():
    global head_coin_sum
    if head_coin_sum - 1 >= 0:
        head_coin_sum -= 1
        text_str = "赢硬币:" + str(head_coin_sum) + "   输硬币:" + str(tail_coin_sum)
        show_text.set(text_str)


# 增加一次输硬币的按钮
def tail_coin_add():
    global tail_coin_sum
    tail_coin_sum += 1
    text_str = "赢硬币:" + str(head_coin_sum) + "   输硬币:" + str(tail_coin_sum)
    show_text.set(text_str)


# 减少一次输硬币的按钮
def tail_coin_minus():
    global tail_coin_sum
    if tail_coin_sum - 1 >= 0:
        tail_coin_sum -= 1
        text_str = "赢硬币:" + str(head_coin_sum) + "   输硬币:" + str(tail_coin_sum)
        show_text.set(text_str)


# 是否置顶
def is_top():
    global top_tk
    if top_tk == 0:
        top_tk = 1
    else:
        top_tk = 0
    conf.set('user', 'top_tk', str(top_tk))
    with open('save.INI', 'w', encoding='utf-8') as f1:
        conf.write(f1)
    root.attributes('-topmost', top_tk)


# 字体重设大小
def set_font():
    lb['font'] = ('Microsoft Yahei', font_size + 2)
    head_coin_add_button['font'] = ('Microsoft Yahei', font_size)
    tail_coin_add_button['font'] = ('Microsoft Yahei', font_size)
    head_coin_minus_button['font'] = ('Microsoft Yahei', font_size)
    tail_coin_minus_button['font'] = ('Microsoft Yahei', font_size)
    top_button['font'] = ('Microsoft Yahei', font_size)
    font_add_button['font'] = ('Microsoft Yahei', font_size)
    font_minus_button['font'] = ('Microsoft Yahei', font_size)
    bug_text['font'] = ('Microsoft Yahei', font_size + 1)
    bili_button['font'] = ('Microsoft Yahei', font_size)
    github_button['font'] = ('Microsoft Yahei', font_size)


# 字体增大
def font_add():
    global font_size
    font_size += 1
    conf.set('user', 'font_size', str(font_size))
    with open('save.INI', 'w', encoding='utf-8') as f1:
        conf.write(f1)
    set_font()


# 字体减小
def font_minus():
    global font_size
    if font_size > 1:
        font_size -= 1
        conf.set('user', 'font_size', str(font_size))
        with open('save.INI', 'w', encoding='utf-8') as f1:
            conf.write(f1)
        set_font()


# 跳转B站
def bili():
    webbrowser.open("https://space.bilibili.com/29666002")


# 跳转github
def github():
    webbrowser.open("https://github.com/konipabai/MasterDuelCoin")


# 关闭按钮触发存储位置大小
def size():
    conf.set('user', 'width_win', str(root.winfo_x()))
    conf.set('user', 'height_win', str(root.winfo_y()))
    conf.set('user', 'width_tk', str(root.winfo_width()))
    conf.set('user', 'height_tk', str(root.winfo_height()))
    with open('save.INI', 'w', encoding='utf-8') as f2:
        conf.write(f2)
    root.destroy()


# GUI
def tk_gui():
    global lb, head_coin_add_button, tail_coin_add_button, head_coin_minus_button, tail_coin_minus_button, top_button, font_add_button, font_minus_button, bug_text, bili_button, github_button
    text_str = "赢硬币:0   输硬币:0"
    root.title("硬币统计")
    show_text.set(text_str)

    lb = tk.Label(root, textvariable=show_text, font=('Microsoft Yahei', font_size + 2))
    lb.grid(row=0, column=0, rowspan=1, columnspan=2, pady=3)

    head_coin_add_button = tk.Button(root, text='赢硬币+1', command=head_coin_add, font=('Microsoft Yahei', font_size))
    head_coin_add_button.grid(row=2, column=0)

    tail_coin_add_button = tk.Button(root, text='输硬币+1', command=tail_coin_add, font=('Microsoft Yahei', font_size))
    tail_coin_add_button.grid(row=2, column=1)

    head_coin_minus_button = tk.Button(root, text='赢硬币 -1', command=head_coin_minus, font=('Microsoft Yahei', font_size))
    head_coin_minus_button.grid(row=3, column=0)

    tail_coin_minus_button = tk.Button(root, text='输硬币 -1', command=tail_coin_minus, font=('Microsoft Yahei', font_size))
    tail_coin_minus_button.grid(row=3, column=1)

    top_button = tk.Button(root, text='是否置顶', command=is_top, font=('Microsoft Yahei', font_size))
    top_button.grid(row=0, column=2, padx=19)

    font_add_button = tk.Button(root, text='字体增大', command=font_add, font=('Microsoft Yahei', font_size))
    font_add_button.grid(row=2, column=2, padx=19)

    font_minus_button = tk.Button(root, text='字体减小', command=font_minus, font=('Microsoft Yahei', font_size))
    font_minus_button.grid(row=3, column=2, padx=19)

    bug_text = tk.Label(root, text="反馈bug:", font=('Microsoft Yahei', font_size + 1))
    bug_text.grid(row=4, column=0, pady=3)

    bili_button = tk.Button(root, text='B站链接', command=bili, font=('Microsoft Yahei', font_size))
    bili_button.grid(row=4, column=1, pady=3)

    github_button = tk.Button(root, text='github链接', command=github, font=('Microsoft Yahei', font_size))
    github_button.grid(row=4, column=2, pady=3)

    root.geometry(width_tk + "x" + height_tk + "+" + width_win + "+" + height_win)
    root.attributes('-topmost', top_tk)
    root.protocol("WM_DELETE_WINDOW", size)
    root.mainloop()


# 启动
def start():
    global p
    p = th.Timer(0.15, comparison_coin)
    p.setDaemon(True)
    p.start()


# 读取用户的初始化数据和加载要对比的硬币图片的dhash
def read_ini():
    global top_tk, width_tk, height_tk, width_win, height_win, font_size, head_coin_dhash, tail_coin_dhash
    conf.read('save.INI', encoding='UTF-8')
    top_tk = int(conf['user']['top_tk'])
    width_tk = conf['user']['width_tk']
    height_tk = conf['user']['height_tk']
    width_win = conf['user']['width_win']
    height_win = conf['user']['height_win']
    font_size = int(conf['user']['font_size'])
    head_coin_dhash = get_coin_message_dhash("./image/headCoin.png")
    tail_coin_dhash = get_coin_message_dhash("./image/tailCoin.png")


if __name__ == '__main__':
    with open(r'./image/headCoin.png', 'wb') as f:
        f.write(base64.b64decode(headCoin.true))
    with open(r'./image/tailCoin.png', 'wb') as f:
        f.write(base64.b64decode(tailCoin.false))
    read_ini()
    start()
    tk_gui()
    os.remove('./image/headCoin.png')
    os.remove('./image/tailCoin.png')
