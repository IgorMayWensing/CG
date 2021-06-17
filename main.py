import sys
from PyQtS.QtWidgets import QApplication, QWidget

from MainWindow import MainWindow

def main():
    app = QApplication(sys.argv)
    w = QWidget()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

