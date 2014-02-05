__author__ = 'christue'



def readFile():
    byteFile = []
    with open('pink_panther.au', 'rb') as musicFile:
        while True:
            byte = musicFile.read(1).encode('hex')
            if not byte:
                break
            byteFile.append(int(byte, 16))
    musicFile.close()
    return byteFile


def writeFile(byteFile):
    with open('destFile.au', 'wb') as musicFile:
        musicFile.write(bytearray(byteFile))
    musicFile.close()


filearray =readFile()
writeFile(filearray)