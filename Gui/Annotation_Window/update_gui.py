import os
pth1 = os.path.abspath('../AllWindows/form2.ui')
pth2 = os.path.abspath('../AllWindows/ui_form2.py')
os.system(f'pyside6-uic {pth1} -o {pth2}')
