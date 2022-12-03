import datetime
import sys
import time

import qdarkstyle
from subprocess import call
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import declarative_base, Session
from PyQt5.QtWidgets import QApplication
from ui import UiMainWindow

base = declarative_base()
engine = create_engine("sqlite:///database.db")

class Macroni(base):
    __tablename__ = "macronis"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable=False)
    path = Column(String(100), nullable=False)
    interval = Column(Float, nullable=False)
    next_run = Column(Float, nullable=False)


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
    macronis = Session(engine).query(Macroni).all()
    while True:
        for macroni in macronis:
            if datetime.datetime.now().timestamp() > macroni.next_run:
                # print(f"{macroni.name}: i run now")
                call(["python", macroni.path])
            # else:
            #     print(f"{macroni.name}: i dont run now")
        time.sleep(1)





def path_picker():
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename

    Tk().withdraw()
    filename = askopenfilename()
    return filename


if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # MainWindow = UiMainWindow()
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    base.metadata.create_all(engine)

    # add_macroni(name="My first Script", interval=30)

    run_macroni()

    # print(datetime.datetime.now().timestamp())

    # MainWindow.show()
    # sys.exit(app.exec_())
