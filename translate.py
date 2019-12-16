#!/usr/bin/python3
# read files, replace strings, output file
import sys
import os
import re
import ast
_map = {}
_map2 = {}
_map2new = {}
_mapUlt = {}


def openFile(filename):
    if os.path.exists(filename):
        with open(os.path.join(sys.path[0], filename), mode='r', encoding='utf-8', errors='ignore') as file:
            text = file.read()
            file.close()
            return text
    else:
        print(filename + ' do not exist')
        sys.exit()


def readDict(filename):
    if os.path.exists(filename):
        with open(os.path.join(sys.path[0], filename), mode='r', encoding='utf-8', errors='ignore') as file:
            line = file.read()
            file.close()
            return ast.literal_eval(line)
    else:
        print(filename + ' do not exist')
        sys.exit()


def writeFile(filename, text):
    with open(os.path.join(sys.path[0], filename), mode='w', encoding='utf-8', errors='ignore') as file:
        file.write(text)
        file.close()


def generateMap(inputFile, inputFile2):
    text = openFile(inputFile)
    text2 = openFile(inputFile2)
    scope = re.findall(r'.*\"(.*[\u4e00-\u9fff]+.*)\".*\"(.*)\";', text)
    for child in scope:
        _map[re.sub(r'([\u4e00-\u9fff]+.*)\".*', r'\g<1>', child[0])] = child[1]

    # for ult names
    scope2old = re.findall('奥义技能：\|(.*)\|r"] (= " \|.*)\|r', text)
    for child in scope2old:
        _map2[child[0]] = child[1]
    scope3new = re.findall('奥义技能：\|(.*)\|r"] (= " \|.*)\|r', text2)
    for child in scope3new:
        _map2new[child[0]] = child[1]
    for key in _map2new:
        _mapUlt[_map2new.get(key)] = _map2.get(key)


def replace(fromFile, toFile):
    text = openFile(fromFile)
    for key, value in _map.items():
        if text.find('"' + key + '";') != -1:
            text = text.replace('"' + key + '";', '"' + value + '";')
    for key, value in _mapUlt.items():
        if text.find(key) != -1:
            text = text.replace(key, value)
    writeFile(toFile, text)


def main():
    if len(sys.argv) == 3:
        generateMap(sys.argv[2], sys.argv[1])
        replace(sys.argv[1], 'Eng_' + sys.argv[1])
    else:
        print('Correct input format: ' + 'py translate.py CNMap EndMap')


main()
