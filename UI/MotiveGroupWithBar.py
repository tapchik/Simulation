import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.uic as uic

from simulation import character
from simulation import motive

#from ui import Ui_MainWindow
Ui_MotiveGroup, baseClass = uic.loadUiType('UI/MotiveGroupWithBar.ui')

class MotiveGroupWithBar(baseClass, Ui_MotiveGroup):
	def __init__(self, motive: motive, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.setupUi(self)
		self.MotiveGroupBox.setTitle(motive.title)
		self.MotiveProgressBar.setValue(motive.percentage)
		#self.show()

if __name__=='__main__':
	app = qtw.QApplication(sys.argv)
	w = MotiveGroupWithBar()
	sys.exit(app.exec_())
