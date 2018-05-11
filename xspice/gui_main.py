import sys

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QWidget, QPushButton, QTextEdit, QFileDialog,
                             QHBoxLayout, QVBoxLayout, QApplication, QMessageBox, QLabel)

from xspice import xspice as nt
from xspice.error import external_error
from xspice.log import OutLog


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.fileName = ""
        self.initUI()

    def initUI(self):
        load_btn = QPushButton("Load file")
        load_btn.clicked.connect(self.openFileNameDialog)
        simu_btn = QPushButton("Run simulation")
        simu_btn.clicked.connect(self.run_simulation)

        save_btn = QPushButton("Save file")
        save_btn.clicked.connect(self.save_file)

        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(app.quit)

        message_label = QLabel("Message:")
        netlist_label = QLabel("Netlist:")
        self.netlist_edit = QTextEdit()
        self.rst_form = QTextEdit()
        self.rst_form.setReadOnly(True)

        sys.stdout = OutLog(self.rst_form, sys.stdout)
        sys.stderr = OutLog(self.rst_form, sys.stderr, QColor(255, 0, 0))

        btn_box = QVBoxLayout()
        btn_box.addWidget(load_btn)

        btn_box.addWidget(simu_btn)
        btn_box.addWidget(save_btn)
        btn_box.addWidget(exit_btn)

        input_box = QHBoxLayout()

        input_box.addWidget(self.netlist_edit)
        input_box.addLayout(btn_box)

        whole = QVBoxLayout()
        whole.addWidget(netlist_label)
        whole.addLayout(input_box, 5)
        whole.addWidget(message_label)
        whole.addWidget(self.rst_form, 2)

        self.setLayout(whole)

        self.setGeometry(500, 200, 400, 400)
        self.setWindowTitle('Xspice')
        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                       "All Files (*);;Spice netlist (*.sp)", options=options)
        if self.fileName:
            with open(self.fileName, 'r') as spice_file:
                netlist = spice_file.read()
                self.netlist_edit.setText(netlist)

    def save_file(self):
        if self.fileName:
            qm = QMessageBox()
            rst = qm.question(self, '', "Are you sure to overwrite?", qm.Yes | qm.No)
            if rst == qm.Yes:
                with open(self.fileName, 'w') as spice_file:
                    spice_file.write(self.netlist_edit.toPlainText())
        else:
            self.fileName, _ = QFileDialog.getSaveFileName(self, 'Save File', filter="Spice netlist (*.sp)")
            with open(self.fileName, 'w') as spice_file:
                spice_file.write(self.netlist_edit.toPlainText())

    def run_simulation(self):
        self.rst_form.setText("")

        circuit = self.netlist_edit.toPlainText()
        if circuit:
            try:
                rst = nt.Xspice(circuit)
            except external_error as e:
                self.rst_form.append("Error:{}".format(str(e)))
                QMessageBox.information(self, 'Error', str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Example()
    sys.exit(app.exec_())
