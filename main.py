import sys
import qdarkstyle
from PyQt5.QtWidgets import QApplication
from ui import UiMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = UiMainWindow()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    MainWindow.show()
    sys.exit(app.exec_())
