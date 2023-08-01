import sys
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

		self.simulation: sim.simulation = simulation
		self.characters_ids: list[str] = list(self.simulation.characters.keys()) # not used yet
		self.tickSpeed: int = 0

		self.setupUi(self)

		self.characterInfoWidgets: dict[str, CharacterInfoWidget] = {}
		for char_id, char in self.simulation.characters.items(): 
			widget = CharacterInfoWidget(char.name, self.simulation.retrieveCharacterStatus(char_id), self.simulation.retrieveCharacterMotives(char_id)) 
			self.characterInfoWidgets[char_id] = widget
		
		layout = self.groupBox_3.layout()
		for i in reversed(range(layout.count())):
			layout.itemAt(i).widget().setParent(None)
		for charWidget in self.characterInfoWidgets.values():
			layout.addWidget(charWidget)

		self.timer=qtc.QTimer()
		self.timer.timeout.connect(self.TickTicked)
		
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
		self.RedrawControlInfo()

	def resetTimer(self): 
		if self.tickSpeed != 0:
			msec = int(1000 / self.tickSpeed)
			self.timer.start(msec)

	def RedrawCharacterInfoWidgets(self):
		"""Redraws status and motives of characters in the interface. """
		for char_id in self.simulation.characters.keys():
			status = self.simulation.retrieveCharacterStatus(char_id)
			motives = self.simulation.retrieveCharacterMotives(char_id)
			self.characterInfoWidgets[char_id].DrawStatus(status)
			active_motive = self.simulation.retrieveCharacterActiveMotive(char_id)
			highlighted = self.simulation.translate[active_motive]
			self.characterInfoWidgets[char_id].DrawMotiveValues(motives, highlighted)
	
	def RedrawControlInfo(self):
		self.TimeLabel.setText(self.simulation.currentTime)
		self.TicksLabel.setText(f"({self.simulation.ticksPassed} ticks)")

	def TickTicked(self):
		
		for character in self.simulation.characters.values(): 
			# do your thing
			character.ActUponAdvertisement(self.simulation.ticksPassed, self.tickSpeed)
			# skipping character if his busy
			if character.isPerformingAction(self.simulation.ticksPassed): 
				continue
			# choosing a motive to fulfill and an action
			motive_to_fulfill = character.chooseMotiveToFulfill()
			action = self.simulation.chooseAdvertismentToFulfillMotive(motive_to_fulfill)
			if action == None: 
				continue
			character.currentAdvertisement = action
			character.timeStartedAdvertisment = self.simulation.ticksPassed
			# writing a console message
			item = qtw.QListWidgetItem(f"{self.simulation.currentTime}: {action.message_start}".format(name=character.name))
			self.listOfMessagesWidget.insertItem(0, item)

		# time passes
		self.simulation.progress(1)
		
		# redrawing interface
		self.RedrawCharacterInfoWidgets()
		self.RedrawControlInfo()

if __name__=='__main__':

	characters = read_characters.read_characters('input/characters.yml', 'translation/russian.yml')
	advertisements = read_advertisements.read_advertisements('input/advertisements.yml')
	translate = sim.translate('translation/russian.yml')
	simulation = sim.simulation(characters=characters, advertisements=advertisements, translate=translate)

	app = qtw.QApplication(sys.argv)
	w = MainWindow(simulation)
	sys.exit(app.exec_())
