# coding:utf-8

import maya.OpenMayaUI as OMUI
import pymel.tools.mel2py as mel2Py
import pymel.all as pm
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore
import PySide
import platform
from shiboken import wrapInstance
import webbrowser


__version__ = 1.2

def getMayaWindow():
    ptr = OMUI.MQtUtil.mainWindow()
    return wrapInstance(long(ptr), QtGui.QMainWindow)


class MelToPyMainWindow(QtGui.QMainWindow):
    
    def __init__(self, parent=getMayaWindow()):
        super(MelToPyMainWindow, self).__init__(parent)
        
        self.isPython = True
        
        self.setWindowTitle('Mel to python Window')
        self.splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        self.setCentralWidget(self.splitter)
        
        self.melWidget = QtGui.QWidget()
        self.melLayout = QtGui.QVBoxLayout()
        self.melLabel = QtGui.QLabel('Mel')
        self.melTextEdit = QtGui.QTextEdit()
        self.melLayout.addWidget(self.melLabel)
        self.melLayout.addWidget(self.melTextEdit)
        self.melWidget.setLayout(self.melLayout)
        self.melLayout.setContentsMargins(10,3,3,3)
        
        self.pyWidget = QtGui.QWidget()
        self.pyLayout = QtGui.QVBoxLayout()
        self.pyLabel  = QtGui.QLabel('Python')
        self.pyTextEdit = QtGui.QTextEdit()
        self.pyTextEdit.setReadOnly(True)
        self.pyLayout.addWidget(self.pyLabel)
        self.pyLayout.addWidget(self.pyTextEdit)
        self.pyWidget.setLayout(self.pyLayout)
        self.pyLayout.setContentsMargins(0,3,10,3)
        
        self.splitter.addWidget(self.melWidget)
        self.splitter.addWidget(self.pyWidget)
        
        convertAction    = self.createAction('&Convert', slot=self.convert, icon=None, tip=None)
        cleanMelAction   = self.createAction('Clean &Mel', slot=self.cleanMel, icon=None, tip=None)
        cleanPyAction    = self.createAction('Clean &Python', slot=self.cleanPython, icon=None, tip=None)
        cleanAllAction   = self.createAction('Clean A&ll', slot=self.cleanAll, icon=None, tip=None)
        quitActionAction = self.createAction('&Quit', slot=self.close, icon=None, tip=None)
        self.operationMenuActions = [convertAction, cleanMelAction, cleanPyAction, cleanAllAction, None, quitActionAction]
        
        operationMenu = self.menuBar().addMenu('Opera&tion')
        self.addActions(operationMenu, self.operationMenuActions)
        
        optionActionGrp = QtGui.QActionGroup(self)
        toPython = self.createAction('To &Python', slot=self.toPython, icon=None, tip=None, checkable=True)
        toPython.setChecked(True)
        toPyMel  = self.createAction('To Py&Mel',  slot=self.toPyMel, icon=None, tip=None, checkable=True)
        optionActionGrp.addAction(toPython)
        optionActionGrp.addAction(toPyMel)
        
        self.optionMenuActions = [toPython, toPyMel]
        optionMenu = self.menuBar().addMenu('&Option')
        self.addActions(optionMenu, self.optionMenuActions)
        
        #help actions
        helpAboutAction = self.createAction("&About MelToPy", slot=self.helpAbout)
        helpHelpAction = self.createAction("About Me", slot=self.helpHelp)
        
        helpMenu = self.menuBar().addMenu('&Help')
        self.addActions(helpMenu, [helpAboutAction,helpHelpAction])
        
        self.status = self.statusBar()
        self.status.showMessage("Ready", 5000)
        
        self.setGeometry(400, 300, 500, 400)
        
        
    def createAction(self, text, slot=None, shortcut=None, icon=None,
                 tip=None, checkable=False, signal="triggered"):
        action = QtGui.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon(":/{}.png".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            getattr(action, signal).connect(slot) 
        if checkable:
            action.setCheckable(True)
        return action
        
    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)  
    
    def convert(self):
        melText = self.melTextEdit.toPlainText()
        if self.isPython and not melText == '':
            try:
                pyText = mel2Py.mel2pyStr(melText, pymelNamespace='cmds')
                pyText = pyText.replace("pymel.all", "maya.cmds")
                self.pyTextEdit.clear()
                self.pyTextEdit.setText(pyText)
                self.printSuccess()
            except:
                self.printError()
        elif not self.isPython and not melText == '':
            try:
                pyText = mel2Py.mel2pyStr(melText, pymelNamespace='pm')
                self.pyTextEdit.clear()
                self.pyTextEdit.setText(pyText)
                self.printSuccess()
            except:
                self.printError()
        else:
            self.printError()
        
    def cleanMel(self):
        self.melTextEdit.clear()
        
    def cleanPython(self):
        self.pyTextEdit.clear()
        
    def cleanAll(self):
        self.cleanMel()
        self.cleanPython()
        
    def toPython(self):
        self.isPython = True
        
    def toPyMel(self):
        self.isPython = False
        
    def printError(self):
        self.status.setStyleSheet("QStatusBar{padding-left:8px;color:red;font-weight:bold;}")
        self.status.showMessage('Please check mel script', 5000)
    
    def printSuccess(self):
        self.status.setStyleSheet("QStatusBar{padding-left:8px;color:yellow;font-weight:bold;}")
        self.status.showMessage('The conversion was completed.', 5000)
    
    def helpAbout(self):
        QtGui.QMessageBox.about(self, "About MelToPy",
                """<b>MelToPy</b> v {0}
                <p>Copyright &copy; 2015-16 GuenMo-Kim (ximya@naver.com). 
                All rights reserved.
                <p>This application can be used to convert
                mel to python or pymel.
                <p>Python {1} - Qt {2} - PySide {3} - Maya {4} on {5}""".format(
                __version__, platform.python_version(),
                QtCore.qVersion(), PySide.__version__, pm.versions.current(),
                platform.system()))

    def helpHelp(self):
        url = 'https://vimeo.com/user32883343'
        webbrowser.open(url)
    
def main():
    global win
    try:
        win.close()
        win.deleteLater()
    except: 
        pass
    win = MelToPyMainWindow()
    win.show()
    
main()