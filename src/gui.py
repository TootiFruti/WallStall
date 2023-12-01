from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import uic
import requests
from src.wallpaper_fetcher import wallFetcher


class MainWindow(QMainWindow):
    def __init__(self, daddypath, wallheavenApi):
        super(QMainWindow, self).__init__()
        uic.loadUi(f"{daddypath}/src/MainWindow.ui", self)
        self.show()

        self.Image.setScaledContents(False)

        imagedata = [" "]
        currentImage = [0]
        currentPage = [1]

        self.leftButton.clicked.connect(
            lambda: self.onLeftClick(currentImage, imagedata))
        self.rightButton.clicked.connect(
            lambda: self.onRightClick(currentPage, currentImage, imagedata, wallheavenApi))

        self.searchBarBtn.clicked.connect(
            lambda: self.onSearchBarBtnClicked(currentPage, currentImage, imagedata, wallheavenApi))

        self.saveTheImageBtn.clicked.connect(
            lambda: self.saveImage(currentImage, imagedata, "test_img"))

    def saveImage(self, currentImage, imagedata, imgName):
        imagedata = eval(imagedata[0])
        url = imagedata[currentImage[0]][1]
        file_type = imagedata[currentImage[0]][3][6::]
        imgPath = f"{imgName}.{file_type}"
        img = requests.get(url).content
        with open(imgPath, "wb") as f:
            f.write(img)
            print(f"saved the image at {imgPath}")
            f.close()

    def setImage(self, url, currentImage):
        img = QImage()
        img.loadFromData(requests.get(url).content)
        img = QPixmap(img)
        aspectRatio = img.width() / img.height()
        size = self.Image.size()
        new_width = size.width()
        new_height = int(new_width / aspectRatio)
        scaled_pixmap = img.scaled(new_width, new_height)
        self.Image.setPixmap(scaled_pixmap)
        print(f"current image = {url} currentImage={currentImage[0]}")

    def getImageData(self, args, wallheavenApi):
        ImagesData = wallFetcher(wallheavenApi, args)
        return ImagesData

    def onLeftClick(self, currentImage, imagedata):
        imagedata = eval(imagedata[0])
        if currentImage[0] == 0:
            print("Reached the left end!")
        else:
            url = imagedata[currentImage[0]-1][1]
            print(f"currentImage[0]-1: {currentImage[0]-1}")
            self.setImage(url, currentImage)
            currentImage[0] = currentImage[0] - 1
            self.updateTextArea(
                "wallheaven,cc", [str(imagedata)], [currentImage[0]-1])

    def onRightClick(self, currentPage, currentImage, imagedata, wallheavenApi):
        imgdata = eval(imagedata[0])
        print(f"currentImage: {currentImage[0]}")
        url = imgdata[currentImage[0]+1][1]
        print(f"currentImage[0]+1: {currentImage[0]+1}")
        self.setImage(url, currentImage)
        self.updateTextArea("wallheaven,cc", [str(imgdata)], currentImage)
        currentImage[0] = currentImage[0] + 1
        if currentImage[0] == 23:
            print("Reached right end!\nLoading more data..")
            args = self.genArgs(wallheavenApi)
            currentPage[0] += 1
            args["pages"] = currentPage[0]
            imgdata = self.getImageData(
                args, wallheavenApi)
            imagedata[0] = str(imgdata)
            print("Loaded!")
            currentImage[0] = 0

    def updateTextArea(self, site, imagedata, currentImage):
        imagedata = eval(imagedata[0])
        temp = imagedata[currentImage[0]+1]
        id = temp[0]
        resolution = temp[2]
        file_type = temp[3]
        imageSize = temp[4] * 0.00000095367432
        path = temp[1]
        text = f"Site: {site}\nID: {id}\nResolution: {resolution}\nImage type: {file_type}\nImage size: {round(imageSize, 1)}MB\nImage link: {path}"
        self.TextArea.setText(text)

    def genArgs(self, wallheavenApi):
        purity = ""
        categories = ""
        if self.sfw.isChecked():
            purity += "100/"
        if self.NSFW.isChecked():
            if len(wallheavenApi.replace(" ", "").lower()) != 0:
                purity += "111/"
            else:
                print("COULDNT FIND AN API KEY, DROPPED NSFW CODE")

        if self.sketchy.isChecked():
            if len(wallheavenApi.replace(" ", "").lower()) != 0:
                purity += "110/"
            else:
                print("COULDNT FIND AN API KEY, DROPPED sketch CODE")

        if self.general.isChecked():
            categories += "100/"
        if self.anime.isChecked():
            categories += "101/"
        if self.people.isChecked():
            categories += "111/"

        sorting = str(self.comboBox.currentText())
        t = {
            "tagname": self.searchBar.text(),
            "purity": purity,
            "categories": categories,
            "sorting": sorting,
            "ratio": self.resolution.text()
        }
        return t

    def onSearchBarBtnClicked(self, currentPage, currentImage, imagedata, wallheavenApi):
        args = self.genArgs(wallheavenApi)
        print(f"args : {args}")
        imagedata[0] = str(self.getImageData(args, wallheavenApi))
        currentImage[0] = 0
        imagedata = eval(imagedata[0])
        if len(imagedata) == 0:
            print(f"Got nothing. {imagedata}")
        else:
            self.setImage(imagedata[currentImage[0]][1], currentImage)
            self.updateTextArea(
                "wallheaven,cc", [str(imagedata)], [-1])


def main(daddypath, wallheavenApi):
    app = QApplication([])
    window = MainWindow(daddypath, wallheavenApi)
    app.exec_()


if __name__ == "__main__":
    main()
