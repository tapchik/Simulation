import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.uic as uic

from simulation import character
from simulation import motive

from UI.MotiveGroupWithBar import MotiveGroupWithBar

#from ui import Ui_MainWindow
Ui_CharacterInfo, baseClass = uic.loadUiType('UI/CharacterInfoWidget.ui')

class CharacterInfoWidget(baseClass, Ui_CharacterInfo):
	def __init__(self, character: character, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setupUi(self)
		self.CharacterNameLabel.setText(character.name)

		
		
		self.DrawMotiveValues(character.motives)

	def DrawStatus(self, status: str | None): 
		statusLabel = self.StatusLabel
		if status != None:
			statusLabel.setText(status)
		else:
			statusLabel.setText("Курит")

	def DrawMotiveValues(self, motives: dict[str, motive]):
		layout = self.ScrollMotivesLayout.layout()
		# deleting old
		for i in reversed(range(layout.count())):
			layout.itemAt(i).widget().setParent(None)
		# drawing
		for title, mot in motives.items():
			mot_groupBox = MotiveGroupWithBar(mot)
			layout.addWidget(mot_groupBox)
		
		#self.show()

if __name__=='__main__':
	app = qtw.QApplication(sys.argv)
	w = CharacterInfoWidget()
	sys.exit(app.exec_())
