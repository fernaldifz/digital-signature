import random
import time
import hashlib

from sqlalchemy import false


class KeyPair:
    def generatePairNumbers(self):
        primes = []
        p, q, counter = 0, 0, 0

        for i in range(2**6, 2**8):
            if self.isPrime(i):
                primes.append(i)
                counter += 1

            if counter == 100:
                break

        while p == q:
            p, q = random.choice(primes), random.choice(primes)

        print("p dan q sudah ada")
        return p, q

    def isPrime(self, num):
        if num == 2:
            return True
        elif num < 2:
            return False
        else:
            for i in range(2, num, 1):
                if num % i == 0:
                    return False
        return True

    def modInverse(self, e, phi):
        for d in range(1, phi):
            if ((e % phi) * (d % phi)) % phi == 1:
                return d

    def generatePairKey(self):  # pembangkit pasangan kunci (privat dan publik)
        p, q = self.generatePairNumbers()
        N = p*q
        phi = (p-1)*(q-1)

        print("mulai cari e")

        publicKeyCandidate = []
        for e in range(2, phi//(2**8)):
            if self.isPrime(e):
                publicKeyCandidate.append(e)

        print("mulai cari d")

        e = random.choice(publicKeyCandidate)

        d = self.modInverse(e, phi)

        return (e, N), (d, N)


def generateHash(message):
    # inisialisasi objek hash menggunakan sha-1
    hashEngine = hashlib.new('sha1')
    
    with open(message, "r") as file:
        lines = file.readlines()
    with open(message, "w") as file:
        for line in lines:
            # if line.strip("\n") != '<ds>':
            if not line.rstrip('\n').startswith('<ds>') and not line.rstrip('\n').endswith('</ds>'):
                file.write(line)
                print('aku ditambah : ' + line)
    
    
    with open(message, "r") as file:
        lines = file.readlines()
        print(lines)
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

    return decimalHex

def encryptDigest(n, e):  # enkripsi menggunakan RSA
    byteArray = openFile('hash')
    signatureArray = [0 for i in range(len(byteArray))]

    for i, value in enumerate(byteArray):
        signatureArray[i] = str(value**e % n)

    print(signatureArray)
    signatureString = " "
    signatureString = signatureString.join(signatureArray)

    print("ini enkripsi hash : ", signatureString)

    return signatureString


def decryptDigest(signature, d, n):  # dekripsi menggunakan RSA
    # startTime = time.time()

    signatureFile = open(signature, "r").readlines()
    signatureString = signatureFile[0]
    signatureArray = signatureString.split()

    messageDigestArray = [0 for i in range(len(signatureArray))]
    for i, value in enumerate(signatureArray):
        messageDigestArray[i] = chr(int(value)**d % n)

    messageDigestString = ""
    for i in range(len(messageDigestArray)):
        messageDigestString += messageDigestArray[i]

    # with open("messageDigest", "w", encoding="utf-8") as messageDigestFile:
    #    messageDigestFile.write(messageDigestString)

    # decryptTime = time.time() - startTime
    print(messageDigestString)
    return messageDigestString


def createSignature(message, n, e):  # Pengirim membuat signature
    generateHash(message)
    signatureString = encryptDigest(n, e)
    return signatureString


def saveSignature(signatureString):
    with open("signature", "w") as signatureFile:
        signatureFile.write(signatureString)


def joinSignatureToMessage(pathMessage, signatureString):
    with open(pathMessage) as messageFile:
        if "<ds>" in messageFile.read():
            signatureJoined = True
        else:
            signatureJoined = False

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
        if "<ds>" in messageFile.read():  # cari <ds>
            signatureJoined = True
        else:
            signatureJoined = False

    # ngecek jumlah newlines di txt
    numberLines = sum(1 for line in open(message))

    if (signatureJoined):
        with open(message, 'r') as messageFile:
            data = messageFile.readlines()
            data = data[numberLines-1]
        # ceritanya menghilangkan <ds> dan </ds>, jadi dapat isinya aja
        signatureInMessage = data[4:len(data) - 5:]
        return signatureInMessage


def signing(message, n, e):
    signatureString = createSignature(message, n, e)
    saveSignature(signatureString)


def verifying(messageSent, signature, d, n):  # Penerima melakukan verifikasi
    generateHash(messageSent)
    hashFile = open('hash', "r").readlines()
    hashString = hashFile[0]

    digest = decryptDigest(signature, d, n)

    if hashString == digest:  # ceritanya mau ngecek pesan ini asli apa nggk
        print("Pesan asli")
    else:
        print("Pesan telah diganti")


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

# def encryptDecryptFile(n, e, d):
#     enc,etime = encryptFile("text-test.txt", n, e)
#     print("array enkripsi: ", enc)
#     print("time : ",round(etime,4))
#     dec, dtime = decryptFile("encrypted", d,n)
#     print("array dekripsi : ", dec)

# encryptDecryptFile(n, e, d)

# kalo mau test keaslian pesan, hilangin char paling akhir aja buat test
# komen aja kalo mau test keaslian pesan terus ganti .txt nya

# KASUS 1, signature di file terpisah
# signing('message.txt', n, e)
# verifying('message.txt', 'signature', d, n)

# KASUS 2
# generateHash('message.txt')
signature = createSignature('message.txt', n, e)
joinSignatureToMessage('message.txt', signature)
print(readSignatureInMessage('message.txt'))
# verifying('message.txt', 'signature', d, n)
