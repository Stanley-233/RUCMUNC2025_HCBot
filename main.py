import sys
from PyQt5.QtWidgets import QApplication
from gui.MainWindow import MessageWindow
from gui.TimerWindow import TimerWindow

def main():
    app = QApplication(sys.argv)
    mwindow = MessageWindow()
    mwindow.show()
    timeWindow = TimerWindow()
    timeWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()