import sys
import datetime
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.uic as uic

import simulation as sim
from readers import read_characters, read_advertisements

from UI.CharacterInfoWidget import CharacterInfoWidget

#from ui import Ui_MainWindow

Ui_MainWindow, baseClass = uic.loadUiType('UI/MainWindow.ui')

class MainWindow(baseClass, Ui_MainWindow):

	def __init__(self, characters: list[sim.character], options: list[sim.advertisement], *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.DATETIME_START: datetime = datetime.datetime(2023, 7, 15, hour=12, minute=00)

		self.characters: list[sim.character] = characters
		self.options: list[sim.options] = options
		self.ticksPassed: int = 0
		self.tickSpeed: int = 0

		self.setupUi(self)

		self.characterInfoWidgets: list[CharacterInfoWidget] = [CharacterInfoWidget(char) for char in self.characters]
		layout = self.groupBox_3.layout()
		for i in reversed(range(layout.count())):
			layout.itemAt(i).widget().setParent(None)
		for charWidget in self.characterInfoWidgets:
			layout.addWidget(charWidget)

		self.timer=qtc.QTimer()
		self.timer.timeout.connect(self.TickTicked)
		self.timer.start(1000)

		
		self.SpeedSlider.valueChanged.connect(self.SpeedSliderMoved)

		self.show()

	@property
	def currentTime(self):
		current_time = self.DATETIME_START + datetime.timedelta(minutes=self.ticksPassed)
		return current_time.strftime("%H:%M")

	def SpeedSliderMoved(self, new_value: int) -> None:
			self.tickSpeed = new_value
			self.SpeedLabel.setText(f"Speed: {self.tickSpeed}")

	def TickTicked(self):
			self.ticksPassed += self.tickSpeed
			self.TicksLabel.setText(f"({self.ticksPassed} ticks)")
			self.timer.start(1000)
			
			message = characters[0].chooseAction(self.options)

			for i in range(len(self.characters)):
				self.characters[i].decayAllMotives(self.tickSpeed)
				self.characters[i].reorderMotives()
				self.characterInfoWidgets[i].DrawMotiveValues(self.characters[i].motives)
			
			
			self.TimeLabel.setText(self.currentTime)


if __name__=='__main__':

	characters: list[sim.character] = read_characters.read_characters('input/characters.yml')
	options: list[sim.advertisement] = read_advertisements.read_advertisements('input/advertisements.yml')

	app = qtw.QApplication(sys.argv)
	w = MainWindow(characters, options)
	sys.exit(app.exec_())
