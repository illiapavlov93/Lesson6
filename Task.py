import zipfile
import itertools
import string
import os
import json


def password(file):
    myLetters = string.ascii_lowercase
    pwd_len = 3
    for i in range(0, pwd_len + 1):
        for j in map(''.join, itertools.product(myLetters, repeat=i)):
            try:
                file.extractall(pwd=str.encode(j))
                #print('\n---- password is {0} ----'.format(j))
                break
            except:
                pass


def bypass():
    folder, logs = [], []
    for i in os.walk('lesson6'):
        folder.append(i)
    for address, dirs, files in folder:
        for file in files:
            s = address + '/' + file
            #print(s)
            myfile = open(s, encoding='utf-8')
            for line in myfile:
                c = line.strip().split('\t')
                logs.append(c)
    return logs


def uniquelogs(logs):
    unique_users, unique_logs = [], []
    for line in logs:
        if line[4] not in unique_users:
            unique_users.append(line[4])
            unique_logs.append(line)
        else:
            pass
    return unique_logs


def writedown(logs, unique_logs):
    os.mkdir('lesson6/cities')
    os.chdir('lesson6/cities')
    cities = []
    counts = {}
    for line in logs:
        if line[3] not in cities:
            cities.append(line[3])
    for city in cities:
        filename = city + '.tsv'
        x = open(filename, 'tw', encoding='utf-8')
        counts.clear()
        for line in unique_logs:
            if line[3] == city:
                if line[5] not in counts.keys():
                    counts[line[5]] = 1
                else:
                    counts[line[5]] += 1
        str_json = json.dumps(counts)
        a = str_json.translate({
            ord('{'): ord(' '),
            ord(':'): ord('\t'),
            ord('}'): ord(' '),
            ord(','): ord('\n')
        })
        x.write(a)
    return


file = zipfile.ZipFile('lesson6.zip', 'r')
password(file)
logs = bypass()
unique_logs = uniquelogs(logs)
writedown(logs, unique_logs)
print('folder with number of requests by cities created')
