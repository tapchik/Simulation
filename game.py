import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.uic as uic

import simulation as sim
from readers import read_characters

from UI.CharacterInfoWidget import CharacterInfoWidget

Ui_MainWindow, baseClass = uic.loadUiType('UI/MainWindow.ui')

class MainWindow(baseClass, Ui_MainWindow):

	def __init__(self, simulation: sim.simulation, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.simulation = simulation
		self.characters_ids: list[str] = list(self.simulation.characterRepository.keys()) # not used yet
		self.tickSpeed: int = 0

		self.setupUi(self)
		self.setWindowTitle("Simulation")

		self.characterInfoWidgets: dict[str, CharacterInfoWidget] = {}
		for char_id, char in self.simulation.characterRepository.items():
			motives = self.simulation.characterRepository[char_id].motives
			widget = CharacterInfoWidget(char.name, self.simulation.retrieveCharacterStatus(char_id), motives)
			self.characterInfoWidgets[char_id] = widget
		
		layout = self.groupBox_3.layout()
		for i in reversed(range(layout.count())):
			layout.itemAt(i).widget().setParent(None)
		for charWidget in self.characterInfoWidgets.values():
			layout.addWidget(charWidget)

		self.timer = qtc.QTimer()
		self.timer.timeout.connect(self.tickTicked)
		
		self.SpeedSlider.valueChanged.connect(self.SpeedSliderMoved)

		self.show()

	def SpeedSliderMoved(self, new_value: int) -> None:
		old_value = self.tickSpeed
		# update interface
		self.tickSpeed = new_value
		self.SpeedLabel.setText(f"Speed: {self.tickSpeed}")
		
		if old_value != 0 and new_value == 0: 
			#self.TickTicked()
			self.timer.stop()
		self.resetTimer()
		self.redrawControlInfo()

	def resetTimer(self): 
		if self.tickSpeed != 0:
			msec = int(1000 / self.tickSpeed)
			self.timer.start(msec)

	def redrawCharacterInfoWidgets(self):
		"""Redraws status and motives of characters in the interface. """
		for char_id in self.simulation.characterRepository.keys():
			character = self.simulation.characterRepository[char_id]
			status = self.simulation.retrieveCharacterStatus(char_id)
			self.characterInfoWidgets[char_id].DrawStatus(status)
			currently_fulfilling_motive = self.simulation.currentlyFulfillingMotive(char_id)
			self.characterInfoWidgets[char_id].DrawMotiveValues(character.motives, currently_fulfilling_motive)
	
	def redrawControlInfo(self):
		self.TimeLabel.setText(self.simulation.retrieveCurrentTime)
		self.TicksLabel.setText(f"({self.simulation.ticksPassed} ticks)")

	def tickTicked(self):

		self.simulation.stopEachFinishedAction()
		self.simulation.assignActionForEachFreeCharacter()
		self.simulation.eachCharacterPerformsAssignedAction()
		# TODO: find a way to write a message in a console
		# item = qtw.QListWidgetItem(f"{self.simulation.RetrieveCurrentTime}: {ad.message_start}".format(name=character.name))
		# self.listOfMessagesWidget.insertItem(0, item)

		# time passes
		self.simulation.progress(1)
		
		# redrawing interface
		self.redrawCharacterInfoWidgets()
		self.redrawControlInfo()


if __name__=='__main__':
	
	translate = sim.translate('translation/russian.yml')
	simulation = sim.simulation(translate=translate)
	simulation.addAdvertisments('input/advertisements.yml')
	simulation.addCharacters('input/characters.yml')

	app = qtw.QApplication(sys.argv)
	w = MainWindow(simulation)
	sys.exit(app.exec_())
