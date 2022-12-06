import datetime
import time
import qdarkstyle
import logging
from subprocess import call

from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base, Session
from PyQt5 import QtWidgets
from UI import mainWindow, entryWidget, entryWidgetV2, mainWindowV3

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
        self.ui = mainWindowV3.Ui_MainWindow()
        self.ui.setupUi(self)
        self.add_widget()

        # self.ui.btn_delete.clicked.connect(self.exit)

    def exit(self):
        # example only
        print("i want to exit")

    def add_widget(self):
        entry = EntryWidget()
        entry2 = EntryWidget()

        # self.ui.gridLayout.removeWidget(self.ui.gridLayout.spacerItem())

        self.ui.gridLayout.addWidget(entry, 0, 0)
        self.ui.gridLayout.addWidget(entry2, 1, 0)

        # spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.ui.gridLayout.addWidget(spacer, 2, 0)

        # spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.ui.gridLayout.addItem(spacerItem, 0, 0, 1, 1)


class EntryWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(EntryWidget, self).__init__(*args, **kwargs)
        self.entry_ui = entryWidgetV2.Ui_Form()
        self.entry_ui.setupUi(self)


def add_macroni(name: str, interval: int) -> None:
    with Session(engine) as session:
        macroni = Macroni()
        macroni.name = name
        macroni.path = path_picker()
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


def path_picker():
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename

    Tk().withdraw()
    filename = askopenfilename()
    return filename


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    mainWin = MainWindow()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    # base.metadata.create_all(engine)
    # add_macroni(name="My second Script", interval=30)
    # run_macroni()

    mainWin.show()
    app.exec()
