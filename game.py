import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.uic as uic

import simulation as sim

from UI.CharacterInfoWidget import CharacterInfoWidget

Ui_MainWindow, baseClass = uic.loadUiType('UI/MainWindow.ui')

class MainWindow(baseClass, Ui_MainWindow):

	def __init__(self, simulation: sim.Simulation, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.simulation = simulation
		self.character_ids: list[str] = self.simulation._characters.retrieveCharacterIds()
		self.tickSpeed: int = 0

		self.setupUi(self)
		self.setWindowTitle("Simulation")

		self.characterInfoWidgets: dict[str, CharacterInfoWidget] = {}
		for char_id, char in self.simulation._characters.items():
			motives = self.simulation._characters[char_id].motives
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
			# self.TickTicked()
			self.timer.stop()
		self.resetTimer()
		self.redrawControlInfo()

	def resetTimer(self): 
		if self.tickSpeed != 0:
			msec = int(1000 / self.tickSpeed)
			self.timer.start(msec)

	def redrawCharacterInfoWidgets(self):
		"""Redraws status and motives of characters in the interface. """
		for char_id in self.character_ids:
			status = self.simulation.retrieveCharacterStatus(char_id)
			motives = self.simulation.retrieveCharacterMotives(char_id)
			currently_fulfilling_motive = self.simulation.retrieveCurrentlyFulfillingMotive(char_id)
			self.characterInfoWidgets[char_id].DrawStatus(status)
			self.characterInfoWidgets[char_id].DrawMotiveValues(motives, currently_fulfilling_motive)
	
	def redrawControlInfo(self):
		current_time = self.simulation.retrieveCurrentTime
		ticks_passed = self.simulation.ticksPassed
		self.TimeLabel.setText(current_time)
		self.TicksLabel.setText(f"({ticks_passed} ticks)")

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


if __name__ == '__main__':
	
	simulation = sim.Simulation()
	simulation.addTranslation('translation/russian.yml')
	simulation.add_advertisments('input/advertisements.yml')
	simulation.addCharacters('input/characters.yml')

	app = qtw.QApplication(sys.argv)
	w = MainWindow(simulation)
	sys.exit(app.exec_())
