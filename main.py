import datetime
import os.path
import subprocess
import sys
import qdarkstyle
import logging
import configparser

from subprocess import run
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base, Session
from PyQt5 import QtWidgets, QtCore, QtGui
from UI import entryWidget, mainWindow, addDialog

# for now the minimum interval is 60 seconds
MINIMUM_INTERVAL = 60

# db setup
base = declarative_base()
engine = create_engine("sqlite:///database.db")
# logging setup
logging.basicConfig(filename="logs/log.log", filemode="w", level=logging.DEBUG,
                    format="%(asctime)s|%(levelname)s|%(funcName)s|%(message)s",
                    datefmt="%d.%m.%Y-%H:%M:%S")


class Macroni(base):
    """Database Structure.
    ID gets filled automatically, name is the name of the Script, path is the absolut path to the Script, interval is
    the time in seconds a script should run, next_run is a timestamp. """

    __tablename__ = "macronis"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    path = Column(String(100), nullable=False)
    interval = Column(Float, nullable=False)
    next_run = Column(Float, nullable=False)


class MainWindow(QtWidgets.QMainWindow):
    """Handles all MainWindow related tasks. It will create a window from UI.mainWindow which was created
    with the Qt Designer."""
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = mainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.entry_ids = []
        self.title = self.windowTitle()
        self.get_theme()

        # setting up the tray
        self.tray = QtWidgets.QSystemTrayIcon()
        self.tray.setToolTip(self.title)
        self.tray_icon = QtGui.QIcon(QtGui.QPixmap(":/icons/assets/icons/macaron_flaticon-com.ico"))
        self.tray.setIcon(self.tray_icon)

        self.tray_menu = QtWidgets.QMenu()
        self.tray_font = self.tray_menu.font()
        self.tray_font.setPointSize(12)
        self.tray_menu.setFont(self.tray_font)

        self.tray_exit = QtWidgets.QAction("Quit", self)
        self.tray_show = QtWidgets.QAction("Show", self)

        self.tray_show.triggered.connect(self.show)  # type: ignore
        self.tray_exit.triggered.connect(self.exit)  # type: ignore

        self.tray_menu.addAction(self.tray_show)
        self.tray_menu.addAction(self.tray_exit)

        self.tray.setContextMenu(self.tray_menu)
        self.tray.activated.connect(self.tray_activated)  # type: ignore
        self.tray.show()

        # setting up the timer
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

    def changeEvent(self, event) -> None:
        """Check if the event comes from minimizing and hides the window."""
        if event.type() == QtCore.QEvent.WindowStateChange:
            if event.oldState() == QtCore.Qt.WindowNoState or not self.windowState() == QtCore.Qt.WindowMaximized:
                print("test")
                self.hide()

    def tray_activated(self, reason) -> None:
        """Check if the tray icon got clicked once or doubleClicked and then brings the window back."""
        if reason == 2 or reason == 3:
            self.showMinimized()
            self.setWindowState(self.windowState() and (not QtCore.Qt.WindowMinimized or QtCore.Qt.WindowActive))
            self.show()

    # noinspection PyMethodMayBeStatic
    def exit(self) -> None:
        """This method will simply close the program."""
        sys.exit()

    def update_title(self) -> None:
        """Will get called every second by a timer, updates the title with the current time and then calls
        the method run_macroni() to see if any script should be executed."""
        self.setWindowTitle(f"{self.title} - {datetime.datetime.now().strftime('%H:%M:%S')}")
        self.run_macroni()

    # noinspection PyMethodMayBeStatic
    def theme_dark(self) -> None:
        """Changes the current color theme to dark."""
        app.setStyleSheet(qdarkstyle.load_stylesheet(palette=qdarkstyle.DarkPalette))
        settings["theme"] = "dark"
        with open("config.ini", mode="w") as file:
            config.write(file)

    # noinspection PyMethodMayBeStatic
    def theme_light(self) -> None:
        """Changes the current color theme to light."""
        app.setStyleSheet(qdarkstyle.load_stylesheet(palette=qdarkstyle.LightPalette))
        settings["theme"] = "light"
        with open("config.ini", mode="w") as file:
            config.write(file)

    def open_dialog(self, xid: int) -> None:
        """Opens the dialog to add or edit a new Script. If xid is given, it will look up the id in the
        Database and pre-fill the Dialog options with the id's contents. Otherwise, it will simply open the dialog."""
        new_dialog = AddDialog()
        if xid:
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

    def delete_entry(self, xid: int) -> None:
        """Will delete the given entry by id from the database, the corresponding GUI entryWidget and id in the
        entry_ids list."""
        with Session(engine) as session:
            session.query(Macroni).filter(Macroni.id == xid).delete()
            session.commit()
            self.entry_ids.remove(xid)
        self.sender().parentWidget().deleteLater()

    def add_entries_to_gui(self) -> None:
        """When called, it will read all entries in the database and add it to the GUI. To ensure that there are no
        entries overlapping, it will add the id of each entry to a list and checks if the id already is in the list."""
        row = 0
        with Session(engine) as session:
            macronis = session.query(Macroni).all()
            for macroni in macronis:
                if macroni.id not in self.entry_ids:
                    days, hours, mins, secs = self.convert_interval(macroni.interval)
                    entry = EntryWidget()
                    entry.row_id = macroni.id
                    entry.entry_ui.lbl_name.setText(macroni.name)
                    # each label and button in the entryWidget will get its own values, corresponding to the database
                    # entry
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

    def run_macroni_manual(self, path, xid, interval) -> None:
        """When called, it will run the script at <path> and calls reset_next_run() with <xid>, <interval>"""
        try:
            if os.path.splitext(path)[1] == ".py":  # type: ignore
                run(["python", path], check=True, capture_output=True)
            else:
                run(["pythonw", path], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Manual run-> ID: {xid} | {path}\nReturncode: {e.returncode}, Output: {e.output}\n"
                          f"{e.stderr.decode('utf-8')}")
        logging.info(f"Manual run-> ID: {xid} - Interval: {interval}")
        self.reset_next_run(xid, interval)

    def run_macroni(self) -> None:
        # TODO: Add a notification to the title to alert the user that an error happened and to suggest to check the
        #  log file. Also add a "view log" button, a reset button and an info button for some program related infos.
        """Queries the database to get all entries and checks if the current time is bigger or equal to the next_run
        variable. If this is true, the Script will be executed and reset_next_run() is called for this entry."""
        with Session(engine) as session:
            macronis = session.query(Macroni).all()
            for macroni in macronis:
                if datetime.datetime.now().timestamp() >= macroni.next_run:
                    try:
                        if os.path.splitext(macroni.path)[1] == ".py":  # type: ignore
                            run(["python", macroni.path], check=True, capture_output=True)
                        else:
                            run(["pythonw", macroni.path], check=True, capture_output=True)
                    except subprocess.CalledProcessError as e:
                        logging.error(f"Autorun-> ID: {macroni.id} | {macroni.path}\n {e.returncode}, Output: "
                                      f"{e.output}\n{e.stderr.decode('utf-8')}")
                    logging.info(f"Autorun-> ID: {macroni.id} - Interval: {macroni.interval}")
                    self.reset_next_run(macroni.id, macroni.interval)

    # noinspection PyMethodMayBeStatic
    def reset_next_run(self, macroni_id, interval) -> None:
        """Resets the next_run variable in the database with a new run time."""
        new_run = datetime.datetime.now() + datetime.timedelta(seconds=interval)
        with Session(engine) as session:
            macroni = session.query(Macroni).get(macroni_id)
            macroni.next_run = new_run.timestamp()
            logging.info(f"ID: {macroni_id} - Next time: {new_run.strftime('%d.%m.%Y %H:%M:%S')}")
            session.commit()

    # noinspection PyMethodMayBeStatic
    def convert_interval(self, interval):
        """Converts the given interval to days, hours, mins and secs. Mostly for format reasons."""
        days = interval // (24 * 3600)
        interval = interval % (24 * 3600)
        hours = interval // 3600
        interval %= 3600
        mins = interval // 60
        interval %= 60
        secs = interval
        return int(days), int(hours), int(mins), int(secs)

    def get_theme(self):
        if settings["theme"] == "dark":
            self.theme_dark()
        else:
            self.theme_light()


