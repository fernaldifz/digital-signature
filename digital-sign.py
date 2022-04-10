#pair key generator
import random, math, time, os, hashlib


class KeyPair:
    def generatePairNumbers(self):
        primes = []
        p,q,counter = 0,0,0

        for i in range(2**6,2**8):
            if self.isPrime(i):
                primes.append(i)
                counter += 1

            if counter == 100:
                break

        while p == q:
            p,q = random.choice(primes),random.choice(primes)
        
        print("p dan q sudah ada")
        return p,q

    def isPrime(self,num):
        if num == 2:
            return True
        elif num < 2:
            return False
        else:
            for i in range(2,num,1):
                if num % i == 0:
                    return False
        return True

    def modInverse(self,e, phi):
        for d in range(1,phi):
            if ((e % phi) * (d % phi)) % phi == 1:
                return d

    def generatePairKey(self): #pembangkit pasangan kunci (privat dan publik)
        p,q = self.generatePairNumbers()
        N = p*q
        phi = (p-1)*(q-1)

        print("mulai cari e")

        publicKeyCandidate = []
        for e in range(2,phi//(2**8)):
            if self.isPrime(e):
                publicKeyCandidate.append(e)

        print("mulai cari d")

        e = random.choice(publicKeyCandidate)

        d = self.modInverse(e,phi)

        return (e,N),(d,N)

def encryptFile(Path, n, e): #enkripsi menggunakan RSA
    startTime = time.time()
    byteArray = openFile(Path)

    encryptArray = [0 for i in range(len(byteArray))]

    for i, value in enumerate(byteArray):
        encryptArray[i] = str(value**e % n)
    
    encryptString = " "
    encryptString = encryptString.join(encryptArray)
        
    with open("encrypted", "w") as encryptedFile:
        encryptedFile.write(encryptString)
    
    encryptTime = time.time() - startTime
    return encryptArray, encryptTime

def hashFactory(path):
    hashEngine = hashlib.new('sha1') #inisialisasi objek hash menggunakan sha-1

    with open(path, 'rb') as file: 
        fileBinary = file.read(2**16) #read per 2**16 size block
        while len(fileBinary) > 0:
            hashEngine.update(fileBinary) #update hingga EoF file / concate block block 
            fileBinary = file.read(2**16)
    
    digest = hashEngine.hexdigest()
    decimalHex = str(int(digest,16)) #jadiin string biar nggk kelamaan pas enkripsi

    return decimalHex

def decryptFile(Path, d,n): #dekripsi menggunakan RSA
    startTime = time.time()

    encryptFile = open(Path, "r").readlines()
    encryptString = encryptFile[0]
    encryptArray = encryptString.split()

    decryptArray = [0 for i in range(len(encryptArray))]
    for i, value in enumerate(encryptArray):
        decryptArray[i] = chr(int(value)**d % n)
    
    decryptString = ""
    for i in range(len(decryptArray)):
        decryptString += decryptArray[i]
    
    with open("decrypted", "w", encoding="utf-8") as decryptedFile:
        decryptedFile.write(decryptString)

    decryptTime = time.time() - startTime
    return decryptString, decryptTime

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

s = hashFactory('text-test.txt')
print(s,type(s))