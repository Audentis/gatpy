"""Play a game of whack-a-mole (gat-a-mole)."""
import re
from PyQt4 import QtGui
from PyQt4.QtCore import QTimer, pyqtSignal, QObject
from random import randint, uniform

from ui.whack import Ui_Dialog
from gatpy.highscores import Highscores


class Settings:
    """Hold settings info for the game.

    Attributes:
        lvlUpTime (int): time to level up
        pIsBad (float): probability of red vs blue squares
    """

    def __init__(self):
        """Init the settings file.

        Sets default settings.
        """
        self.pIsBad = 0.1
        self.lvlUpTime = 10000


class TimedBtn(QObject):
    """Time a button.

    Attributes:
        btn (QPushButton): ptr to button
        correct (pyqtSignal): signal to flag correct press of button
        isActive (bool): true if active
        isCorrect (bool): true if button is blue
        patient (pyqtSignal): signal to flag if somebody is too quick
        timeOut (pyqtSignal): signal if user was too slow
        wrong (pyqtSignal): signal if uer pressed incorrectly
    """

    # signalling for how this button was handled
    correct = pyqtSignal()
    wrong = pyqtSignal()
    timeOut = pyqtSignal()
    patient = pyqtSignal()

    def __init__(self, btn, mode='correct', time=1000):
        """Init the button.

        Args:
            btn (QPushButton): ptr to pushbutton
            mode (str, optional): mode to describe if button is blue or red
            time (int, optional): timeout time
        """
        super().__init__()
        # remember this button
        self.isActive = True
        self.btn = btn
        if mode == 'correct':
            self.makeCorrect()
        else:
            self.makeWrong()

        # set it to time out
        QTimer().singleShot(time, self.timeUp)

    def makeCorrect(self):
        """Make htis button correct (blue).

        Returns:
            None
        """
        self.isCorrect = True
        self.btn.setStyleSheet('background-color: #89BDFF')
        self.btn.clicked.connect(self.btnCallback)

    def makeWrong(self):
        """Make this button wrong (red).

        Returns:
            None
        """
        self.isCorrect = False
        self.btn.setStyleSheet('background-color: #F92672')
        self.btn.clicked.connect(self.btnCallback)

    def makeInactive(self):
        """Make this butotn inactive.

        Returns:
            None
        """
        self.isActive = False
        self.btn.setStyleSheet('')

    def btnCallback(self):
        """Handle clicked event.

        Returns:
            None
        """
        self.makeInactive()
        if self.isCorrect:
            self.correct.emit()
        else:
            self.wrong.emit()

    def timeUp(self):
        """Handle timeout event.

        Returns:
            None
        """
        if self.isActive and self.isCorrect:
            self.timeOut.emit()
        elif self.isActive:
            self.patient.emit()
        self.makeInactive()


