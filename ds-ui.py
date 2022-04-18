import sys
import digitalSign as ds
from os import environ
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog


class Signing(QDialog):
    d, N = 0, 0

    def __init__(self):
        super(Signing, self).__init__()
        loadUi("Signing.ui", self)
        self.verify.clicked.connect(self.goforVerify)
        self.genKey.clicked.connect(self.gotoGenKey)
        self.signfile.clicked.connect(self.signing)
        self.selectfile.clicked.connect(self.selectFile)
        self.selectkey.clicked.connect(self.selectKey)
        self.savefile.clicked.connect(self.saveSign)
        self.savesignature.clicked.connect(self.saveDigitalSignature)

    def saveDigitalSignature(self):
        if len(self.file.toPlainText()) != 0:
            self.warn_red.setText("")
            option = QFileDialog.Options()
            option |= QFileDialog.DontUseNativeDialog

            file = QFileDialog.getSaveFileName(
                widget, "Save Digital Signature", "signature", "All Files (*)", options=option)

            if file[0] != '':
                file1 = open(file[0], "w", encoding="utf-8")
                digitalSignature = ds.readSignatureInMessage("dummy.txt")
                file1.write(digitalSignature)
                file1.close()
                self.warn_green.setText("Digital Signature has been saved !")
        else:
            self.warn_red.setText("Select file first !")
        pass

    def gotoGenKey(self):
        genKeyPair = GenKey()
        widget.addWidget(genKeyPair)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def selectKey(self):
        self.warn_red.setText("")
        self.warn_green.setText("")
        option = QFileDialog.Options()
        file = QFileDialog.getOpenFileName(
            widget, "Open Private Key", "Default File", "*.pri", options=option)

        if file[0] != '':
            tuples = open(file[0], 'r')
            key = tuples.read()
            tuples.close()

            d, N = ds.unpackKeyTuples(key)

            self.d = d
            self.N = N

        self.key.setWordWrap(True)
        self.key.setText(file[0])

    def selectFile(self):
        if self.key.text() != "":
            self.warn_red.setText("")
            self.warn_green.setText("")
            option = QFileDialog.Options()
            file = QFileDialog.getOpenFileName(
                widget, "Open file for signing", "Default File", "All Files (*)", options=option)
            if file[0] != '':
                with open(file[0], "r") as file:
                    lines = file.readlines()
                text = ''

                for line in lines:
                    text += line

                self.file.setText(text)
        else:
            self.warn_red.setText("Select key First!")

    def signing(self):
        if self.file.toPlainText() != "":
            self.warn_red.setText("")
            self.warn_green.setText("")
            text = self.file.toPlainText()
            with open('dummy.txt', 'w') as file:
                file.write("")
            with open('dummy.txt', 'w') as file:
                file.write(text)

            ds.signingSameFile('dummy.txt', self.N, self.d)

            with open('dummy.txt', 'r') as file:
                lines = file.readlines()

            text = ''

            for line in lines:
                text += line
            print(text)
            self.file.setText(text)
        else:
            self.warn_red.setText("Select file First!")

    def goforVerify(self):
        verifying = Verify()
        widget.addWidget(verifying)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def saveSign(self):
        if len(self.file.toPlainText()) != 0:
            self.warn_red.setText("")
            option = QFileDialog.Options()
            option |= QFileDialog.DontUseNativeDialog

            file = QFileDialog.getSaveFileName(
                widget, "Save Encryption", "signedText.txt", "All Files (*)", options=option)

            if file[0] != '':
                file1 = open(file[0], "w", encoding="utf-8")
                file2 = open("dummy.txt", "r", encoding="utf-8")
                digitalSignature = file2.read()
                file1.write(digitalSignature)
                file1.close()
                file2.close()
                self.warn_green.setText("File has been saved !")
        else:
            self.warn_red.setText("Select file first !")


