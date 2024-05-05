from PySide6.QtWidgets import QApplication
import sys

import Gui.AllWindows.annotationwindow as ann_Window, Gui.AllWindows.initialwindow as iWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    initial = iWindow.MainWindow()
    annWindow = ann_Window.MainWindow(initial)
    initial.ui.menuCreateModels.actions()[0].triggered.connect(annWindow.show_self)
    annWindow.ui.menuReturn.actions()[0].triggered.connect(annWindow.return_to_main)
    initial.show_self()
    # ALL Signals below this comment
    initial.getactions()
    annWindow.getactions()
    annWindow.runner.getWidgets.connect(annWindow.getActive)
    annWindow.hide()

    if app.exit():
        annWindow.runner.stop()
        annWindow.runner2.stop()
    sys.exit(app.exec())
