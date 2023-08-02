import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.uic as uic

from simulation import character
from simulation import motive

from UI.MotiveGroupWithBar import MotiveGroupWithBar
from UI.MotivePill import MotivePill

#from ui import Ui_MainWindow
Ui_CharacterInfo, baseClass = uic.loadUiType('UI/CharacterInfoWidget.ui')

class CharacterInfoWidget(baseClass, Ui_CharacterInfo):
	def __init__(self, name: str, status: str, motives: dict[str, motive], *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setupUi(self)
		
		self.CharacterNameLabel.setText(name)
		self.DrawStatus(status)
		self.DrawMotiveValues(motives)

	def DrawStatus(self, status: str | None): 
		statusLabel = self.StatusLabel
		if status != None:
			statusLabel.setText(status)
		else:
			statusLabel.setText("Курит")

	def DrawMotiveValues(self, motives: dict[str, motive], highlighted: str | None = None):
		layout = self.ScrollMotivesLayout.layout()
		# deleting old
		for i in reversed(range(layout.count())):
			layout.itemAt(i).widget().setParent(None)
		# draw highlighted motive first
		if highlighted != None:
			mot = motives[highlighted]
			mot_groupBox = MotivePill(mot.title, mot.percentage, True)
			layout.addWidget(mot_groupBox)
		# draw other motives next
		for key, mot in motives.items():
			#highlight = True if key == highlighted else False
			if key == highlighted:
				continue
			mot_groupBox = MotivePill(mot.title, mot.percentage, False) #MotiveGroupWithBar(title, value)
			layout.addWidget(mot_groupBox)
		#self.show()

if __name__=='__main__':
	app = qtw.QApplication(sys.argv)
	w = CharacterInfoWidget()
	sys.exit(app.exec_())
