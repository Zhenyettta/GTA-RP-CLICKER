#  Copyright (c) Made by Zhenyok!

from ctypes import windll

import win32api
import win32con
from numpy.compat import unicode


def _char2key(c):
    # https://msdn.microsoft.com/en-us/library/windows/desktop/ms646329(v=vs.85).aspx
    result = windll.User32.VkKeyScanW(ord(unicode(c)))
    shift_state = (result & 0xFF00) >> 8
    vk_key = result & 0xFF

    return vk_key


class Keyboard:
    @staticmethod
    def press(c: str):
        win32api.keybd_event(_char2key(c), win32api.MapVirtualKey(_char2key(c), 0), 0, 0)

    @staticmethod
    def release(c: str):
        win32api.keybd_event(_char2key(c), win32api.MapVirtualKey(_char2key(c), 0), win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def press_left_click():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.Sleep(100)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
