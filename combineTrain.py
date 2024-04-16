import datetime  # used for naming
import random
import shutil
import torch
from ultralytics import YOLO
import os
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


def grabAFew(dataset, nc=1, listdata=['train', 'valid', 'test']):
    files = []
    null = []
    for i in range(nc + 1):
        files.append([])

    for i in range(len(listdata) - 1):
        for fn in os.listdir(os.path.join(os.path.abspath(dataset), f'{listdata[i]}/labels')):
            # print(os.path.join(os.path.join(os.path.abspath(dataset), f'{i}/labels'), fn))
            path = os.path.join(os.path.join(os.path.abspath(dataset), f'{listdata[i]}/labels'), fn)
            with open(path, 'r') as file:
                data = file.read()
                count = 0
                for x in data:
                    if x != " ":
                        count += 1
                    else:
                        break
                try:
                    files[int(data[0:count].strip()) - 1].append(listdata[i] + file.name)
                except ValueError:
                    # in the event of a null image we want to add it
                    null.append(random.choice(listdata) + file.name)
                except IndexError:
                    print('Error')
        newFiles = list()
        for i in range(len(files) - 1):
            for b in range(10):
                try:
                    newFiles.append(random.choice(files[i]))
                except IndexError:
                    print('error')
        for i in range(len(null) - 1):
            for b in range(3):
                newFiles.append(random.choice(null))
        return newFiles


def getCorresponding(list_of_files: list[str], newDir):
    # Needs to be used with a dataset
    os.mkdir(newDir)
    os.mkdir(os.path.join(newDir, 'train'))
    os.mkdir(os.path.join(newDir, 'train/labels'))
    os.mkdir(os.path.join(newDir, 'valid'))
    os.mkdir(os.path.join(newDir, 'valid/labels'))
    os.mkdir(os.path.join(newDir, 'test'))
    os.mkdir(os.path.join(newDir, 'test/labels'))
    os.mkdir(os.path.join(newDir, 'train/images'))
    os.mkdir(os.path.join(newDir, 'valid/images'))
    os.mkdir(os.path.join(newDir, 'test/images'))

    # TODO make sure images are formatted to be jpgs
    print(list_of_files)
    for i in list_of_files:
        if i.__contains__('trainC'):
            i = i[5:]
            shutil.copy(i, os.path.join(newDir, 'train/labels'))
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
            shutil.copy(path, os.path.join(newDir, 'train/images'))

        elif i.__contains__('testC'):
            i = i[4:]
            shutil.copy(i, os.path.join(newDir, 'test/labels'))
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
            shutil.copy(path, os.path.join(newDir, 'test/images'))
        elif i.__contains__('validC'):
            i = i[5:]
            shutil.copy(i, os.path.join(newDir, 'valid/labels'))
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
            shutil.copy(path, os.path.join(newDir, 'valid/images'))


def combineTrain(dataset, latestModel):
    model = YOLO('yolov8n-seg.pt').load(latestModel)
    dataset = os.path.abspath(dataset)
    model.train(data=(dataset + '/data.yaml'), epochs=30, cls=.7, warmup_epochs=0)


def makeSmallDataSet(d1, d2):
    nc = get_data(d1 + '/data.yaml').get('nc') + get_data(d2 + '/data.yaml').get('nc')
    combineYaml(d1, d2, newNC=nc)


# getCorresponding(grabAFew('./Datasets/yolov8seg/IDREC-3.v1i.yolov8', nc=10), './balls')
def mainCombine(dataset1, dataset2):
    dataset1 = os.path.abspath(dataset1)
    dataset2 = os.path.abspath(dataset2)
    a = get_data(dataset1 + '/data.yaml')
    b = get_data(dataset2 + '/data.yaml')
    newNc = a.get('nc') + b.get('nc')
    new = ""
    for _ in range(10):
        new += str((random.randint(0, 10) % 10))

    new += str(datetime.date.today())

    fD = os.path.abspath('./CombinedDatasets')
    complete = os.path.join(fD, new)
    os.mkdir(complete)
    combineYaml(dataset1, dataset2, complete, new)
    combineFolders(dataset1, dataset2, complete)
    l1 = grabAFew(complete, newNc - 1)
    os.chdir('/Test')
    getCorresponding(l1, 'nest')


def combineBothDatasets(d1, d2):
    combineYaml(d1, d2)


getCorresponding(grabAFew(dataset='Datasets/yolov8seg/IDREC-3.v1i.yolov8', nc=9), 'balls')
