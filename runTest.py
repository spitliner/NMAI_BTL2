import importlib
import subprocess
from time import sleep

def main():
    fileNamePrefix = 'memTestRead/memread'
    fileNameBase = ''
    fileName = ''
    for i in range(3):
        fileNameBase = fileNamePrefix + str(i)
        for ii in range(8):
            fileName = fileNameBase + '-' + str(ii) + 'txt'
            subprocess.Popen('python3 testCase.py ' + str(i + 1) + ' > '+ fileName, shell=True)

        sleep(480)    

if __name__ == '__main__':
    main()