import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import PyQt5.uic as uic

Ui_MotivePill, baseClass = uic.loadUiType('UI/MotivePill.ui')

class MotivePill(baseClass, Ui_MotivePill):
    # constants
    GREEN_BACKGROUND = (160, 239, 166)
    RED_BACKGROUND = (233, 107, 107)
    GREEN_BORDER = (142, 219, 148)
    RED_BORDER = (205, 98, 98)
    def __init__(self, title: str, value: int, highlighted: bool, *args, **kwargs):
        """0 <= value <= 100"""
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.MotiveLabel.setText(title)
        backgroundColor = self._ShiftColors(self.GREEN_BACKGROUND, self.RED_BACKGROUND, value/100)
        if highlighted == True:
            borderColor = "rgb(250, 231, 23)"
        else:
            borderColor = self._ShiftColors(self.GREEN_BORDER, self.RED_BORDER, value/100)
        self.MotiveLabel.setStyleSheet(f"border-radius: 12px; border: 2px solid {borderColor}; background-color: {backgroundColor}")
        #self.show()

    def _ShiftColors(self, color1: tuple, color2: tuple, shift: float) -> str: 
        """Return rbg(r, g, b) color shifting from color1 to color 2. shift==0->color1, shift==2->color2. """
        r = int(color1[0] + (color2[0] - color1[0]) * shift)
        g = int(color1[1] + (color2[1] - color1[1]) * shift)
        b = int(color1[2] + (color2[2] - color1[2]) * shift)
        return f"rgb({r}, {g}, {b})"

if __name__=='__main__':
	app = qtw.QApplication(sys.argv)
	#w = MotivePill()
	sys.exit(app.exec_())
