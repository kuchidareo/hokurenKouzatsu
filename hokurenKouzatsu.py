import tkinter as tk
from tkinter import PhotoImage, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
import pathlib, shutil
import functools

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)

        self.master.title("Hokuren Kouzatsu")
        self.master.state("zoomed")

        self.animalIdStrip = [3, 13]

        self.master.update_idletasks()
        self.winWidth = self.master.winfo_width()
        self.winHeight = self.master.winfo_height()
        self.dirPathList = []
        self.processCount = 0
        self.initImagePlace()
        self.autoSetInput = 6

        self.imageWidth = 0
        self.imageHeight = 0

        self.panelHoriSet = 3
        self.panelVerSet = 2
        self.panelXPadding = 200
        self.panelYPadding = 180

        self.fourSortedDir = ""
        self.sixSortedDir = ""
        self.panelDir = ""

        self.initFrameAndButtonSet()

    def makeDir(self, dirPath):
        self.fourSortedDir = dirPath.parent / "MIJ-15(4枚整頓版)"
        self.sixSortedDir = dirPath.parent / "MIJ-15(6枚整頓版)"
        self.panelDir = dirPath.parent / "パネル画像"

        if not self.fourSortedDir.exists():
            self.fourSortedDir.mkdir()

        if not self.sixSortedDir.exists():
            self.sixSortedDir.mkdir()

        if not self.panelDir.exists():
            self.panelDir.mkdir()

    def initFrameAndButtonSet(self):
        self.imageFrame = tk.Frame(
            self.master,
            height = self.winHeight,
            width = self.winWidth * 4 / 5,
            bg = "#c0c0c0"
        )

        operateFrame = tk.Frame(
            self.master,
            height = self.winHeight,
            width = self.winWidth / 5,
            bg = "#c0c0c0"
        )

        inputFrame = tk.Frame(
            operateFrame,
            height = 10,
            width = 50,
            bg = "#c0c0c0"
        )

        self.csvButton = tk.Button(
            operateFrame,
            text = "Click to Load Images",
            height = 10,
            width = 50,
            command = self.getImagePathsFromDir
        )

        self.clearButton = tk.Button(
            operateFrame,
            text = "Clear",
            height = 10,
            width = 50,
            command = self.clearButtonClicked,
            state = tk.DISABLED
        )

        self.processLabel = tk.Label(
            operateFrame,
            height = 4,
            width = 50,
        )

        self.carcassLabel = tk.Label(
            operateFrame,
            height = 4,
            width = 50
        )

        self.stringVar = tk.StringVar()
        self.stringVar.set(self.autoSetInput)

        self.inputDialog = tk.Entry(
            inputFrame,
            width = 5,
            font = ("arial.ttf", 20),
            background = "#f0f0f0",
            justify = tk.CENTER,
            textvariable = self.stringVar
        )

        self.inputDialogButton = tk.Button(
            inputFrame,
            width = 5,
            height = 1,
            text = "Set",
            command = self.reloadButtonClicked
        )

        self.doneButton = tk.Button(
            operateFrame,
            text = "Done",
            height = 10,
            width = 50, 
            command = self.doneButtonClicked,
            state = tk.DISABLED
        )

        self.imageFrame.pack(side = tk.LEFT, fill = tk.BOTH)
        operateFrame.pack(side = tk.RIGHT, fill = tk.BOTH)
        self.csvButton.pack(side = tk.TOP, pady = 10,)
        self.processLabel.pack(side = tk.TOP, pady = 10,)
        inputFrame.pack(side = tk.TOP, fill = tk.X, pady = 15)
        self.inputDialog.pack(side = tk.LEFT, padx = 40)
        self.inputDialogButton.pack(side = tk.RIGHT, padx = 40)
        self.doneButton.pack(side = tk.BOTTOM, pady = 10,)
        self.clearButton.pack(side = tk.BOTTOM, pady = 10,)
        self.carcassLabel.pack(side = tk.BOTTOM, pady = 10,)


    def reloadButtonClicked(self):
        self.autoSetInput = int(self.stringVar.get())
        self.initImagePlace()
        self.imageSet(self.dirPathList[self.processCount], True)

    def getImagePathsFromDir(self):
        iDir = os.path.expanduser('~/Document/MIJDB')
        dPath = filedialog.askdirectory(initialdir = iDir)

        dPath = pathlib.Path(dPath)
        dPathList = list(dPath.iterdir())

        self.makeDir(dPath)
        self.sortByIndivNumber(dPathList)
    

    def sortByIndivNumber(self, dPathList):
        # WindowsPath('C:/Users/user/Downloads/AmazonPhotos (1)/
        # 20220217102111_
        # 2511447117498112202153101002440700201351761220019_
        # 5176.jpg')

        tempList = []
        for path in dPathList:
            if path.suffix in [".jpeg", ".jpg"]:
                date = path.stem.split("_")[0]
                indivNum = path.stem.split("_")[1]
                carcassNum = path.stem.split("_")[2]

                tempList.append([path, date, indivNum, carcassNum])
        tempList = sorted(tempList, key=lambda x: x[3]) # 枝肉番号順にソートしておく

        flagIndexList = []
        for i, temp in enumerate(tempList):
            if i in flagIndexList:
                continue
            
            sameIndivList = []
            sameIndivList.append(temp)

            for j, t in enumerate(tempList):
                if temp[2] == t[2] and i != j:
                    sameIndivList.append(t)
                    flagIndexList.append(j)

            self.dirPathList.append(sameIndivList)
        
        self.imageSet(self.dirPathList[0], True)
        self.switchToEditMode(self.dirPathList[0])
        

    def switchToEditMode(self, dir):
        self.csvButton.configure(state = tk.DISABLED)
        self.csvButton.configure(text = "Image Loaded")
        self.clearButton.configure(state = tk.NORMAL)
        self.processLabel.configure(text = str(self.processCount + 1) + " / " + str(len(self.dirPathList)))
        self.carcassLabel.configure(text = dir[0][3])

    def initImageSet(self, horiSet, verSet, xPadding, yPadding, imageWidth, imageHeight, length):
        for i in range(verSet):
            for j in range(horiSet):
                if horiSet*i+j >= length:
                    break
                self.imageButton = tk.Button(
                    self.imageFrame,
                    image = PhotoImage(width = 1, height = 1),
                    width = imageWidth,
                    height = imageHeight
                )
                self.imageButton.place(
                    x = xPadding / 2 + (self.winWidth * 4 / (5 * horiSet)) * j,
                    y = (self.winHeight / verSet - imageHeight) / 2 + (self.winHeight / verSet) * i
                )
                self.imageButtonList.append(self.imageButton)

    
    def imageSet(self, dirPath, autoSetFlag):
        xPadding = 20
        yPadding = 20
        horiSet = 4
        verSet = 2

        displayImageWidth = int(self.winWidth * 4 / (5 * horiSet) - xPadding)
        displayImageHeight = int(19 * displayImageWidth / 22)

        img = Image.open(str(dirPath[0][0]))
        self.imageWidth = img.width
        self.imageHeight = img.height

        self.initImageSet(horiSet, verSet, xPadding, yPadding, displayImageWidth, displayImageHeight, len(dirPath))

        for i in range(verSet):
            for j in range(horiSet):
                if horiSet*i+j >= len(dirPath):
                    break
                img = Image.open(str(dirPath[horiSet*i+j][0]))
                img = img.resize((displayImageWidth, displayImageHeight))
                self.PILimageList.append(img)

                img = ImageTk.PhotoImage(img)
                self.imageButtonList[horiSet*i+j].configure(
                    image = img,
                    command = functools.partial(self.imageClicked, [dirPath[horiSet*i+j], horiSet*i+j, len(dirPath)])
                )
                self._temp_list.append(img)

        if len(dirPath) == self.autoSetInput and autoSetFlag:
            for i in range(len(dirPath)):
                self.imageClicked([dirPath[i], i, len(dirPath)])



    def imageClicked(self, dirPathAndIndex):
        dirPath = dirPathAndIndex[0]
        clickedIndex = dirPathAndIndex[1]
        displayedImageNum = dirPathAndIndex[2]

        if self.nameIndexCount > self.autoSetInput:
            return

        # if clickedIndex not in [i[1] for i in self.clickOrderPathList]:
        self.clickOrderPathList.append([dirPath, clickedIndex, self.nameIndexCount])
        self.nameOnImage(clickedIndex, self.nameIndexCount)
        
        if self.nameIndexCount == displayedImageNum or self.nameIndexCount == self.autoSetInput:
            self.doneButton.configure(state = tk.NORMAL)

        self.nameIndexCount += 1
        
    
    def nameOnImage(self, clickedIndex, nameIndexCount):
        img = self.PILimageList[clickedIndex].convert("RGBA")
        img.putalpha(128)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 100)
        draw.text((img.width/2-50,img.height/2-50), str(nameIndexCount) ,(20,20,20),font=font)

        img = ImageTk.PhotoImage(img)
        self.imageButtonList[clickedIndex].configure(image = img)
        self._temp_list[clickedIndex] = img

    def clearButtonClicked(self):
        self.initImagePlace()
        self.imageSet(self.dirPathList[self.processCount], False)
        self.doneButton.configure(state = tk.DISABLED)

    def initImagePlace(self):
        self._temp_list = []
        if self.processCount != 0:
            for i in self.imageButtonList:
                i.place_forget()
        self.imageButtonList = []
        self.clickOrderPathList = []
        self.PILimageList = []
        self.nameIndexCount = 1

    def doneButtonClicked(self):
        self.renamePaths()
        self.createPanelImage()
        self.processCount += 1
        self.processLabel.configure(text = str(self.processCount + 1) + " / " + str(len(self.dirPathList)))
        self.carcassLabel.configure(text = str(self.dirPathList[self.processCount][0][3]))
        
        self.initImagePlace()
        self.doneButton.configure(state = tk.DISABLED)

        if self.processCount + 1 > len(self.dirPathList):
            self.processLabel.configure(text = "")
            self.carcassLabel.configure(text = "")
            return
        
        self.imageSet(self.dirPathList[self.processCount], True)

    def createPanelImage(self):
        panelWidth = self.imageWidth * self.panelHoriSet + self.panelXPadding * (self.panelHoriSet+1)
        panelHeight = self.imageHeight * self.panelVerSet + self.panelYPadding * (self.panelVerSet+1)
        dst = Image.new('RGB', (panelWidth, panelHeight), color="white")

        for path in self.clickOrderPathList:
            oriPath = path[0][0]
            order = path[2] - 1 # index(0から開始)に変更
            img = Image.open(oriPath)
            ver = order // self.panelHoriSet
            hori = order % self.panelHoriSet
            dst.paste(img, (img.width*hori + self.panelXPadding*(hori+1), img.height*ver + self.panelYPadding*(ver+1)))

        ushi = self.clickOrderPathList[0][0]
        date = ushi[1]
        carcassNumber = ushi[3]

        draw = ImageDraw.Draw(dst)
        font = ImageFont.truetype("arial.ttf", 180)
        draw.text((self.imageWidth*(3/2) + self.panelXPadding - 90, self.imageHeight + self.panelYPadding), str(carcassNumber), (0, 0, 0), font=font)
        
        dst.save(str(self.panelDir) + "\\" + date + "_" + carcassNumber + ".jpg", quality=95)

    def renamePaths(self):
        for path in self.clickOrderPathList:
            oriPath = path[0][0]
            order = path[2]
            # imageNameを変えないといけない。日付時刻_枝肉番号_個体識別番号_部位名
            # 20220217102111_
            # 2511447117498112202153101002440700201351761220019_
            # 5176.jpg'
            stem = oriPath.stem.split("_")
            date = stem[0]
            indivNum = stem[1][self.animalIdStrip[0] : self.animalIdStrip[1]]
            carcassId = stem[2]

            nameFour = oriPath.stem
            nameSix = str(date) + "_" + str(carcassId) + "_" + str(indivNum) + "_" + str(order)

            sixPath = str(self.sixSortedDir) + "/" + nameSix + oriPath.suffix

            if order in [1, 2, 3, 4]:
                fourPath = str(self.fourSortedDir) + "/" + nameFour + oriPath.suffix
                shutil.copy(oriPath, fourPath)
                
            shutil.copy(oriPath, sixPath)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    app.mainloop()