class WhackDialog(QtGui.QDialog, Ui_Dialog):
    """Make a screen to play gat-a-mole.

    Attributes:
        actives (list): list of active buttons
        btns (list): list of buttons
        h (Highscores): highscores class
        lifes (int): number of lifes left
        score (int): current score of user
        settings (Settings): settings object
        stop (bool): flag to signal stop playing
        timer (QTimer): Timer to insert extra buttons
    """

    def __init__(self, parent=None):
        """Init the window.

        reads highscores, prepares buttons.
        """
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(800, 600)
        self.btns = []
        self.actives = []
        self.settings = Settings()
        self.timer = None
        self.stop = False

        self.score = -1
        self.scoreOne()

        self.lifes = 4
        self.loseOne()

        # highscore list
        self.h = Highscores()
        self.setHighscoreList()

        # get the buttons
        for idx in range(self.molesLayout.count()):
            self.btns.append(self.molesLayout.itemAt(idx).widget())
        # remove text
        for btn in self.btns:
            btn.setText("")

        # connect buttons
        self.startButton.clicked.connect(self.start)
        self.startButton.setStyleSheet('background-color: #89BDFF')
        self.saveButton.clicked.connect(self.saveScore)

    def setHighscoreList(self):
        """Read the highscorelist to the screen.

        Returns:
            None
        """
        self.highscoreList.clear()
        self.h.readFile(self.h.fname)
        for idx, s in enumerate(self.h.scores):
            self.highscoreList.addItem('%i. %s - %i' % (idx+1,
                                       s.name, float(s.score)))

    def start(self):
        """Start the game.

        Returns:
            None
        """
        self.startButton.setEnabled(False)
        self.startButton.setStyleSheet('')

        for btn in self.btns:
            btn.setEnabled(True)
        self.nameLineEdit.setEnabled(False)

        # init game
        self.stop = False
        self.score = -1
        self.scoreOne()
        self.lifes = 4
        self.loseOne()

        # timer here
        self.timer = QTimer()
        self.timer.timeout.connect(self.runOne)
        self.timer.start(self.settings.lvlUpTime)
        self.runOne()

    def runOne(self):
        """Run a single button.

        Call this repeatedly to get a running game.

        Returns:
            None
        """
        if self.stop:
            return
        mode = self.getMode()
        time = self.getTime()

        idx = self.getRandomBtnIdx()
        if idx != -1:
            b = TimedBtn(self.btns[idx], mode, time)
            b.correct.connect(self.correctBtnClicked)
            b.wrong.connect(self.wrongBtnClicked)
            b.timeOut.connect(self.late)
            b.patient.connect(self.runOne)
            self.actives.append(b)
            del self.btns[idx]

    def getRandomBtnIdx(self):
        """Get a random index.

        returns 1 to N, where N is number of buttons.

        Returns:
            int: random index
        """
        N = len(self.btns)
        if N < 1:
            return -1
        else:
            return randint(0, N-1)

    def correctBtnClicked(self):
        """Handle callback for correct button click.

        adds to score, makes button inactive.

        Returns:
            None
        """
        if self.stop:
            return
        tbtn = self.sender()
        tbtn.btn.clicked.disconnect()
        self.btns.append(tbtn.btn)
        del tbtn
        self.scoreOne()
        QTimer().singleShot(1000, self.runOne)

    def wrongBtnClicked(self):
        """Handle wrong button click.

        Returns:
            None
        """
        if self.stop:
            return
        tbtn = self.sender()
        tbtn.btn.clicked.disconnect()
        self.btns.append(tbtn.btn)
        del tbtn
        self.scoreOne(-1)
        QTimer().singleShot(1000, self.runOne)

    def late(self):
        """Handle callback for no button clicked (time out, late).

        Returns:
            None
        """
        if self.stop:
            return
        tbtn = self.sender()
        tbtn.btn.clicked.disconnect()
        self.btns.append(tbtn.btn)
        del tbtn
        self.loseOne()
        QTimer().singleShot(1000, self.runOne)

    def scoreOne(self, i=1):
        """Add i to the score.

        Args:
            i (int, optional): score to add

        Returns:
            None
        """
        self.score = self.score + i
        self.scoreLineEdit.setText('%i' % self.score)

    def loseOne(self):
        """Lose one life.

        also checks for death.

        Returns:
            None
        """
        self.lifes = self.lifes - 1
        self.lifeLineEdit.setText('%i' % self.lifes)

        if self.lifes == 0:
            self.stop = True
            if self.h.isHighscore(self.score):
                self.startButton.setEnabled(False)
                for btn in self.btns:
                    btn.setEnabled(False)
                self.saveBtn.setEnabled(True)
                self.nameLineEdit.setText('Vul je naam in')
                self.nameLineEdit.setEnabled(True)
                self.saveBtn.setStyleSheet('background-color: #89BDFF')
            else:
                self.startButton.setEnabled(True)
                self.startButton.setStyleSheet('background-color: #89BDFF')

    def saveScore(self):
        """Save the score using highscorelist.

        Returns:
            None
        """
        name = re.sub('[\s+]', '', self.nameLineEdit.text())
        self.h.appendScore([name, self.score])
        self.h.writeOut()

        # reset interface for playing
        self.setHighscoreList()
        self.saveBtn.setEnabled(False)
        self.saveBtn.setStyleSheet('')
        self.startButton.setEnabled(True)
        self.startButton.setStyleSheet('background-color: #89BDFF')
        self.nameLineEdit.setText('')

    def getTime(self):
        """Get time for a button.

        Returns:
            int: time for a button in ms
        """
        return 1000

    def getMode(self):
        """Get random mode for a button.

        Returns:
            str: correct or wrong, at random
        """
        r = uniform(0, 1)
        if r > self.settings.pIsBad:
            return 'correct'
        else:
            return 'wrong'
