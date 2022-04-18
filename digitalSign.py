import random
import time
import hashlib
from tkinter import messagebox


def generatePairNumbers():
    primes = []
    p, q, counter = 0, 0, 0

    for i in range(2**16, 2**64):
        if isPrime(i):
            primes.append(i)
            counter += 1

        if counter == 100:
            break

    while p == q:
        p, q = random.choice(primes), random.choice(primes)

    print("p dan q sudah ada")
    return p, q


def isPrime(num):
    if num == 2:
        return True
    elif num < 2:
        return False
    else:
        for i in range(2, num, 1):
            if num % i == 0:
                return False
    return True


def modInverse(e, phi):
    for d in range(1, phi):
        if ((e % phi) * (d % phi)) % phi == 1:
            return d


def generatePairKey():  # pembangkit pasangan kunci (privat dan publik)
    p, q = generatePairNumbers()
    N = p*q
    phi = (p-1)*(q-1)

    print("mulai cari e")

    publicKeyCandidate = []
    for e in range(2, phi//(2**64)):
        if isPrime(e):
            publicKeyCandidate.append(e)

    print("mulai cari d")

    e = random.choice(publicKeyCandidate)

    d = modInverse(e, phi)

    return (e, N), (d, N)


def generateHash(message):
    # inisialisasi objek hash menggunakan sha-1
    hashEngine = hashlib.new('sha1')

    with open(message, "r") as file:
        lines = file.readlines()
        hashTemp = lines
    with open(message, "w") as file:
        for line in lines:
            # if line.strip("\n") != '<ds>':
            if not line.rstrip('\n').startswith('<ds>') and not line.rstrip('\n').endswith('</ds>'):
                file.write(line)
                # print('aku ditambah : ' + line)

    with open(message, "r") as file:
        lines = file.readlines()
    with open(message, "w") as file:
        for line in lines:
            if line == lines[-1]:
                file.write(line.strip())
            else:
                file.write(line)

    with open(message, 'rb') as file:
        fileBinary = file.read(2**16)  # read per 2**16 size block

        while (len(fileBinary) > 0):
            # update hingga EoF file / concate block block

            hashEngine.update(fileBinary)
            fileBinary = file.read(2**16)

    digest = hashEngine.hexdigest()
    # jadiin string biar nggk kelamaan pas enkripsi
    decimalHex = str(int(digest, 16))

    with open("hash", "w") as hashedFile:
        hashedFile.write(decimalHex)

    with open(message, "w") as file:
        for line in hashTemp:
            file.write(line)

    return decimalHex


def encryptDigest(n, key):  # enkripsi menggunakan RSA
    byteArray = openFile('hash')
    signatureArray = [0 for i in range(len(byteArray))]

    for i, value in enumerate(byteArray):
        signatureArray[i] = str(value**key % n)

    # print(signatureArray)
    signatureString = " "
    signatureString = signatureString.join(signatureArray)

    # print("ini enkripsi hash : ", signatureString)

    return signatureString


def decryptDigest(signatureArray, key, n):  # dekripsi menggunakan RSA
    # startTime = time.time()

    messageDigestArray = [0 for i in range(len(signatureArray))]
    for i, value in enumerate(signatureArray):
        messageDigestArray[i] = chr(int(value)**key % n)

    messageDigestString = ""
    for i in range(len(messageDigestArray)):
        messageDigestString += messageDigestArray[i]

    # with open("messageDigest", "w", encoding="utf-8") as messageDigestFile:
    #    messageDigestFile.write(messageDigestString)

    # decryptTime = time.time() - startTime
    return messageDigestString


def createSignature(message, n, d):  # Pengirim membuat signature
    generateHash(message)
    signatureString = encryptDigest(n, d)
    return signatureString


def saveSignatureToFile(signatureString):
    with open("signature", "w") as signatureFile:
        signatureFile.write(signatureString)


def joinSignatureToMessage(pathMessage, signatureString):
    with open(pathMessage) as messageFile:
        lines = messageFile.readlines()
        signatureJoined = False
        for line in lines:
            if line.rstrip('\n').startswith('<ds>') and line.rstrip('\n').endswith('</ds>'):
                signatureJoined = True

    if (signatureJoined):
        numberLines = sum(1 for line in open(pathMessage))
        with open(pathMessage, 'r') as messageFile:
            data = messageFile.readlines()
        data[numberLines-1] = "<ds>" + signatureString + "</ds>"

        with open(pathMessage, 'w') as messageFile:
            messageFile.writelines(data)
    else:
        with open(pathMessage, "a") as messageFile:
            messageFile.write("\n")
            messageFile.write("<ds>" + signatureString + "</ds>")


def readSignatureInMessage(message):
    with open(message) as messageFile:
        lines = messageFile.readlines()
        signatureJoined = False
        for line in lines:
            if line.rstrip('\n').startswith('<ds>') and line.rstrip('\n').endswith('</ds>'):
                signatureJoined = True

    # ngecek jumlah newlines di txt
    numberLines = len(lines)

    if (signatureJoined):
        with open(message, 'r') as messageFile:
            data = messageFile.readlines()
            data = data[numberLines-1]
        # ceritanya menghilangkan <ds> dan </ds>, jadi dapat isinya aja
        signatureInMessage = data[4:len(data) - 5:]
        return signatureInMessage
    else:
        messagebox.showinfo(
            "Warning", "Tidak ada digital signature di message, gagal melihat digital signature")


def deleteSignatureInMessage(message):
    with open(message, "r") as messageFile:
        lines = messageFile.readlines()
        signatureJoined = False
        for line in lines:
            if line.rstrip('\n').startswith('<ds>') and line.rstrip('\n').endswith('</ds>'):
                signatureJoined = True

    if(signatureJoined == False):
        messagebox.showinfo(
            "Warning", "Tidak ada digital signature di message, gagal menghapus digital signature")
    else:
        i = 0
        with open(message, "w") as messageFile:
            for line in lines:
                if not line.rstrip('\n').startswith('<ds>') and not line.rstrip('\n').endswith('</ds>'):
                    if(i != len(lines)-2):
                        messageFile.write(line)
                    else:
                        messageFile.write(line.rstrip('\n'))
                    i += 1


def signingOtherFile(message, n, d):
    signatureString = createSignature(message, n, d)
    saveSignatureToFile(signatureString)


def verifyingOtherFile(messageSent, signature, e, n):  # Penerima melakukan verifikasi
    generateHash(messageSent)
    hashFile = open('hash', "r").readlines()
    hashString = hashFile[0]

    signatureFile = open(signature, "r").readlines()
    signatureString = signatureFile[0]
    signatureArray = signatureString.split()
    digest = decryptDigest(signatureArray, e, n)

    if hashString == digest:  # ceritanya mau ngecek pesan ini asli apa nggk
        print("pesan asli")
    else:
        messagebox.showinfo(
            "Warning", "Pesan atau tanda-tangan digital telah diganti!")


def signingSameFile(message, n, d):
    signatureString = createSignature(message, n, d)
    joinSignatureToMessage(message, signatureString)


def verifyingSameFile(messageSent, e, n):
    signatureArray = readSignatureInMessage(messageSent).split()

    digest = decryptDigest(signatureArray, e, n)

    generateHash(messageSent)
    hashFile = open('hash', "r").readlines()
    hashString = hashFile[0]

    if hashString == digest:  # ceritanya mau ngecek pesan ini asli apa nggk
        messagebox.showinfo(
            "Warning", "Pesan asli!")
    else:
        messagebox.showinfo(
            "Warning", "Pesan atau tanda-tangan digital telah diganti!")


def unpackKeyTuples(string):
    sX, sY = '', ''

    for idx in range(0, string.index(',')):
        if string[idx] != "(":
            sX += string[idx]

    for idx in range(string.index(',')+1, len(string)):
        if string[idx] != ")":
            sY += string[idx]

    return int(sX), int(sY)


def openFile(Path):
    file = open(Path, "rb")
    data = file.read()
    file.close()

    byteArray = bytearray(data)
    return byteArray

# kP = KeyPair()
# keys = kP.generatePairKey()
# print(keys)


#############
# SEMENTARA #
n = 3337
e = 79
d = 1019
#############

# KASUS 1, signature di file terpisah
#signingOtherFile('message.txt', n, d)
#verifyingOtherFile('message.txt', 'signature', e, n)

# KASUS 2, signature di message (file sama)
# signingSameFile('message.txt', n, d)
# verifyingSameFile('message.txt', e, n)

# deleteSignatureInMessage('message.txt')
