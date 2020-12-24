from view import Ui_Form
from PyQt5 import QtWidgets
import os
import subprocess
import re


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.operationTypeBox.currentIndexChanged.connect(self.operation_changed)
        self.ui.operationTypeBox.setCurrentIndex(1)
        self.ui.selectOriginalFile.clicked.connect(self.select_original_file)
        self.ui.selectCopyFile.clicked.connect(self.select_copy_file)
        self.ui.startButton.clicked.connect(self.start_exec)

    def operation_changed(self, index):
        self.ui.originalFilePathLine.setText('')
        self.ui.copyFilePathLine.setText('')
        if index == 0:
            self.ui.selectOriginalFile.setEnabled(False)
            self.ui.originalFilePathLine.setReadOnly(False)
            self.ui.selectCopyFile.setEnabled(True)
            self.ui.copyFilePathLine.setReadOnly(True)
        elif index == 1:
            self.ui.selectOriginalFile.setEnabled(True)
            self.ui.originalFilePathLine.setReadOnly(True)
            self.ui.selectCopyFile.setEnabled(False)
            self.ui.copyFilePathLine.setReadOnly(False)

    def select_original_file(self):
        file_names = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file...', os.path.dirname(os.getcwd()))
        if len(file_names) == 0:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Файл не выбран')
            return
        else:
            self.ui.originalFilePathLine.setText(file_names[0])

    def select_copy_file(self):
        dir_name = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select file...', os.path.dirname(os.getcwd()))
        if not dir_name:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Файл не выбран')
            return
        else:
            original_file_path = self.ui.originalFilePathLine.text()
            last_ind = original_file_path.rfind('/')
            original_filename = original_file_path[last_ind if last_ind != -1 else 0: ]
            self.ui.copyFilePathLine.setText(dir_name + '/' + original_filename)

    def start_exec(self):
        original_filename = self.ui.originalFilePathLine.text()
        if original_filename == '':
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Неверно указан исходный путь')
            return
        copy_filename = self.ui.copyFilePathLine.text()
        if copy_filename == '':
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Неверно указан путь копирования')
            return
        operation_type = self.ui.operationTypeBox.currentIndex()
        host_ip = self.ui.ipLineEdit.text()
        if not re.match(r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', host_ip):
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Неверно указан IP адрес назначения')
            return

        host_port = self.ui.portLineEdit.text()
        if host_port == '' or not str.isnumeric(host_port):
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Неверно указан порт')
            return

        operation_name = 'send'
        if operation_type == 0:
            operation_name = 'receive'

        large_output = 'false'
        if self.ui.outputCheckBox.isChecked():
            large_output = 'true'

        subprocess_name = './SimpleTFTPClient'
        self.ui.statusLabel.setText(f'Статус: задача выполняется')
        reply = subprocess.run(
            [subprocess_name, operation_name, host_ip, host_port, original_filename, copy_filename, large_output],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8'
        )
        self.ui.logsTextView.clear()
        self.ui.statusLabel.setText(f'Статус: {reply.returncode}')
        if reply.returncode == 0:
            self.ui.logsTextView.appendPlainText(reply.stdout)
        else:
            self.ui.logsTextView.appendPlainText(reply.stderr)
