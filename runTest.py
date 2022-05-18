import importlib
import os
import subprocess
from time import sleep


def main():
    wd = os.path.join(os.getcwd(), 'memTestRead')
    if not os.path.exists(wd):
        os.makedirs(wd)
        
    fileNamePrefix = 'memTestRead/memread'
    for i in range(3):
        fileNameBase = fileNamePrefix + str(i)
        for ii in range(8):
            fileName = fileNameBase + '-' + str(ii) + '.txt'
            subprocess.Popen('python3 testCase.py ' + str(i + 1) + ' > ' + fileName, shell=True)

        sleep(480)


if __name__ == '__main__':
    main()