class Verify(QDialog):
    e, N = 0, 0

    def __init__(self):
        super(Verify, self).__init__()
        loadUi("Verify.ui", self)
        self.signing.clicked.connect(self.goforSigning)
        self.selectfile.clicked.connect(self.selectFile)
        self.verify.clicked.connect(self.verifying)
        self.genKey.clicked.connect(self.gotoGenKey)
        self.selectkey.clicked.connect(self.selectKey)

    def selectKey(self):
        self.warn_red.setText("")
        self.warn_green.setText("")
        option = QFileDialog.Options()
        file = QFileDialog.getOpenFileName(
            widget, "Open Key", "Default File", "*.pub", options=option)

        if file[0] != '':
            tuples = open(file[0], 'r')
            key = tuples.read()
            tuples.close()

            e, N = ds.unpackKeyTuples(key)

            self.e = e
            self.N = N
            print(self.e, self.N)

        self.key.setWordWrap(True)
        self.key.setText(file[0])

    def selectFile(self):
        if self.key.text() != "":
            self.warn_red.setText("")
            self.warn_green.setText("")
            option = QFileDialog.Options()
            file = QFileDialog.getOpenFileName(
                widget, "Open file for signing", "Default File", "All Files (*)", options=option)
            if file[0] != '':
                with open(file[0], "r") as file:
                    lines = file.readlines()
                text = ''

                for line in lines:
                    text += line
                with open('dummyVerify.txt', 'w') as file:
                    file.write(text)
                self.file.setText(text)
        else:
            self.warn_red.setText("Select key First!")

    def goforSigning(self):
        sign = Signing()
        widget.addWidget(sign)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def verifying(self):
        if self.file.toPlainText() != "":
            self.warn_red.setText("")
            self.warn_green.setText("")
            text = self.file.toPlainText()
            with open('dummyVerify.txt', 'w') as file:
                    file.write(text)
            with open('dummyVerify.txt', 'r') as file:
                ds.verifyingSameFile('dummyVerify.txt', self.e, self.N)
        else:
            self.warn_red.setText("Select File First!")

    def gotoGenKey(self):
        genKeyPair = GenKey()
        widget.addWidget(genKeyPair)
        widget.setCurrentIndex(widget.currentIndex()+1)


class GenKey(QDialog):
    def __init__(self):
        super(GenKey, self).__init__()
        loadUi("GenKey.ui", self)
        self.sign.clicked.connect(self.goforSigning)
        self.verify.clicked.connect(self.goforVerifying)
        self.genKey.clicked.connect(self.genKeyPair)
        self.savePri.clicked.connect(self.savePriKey)
        self.savePub.clicked.connect(self.savePubKey)

    def savePubKey(self):
        if len(self.N.text()) != 0:
            option = QFileDialog.Options()
            option |= QFileDialog.DontUseNativeDialog

            file = QFileDialog.getSaveFileName(
                widget, "Save File Window Title", "publicKey.pub", "*.pub", options=option)

            if file[0] != '':
                file = open(file[0], "w", encoding="utf-8")
                file.write('(' + self.e.text() + ',' + self.N.text() + ')')
                file.close()

    def savePriKey(self):
        if len(self.N.text()) != 0:
            option = QFileDialog.Options()
            option |= QFileDialog.DontUseNativeDialog

            file = QFileDialog.getSaveFileName(
                widget, "Save File Window Title", "privateKey.pri", "*.pri", options=option)
            if file[0] != '':
                file = open(file[0], "w", encoding="utf-8")
                file.write('(' + self.d.text() + ',' + self.N.text() + ')')
                file.close()

    def genKeyPair(self):
        pubKey, privKey = ds.generatePairKey()
        e, N = pubKey
        d, N = privKey

        self.e.setText(str(e))
        self.d.setText(str(d))
        self.N.setText(str(N))

    def goforSigning(self):
        sign = Signing()
        widget.addWidget(sign)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def goforVerifying(self):
        verifying = Verify()
        widget.addWidget(verifying)
        widget.setCurrentIndex(widget.currentIndex()+1)


def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


def run():
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")


suppress_qt_warnings()
app = QApplication(sys.argv)
menu = GenKey()
widget = QtWidgets.QStackedWidget()
widget.addWidget(menu)
widget.setFixedHeight(512)
widget.setFixedWidth(720)

run()
