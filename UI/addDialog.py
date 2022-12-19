# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MaCron-AddDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 220)
        font = QtGui.QFont()
        font.setPointSize(12)
        Dialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/assets/icons/macaron_flaticon-com.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setWhatsThis("")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btn_select = QtWidgets.QPushButton(Dialog)
        self.btn_select.setObjectName("btn_select")
        self.horizontalLayout_3.addWidget(self.btn_select)
        self.btn_add = QtWidgets.QPushButton(Dialog)
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout_3.addWidget(self.btn_add)
        self.btn_cancel = QtWidgets.QPushButton(Dialog)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout_3.addWidget(self.btn_cancel)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 6, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.spn_days = QtWidgets.QSpinBox(Dialog)
        self.spn_days.setObjectName("spn_days")
        self.horizontalLayout.addWidget(self.spn_days)
        self.lbl_days = QtWidgets.QLabel(Dialog)
        self.lbl_days.setObjectName("lbl_days")
        self.horizontalLayout.addWidget(self.lbl_days)
        self.spn_hours = QtWidgets.QSpinBox(Dialog)
        self.spn_hours.setObjectName("spn_hours")
        self.horizontalLayout.addWidget(self.spn_hours)
        self.lbl_hours = QtWidgets.QLabel(Dialog)
        self.lbl_hours.setObjectName("lbl_hours")
        self.horizontalLayout.addWidget(self.lbl_hours)
        self.spn_mins = QtWidgets.QSpinBox(Dialog)
        self.spn_mins.setObjectName("spn_mins")
        self.horizontalLayout.addWidget(self.spn_mins)
        self.lbl_mins = QtWidgets.QLabel(Dialog)
        self.lbl_mins.setObjectName("lbl_mins")
        self.horizontalLayout.addWidget(self.lbl_mins)
        self.spn_secs = QtWidgets.QSpinBox(Dialog)
        self.spn_secs.setProperty("value", 60)
        self.spn_secs.setObjectName("spn_secs")
        self.horizontalLayout.addWidget(self.spn_secs)
        self.lbl_secs = QtWidgets.QLabel(Dialog)
        self.lbl_secs.setObjectName("lbl_secs")
        self.horizontalLayout.addWidget(self.lbl_secs)
        self.gridLayout_2.addLayout(self.horizontalLayout, 5, 0, 1, 1)
        self.edit_name = QtWidgets.QLineEdit(Dialog)
        self.edit_name.setObjectName("edit_name")
        self.gridLayout_2.addWidget(self.edit_name, 3, 0, 1, 1)
        self.lbl_schedula = QtWidgets.QLabel(Dialog)
        self.lbl_schedula.setObjectName("lbl_schedula")
        self.gridLayout_2.addWidget(self.lbl_schedula, 4, 0, 1, 1)
        self.lbl_path = QtWidgets.QLabel(Dialog)
        self.lbl_path.setObjectName("lbl_path")
        self.gridLayout_2.addWidget(self.lbl_path, 0, 0, 1, 1)
        self.lbl_name = QtWidgets.QLabel(Dialog)
        self.lbl_name.setObjectName("lbl_name")
        self.gridLayout_2.addWidget(self.lbl_name, 2, 0, 1, 1)
        self.edit_path = QtWidgets.QLineEdit(Dialog)
        self.edit_path.setReadOnly(True)
        self.edit_path.setObjectName("edit_path")
        self.gridLayout_2.addWidget(self.edit_path, 1, 0, 1, 1)
        self.horizontalLayout_4.addLayout(self.gridLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Add new Script"))
        self.btn_select.setText(_translate("Dialog", "Select Script"))
        self.btn_add.setText(_translate("Dialog", "Add Script"))
        self.btn_cancel.setText(_translate("Dialog", "Cancel"))
        self.lbl_days.setText(_translate("Dialog", "Days"))
        self.lbl_hours.setText(_translate("Dialog", "Hours"))
        self.lbl_mins.setText(_translate("Dialog", "Minutes"))
        self.lbl_secs.setText(_translate("Dialog", "Secs."))
        self.edit_name.setPlaceholderText(_translate("Dialog", "Please type a name here."))
        self.lbl_schedula.setText(_translate("Dialog", "Schedule:"))
        self.lbl_path.setText(_translate("Dialog", "Path:"))
        self.lbl_name.setText(_translate("Dialog", "Name:"))
        self.edit_path.setPlaceholderText(_translate("Dialog", "Please click \"Select Script\" to add a path."))
import ui_resources_rc
