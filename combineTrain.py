import datetime  # used for naming
import random
import shutil
import time

import numpy
import torch
from ultralytics import YOLO
import os
from combine_data import combineYaml, get_data, moveData, fixLabels, combineFolders
from project_utils import flip


def grabAFew(dataset, nc=1):
    dataset = os.path.abspath(dataset)
    null = []
    files = [[]] * (nc)
    for x in ['train', 'valid', 'test']:
        for a in os.listdir(os.path.join(os.path.join(dataset, x), 'labels')):
            a = os.path.join(os.path.join(dataset, x), f'labels/{a}')
            with open(os.path.abspath(a)) as file:
                data = file.read()
                for _ in data:
                    count = 0
                    if file.read() == " ":
                        break
                    else:
                        count += 1
                classN = data[0:count]
                if classN != "":

                    print(len(files))
                    print(int(classN) - 1)
                    files[int(classN) - 1].append(x + file.name)
                else:
                    null.append(x + file.name)
                file.close()
            time.sleep(0.0001)
    for i in range(len(files)):
        print(len(files[i]))
    newFiles = []
    for i in range(len(files)):
        # print(i)
        newT = numpy.char.find(files[i], 'train', 0, 5)
        newTe = numpy.char.find(files[i], 'test', 0, 4)
        newV = numpy.char.find(files[i], 'valid', 0, 5)
        newTrain = []
        newTest = []
        newValid = []
        print(f'Grabbing images and labels for class {i}')
        for x in range(len(newT)):
            if newT[x] == 0:
                newTrain.append(files[i][x])

        for x in range(len(newTe)):
            if newTe[x] == 0:
                newTest.append(files[i][x])

        for x in range(len(newV)):
            if newV[x] == 0:
                newValid.append(files[i][x])

        for _ in range(20):
            a = random.choice(newTrain)
            newFiles.append(a)
            newTrain.remove(a)
            if len(newTrain) < 1:
                print(f'Ran out of training images at {_} for class {i}')
                break
        for _ in range(7):
            a = random.choice(newValid)
            newFiles.append(a)
            newValid.remove(a)
            if len(newValid) < 1:
                print(f'Ran out of validation images at {_} for class {i}')
                break
        for _ in range(3):
            a = random.choice(newTest)
            newFiles.append(a)
            newTest.remove(a)
            if len(newTest) < 1:
                print(f'Ran out of test images at {_} for class {i}')
                break

    return newFiles


def checkString(string):
    string = str(string[0:5])
    print(string)
    if string[0:5] == 'valid':
        return 1
    if string[0:4] == 'test':
        return 2
    if string[0:5] == 'train':
        return 0


