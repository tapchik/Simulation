import sys
import datetime
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.uic as uic

import simulation as sim
from readers import read_characters, read_advertisements

from UI.CharacterInfoWidget import CharacterInfoWidget

Ui_MainWindow, baseClass = uic.loadUiType('UI/MainWindow.ui')

class MainWindow(baseClass, Ui_MainWindow):

	def __init__(self, simulation: sim.simulation, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.DATETIME_START = datetime.datetime(2023, 7, 15, hour=12, minute=00)

		self.simulation: sim.simulation = simulation
		self.characters_ids: list[str] = list(self.simulation.characters.keys()) # not used yet
		self.tickSpeed: int = 0

		self.setupUi(self)

		self.characterInfoWidgets: dict[str, CharacterInfoWidget] = {char_id: CharacterInfoWidget(char) for char_id, char in self.simulation.characters.items()}
		layout = self.groupBox_3.layout()
		for i in reversed(range(layout.count())):
			layout.itemAt(i).widget().setParent(None)
		for charWidget in self.characterInfoWidgets.values():
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

	def RedrawCharacterInfoWidgets(self):
		"""Redraws status and motives of characters in the interface. """
		for char_id in self.simulation.characters.keys():
			character = self.simulation.characters[char_id]
			self.characterInfoWidgets[char_id].DrawStatus(character.status)
			self.characterInfoWidgets[char_id].DrawMotiveValues(character.motives)

	def TickTicked(self):
			
		# don't do anything if speed is zero
		if self.tickSpeed == 0:
			return

		self.TicksLabel.setText(f"({self.simulation.ticksPassed} ticks)")
		self.timer.start(1000)
		
		if characters['max'].isPerformingAction == False: 
			chosen_motive = characters['max'].chooseMotiveToFulfill()
			action = self.simulation.chooseAdvertismentToFulfillMotive(chosen_motive)
		
			if action != None:
				characters['max'].currentAdvertisement = action
				characters['max'].timeStartedAdvertisment = self.simulation.ticksPassed
				item = qtw.QListWidgetItem(f"{self.currentTime}: {action.message_start}".format(name=characters['max'].name))
				self.listOfMessagesWidget.insertItem(0, item)
		characters['max'].ActUponAdvertisement(self.simulation.ticksPassed, self.tickSpeed)

		# time passes
		self.simulation.ticksAdd(self.tickSpeed)

		# 
		
		# redrawing interface
		self.RedrawCharacterInfoWidgets()
		self.TimeLabel.setText(self.currentTime)


if __name__=='__main__':

	characters = read_characters.read_characters('input/characters.yml')
	advertisements = read_advertisements.read_advertisements('input/advertisements.yml')
	simulation = sim.simulation(characters=characters, advertisements=advertisements)

	app = qtw.QApplication(sys.argv)
	w = MainWindow(simulation)
	sys.exit(app.exec_())
