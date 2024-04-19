import datetime  # used for naming
import random
import shutil
import time

import numpy
import torch
from ultralytics import YOLO
import os, sys, stat
from combine_data import combineYaml, get_data, moveData, fixLabels, combineFolders
from project_utils import flip


def addData(model1, data2):
    model = YOLO(os.path.abspath(model1))
    model.train(data=os.path.abspath(data2), epochs=50, freeze=22)


def compare_dicts(state_dict1, state_dict2):
    # Compare the keys
    keys1 = set(state_dict1.keys())
    keys2 = set(state_dict2.keys())

    if keys1 != keys2:
        print("Models have different parameter names.")
        return False

    # Compare the values (weights)
    for key in keys1:
        if not torch.equal(state_dict1[key], state_dict2[key]):
            print(f"Weights for parameter '{key}' are different.")
            if "bn" in key and "22" not in key:
                state_dict1[key] = state_dict2[key]


def newModel():
    model = YOLO('yolov8n-seg.pt')
    model.load(os.path.abspath('./Working_Models/yolov8segment/best.pt'))
    model.train(data=os.path.abspath('./CombinedDatasets/66860504442024-04-14/66860504442024-04-14.yaml'), device=0,
                epochs=120)


def createTrainingSet(trainedModel, newDataSet):
    names = YOLO(trainedModel).names
    data1_yaml = newDataSet + '/data.yaml'
    data1 = get_data(data1_yaml)

    nc = len(names) + data1.get('nc')
    x = list()

    for i in names:
        x.append(names.__getitem__(i))
    fixLabels(newDataSet, nc - 1)
    b = ""
    for i in range(5):
        b += str(random.randint(0, 10) % 10)
    newDir = f'CombinedDatasets/{datetime.date.today()} {b}'
    os.mkdir(newDir)
    combineYaml(newDataSet, None, os.path.abspath(newDir), 'data', True, nc, x)
    moveData(newDataSet, os.path.join(os.path.abspath(newDir), 'data'))


def nested_children(m: torch.nn.Module):
    children = dict(m.named_children())
    output = {}
    if children == {}:
        # if module has no children; m is last child! :O
        return m
    else:
        # look for children from children... to the last child!
        for name, child in children.items():
            try:
                output[name] = nested_children(child)
            except TypeError:
                output[name] = nested_children(child)
    return output


def grabAFew(dataset, nc=1):
    dataset = os.path.abspath(dataset)
    null = []
    files = [[]] * nc
    for x in ['train', 'valid', 'test']:
        for a in os.listdir(os.path.join(os.path.join(dataset, x), 'labels')):
            a = os.path.join(os.path.join(dataset, x), f'labels/{a}')
            with open(os.path.abspath(a)) as file:
                data = file.read()
                for i in data:
                    count = 0
                    if file.read() == " ":
                        break
                    else:
                        count += 1
                classN = data[0:count]
                if classN != "":
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
        print(newTe)
        print(newV)
        for x in range(len(newT)):
            if newT[x] == 0:
                newTrain.append(files[i][x])

        for x in range(len(newTe)):
            if newTe[x] == 0:
                newTest.append(files[i][x])

        for x in range(len(newV)):
            if newV[x] == 0:
                newValid.append(files[i][x])

        for _ in range(10):
            newFiles.append(random.choice(newTrain))
        for _ in range(5):
            newFiles.append(random.choice(newValid))
        newFiles.append(random.choice(newTest))
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

    # TODO make sure images are formatted to be jpgs
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


def combineTrain(dataset, latestModel):
    model = YOLO('yolov8n-seg.pt').load(latestModel)
    dataset = os.path.abspath(dataset)
    model.train(data=(dataset + '/data.yaml'), epochs=30, cls=.7, warmup_epochs=0)


def makeSmallDataSet(d1, d2):
    nc = get_data(d1 + '/data.yaml').get('nc') + get_data(d2 + '/data.yaml').get('nc')
    combineYaml(d1, d2, newNC=nc)


# getCorresponding(grabAFew('./Datasets/yolov8seg/IDREC-3.v1i.yolov8', nc=10), './balls')
def mainCombine(dataset1, dataset2=None, nc=0):
    dataset1 = os.path.abspath(dataset1)
    a = get_data(dataset1 + '/data.yaml')
    if dataset2 is not None:
        fixLabels(dataset2, nc=nc)
        dataset2 = os.path.abspath(dataset2)
        b = get_data(dataset2 + '/data.yaml')
        newNc = a.get('nc') + b.get('nc')

    new = ""
    for _ in range(10):
        new += str((random.randint(0, 10) % 10))

    new += str(datetime.date.today())

    fD = os.path.abspath('./Cool')
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
        getCorresponding(grabAFew(dataset1, nc), path)
    else:
        getCorresponding(grabAFew(dataset1, nc), path)
        getCorresponding(grabAFew(dataset2, nc), path)


def combineBothDatasets(d1, d2, newDir):
    combineYaml(d1, d2, newDir)
    combineFolders(d1, d2, newDir)
    return newDir


# Function not works properly
# combineBothDatasets('Datasets/yolov8seg/IDREC-3.v1i.yolov8','Datasets/yolov8seg/IDREC-3-ONESHOTS 2.v2i.yolov8', './S')


# mainCombine('Datasets/yolov8seg/IDREC-3.v1i.yolov8','Datasets/yolov8seg/IDREC-3-ONESHOTS 2.v2i.yolov8',nc=11)

print(grabAFew('./S', 11))