def getCorresponding(list_of_files: list[str], newDir):
    # Needs to be used with a dataset
    if not os.path.exists(newDir):
        os.mkdir(newDir)
    if not os.path.exists(os.path.join(newDir, 'train')):
        os.mkdir(os.path.join(newDir, 'train'))
        os.mkdir(os.path.join(newDir, 'train/labels'))
        os.mkdir(os.path.join(newDir, 'train/images'))
    if not os.path.exists(os.path.join(newDir, 'valid')):
        os.mkdir(os.path.join(newDir, 'valid'))
        os.mkdir(os.path.join(newDir, 'valid/labels'))
        os.mkdir(os.path.join(newDir, 'valid/images'))
    if not os.path.exists(os.path.join(newDir, 'test')):
        os.mkdir(os.path.join(newDir, 'test'))
        os.mkdir(os.path.join(newDir, 'test/labels'))
        os.mkdir(os.path.join(newDir, 'test/images'))

    # TODO make sure images are formatted to be jpgs -- Maybe not idk
    for i in list_of_files:
        if i.__contains__('trainC'):
            i = i[5:]
            shutil.copy2(i, os.path.join(newDir, 'train/labels'), follow_symlinks=True)
            time.sleep(.001)
            i = i[:len(i) - 2]
            z = ""
            for x in range((len(i) - 1), -1, -1):
                if (i[x - 1:x] == '/') or (i[x - 1:x] == '\\'):
                    break
                else:
                    z += i[x - 1:x]
            z = flip(z)
            z += '.jpg'
            prePath = i[0: len(i) - (len(z) - 1)]
            prePath = os.path.split(prePath)[0]
            prePath = os.path.join(prePath, 'images')
            path = os.path.abspath(os.path.join(prePath, z))
            shutil.copy2(path, os.path.join(newDir, 'train/images'), follow_symlinks=True)
            time.sleep(.001)
    for i in list_of_files:
        if i.__contains__('testC'):
            i = i[4:]

            shutil.copy2(i, os.path.join(newDir, 'test/labels'), follow_symlinks=True)
            i = i[:len(i) - 2]
            z = ""
            for x in range((len(i) - 1), -1, -1):
                if (i[x - 1:x] == '/') or (i[x - 1:x] == '\\'):
                    break
                else:
                    z += i[x - 1:x]
            z = flip(z)
            z += '.jpg'
            prePath = i[0: len(i) - (len(z) - 1)]
            prePath = os.path.split(prePath)[0]
            prePath = os.path.join(prePath, 'images')
            path = os.path.abspath(os.path.join(prePath, z))
            shutil.copy2(path, os.path.join(newDir, 'test/images'), follow_symlinks=True)
            time.sleep(.001)
    for i in list_of_files:
        if i.__contains__('validC'):

            i = i[5:]
            shutil.copy(i, os.path.join(newDir, 'valid/labels'), follow_symlinks=True)

            i = i[:len(i) - 2]
            z = ""
            for x in range((len(i) - 1), -1, -1):
                if (i[x - 1:x] == '/') or (i[x - 1:x] == '\\'):
                    break
                else:
                    z += i[x - 1:x]
            z = flip(z)
            z += '.jpg'
            prePath = i[0: len(i) - (len(z) - 1)]
            prePath = os.path.split(prePath)[0]
            prePath = os.path.join(prePath, 'images')

            path = os.path.abspath(os.path.join(prePath, z))
            shutil.copy2(path, os.path.join(newDir, 'valid/images'))
            time.sleep(.001)


def makeSmallDataSet(d1, d2):
    nc = get_data(d1 + '/data.yaml').get('nc') + get_data(d2 + '/data.yaml').get('nc')
    combineYaml(d1, d2, newNC=nc)


# getCorresponding(grabAFew('./Datasets/yolov8seg/IDREC-3.v1i.yolov8', nc=10), './balls')

# TODO Implement this in the gui
def mainCombine(dataset1, dataset2=None, path=os.path.abspath('./CombinedDatasets')):
    dataset1 = os.path.abspath(dataset1)
    path = os.path.abspath(path)
    a = get_data(dataset1 + '/data.yaml')
    if dataset2 is not None:
        fixLabels(dataset2, first_nc=int(a.get('nc')))
        dataset2 = os.path.abspath(dataset2)
        b = get_data(dataset2 + '/data.yaml')

    new = ""
    for _ in range(10):
        new += str((random.randint(0, 10) % 10))

    new += str(datetime.date.today())
    fD = os.path.abspath(path)
    complete = fD
    if not os.path.exists(complete):
        os.mkdir(complete)
    os.mkdir(os.path.join(complete, new))
    path = os.path.join(complete, new)
    if dataset2 is not None:
        combineYaml(dataset1, dataset2, path, new)
    else:
        shutil.copy(os.path.join(dataset1, 'data.yaml'), path)
    if dataset2 is None:
        getCorresponding(grabAFew(dataset1, int(a.get('nc'))), path)
    else:

        getCorresponding(grabAFew(dataset1, int(a.get('nc'))), path)
        getCorresponding(grabAFew(dataset2, int(b.get('nc'))), path)


# TODO Implement this in the gui
def combineBothDatasets(d1, d2, newDir):
    if not os.path.exists(os.path.abspath(newDir)):
        os.mkdir(newDir)
    combineYaml(d1, d2, newDir)
    data = get_data(os.path.join(d2, 'data.yaml'))
    fixLabels(d2, first_nc=int(data.get('nc')))
    combineFolders(d1, d2, newDir)
    return newDir


# Function work?

# combineBothDatasets('Datasets/yolov8seg/IDREC-3.v1i.yolov8','Datasets/yolov8seg/IDREC-3-ONESHOTS 2.v2i.yolov8',
#                  './CombinedDatasets')
mainCombine('Datasets/yolov8seg/IDREC-3.v1i.yolov8',
            'Datasets/yolov8seg/IDREC-3-ONESHOTS 2.v2i.yolov8')

# print(grabAFew('./S', 11))
