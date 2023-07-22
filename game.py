import sys
import datetime
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.uic as uic

from random import choice

import simulation as sim
from readers import read_characters, read_advertisements

from UI.CharacterInfoWidget import CharacterInfoWidget

Ui_MainWindow, baseClass = uic.loadUiType('UI/MainWindow.ui')

class MainWindow(baseClass, Ui_MainWindow):

	def __init__(self, simulation: sim.simulation, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.DATETIME_START = datetime.datetime(2023, 7, 15, hour=12, minute=00)

		self.simulation: sim.simulation = simulation
		self.tickSpeed: int = 0

		self.setupUi(self)

		self.characterInfoWidgets: list[CharacterInfoWidget] = [CharacterInfoWidget(char) for char in self.simulation.characters.values()]
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
		t = self.simulation.ticksPassed
		current_time = self.DATETIME_START + datetime.timedelta(minutes=t)
		return current_time.strftime("%H:%M")

	def SpeedSliderMoved(self, new_value: int) -> None:
		self.tickSpeed = new_value
		self.SpeedLabel.setText(f"Speed: {self.tickSpeed}")

	def TickTicked(self):
			
		# don't do anything if speed is zero
		if self.tickSpeed == 0:
			return

		# time passes
		self.simulation.ticksAdd(self.tickSpeed)
		self.TicksLabel.setText(f"({self.simulation.ticksPassed} ticks)")
		self.timer.start(1000)
		
		if characters['max'].isPerformingAction == False: 
			chosen_motive = characters['max'].chooseMotiveToFulfill()
			options = list(filter(lambda ad: ad.motive==chosen_motive, self.simulation.advertisements.values()))
			action = choice(options) if options != [] else None
		
			if action != None:
				characters['max'].currentAdvertisement = action
				characters['max'].timeStartedAdvertisment = self.simulation.ticksPassed
				item = qtw.QListWidgetItem(f"{self.currentTime}: {action.message_start}".format(name=characters['max'].name))
				self.listOfMessagesWidget.insertItem(0, item)
		characters['max'].ActUponAdvertisement(self.simulation.ticksPassed, self.tickSpeed)

		# redraw interface
		count = 0
		for character in self.simulation.characters.values():
			character.decayAllMotives(self.tickSpeed)
			character.reorderMotives()
			self.characterInfoWidgets[count].DrawStatus(character.status)
			self.characterInfoWidgets[count].DrawMotiveValues(character.motives)
			count += 1
		
		
		self.TimeLabel.setText(self.currentTime)


if __name__=='__main__':

	characters = read_characters.read_characters('input/characters.yml')
	advertisements = read_advertisements.read_advertisements('input/advertisements.yml')
	simulation = sim.simulation(characters=characters, advertisements=advertisements)

	app = qtw.QApplication(sys.argv)
	w = MainWindow(simulation)
	sys.exit(app.exec_())
