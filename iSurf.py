from random import randint
from threading import Thread, Timer
import pygetwindow
from PIL import Image  # pip install pillow
from PIL.ImageFilter import *
from PyQt5.QtCore import *  # pip install PyQt5
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *  # search for it
from PyQt5.QtWidgets import *
from pyautogui import *
from win32api import *
from win10toast import ToastNotifier
import keyboard
from PyQt5 import QtWidgets, QtCore, QtGui, uic
from pygame import mixer, error, USEREVENT, event
from mutagen.mp3 import MP3, HeaderNotFoundError, MutagenError

# constants
WIDTH_ = GetSystemMetrics(0)
HEIGHT_ = GetSystemMetrics(1)
USER = GetUserName()
PATH_ = ""
# may be i not pretty
if not os.path.isdir(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache'):
    os.makedirs(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache')


class BlurEffect(QtWidgets.QGraphicsBlurEffect):
    effectRect = None

    def setEffectRect(self, rect):
        self.effectRect = rect
        self.update()

    def draw(self, qp):
        if self.effectRect is None or self.effectRect.isNull():
            # no valid effect rect to be used, use the default implementation
            super().draw(qp)

        else:
            qp.save()
            # clip the drawing so that it's restricted to the effectRect
            qp.setClipRect(self.effectRect)
            # call the default implementation, which will draw the effect
            super().draw(qp)
            # get the full region that should be painted
            fullRegion = QtGui.QRegion(qp.viewport())
            # and subtract the effect rectangle
            fullRegion -= QtGui.QRegion(self.effectRect)
            qp.setClipRegion(fullRegion)
            # draw the *source*, which has no effect applied
            self.drawSource(qp)
            qp.restore()


class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.value = False
        self.setMinimumSize(int(WIDTH_ / 1.2), int(HEIGHT_ / 1.2))
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(True)
        self.username = GetUserName()


        # # UI Setup
        self.ui = uic.loadUi("D:/file_explorer_ui/UPDATE4.ui", self)
        self.show()

        # radio button manager
        with open("lib.dll", "r") as reader:
            read = str(reader.read())

        # combobox manager
        with open('rep32.dll', 'r') as theme_reader:
            read_theme = theme_reader.read()

        if read == "True":
            self.effect_radiobutton.setChecked(True)
            self.set_acrylic(True, "set_all")
        else:
            self.effect_radiobutton.setChecked(False)
            self.set_acrylic(False, "dark")
            print('dark')

        if read_theme == 'acrylic':
            self.theme_box.setCurrentIndex(1)
        elif read_theme == 'transparent':
            self.theme_box.setCurrentIndex(2)
        elif read_theme == 'blur':
            self.theme_box.setCurrentIndex(3)
        elif read_theme == 'light':
            self.theme_box.setCurrentIndex(4)
        elif read_theme == 'dark':
            self.theme_box.setCurrentIndex(5)
        elif read_theme == 'amoled':
            self.theme_box.setCurrentIndex(6)
        elif read_theme == 'default':
            self.theme_box.setCurrentIndex(0)
        # self.setupUi(self)
        self.functionalities()
        self.setGeometry(int(WIDTH_ / 12), int(HEIGHT_ / 16), int(WIDTH_ / 1.14), int(HEIGHT_ / 1.19))
        self.showMaximized()

        get_image = screenshot()
        r = str(randint(10, 100000))
        with open("assets/resources/holder.tru", 'w') as hold:
            hold.write(r)

        try:
            get_image.save(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_ref{r}.jpeg')
            frame_one_image = Image.open(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_ref{r}.jpeg')
            skinned_ = Image.eval(frame_one_image, lambda x: x / 2)
            frame_one_blurred_image = skinned_.filter(GaussianBlur(radius=3))
            frame_one_blurred_image.save(f"C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_reb1{r}.jpeg")
        except FileNotFoundError:
            pass

        if self.isMaximized():
            self.setWindowOpacity(1.0)

            # FRAMES UI

            # FRAME 1
            try:
                self.graphics.setStyleSheet(f"""
                                      background: url(C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_reb1{r}.jpeg);
                                      background-repeat: repeat;
                                      background-position: left;
                                      border: 0;""")


            except FileNotFoundError:
                pass

    #     self.mainlayout = QtWidgets.QVBoxLayout(self)
    #     self.mainlayout.setContentsMargins(0, 0, 0, 0)
    #
    #     self.subWidget = QtWidgets.QWidget()
    #     self.mainlayout.addWidget(self.subWidget)
    #
    #     self.effect = BlurEffect()
    #
    #     self.subWidget.setGraphicsEffect(self.effect)
    #     self.effect.setEnabled(True)
    #     self.effect.setBlurRadius(40)
    #
    #     self.menu = QtWidgets.QWidget(self)
    #     self.menu.setVisible(False)
    #     self.menu.setFixedWidth(300)
    #     self.menu.move(-self.menu.width(), 0)
    #
    #     self.menuLayout = QtWidgets.QVBoxLayout(self.menu)
    #
    #     self.menuAnimation = QtCore.QVariantAnimation()
    #     self.menuAnimation.setDuration(400)
    #     self.menuAnimation.setEasingCurve(QtCore.QEasingCurve.OutQuart)
    #     self.menuAnimation.setStartValue(-self.menu.width())
    #     self.menuAnimation.setEndValue(0)
    #
    #
    # def openMenu(self):
    #     # if self.menu.x() >= 0:
    #     #     # the menu is already visible
    #     #     return
    #     # ensure that the menu starts hidden (that is, with its right border
    #     # aligned to the left of the main widget)
    #     self.menu.move(-self.menu.width(), 0)
    #     self.menu.setVisible(True)
    #     self.menu.setFocus()
    #
    #     # enable the effect, set the forward direction for the animation, and
    #     # start it; it's important to set the effect rectangle here too, otherwise
    #     # some flickering might show at the beginning
    #     self.effect.setEffectRect(self.menu.geometry())
    #     self.effect.setEnabled(True)
    #     self.menuAnimation.setDirection(QtCore.QVariantAnimation.Forward)
    #     self.menuAnimation.start()
    #     print("Trying ..")
    def set_acrylic(self, val=True or False, *args):
        if val:
            for i in args:
                if i == "set_all":
                    self.all_frame.setStyleSheet(f"""background: transparent;""")
                    self.window_frame.setStyleSheet(f"""background: transparent;""")
                    self.graphics.setStyleSheet(f"""background: transparent;""")

                    with open("assets/resources/holder.tru", "r") as reader:
                        r = str(reader.read())
                    self.all_frame.setStyleSheet(f"""
                        background: transparent;
                        background: url('C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_reb1{r}.jpeg');
                        background-repeat: no-repeat;
                        background-position: left;
                        border: 0;""")

                if i == "set_on_left" or i == 'default':

                    with open("assets/resources/holder.tru", "r") as reader:
                        r = str(reader.read())
                    self.all_frame.setStyleSheet(f"""
                        background:  url('C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_reb1{r}.jpeg');
                        background-repeat: no-repeat;
                        background-position: left;
                        border: 0;""")
                    self.window_frame.setStyleSheet("background: black;")

                if i == "set_on_right":
                    with open("assets/resources/holder.tru", "r") as reader:
                        r = str(reader.read())
                    self.window_frame.setStyleSheet(f"""
                        background: transparent;
                        background: url('C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_reb1{r}.jpeg');
                        background-repeat: no-repeat;
                        background-position: left;
                        border: 0;""")

            return
        else:
            for i in args:
                if i == "amoled":
                    self.all_frame.setStyleSheet("""background: black;""")
                    self.window_frame.setStyleSheet("""background: black;""")
                    self.graphics.setStyleSheet("""background: black;""")
                if i == "dark":
                    self.all_frame.setStyleSheet(f"""background: rgb(40, 40, 40);""")
                    self.window_frame.setStyleSheet(f"""background: rgb(40, 40, 40);""")
                    self.graphics.setStyleSheet(f"""background: rgb(30, 30, 30);""")
                if i == "light":
                    self.all_frame.setStyleSheet(f"""
                    background: rgb(255, 255, 255);
                    color: rgb(0, 0, 0)""")
                if i == "transparent":
                    self.all_frame.setStyleSheet(f"""background: 	transparent;""")
                    self.window_frame.setStyleSheet(f"""background: transparent;""")
                    self.graphics.setStyleSheet(f"""background: transparent;""")
                if i == 'semi-transparent':
                    self.all_frame.setStyleSheet(f"""background: rgba(0, 0, 0, 128);""")
                    self.window_frame.setStyleSheet(f"""background: rgba(0, 0, 0, 128);""")
                    self.graphics.setStyleSheet(f"""background: rgba(0, 0, 0, 128);""")
                    self.setWindowOpacity(0.8)

    def setup_elegantUi(self):
        if self.isMaximized():
            if self.effect_radiobutton.isChecked():
                self.set_acrylic(True, "set_all")
                with open("lib.dll", "w") as writer:
                    writer.write("True")
            else:
                self.set_acrylic(False, 'dark')
                with open("lib.dll", "w") as writer:
                    writer.write("False")

    def slideMenu(self, value= True or False):
        width = self.graphics.width()


        if value:
            # decrease the slide menu size

            # set name
            self.collapse.setText("")
            self.search_box.setVisible(False)
            # self.search.setMaximumWidth(20)
            self.search.setStyleSheet("""
                QPushButton{
color: white;
background: transparent;
padding-right: 5px;
	
}

QPushButton::hover{
	color: white;
	background-color : rgba(255, 255  ,255 ,50);

}

QPushButton::pressed{
	background-color: rgba(255, 255, 255, 80)
}
            """)

            #
            # if width == 380:
            #     new_width = 45
            # else:
            #     new_width = 380
            #
            #
            # self.animation = QtCore.QPropertyAnimation(self.graphics, b"maximumWidth", self)
            # self.animation.setStartValue(width)
            # self.animation.setEndValue(new_width)
            # self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            # self.animation.setDuration(200)
            # self.animation.start()

            self.graphics.setMaximumWidth(10)
            self.graphics.setMinimumWidth(45)

            self.gdrive_line.setVisible(False)
            self.settings_line.setVisible(False)



            return -1

        else:
            # increae the size
            # set name
            self.collapse.setText("  Fluent Explorer")
            self.search.setStyleSheet("""
                QPushButton{
                    color: white;
                    background: transparent;
                    padding-right: 5px;
                    }
 """)

            # if width == 45:
            #     new_width = 380
            # else:
            #     new_width = 45
            #
            #
            # self.animation_down = QtCore.QPropertyAnimation(self.graphics, b"minimumWidth", self)
            # self.animation_down.setStartValue(45)
            # self.animation_down.setEndValue(350)
            # self.animation_down.setEasingCurve(QtCore.QEasingCurve.InElastic)
            # self.animation_down.setDuration(200)
            # self.animation_down.start()
            #
            # print("Down Width : ", width)

            # self.search.setMaximumWidth(200)
            self.graphics.setMaximumWidth(380)
            self.graphics.setMinimumWidth(350)

            self.search_box.setVisible(True)
            self.gdrive_line.setVisible(True)
            self.settings_line.setVisible(True)
            # self.search_clear.setVisible(True)

    def menu_handler(self):

        with open("assets/resources/Core.dll", "r") as reader:
            read = reader.read()

        if read == "True":
            self.slideMenu(False)
            with open("assets/resources/Core.dll", "w") as writer:
                writer.write("False")

            self.search.clicked.connect(lambda: self.slideMenu(False))

        else:
            self.slideMenu(True)
            with open("assets/resources/Core.dll", "w") as writer:
                writer.write("True")

    def fluentHandler(self):
        # FRAME 1
        with open("assets/resources/holder.tru", "r") as reader_:
            r = str(reader_.read())

        self.graphics.setStyleSheet(f"""
                                   background: url(C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_reb1{r}.jpeg);
                                   background-repeat: repeat;
                                   background-position: left;
                                   border: 0;""")

    def min(self):
        self.showMinimized()

    def max_reduce(self):
        if self.isMaximized():
            self.showNormal()
            icon = QIcon()
            icon.addFile("assets/resources/images/maximize.png", QSize(), QIcon.Normal, QIcon.Off)
            self.maximize.setIcon(icon)

            self.set_acrylic(True)
        else:
            self.showMaximized()
            icon = QIcon()
            icon.addFile("assets/resources/images/estore.png", QSize(), QIcon.Normal, QIcon.Off)
            self.maximize.setIcon(icon)
            self.set_acrylic(True)

    def stop(self):
        app.closeAllWindows()
        sys.exit()

# ################################################### Main UI ######################################################
    # ************************* This Pc *************************** #
    def thisPC_UI(self):
        drives = GetLogicalDriveStrings()
        lst = []
        for i in drives:
            if str(i).isalpha():
                lst.append("  " + i)

        for i in range(len(lst)):
            pushbuton = QPushButton(f"{lst[i]}")
            pushbuton.setMinimumSize(150, 45)
            # pushbuton.setMaximumWidth(200)

            pushbuton.setFont(QFont("Segoe UI", 16))

            if lst[i] == "  C":
                pushbuton.setIcon(QIcon("assets/resources/images/drive.png"))
                pushbuton.setIconSize(QSize(25, 25))
            pushbuton.setStyleSheet("""
            QPushButton{
                    color: white;
                    background: transparent;
                    text-align: left;
                    align: left;
                    padding-left: 25px;
                    }
                    
                    QPushButton::hover{
                        color: white;
                        background-color : rgba(255, 255  ,255 ,50);
                    
                    }
                    
                    QPushButton::pressed{
                        background-color: rgba(255, 255, 255, 80)
                    }
""")
            self.drives_layout.addWidget(pushbuton)
        # self.drives_layout.addWidget()

    # ************************* MUSIC ***************************** #

    def music_indexer(self, *args):
        from random import choice
        # provide te choice
        t = ('Please wait while we take care of few things.', 'Indexing will help to search entire drive faster.',
             'Some changes have been found since last run. Please wait while we index.')

        def toast_r():
            # show toast
            try:
                ToastNotifier().show_toast(title='Indexing Musics in Local Drives.',
                                           msg=choice(t),
                                           duration=7,
                                           icon_path='Graphics/Elements/icon.ico')
            except (AttributeError, RuntimeError, AssertionError):
                pass

        Thread(target=toast_r).start()

        # def assist():
        #     try:
        #         loader = MP3("Assist/indexing.mp3")
        #         mixer.init(frequency=loader.info.sample_rate)
        #         mixer.music.load("Assist/indexing.mp3")
        #         mixer.music.play()
        #     except error:
        #         pass
        #     except Exception:
        #         pass
        #
        # Thread(target=assist).start()

        # main indexer to find the mp3 file
        musics = open(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/mr.tru', 'w')
        path = open(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/mp.tru', 'w')

        # walker
        for v in os.walk(r'C:/Users'):
            for g in v[2]:
                try:
                    if g.endswith('.mp3'):
                        musics.write(f'{g}\n')
                        path.write(f'{v[0]}\n')
                except UnicodeEncodeError:
                    pass

        new_songs = 0
        # # new drive walker
        # for i in range(current_active - 1):
        #     for e in get_active_drives[1:current_active]:
        #         walker_drives = os.walk(f'{e}')
        #         for z in walker_drives:
        #             for r in z[2]:
        #                 try:
        #                     if r.endswith('.mp3'):
        #                         f.write(f'{r}\n')
        #                         reviser.write(f'{z[0]}\n')
        #                         new_songs += 1
        #                 except UnicodeEncodeError:
        #                     pass
        # save and close the file
        musics.close()
        path.close()

        # with open('Asse', 'w') as ne:
        #     ne.write('False')

        # with open(f'C:/Users/{GetUserName()}/Fluent Player+/temp/Assets/optimizer.tru', "r") as optimize:
        #     reader = optimize.read()
        #
        # if reader == "True":
        #     try:
        #         ToastNotifier().show_toast(title=f"Added {new_songs} songs into library.",
        #                                    msg=f"We have found {new_songs} in your device and added to library. ",
        #                                    duration=14,
        #                                    icon_path="Graphics/Elements/icon.ico")
        #     except (RuntimeError, AttributeError, AssertionError):
        #         pass
        with open(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/optimizer.tru', "w") as optimization:
            optimization.write("False")

    def music_UI(self):
        if not os.path.isfile(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/mr.tru'):
            Thread(target=self.music_indexer)

        read_music = open(f'C:/Users/{GetUserName()}/AppData/Local/Temp/CachedData/mr.tru', 'r').readlines()

        total = 0

        for i in read_music:
            total += 1
        print('Total Songs : ', total)

        for i in range(total):
            for z in read_music:
                print(z)
                # songs_button = QPushButton(text=str(z))
                # songs_button.setMaximumHeight(45)
                # songs_button.setStyleSheet("""
                #     QPushButton{
                #         color: white;
                #         background: transparent;
                #         text-align: left;
                #         padding-left: 10px;
                #         }
                #
                #         QPushButton::hover{
                #             color: white;
                #             background-color : rgba(255, 255  ,255 ,50);
                #
                #         }
                #
                # """)
                item = QListWidgetItem('akash')
                self.song_view.addItem(item)


    def clear_search(self):
        self.search_box.setText('')

    def functionalities(self):

        # Title bar buttons
        # self.close.clicked.connect(self.stop)
        self.music.clicked.connect(self.music_UI)
        self.minimize.clicked.connect(self.min)
        self.maximize.clicked.connect(self.max_reduce)
        self.collapse.clicked.connect(self.menu_handler)
        self.close.clicked.connect(self.stop)
        self.thisPC.clicked.connect(self.thisPC_UI)
        # self.search_clear.clicked.connect(self.clear_search)
        # self.downloads.clicked.connect(self.downloads_UI)
        self.effect_radiobutton.toggled.connect(self.setup_elegantUi)
        self.theme_box.activated.connect(self.theme_manager)

    def themeRegistry(self, theme='acrylic'):
        with open('rep32.dll', 'w') as theme_writer:
            theme_writer.write(theme)

    def setTheme(self):
        with open('rep32.dll', 'r') as reader:
            read = reader.read()

        if read == 'dark':
            self.set_acrylic(False, 'dark')
        elif read == 'amoled':
            self.set_acrylic(False, 'amoled')
        elif read == 'acrylic':
            if self.effect_radiobutton.isChecked():
                self.set_acrylic(True, 'set_all')
            else:
                self.set_acrylic(True, 'set_on_left')
        elif read == 'blur':
            if self.effect_radiobutton.isChecked():
                self.set_acrylic(True, 'set_all')
            else:
                self.set_acrylic(True, 'set_on_left')
        elif read == 'default':
            self.set_acrylic(True, 'default')

    def theme_manager(self):

        if self.theme_box.currentText() == 'Dark':
            self.set_acrylic(False, 'dark')
            self.themeRegistry('dark')

        elif self.theme_box.currentText() == 'Blur':
            with open('effectSupport.dll', 'w') as writer:
                writer.write('ten')
            self.themeRegistry('blur')

            with open("assets/resources/holder.tru", 'r') as val:
                    r = val.read()
            # Frame One UI
            frame_one_image = Image.open(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_ref{r}.jpeg')
            skinned_ = Image.eval(frame_one_image, lambda x: x / 2.2)

            frame_one_blurred_image = skinned_.filter(GaussianBlur(radius=10))
            frame_one_blurred_image.save(f"C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_rea.jpeg")

            if self.effect_radiobutton.isChecked():
                self.set_acrylic(False, 'transparent')
                self.all_frame.setStyleSheet(f"""
                    background: url('C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_rea.jpeg');
                    background-repeat: no-repeat;
                    background-position: left;
                    border: 0;""")

        elif self.theme_box.currentText() == 'Default':
            self.set_acrylic(True, 'set_on_left')
            self.themeRegistry('default')

        elif self.theme_box.currentText() == 'Amoled':
            self.set_acrylic(False, 'amoled')
            self.themeRegistry('amoled')

        elif self.theme_box.currentText() == 'Acrylic':
            with open('effectSupport.dll', 'w') as writer:
                writer.write('acrylic')
            with open("assets/resources/holder.tru", 'r') as val:
                r = val.read()
            # Frame One UI
            frame_one_image = Image.open(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_ref{r}.jpeg')
            skinned_ = Image.eval(frame_one_image, lambda x: x / 2.2)

            frame_one_blurred_image = skinned_.filter(GaussianBlur(radius=35))
            frame_one_blurred_image.save(f"C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_rea.jpeg")

            if self.effect_radiobutton.isChecked():
                self.set_acrylic(False, 'transparent')
                self.all_frame.setStyleSheet(f"""
                    background: url('C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_rea.jpeg');
                    background-repeat: no-repeat;
                    background-position: left;
                    border: 0;""")
            else:
                self.set_acrylic(False, 'amoled')
                self.graphics.setStyleSheet(f"""
                    
                    background: url('C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_rea.jpeg');
                    background-repeat: no-repeat;
                    background-position: left;
                    border: 0;""")

            self.themeRegistry('acrylic')
        elif self.theme_box.currentText() == 'Transparent':
            self.set_acrylic(False, 'semi-transparent')

def switch_check():
    writer =  open("config.dll", "w")
    if keyboard.is_pressed("alt"):
        writer.write("False")
    elif keyboard.read_key() == 'left windows':
        writer.write('False')
        print('window set up')
    else:
        writer.write("True")

    print('Checking switch..')
    writer.close()

# @ staticmethod
def check_window():
    try:
        # get the current active window
        a = pygetwindow.getActiveWindowTitle()

        if str(a) != "Fluent Explorer.exe":
            try:

                # minimize
                MainWindow.showMinimized()

                with open("config.dll", "r") as reader:
                    read_config = reader.read()

                # grab screen
                if read_config == "True" or read_config == '':
                    get_image = screenshot()
                    print('Using Brush..')

                    # random value grabber
                    r = str(randint(10, 100000))

                    # save value into a file for furure use   this is the fool
                    with open("assets/resources/holder.tru", 'w') as hold:
                        hold.write(r)

                    # save at this location thi
                    get_image.save(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_ref{r}.jpeg')

                with open("assets/resources/holder.tru", 'r') as val:
                    r = val.read()
                # Frame One UI
                frame_one_image = Image.open(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_ref{r}.jpeg')
                skinned_ = Image.eval(frame_one_image, lambda x: x / 2.2)
                # blur the image
                with open('effectSupport.dll', 'r') as reader:
                    read = reader.read()

                if read == 'ten':
                    radii = 10
                else:
                    radii = 35

                frame_one_blurred_image = skinned_.filter(GaussianBlur(radius=radii))
                frame_one_blurred_image.save(f"C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/vis_reb1{r}.jpeg")

            # will raise OS error if imaghow to add padding in pushbutton icon in pyqte is subjected to modifications
            except OSError:
                pass

        elif MainWindow.isMaximized():
            MainWindow.setWindowOpacity(1.0)

            # FRAMES UI

            # FRAME 1
            with open("assets/resources/qr.tru", "r") as reader:
                read = str(reader.read())

            if read == "True":
                with open("lib.dll", "r") as reader:
                    read = str(reader.read())

                if read == "True":
                    # MainWindow.set_acrylic(True, "set_all")
                    MainWindow.setTheme()
                else:
                    # MainWindow.set_acrylic(True, "set_on_left")
                    MainWindow.setTheme()
                with open("assets/resources/qr.tru", "w") as writer:
                    writer.write("False")


        else:
            MainWindow.set_acrylic(False, "dark")

    except NameError:
        pass


def no_screen():
    current = pygetwindow.getActiveWindowTitle()
    if MainWindow.isMinimized() or current != "Fluent Explorer.exe" or not MainWindow.isMaximized():
        with open("assets/resources/block.tru", "w") as writer:
            writer.write("True")
        with open("assets/resources/qr.tru", "w") as writer:
            writer.write("True")
    if MainWindow.isMaximized():
        MainWindow.setWindowOpacity(1.0)
        with open("assets/resources/block.tru", 'r') as reader:
            read = str(reader.read())
        if read == "True":
            MainWindow.fluentHandler()
            with open("assets/resources/block.tru", "w") as writer:
                writer.write("False")
    if MainWindow.isMinimized() or current != "Fluent Explorer.exe":
        with open("assets/resources/QtS.dll", "w") as writer:
            writer.write("True")

    if not MainWindow.isMaximized():

        with open("assets/resources/QtS.dll", "r") as reader:
            read = str(reader.read())

        if read == "True":
            MainWindow.setStyleSheet("""background-color: black;""")
            MainWindow.graphics.setStyleSheet("""background-color: black;""")


def cleaner():
    walker = os.walk(f'C:/Users/{USER}/AppData/Local/Temp/CachedData/cache')

    for i in walker:
        r = i[2]
        for g in r:
            if g.endswith('.jpeg'):
                with open(f'assets/resources/holder.tru', "r") as t:
                    ri = str(t.read())
                if ri in str(g):
                    pass
                else:
                    z = g
                    try:
                        os.remove(f"C:/Users/{USER}/AppData/Local/Temp/CachedData/cache/{z}")
                    except (PermissionError, FileNotFoundError):
                        pass


def clock(func, sec):
    def wrapper():
        clock(func, sec)
        func()

    t = Timer(sec, wrapper)
    try:
        t.start()
    except RuntimeError:
        pass


clock(cleaner, 1.0)
clock(switch_check, 0.2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = Main()
    windowTimer = QTimer()
    windowTimer.timeout.connect(no_screen)
    windowTimer.timeout.connect(check_window)
    windowTimer.setInterval(1)
    windowTimer.start()
    MainWindow.show()
    app.exec()


