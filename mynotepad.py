#QTPY

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtCore

# 단어 찾기 팝업
class findWindow(QDialog):
    def __init__(self, parent):
        super(findWindow, self).__init__(parent)
        uic.loadUi('find.ui', self)
        self.show()

        self.parent = parent
        self.cursor = parent.mytext.textCursor()
        self.pe = parent.mytext

        self.pushButton_findnext.clicked.connect(self.findNext)
        self.pushButton_cancle.clicked.connect(self.close)

        self.radioButton_down.clicked.connect(self.updown_radio_button)
        self.radioButton_up.clicked.connect(self.updown_radio_button)
        self.up_down = "down"

    # 위 아래 이동 버튼
    def updown_radio_button(self):
        if self.radioButton_up.isChecked():
            self.up_down = "up"
        elif self.radioButton_down.isChecked():
            self.up_down = "down"

    # 키 입력시 작동하는 함수
    def keyReleaseEvent(self, event):
        if self.lineEdit.text():
            self.pushButton_findnext.setEnabled(True)
        else:
            self.pushButton_findnext.setEnabled(False)

    # 검색
    def findNext(self):
        pattern = self.lineEdit.text()
        text = self.pe.toPlainText()
        reg = QtCore.QRegExp(pattern)
        self.cursor = self.parent.mytext.textCursor()

        if self.checkBox_CaseSenesitive.isChecked():
            # 대소문자 구분하기
            cs = QtCore.Qt.CaseSensitive
        else:
            # 대소문자 구분 안하기
            cs = QtCore.Qt.CaseInsensitive

        reg.setCaseSensitivity(cs)
        pos = self.cursor.position()
        # 검색
        index = reg.indexIn(text, 0)

        # 검색된 결과가 있다면
        if index != -1:
            self.setCursor(index, len(pattern) + index)

    # 해당 단어 위치로 커서 조절
    def setCursor(self, start, end):
        # 앞에 커서 조절
        self.cursor.setPosition(start)
        # 뒤로 커서 조절
        self.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end - start)
        self.pe.setTextCursor(self.cursor)

    # 종료시 자동으로 검색
    def closeEvent(self, event):
        self.findNext()

# 저장 확인 팝업
class LoadCheckDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.save = False

    def setupUI(self):
        self.setGeometry(800, 500, 300, 150)
        self.setWindowTitle("PT`s NotePad")
        self.setWindowIcon(QIcon('profile.jpg'))

        saveText = QLabel("Save Change?")

        self.pushButton1= QPushButton("Save")
        self.pushButton1.clicked.connect(self.pushButton1Clicked)
        self.pushButton2= QPushButton("No Save")
        self.pushButton2.clicked.connect(self.pushButton2Clicked)

        layout = QGridLayout()
        layout.addWidget(saveText, 0, 1)
        layout.addWidget(self.pushButton1, 1, 0)
        layout.addWidget(self.pushButton2, 1, 2)

        self.setLayout(layout)

    # 저장하기
    def pushButton1Clicked(self):
        self.save = True
        self.close()

    # 저장하지 않음
    def pushButton2Clicked(self):
        self.save = False
        self.close()

# 끝내기 전 저장 확인 팝업
class ExitCheckDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.save = False
        self.exit = False

    def setupUI(self):
        self.setGeometry(800, 500, 300, 150)
        self.setWindowTitle("PT`s NotePad")
        self.setWindowIcon(QIcon('profile.jpg'))

        saveText = QLabel("Save Change?")

        self.pushButton1= QPushButton("Save")
        self.pushButton1.clicked.connect(self.pushButton1Clicked)
        self.pushButton2= QPushButton("No Save")
        self.pushButton2.clicked.connect(self.pushButton2Clicked)
        self.pushButton3 = QPushButton("Cancel")
        self.pushButton3.clicked.connect(self.pushButton3Clicked)

        layout = QGridLayout()
        layout.addWidget(saveText, 0, 1)
        layout.addWidget(self.pushButton1, 1, 0)
        layout.addWidget(self.pushButton2, 1, 1)
        layout.addWidget(self.pushButton3, 1, 2)

        self.setLayout(layout)

    # 저장하기
    def pushButton1Clicked(self):
        self.save = True
        self.exit = True
        self.close()

    # 저장하지 않음
    def pushButton2Clicked(self):
        self.save = False
        self.exit = True
        self.close()

    # 종료
    def pushButton3Clicked(self):
        self.save = False
        self.exit = False
        self.close()

