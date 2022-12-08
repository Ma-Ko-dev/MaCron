import datetime
import sys
import time
import qdarkstyle
import logging
from subprocess import call

from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base, Session
from PyQt5 import QtWidgets, QtCore, QtGui
from UI import entryWidget, mainWindow, addDialog

MINIMUM_INTERVAL = 60

# db setup
base = declarative_base()
engine = create_engine("sqlite:///database.db")
# logging setup
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s|%(levelname)s|%(funcName)s|%(message)s",
                    datefmt="%d.%m.%Y-%H:%M:%S")


class Macroni(base):
    __tablename__ = "macronis"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    path = Column(String(100), nullable=False)
    interval = Column(Float, nullable=False)
    next_run = Column(Float, nullable=False)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = mainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        # adding entries to GUI
        self.add_entries_to_gui()

        # sub window
        self.sub_window = AddDialog()

        # Menu trigger
        self.ui.menu_action_exit.triggered.connect(self.exit)
        self.ui.menu_action_add.triggered.connect(self.open_dialog)
        # Button clicked
        self.ui.btn_addScript.clicked.connect(self.open_dialog)

    def open_dialog(self):
        self.sub_window.exec_()

    def add_entries_to_gui(self) -> None:
        """When this method is called, it will read all entries in the database and add it to the GUI."""
        row = 0
        with Session(engine) as session:
            macronis = session.query(Macroni).all()
            for macroni in macronis:
                days, hours, mins, secs = self.convert_interval(macroni.interval)
                entry = EntryWidget()
                entry.entry_ui.lbl_name.setText(macroni.name)
                entry.entry_ui.lbl_interval.setText(f"{days:02}:{hours:02}:{mins:02}:{secs:02}")
                row += 1
                self.ui.gridLayout.addWidget(entry, row, 0)

    def exit(self) -> None:
        """This method will simply close the program."""
        sys.exit()

    def convert_interval(self, interval):
        days = interval // (24 * 3600)
        interval = interval % (24 * 3600)
        hours = interval // 3600
        interval %= 3600
        mins = interval // 60
        interval %= 60
        secs = interval
        return int(days), int(hours), int(mins), int(secs)


class AddDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(AddDialog, self).__init__(*args, **kwargs)
        self.add_dialog = addDialog.Ui_Dialog()
        self.add_dialog.setupUi(self)
        # remove the question mark and keep the dialog on top
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        # self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowCloseButtonHint)

        # button events
        self.add_dialog.btn_cancel.clicked.connect(self.cancel_dialog)
        self.add_dialog.btn_select.clicked.connect(self.select_script)
        self.add_dialog.btn_add.clicked.connect(self.add_to_db)

    def cancel_dialog(self):
        self.close()

    def select_script(self):
        path_name = QtWidgets.QFileDialog.getOpenFileName(self, "Select Script", "c:\\", "Python files (*.py)")
        self.add_dialog.edit_path.setText(path_name[0])

    def add_to_db(self):
        # TODO: Clean up and move some of this in extra functions
        path = self.add_dialog.edit_path.text()
        name = self.add_dialog.edit_name.text()
        days = self.add_dialog.spn_days.value()
        hours = self.add_dialog.spn_hours.value()
        mins = self.add_dialog.spn_mins.value()
        secs = self.add_dialog.spn_secs.value()
        interval = datetime.timedelta(days=days, hours=hours, minutes=mins, seconds=secs).total_seconds()

        if path and name and interval >= MINIMUM_INTERVAL:
            with Session(engine) as session:
                macroni = Macroni()
                macroni.name = name
                macroni.path = path
                macroni.interval = interval
                # calculate when the next run is according to current dateTime.now().timestamp() plus interval
                new_run = datetime.datetime.now() + datetime.timedelta(seconds=interval)
                macroni.next_run = new_run.timestamp()

                session.add_all([macroni])
                session.commit()
            # TODO: See if i need a separate update method to maybe wipe all entries because i suspect at the moment
            #  this will currently add some of the entries over old entries.
            mainWin.add_entries_to_gui()
            self.close()
        else:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/icons/assets/icons/macaron_flaticon-com.ico"))

            msg = QtWidgets.QMessageBox()
            msg.setWindowIcon(icon)
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("All fields are mandatory to fill!\nSee details for more Information.")
            msg.setDetailedText("See below for more Information:\n"
                                "The Path has to be filled with a valid Path.\n"
                                "The Name field has to be at least 6 chars long.\n"
                                "The minimum Interval is 60 seconds.")
            msg.setWindowTitle("ERROR")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()


class EntryWidget(QtWidgets.QWidget):
    """This Class acts as the entry for the main GUI"""
    def __init__(self, *args, **kwargs):
        super(EntryWidget, self).__init__(*args, **kwargs)
        self.entry_ui = entryWidget.Ui_Form()
        self.entry_ui.setupUi(self)


def add_macroni(name: str, interval: int) -> None:
    with Session(engine) as session:
        macroni = Macroni()
        macroni.name = name
        # macroni.path = path_picker()
        # INFO: we need to calculate the interval here in seconds or when we get the data from the add gui, we already
        #  get it in seconds.
        macroni.interval = interval
        # calculate when the next run is according to current dateTime.now().timestamp() plus interval
        new_run = datetime.datetime.now() + datetime.timedelta(seconds=interval)
        macroni.next_run = new_run.timestamp()

        session.add_all([macroni])
        session.commit()


def run_macroni():
    with Session(engine) as session:
        macronis = session.query(Macroni).all()
        for macroni in macronis:
            if datetime.datetime.now().timestamp() > macroni.next_run:
                # print(f"[DEBUG][{macroni.name}][{macroni.id}][{datetime.datetime.now().time()}]: i run now")
                logging.debug(f"Scriptname: {macroni.name} - ID: {macroni.id}")
                call(["python", macroni.path])
                reset_next_run(macroni.id, macroni.interval)
        wait_timer()


def reset_next_run(macroni_id, interval):
    new_run = datetime.datetime.now() + datetime.timedelta(seconds=interval)
    with Session(engine) as session:

        session.query(Macroni).filter(Macroni.id == macroni_id).update(
            {
                Macroni.next_run: new_run.timestamp()
            }
        )
        session.commit()


def wait_timer():
    time.sleep(1)
    run_macroni()


# def path_picker():
#     from tkinter import Tk
#     from tkinter.filedialog import askopenfilename
#
#     Tk().withdraw()
#     filename = askopenfilename()
#     return filename


if __name__ == "__main__":
    base.metadata.create_all(engine)
    app = QtWidgets.QApplication([])
    mainWin = MainWindow()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # run_macroni()

    mainWin.show()
    app.exec()