class AddDialog(QtWidgets.QDialog):
    """Works as the dialog that pops up when the edit or add button is clicked."""
    def __init__(self, *args, **kwargs):
        super(AddDialog, self).__init__(*args, **kwargs)
        self.add_dialog = addDialog.Ui_Dialog()
        self.add_dialog.setupUi(self)
        # self.check_ini()

        # remove the question mark
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        # we need this to make sure to know when to add and when to edit an entry
        self.edit = False
        self.edit_id = 0
        self.edit_object = EntryWidget()

        # button events
        self.add_dialog.btn_cancel.clicked.connect(self.cancel_dialog)
        self.add_dialog.btn_select.clicked.connect(self.select_script)
        self.add_dialog.btn_add.clicked.connect(self.add_to_db)

    def cancel_dialog(self) -> None:
        """Simply closes the dialog."""
        self.close()

    def select_script(self) -> None:
        """Opens a filedialog to pick a python script and set its path to the correct label."""
        path_name = QtWidgets.QFileDialog.getOpenFileName(self, "Select Script", settings["last_path"],
                                                          "Python files (*.py *pyw)")
        self.add_dialog.edit_path.setText(path_name[0])
        settings["last_path"] = os.path.dirname(path_name[0])
        with open("config.ini", mode="w") as file:
            config.write(file)

    def add_to_db(self):
        """Adds a new entry to the database. It will take data from all given fields and first checks if nothing is
        empty, if any is empty it will display an info popup with some information. When all fields have data, it will
        then check if <edit> is true to determine if it has to update an entry or create a new one. In the end it will
        call add_entries_to_gui from the mainWindow and close itself."""
        path = self.add_dialog.edit_path.text()
        name = self.add_dialog.edit_name.text()
        days = self.add_dialog.spn_days.value()
        hours = self.add_dialog.spn_hours.value()
        mins = self.add_dialog.spn_mins.value()
        secs = self.add_dialog.spn_secs.value()
        interval = datetime.timedelta(days=days, hours=hours, minutes=mins, seconds=secs).total_seconds()

        if path and len(name) >= 6 and interval >= MINIMUM_INTERVAL:
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
                    # a newly added script will run after it got added, an edited one will not
                    # new_run = datetime.datetime.now() + datetime.timedelta(seconds=interval)
                    new_run = datetime.datetime.now()
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
                                "The Path has to be filled with a valid Path to a Python file.\n"
                                "The Name field has to be at least 6 chars long.\n"
                                "The minimum Interval is 60 seconds.")
            msg.setWindowTitle("ERROR")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()


class EntryWidget(QtWidgets.QWidget):
    """Acts as the entry for the main GUI"""
    def __init__(self, *args, **kwargs):
        super(EntryWidget, self).__init__(*args, **kwargs)
        self.entry_ui = entryWidget.Ui_Form()
        self.entry_ui.setupUi(self)


def create_default_ini():
    # creating an ini with some default values
    new_config = configparser.ConfigParser()
    # default theme is dark and the default value for the script path is the current working directory. This feature is
    # not implemented yet.
    new_config["MaCron Settings"] = {
        "theme": "dark",
        "last_path": os.getcwd()
    }
    with open("config.ini", mode="w") as file:
        new_config.write(file)


if __name__ == "__main__":
    # check for log folder, create one if non is found
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # check if ini file exists, call function to create default one
    if not os.path.exists("config.ini"):
        create_default_ini()

    # creating configparser for future reference
    config = configparser.ConfigParser()
    config.read("config.ini")
    settings = config["MaCron Settings"]

    # basic setup
    base.metadata.create_all(engine)
    app = QtWidgets.QApplication([])
    mainWin = MainWindow()

    mainWin.show()
    app.exec()