# 메인 화면
class MyNotePad(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setWindowTitle("No Title")
        self.setWindowIcon(QIcon('profile.jpg'))
        menubar = self.menuBar()
        self.fileLocation = ''
        self.originaltitle = 'No Title'
        self.isdefault = True

        Filemenu = menubar.addMenu("File")
        Filemenu1 = menubar.addMenu("Edit")
        Filemenu2 = menubar.addMenu("Etc")

        loadfile = QAction('Open', self)
        savefile = QAction('Save', self)
        saveas = QAction('Save As', self)
        exit = QAction('Exit', self)

        loadfile.setShortcut('Ctrl+D')
        savefile.setShortcut('Ctrl+S')
        saveas.setShortcut('Ctrl+Shift+S')
        exit.setShortcut('Esc')

        loadfile.triggered.connect(self.add_open)
        savefile.triggered.connect(self.add_save)
        saveas.triggered.connect(self.add_save_as)
        exit.triggered.connect(self.add_exit)
        Filemenu.addAction(loadfile)
        Filemenu.addAction(savefile)
        Filemenu.addAction(saveas)
        Filemenu.addAction(exit)

        undo = QAction('Undo', self)
        redo = QAction('Redo', self)
        copy = QAction('Copy', self)
        paste = QAction('Paste', self)

        undo.setShortcut('Ctrl+Z')
        redo.setShortcut('Ctrl+Y')
        copy.setShortcut('Ctrl+C')
        paste.setShortcut('Ctrl+V')

        undo.triggered.connect(self.Undo)
        redo.triggered.connect(self.Redo)
        copy.triggered.connect(self.Copy)
        paste.triggered.connect(self.Paste)

        Filemenu1.addAction(undo)
        Filemenu1.addAction(redo)
        Filemenu1.addAction(copy)
        Filemenu1.addAction(paste)

        font = QAction('Font', self)
        find = QAction('Find', self)
        find.setShortcut('Ctrl+F')
        font.triggered.connect(self.add_font)
        find.triggered.connect(self.add_find)
        Filemenu2.addAction(font)
        Filemenu2.addAction(find)

        self.mytext = QTextEdit(self)
        self.mytext.setAcceptRichText(True)
        self.setCentralWidget(self.mytext)
        self.originaltext = ''
        self.ischange = False

        # 현재 날짜 정보 상태표시줄 표시
        self.date = QDate.currentDate()
        self.statusBar().showMessage(self.date.toString(Qt.DefaultLocaleLongDate))

        self.show()

    # 내용이 바뀌면 제목에 * 추가
    def keyReleaseEvent(self, event):
        if self.ischange:
            return

        if self.CheckText():
            self.SetTitle('*')
            self.ischange = True

    # 종료 전 저장 여부 확인
    def closeEvent(self, event):
        if self.ischange:
            dlg = ExitCheckDialog()
            dlg.exec_()

            if dlg.save:
                self.add_save()
                self.SetTitle()

            if dlg.exit:
                qApp.quit()
            else:
                event.ignore()

    # 파일 열기
    def add_open(self):
        if self.ischange:
            dlg = LoadCheckDialog()
            dlg.exec_()

            if dlg.save:
                self.add_save()
                self.SetTitle()

        FileOpen = QFileDialog.getOpenFileName(self, 'Open File', './', "텍스트 파일(*.txt)")

        if FileOpen != ('', ''):
            self.fileLocation = FileOpen[0]
            f = open(FileOpen[0], 'r')
            self.SetTitle(FileOpen[0])
            textcontenct = f.read()
            self.mytext.setText(textcontenct)
            self.originaltext = self.mytext.toPlainText()
            self.SetTitle()
            f.close()

    # 파일 저장
    def add_save(self):
        if self.CheckTitle():
            textcontent = self.mytext.toPlainText()
            f = open(self.fileLocation, 'w')
            f.write(textcontent)
            self.originaltext = self.mytext.toPlainText()
            self.SetTitle()
            f.close()
        else:
            FileSave = QFileDialog.getSaveFileName(self, 'Save File', './', "텍스트 파일(*.txt)")

            if FileSave != ('', ''):
                self.fileLocation = FileSave[0]
                textcontent = self.mytext.toPlainText()
                f = open(FileSave[0], 'w')
                self.SetTitle(FileSave[0])
                f.write(textcontent)
                self.originaltext = self.mytext.toPlainText()
                self.SetTitle()
                f.close()

    # 파일 다른 이름으로 저장
    def add_save_as(self):
        FileSave = QFileDialog.getSaveFileName(self, 'Save As', './', "텍스트 파일(*.txt)")

        if FileSave != ('', ''):
            self.fileLocation = FileSave[0]
            textcontent = self.mytext.toPlainText()
            f = open(FileSave[0], 'w')
            self.SetTitle(FileSave[0])
            f.write(textcontent)
            self.originaltext = self.mytext.toPlainText()
            self.SetTitle()
            f.close()

    # 끝내기 전 저장 여부 확인
    def add_exit(self):
        if self.CheckText():
            dlg = ExitCheckDialog()
            dlg.exec_()

            if dlg.save:
                self.add_save()
                self.SetTitle()

            if dlg.exit:
                qApp.quit()
        else:
            qApp.quit()

    # 폰트 바꾸기
    def add_font(self):
        font, ok = QFontDialog.getFont()

        if ok:
            self.mytext.setFont(font)

    # 단어 검색
    def add_find(self):
        findWindow(self)

    # 텍스트 비교해서 저장 여부 확인
    def CheckText(self):
        return self.mytext.toPlainText() != self.originaltext

    # 제목 바꾸기
    def SetTitle(self, name='0'):
        if name != '0' and name != '*':
            temp = name.split('/')
            self.setWindowTitle(temp[-1])
            self.originaltitle = temp[-1]

            if self.isdefault:
                self.isdefault = False
        elif name == '*':
            self.setWindowTitle('*' + self.windowTitle())
        else:
            self.setWindowTitle(self.originaltitle)

        self.ischange = False

        return

    # 기본 제목인지 확인하기
    def CheckTitle(self):
        return not self.isdefault

    # 되돌리기
    def Undo(self):
        self.mytext.undo()

    # 다시 실행
    def Redo(self):
        self.mytext.redo()

    # 복사
    def Copy(self):
        self.mytext.copy()

    # 붙여넣기
    def Paste(self):
        self.mytext.paste()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyNotePad()
    app.exec_()
