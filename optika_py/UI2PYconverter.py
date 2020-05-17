
#   pyuic5 -x optik.ui -o UiMainApp.py
""" PyQt5 uic module convert ui file (XML code) into py file ( Python code)"""
from PyQt5 import uic
fin = open("optik.ui", "r")
fout = open("UiMainApp.py", "w")
uic.compileUi(fin, fout, execute=True)
fin.close()
fout.close()
