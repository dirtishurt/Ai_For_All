import os
from random import randint
import cv2
def flip(x: str):
    a = list()
    for i in x:
        a.append(i)
    a.reverse()
    b = ""
    for o in range(len(a)-1):
        b += a[o]
    return b

def getRandomName():
    x = ''
    for i in range(20):
        x += str(randint(0,9))
    return x

def resize_all(directory, save_dir='./ChangedImages'):
    count = 0
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    if os.path.exists(os.path.abspath(directory)):
        for fn in os.listdir(os.path.abspath(directory)):
            path = os.path.join(os.path.abspath(directory), fn)
            i = resize_img(path)
            cv2.imwrite(f'{save_dir}/{count}.jpg', i)
            #i.save(os.path.join(save_dir, ))
            count += 1
    else:
        print('Directory not found')
def resize_img(images):
    old = cv2.imread(images)

    new = cv2.resize(old, (640, 640))
    return new

resize_all('./Datasets/yolov8seg/IDREC-3.v1i.yolov8/train/images')
