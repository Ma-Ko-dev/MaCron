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

MINIMUM_INTERVAL = 10

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
        self.entry_ids = []
        self.title = self.windowTitle()

        #setting up the timer
        self.update_title()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_title)
        self.timer.start(1000)

        # adding entries to GUI
        self.add_entries_to_gui()

        # Menu trigger
        self.ui.menu_action_exit.triggered.connect(self.exit)
        self.ui.menu_action_add.triggered.connect(self.open_dialog)
        self.ui.menu_theme_dark.triggered.connect(self.theme_dark)
        self.ui.menu_theme_light.triggered.connect(self.theme_light)
        # Button connections
        self.ui.btn_addScript.clicked.connect(self.open_dialog)

    def update_title(self):
        self.setWindowTitle(f"{self.title} - {datetime.datetime.now().strftime('%H:%M:%S')}")
        self.run_macroni()

    def theme_dark(self):
        app.setStyleSheet(qdarkstyle.load_stylesheet(palette=qdarkstyle.DarkPalette))

    def theme_light(self):
        app.setStyleSheet(qdarkstyle.load_stylesheet(palette=qdarkstyle.LightPalette))

    def open_dialog(self, xid):
        new_dialog = AddDialog()
        if id:
            with Session(engine) as session:
                macroni = session.query(Macroni).get(xid)
            days, hours, mins, secs = self.convert_interval(macroni.interval)
            new_dialog.add_dialog.edit_path.setText(macroni.path)
            new_dialog.add_dialog.edit_name.setText(macroni.name)
            new_dialog.add_dialog.spn_days.setValue(days)
            new_dialog.add_dialog.spn_hours.setValue(hours)
            new_dialog.add_dialog.spn_mins.setValue(mins)
            new_dialog.add_dialog.spn_secs.setValue(secs)
            new_dialog.edit_id = xid
            new_dialog.edit = True
            new_dialog.edit_object = self.sender().parentWidget()
        new_dialog.exec_()

    def delete_entry(self, xid):
        with Session(engine) as session:
            session.query(Macroni).filter(Macroni.id == xid).delete()
            session.commit()
            self.entry_ids.remove(xid)
        self.sender().parentWidget().deleteLater()

    def add_entries_to_gui(self) -> None:
        """When this method is called, it will read all entries in the database and add it to the GUI."""
        row = 0
        with Session(engine) as session:
            macronis = session.query(Macroni).all()
            for macroni in macronis:
                if macroni.id not in self.entry_ids:
                    days, hours, mins, secs = self.convert_interval(macroni.interval)
                    entry = EntryWidget()
                    entry.row_id = macroni.id
                    entry.entry_ui.lbl_name.setText(macroni.name)
                    entry.entry_ui.lbl_interval.setText(f"{days:02}:{hours:02}:{mins:02}:{secs:02}")
                    entry.entry_ui.btn_delete.clicked.connect(lambda state, entry_id=entry.row_id:
                                                              self.delete_entry(entry_id))
                    entry.entry_ui.btn_edit.clicked.connect(lambda state, entry_id=entry.row_id:
                                                            self.open_dialog(entry_id))
                    entry.entry_ui.btn_run.clicked.connect(lambda state, path=macroni.path:
                                                           self.run_macroni_manual(path, macroni.id, macroni.interval))
                    self.entry_ids.append(entry.row_id)
                    self.ui.gridLayout.addWidget(entry, row, 0)
                row += 1

    def run_macroni_manual(self, path, xid, interval):
        call(["python", path])
        logging.debug(f"Manual run of ID: {xid}")
        self.reset_next_run(xid, interval)

    def run_macroni(self):
        with Session(engine) as session:
            macronis = session.query(Macroni).all()
            for macroni in macronis:
                if datetime.datetime.now().timestamp() >= macroni.next_run:
                    logging.debug(f"Scriptname: {macroni.name} - ID: {macroni.id}")
                    call(["python", macroni.path])
                    self.reset_next_run(macroni.id, macroni.interval)

    def reset_next_run(self, macroni_id, interval):
        new_run = datetime.datetime.now() + datetime.timedelta(seconds=interval)
        with Session(engine) as session:
            # TODO: Change the update here
            session.query(Macroni).filter(Macroni.id == macroni_id).update(
                {
                    Macroni.next_run: new_run.timestamp()
                }
            )
            logging.info(f"ID: {macroni_id} got new runtime: {new_run}")
            session.commit()

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

        # edit flag
        self.edit = False
        self.edit_id = 0
        self.edit_object = EntryWidget()

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
        path = self.add_dialog.edit_path.text()
        name = self.add_dialog.edit_name.text()
        days = self.add_dialog.spn_days.value()
        hours = self.add_dialog.spn_hours.value()
        mins = self.add_dialog.spn_mins.value()
        secs = self.add_dialog.spn_secs.value()
        interval = datetime.timedelta(days=days, hours=hours, minutes=mins, seconds=secs).total_seconds()

        if path and name and interval >= MINIMUM_INTERVAL:
            with Session(engine) as session:
                if self.edit:
                    macroni = session.query(Macroni).get(self.edit_id)
                    macroni.name = name
                    macroni.path = path
                    macroni.interval = interval
                    new_run = datetime.datetime.now() + datetime.timedelta(seconds=interval)
                    macroni.next_run = new_run.timestamp()
                    mainWin.entry_ids.remove(self.edit_id)
                    self.edit_object.deleteLater()
                    session.commit()
                else:
                    macroni = Macroni()
                    macroni.name = name
                    macroni.path = path
                    macroni.interval = interval
                    # calculate when the next run is according to current dateTime.now().timestamp() plus interval
                    new_run = datetime.datetime.now() + datetime.timedelta(seconds=interval)
                    macroni.next_run = new_run.timestamp()

                    session.add_all([macroni])
                    session.commit()
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


# def add_macroni(name: str, interval: int) -> None:
#     with Session(engine) as session:
#         macroni = Macroni()
#         macroni.name = name
#         # macroni.path = path_picker()
#         # INFO: we need to calculate the interval here in seconds or when we get the data from the add gui, we already
#         #  get it in seconds.
#         macroni.interval = interval
#         # calculate when the next run is according to current dateTime.now().timestamp() plus interval
#         new_run = datetime.datetime.now() + datetime.timedelta(seconds=interval)
#         macroni.next_run = new_run.timestamp()
#
#         session.add_all([macroni])
#         session.commit()


# def run_macroni():
#     with Session(engine) as session:
#         macronis = session.query(Macroni).all()
#         for macroni in macronis:
#             if datetime.datetime.now().timestamp() > macroni.next_run:
#                 # print(f"[DEBUG][{macroni.name}][{macroni.id}][{datetime.datetime.now().time()}]: i run now")
#                 logging.debug(f"Scriptname: {macroni.name} - ID: {macroni.id}")
#                 call(["python", macroni.path])
#                 reset_next_run(macroni.id, macroni.interval)
#         wait_timer()
#
#
# def reset_next_run(macroni_id, interval):
#     new_run = datetime.datetime.now() + datetime.timedelta(seconds=interval)
#     with Session(engine) as session:
#
#         session.query(Macroni).filter(Macroni.id == macroni_id).update(
#             {
#                 Macroni.next_run: new_run.timestamp()
#             }
#         )
#         session.commit()


# def wait_timer():
#     time.sleep(1)
#     run_macroni()


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
    # TODO: save and load last used theme here
    app.setStyleSheet(qdarkstyle.load_stylesheet(palette=qdarkstyle.DarkPalette))

    mainWin.show()
    app.exec()
