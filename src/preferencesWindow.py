from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5 import uic


class prefencesWindow(QMainWindow):
    def __init__(self, daddypath):
        super(QMainWindow, self).__init__()
        uic.loadUi(f"{daddypath}/src/PreferencesWindow.ui", self)
        self.show()
        with open(f"{daddypath}/data/config.json", 'r') as f:
            data = eval(str(f.read()))
            wallheavenapi = data["wallheaven"][0]
            defaultLocation = data["defaultSaveLocation"][0]
            f.close()
        self.wahheavenApiBar.setText(wallheavenapi)
        self.defaultLocationBar.setText(defaultLocation)
        self.Save.clicked.connect(lambda: self.SaveAPI(daddypath))
        self.saveDefaultLocationBtn.clicked.connect(
            lambda: self.saveDefaultLocation(daddypath))
        self.browse.clicked.connect(lambda: self.browsefile())

    def SaveAPI(self, daddypath):
        path = f"{daddypath}/data/config.json"
        with open(path, 'r') as f:
            data = eval(f.read())
            f.close()
        data["wallheaven"] = [str(self.wahheavenApiBar.text())]
        with open(path, 'w') as f:
            f.write(str(data))
            f.close()

    def browsefile(self):
        imgPath = QFileDialog.getExistingDirectory(
            self, "Open Directory", "/home")
        self.defaultLocationBar.setText(imgPath)

    def saveDefaultLocation(self, daddypath):
        path = f"{daddypath}/data/config.json"
        with open(path, 'r') as f:
            data = eval(f.read())
            f.close()
        data["defaultSaveLocation"] = [str(self.defaultLocationBar.text())]
        with open(path, 'w') as f:
            f.write(str(data))
            f.close()


def main(daddypath):
    app = QApplication([])
    window = prefencesWindow(daddypath)
    app.exec_()


if __name__ == "__main__":
    main("./..")
