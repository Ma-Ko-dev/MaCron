from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow


class UiMainWindow(QMainWindow):

    def __init__(self):
        super(UiMainWindow, self).__init__()
        self.resize(1200, 500)
        self.setMinimumSize(QtCore.QSize(1250, 500))
        self.setWindowIcon(QtGui.QIcon("assets/macaron_flaticon-com.ico"))
        self.setObjectName("MainWindow")
        self.setWindowTitle("MaCron")
        self.setup_ui()

    def setup_ui(self):
        font = QtGui.QFont()
        font.setPointSize(11)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setStyleSheet("QLabel {border: 1px solid white; border-radius: 6px; }")
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setStyleSheet("QScrollArea { border: none; }")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1182, 441))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(3, 0, 3, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.btn_add_script = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_add_script.setMinimumSize(QtCore.QSize(130, 30))
        self.btn_add_script.setMaximumSize(QtCore.QSize(130, 30))
        self.btn_add_script.setFont(font)
        self.btn_add_script.setObjectName("btn_add_script")
        self.btn_add_script.setText("Add new Script")
        self.gridLayout.addWidget(self.btn_add_script, 0, 0, 1, 1)

        self.line = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 5)

        self.label_script = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_script.setMinimumSize(QtCore.QSize(600, 30))
        self.label_script.setMaximumSize(QtCore.QSize(16777215, 30))
        self.label_script.setFont(font)
        self.label_script.setStyleSheet("")
        self.label_script.setObjectName("label_script")
        self.label_script.setText("ThisIsAPythonScriptAndBecomeVeryLongSinceItsAlsoThePathOrIImplementANameInstead.py")
        self.gridLayout.addWidget(self.label_script, 2, 0, 1, 1)

        self.label_time = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_time.setMinimumSize(QtCore.QSize(110, 30))
        self.label_time.setMaximumSize(QtCore.QSize(120, 30))
        self.label_time.setFont(font)
        self.label_time.setAlignment(QtCore.Qt.AlignCenter)
        self.label_time.setObjectName("label_time")
        self.label_time.setText("00:00:00:00")
        self.gridLayout.addWidget(self.label_time, 2, 1, 1, 1)

        self.btn_run = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_run.setMinimumSize(QtCore.QSize(130, 30))
        self.btn_run.setMaximumSize(QtCore.QSize(16777215, 30))
        self.btn_run.setFont(font)
        self.btn_run.setObjectName("btn_run")
        self.btn_run.setText("Run now")
        self.gridLayout.addWidget(self.btn_run, 2, 2, 1, 1)

        self.btn_edit = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_edit.setMinimumSize(QtCore.QSize(130, 30))
        self.btn_edit.setMaximumSize(QtCore.QSize(16777215, 30))
        self.btn_edit.setFont(font)
        self.btn_edit.setObjectName("btn_edit")
        self.btn_edit.setText("Edit")
        self.gridLayout.addWidget(self.btn_edit, 2, 3, 1, 1)

        self.btn_delete = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.btn_delete.setMinimumSize(QtCore.QSize(130, 30))
        self.btn_delete.setMaximumSize(QtCore.QSize(16777215, 30))
        self.btn_delete.setFont(font)
        self.btn_delete.setObjectName("btn_delete")
        self.btn_delete.setText("Delete")
        self.gridLayout.addWidget(self.btn_delete, 2, 4, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 1, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 21))
        self.menubar.setObjectName("menubar")

        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuMenu.setTitle("Menu")
        self.setMenuBar(self.menubar)

        self.actionAdd_Script = QtWidgets.QAction(QIcon("assets/plus-button.png"), "Add Script", self)
        self.actionAdd_Script.setObjectName("actionAdd_new_Script")

        self.actionCheck_Updates = QtWidgets.QAction(QIcon("assets/compile.png"), "Check for Updates",  self)
        self.actionCheck_Updates.setObjectName("actionCheck_for_Updates")

        self.actionQuit = QtWidgets.QAction(QIcon("assets/cross-circle.png"), "Quit", self)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.triggered.connect(self.clicked)

        self.menuMenu.addAction(self.actionAdd_Script)
        self.menuMenu.addAction(self.actionCheck_Updates)
        self.menuMenu.addSeparator()
        self.menuMenu.addAction(self.actionQuit)
        self.menubar.addAction(self.menuMenu.menuAction())

        QtCore.QMetaObject.connectSlotsByName(self)

    def clicked(self):
        self.close()

