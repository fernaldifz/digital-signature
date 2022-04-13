import random
import time
import hashlib


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


def generateHash(path):
    # inisialisasi objek hash menggunakan sha-1
    hashEngine = hashlib.new('sha1')
    with open(path, 'rb') as file:
        fileBinary = file.read(2**16)  # read per 2**16 size block
        while len(fileBinary) > 0:
            # update hingga EoF file / concate block block
            hashEngine.update(fileBinary)
            fileBinary = file.read(2**16)

    digest = hashEngine.hexdigest()
    # jadiin string biar nggk kelamaan pas enkripsi
    decimalHex = str(int(digest, 16))

    with open("hash", "w") as hashedFile:
        hashedFile.write(decimalHex)

    # return decimalHex  # optional, mau dikomen juga gpp soalnya udah disimpen di file 'hash'


def encryptDigest(n, e):  # enkripsi menggunakan RSA
    # startTime = time.time()
    byteArray = openFile('hash')

    signatureArray = [0 for i in range(len(byteArray))]

    for i, value in enumerate(byteArray):
        signatureArray[i] = str(value**e % n)

    signatureString = " "
    signatureString = signatureString.join(signatureArray)

    with open("signature", "w") as signatureFile:
        signatureFile.write(signatureString)

    # encryptTime = time.time() - startTime
    # return signatureArray


def decryptDigest(d, n):  # dekripsi menggunakan RSA
    # startTime = time.time()

    signatureFile = open('signature', "r").readlines()
    signatureString = signatureFile[0]
    signatureArray = signatureString.split()

    messageDigestArray = [0 for i in range(len(signatureArray))]
    for i, value in enumerate(signatureArray):
        messageDigestArray[i] = chr(int(value)**d % n)

    messageDigestString = ""
    for i in range(len(messageDigestArray)):
        messageDigestString += messageDigestArray[i]

    with open("messageDigest", "w", encoding="utf-8") as messageDigestFile:
        messageDigestFile.write(messageDigestString)

    # decryptTime = time.time() - startTime
    # return messageDigestString


def signing(Path, n, e):  # Pengirim membuat signature
    generateHash(Path)
    encryptDigest(n, e)


def verifying(Path, d, n):  # Penerima melakukan verifikasi
    generateHash(Path)
    decryptDigest(d, n)

    hash = openFile("hash")
    digest = openFile("messageDigest")

    print(hash)
    print(digest)

    if hash == digest:  # ceritanya mau ngecek pesan ini asli apa nggk
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
signing('message.txt', n, e)
verifying('message.txt', d, n)
