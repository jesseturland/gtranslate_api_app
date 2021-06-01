from PyQt5 import QtWidgets, uic
import sys
from selenium import webdriver
from google.cloud import translate_v2
import keyboard
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QAction, QApplication, QMainWindow, QMenu
import pyautogui
import clipboard
import pinyin
import os
import json
import html

f = open('polyphones.json', "r" ,encoding = "Utf-8")
ch_dat = json.load(f)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\jesse\My Documents\LiClipse Workspace\words_parsing\GoogleCloudKey.json"
translate_client = translate_v2.Client()

class KeyBoardManager(QObject):
    PSignal = pyqtSignal()
    def start(self):
        keyboard.add_hotkey("9", self.PSignal.emit, suppress=True)  # put the keyboard shortcuts here

class Replacing(QtWidgets.QMainWindow):
    def __init__(self):
        super(Replacing, self).__init__()
        uic.loadUi('parsing_utility.ui',self)
        manager = KeyBoardManager(self)
        manager.PSignal.connect(self.onClickpb)
        manager.start()

    def onClickpb(self):
        html_var = self.lineEdit.text()
        f = open(html_var + ".html","a+",encoding="utf-8")
        
        
        pols = ''
        pyautogui.hotkey('ctrl', 'c')
        var_1 = ''
        for item in clipboard.paste().split():
            var_1 = var_1 + item
        self.textEdit.setText(var_1)
        for item in var_1:
            if str(ch_dat.get(item)) == "None":
                pass
            else:
                pols = pols + item + "," + str(ch_dat.get(item))
        self.textEdit_2.setText(pinyin.get(var_1,delimiter="") + "         " + pols)
        output = translate_client.translate(var_1, target_language="EN",source_language="Zh")
        self.textEdit_3.setText(html.unescape(output.get("translatedText")))
        f.write(pinyin.get(var_1,delimiter="") + "         " + pols+ "</br>")
        f.write(html.unescape(output.get("translatedText"))+ "</br>")
        f.write(clipboard.paste() + "</br>")
        f.close()

app = QtWidgets.QApplication([])
win = Replacing()
win.show()
sys.exit(app.exec())