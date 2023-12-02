from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5 import uic
import requests


class prefencesWindow(QMainWindow):
    def __init__(self, daddypath):
        super(QMainWindow, self).__init__()
        uic.loadUi(f"{daddypath}/src/PreferencesWindow.ui", self)
        self.show()
        with open(f"{daddypath}/data/config.json", 'r') as f:
            try:
                data = eval(str(f.read()))
                wallheavenapi = data["wallheaven"][0]
                defaultLocation = data["defaultSaveLocation"][0]
                savedMsgPopUpCond = data["savedMsgPopUp"]
            except (Exception) as e:
                print(e)
            f.close()
        self.wahheavenApiBar.setText(wallheavenapi)
        self.defaultLocationBar.setText(defaultLocation)
        self.Save.clicked.connect(lambda: self.SaveAPI(daddypath))
        self.saveDefaultLocationBtn.clicked.connect(
            lambda: self.saveDefaultLocation(daddypath))
        self.browse.clicked.connect(lambda: self.browsefile())
        self.AuthenticateBtn.clicked.connect(self.onAuthenticateBtnClicked)
        self.savedMsgPopUp(savedMsgPopUpCond)
        self.savedImgPopUp.stateChanged.connect(
            lambda: self.savedMsgPopUpChanged(daddypath))

    def savedMsgPopUpChanged(self, daddypath):
        path = f"{daddypath}/data/config.json"
        with open(path, "r") as f:
            data = eval(str(f.read()))
            f.close()
        if self.savedImgPopUp.isChecked():
            data["savedMsgPopUp"] = True
        else:
            data["savedMsgPopUp"] = False
        with open(path, 'w') as f:
            f.write(str(data))
            f.close()

    def savedMsgPopUp(self, cond):
        if cond is True:
            self.savedImgPopUp.setCheckState(True)
        else:
            self.savedImgPopUp.setCheckState(False)

    def SaveAPI(self, daddypath):
        path = f"{daddypath}/data/config.json"
        with open(path, 'r') as f:
            data = eval(f.read())
            f.close()
        data["wallheaven"] = [str(self.wahheavenApiBar.text())]
        with open(path, 'w') as f:
            f.write(str(data))
            f.close()
        msg = QMessageBox()
        msg.setWindowTitle("Saved the API")
        msg.setText("Saved the API")
        msg.exec_()

    def browsefile(self):
        imgPath = QFileDialog.getExistingDirectory(
            self, "Open Directory", "/home")
        self.defaultLocationBar.setText(imgPath)

    def onAuthenticateBtnClicked(self):
        msg = QMessageBox()
        msg.setWindowTitle("API status")
        api = self.wahheavenApiBar.text()
        if len(api.replace(" ", "")) != 0:

            url = f"https://wallhaven.cc/api/v1/collections?apikey={api}"
            code = requests.get(url).status_code
            if code == 200:
                print("Vaild api")
                msg.setText("Vaild api")
            elif code == 401:
                print("Invaild api")
                msg.setText("Invaild api")
            else:
                msg.setText("Something went wrong.")
                print(f"something went wrong. status code: {code}")
        else:
            msg.setText("Enter an API key.")

        msg.exec_()

    def saveDefaultLocation(self, daddypath):
        path = f"{daddypath}/data/config.json"
        with open(path, 'r') as f:
            data = eval(f.read())
            f.close()
        location = str(self.defaultLocationBar.text())
        data["defaultSaveLocation"] = [location]
        with open(path, 'w') as f:
            f.write(str(data))
            f.close()
        msg = QMessageBox()
        msg.setWindowTitle("Saved the default location")
        msg.setText(f"Saved the default location as {location}")
        msg.exec_()


def main(daddypath):
    app = QApplication([])
    window = prefencesWindow(daddypath)
    app.exec_()


if __name__ == "__main__":
    main("./..")
