import os
import random
import time
from datetime import date

import yaml
import shutil


def combineYaml(dataset1, dataset2=None, newDir='CombinedDatasets', name='data', overwrite=False, newNC=0, b=None):

    newDir = os.path.abspath(newDir)
    if b is None:
        b = list()
    newDir2 = str(newDir) + "2"
    data1_yaml = dataset1 + '/data.yaml'
    if not overwrite:
        data2_yaml = dataset2 + '/data.yaml'

        print(f'Combining {dataset1} and {dataset2} in directory {newDir} with name {name}.')
    os.open(os.path.join(newDir, 'data.yaml'), os.O_CREAT)
    new_yaml = open(os.path.join(newDir, 'data.yaml'), 'a')


    new_yaml.write('train: ./train/images\n')
    # new_yaml.write('train: \n')
    # new_yaml.write(f'   - ./data/train/images\n')
    # new_yaml.write(f'   - ./data2/train/images\n')
    new_yaml.write('val: ./valid/images\n')
    # new_yaml.write('val: \n')
    # new_yaml.write(f'   - ./data/valid/images\n')
    # new_yaml.write(f'   - ./data2/valid/images\n')
    # new_yaml.write('test:\n')
    # new_yaml.write(f'   - ./data/test/images\n')
    # new_yaml.write(f'   - ./data2/test/images\n')
    new_yaml.write('test: ./test/images \n')
    data1 = get_data(data1_yaml)
    if not overwrite:
        data2 = get_data(data2_yaml)

        newNC = data1.get('nc') + data2.get('nc')
        newNames = data1.get('names') + data2.get('names')
        x = []
        for i in newNames:
            x.append(i)
        print(x)

    new_yaml.write('\n')
    new_yaml.write('nc: ' + str(newNC) + '\n')
    if not overwrite:
        new_yaml.write('names: ' + str(x))
    else:
        newNames = b + data1.get('names')
        x = []
        for i in newNames:
            x.append(i)
        new_yaml.write('names: ' + str(x))
    new_yaml.close()
    print('Done.')
    return newDir


def combineFolders(dataset1, dataset2, newDir):
    newDir = os.path.abspath(newDir)
    valid_dirs = ['train', 'valid', 'test']
    print(f'Combining datasets, this may take a while.')
    moveData(dataset1, newDir)
    print(str(dataset1))
    # What's funny is that the code WILL NOT WORK WITHOUT THIS?
    # WHY, WHY Python? I know there is nothing wrong here with my code, I SPENT ALLL DAY, trying to find the issue with
    # This code, there was none, there was an issue with moving too many files at once
    time.sleep(.1)
    moveData(dataset2, newDir)
    print(str(dataset2))
    print(f'Done. Results saved at {newDir}')
    return newDir


def moveData(dataset, newDir):
    dataset = os.path.abspath(dataset)
    valid_dirs = ['train', 'valid', 'test']
    if valid_dirs.__contains__('valid'):
        shutil.copytree(os.path.join(dataset, 'valid'), os.path.join(newDir, 'valid'), dirs_exist_ok=True)
        time.sleep(.1)
    if valid_dirs.__contains__('test'):
        shutil.copytree(os.path.join(dataset, 'test'), os.path.join(newDir, 'test'), dirs_exist_ok=True)
        time.sleep(.1)
    if valid_dirs.__contains__('train'):
        shutil.copytree(os.path.join(dataset, 'train'), os.path.join(newDir, 'train'), dirs_exist_ok=True)
        time.sleep(.1)




def checkFolders(d1, d2):
    tryList = ['test', 'train', 'valid']
    exist1 = []
    exist2 = []
    for i in tryList:
        try:
            os.chdir(os.path.join(d1, i))
            exist1.append(i)
        except FileNotFoundError:
            pass
    if d2 is not None:
        for i in tryList:
            try:
                os.chdir(os.path.join(d2, i))
                exist2.append(i)
            except FileNotFoundError:
                pass
        return set(exist1) & set(exist2)
    else:
        return exist1


def get_data(dataset):
    with open(dataset, 'r') as f:
        data = yaml.full_load(f)
    return data

#TODO Change this to be dynamic with combining datasets that have many classes
def fixLabels(dataset, nc=1, listdata=('train', 'valid', 'test')):
    for i in listdata:
        for fn in os.listdir(os.path.join(os.path.abspath(dataset), f'{i}/labels')):
            print(os.path.join(os.path.join(os.path.abspath(dataset), f'{i}/labels'), fn))
            path = os.path.join(os.path.join(os.path.abspath(dataset), f'{i}/labels'), fn)
            with open(path, 'r') as file:
                data = file.read()
                count = 0
                for x in data:
                    if x != " ":
                        count += 1
                    else:
                        break
                new_data = str(nc) + data[count:]
                file.close()
                with open(path, 'w') as filew:
                    filew.write(new_data)
                    filew.close()
                file.close()

# For future refrence, add a check to see if the combined datasets are being used for a pretrained model becaue the added
# Dataset needs to be second.


#fixLabels('Datasets/yolov8seg/IDREC-3-ONESHOTS 2.v2i.yolov8', 10)
#moveData('Datasets/yolov8seg/IDREC-3.v1i.yolov8', os.path.abspath('./CombinedDatasets'))
#combineFolders('Datasets/yolov8seg/IDREC-3.v1i.yolov8',
     #          'Datasets/yolov8seg/IDREC-3-ONESHOTS 2.v2i.yolov8', os.path.abspath('./CombinedDatasets/1'))