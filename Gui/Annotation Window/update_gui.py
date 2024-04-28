import os
pth1 = os.path.abspath('form.ui')
pth2 = os.path.abspath('ui_form.py')
os.system(f'pyside6-uic {pth1} -o {pth2}')
