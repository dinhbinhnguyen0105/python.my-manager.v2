# src/views/robot/action_payload_container.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSlot
from src.ui.action_payload_ui import Ui_ActionPayloadContainer


class ActionPayloadContainer(QWidget, Ui_ActionPayloadContainer):
    def __init__(self, parent=None):
        super(ActionPayloadContainer, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("action payload container")
        self.action_name.clear()
        self.action_payload.clear()
        # self.pid_input
        self.pid_input.setHidden(True)
        self.set_comboboxes()
        self.set_events()

    def set_comboboxes(self):
        self.action_name.addItem("List on group", "list_on_group")
        self.action_name.addItem("List on marketplace", "list_on_marketplace")
        self.action_name.addItem("Interaction", "interaction")
        self.action_payload.addItem("Random PID", "random_pid")
        self.action_payload.addItem("Set PID", "set_pid")

    def set_events(self):
        self.action_payload.currentIndexChanged.connect(self.on_action_payload_changed)
        self.action_name.currentIndexChanged.connect(self.on_action_name_changed)

    @pyqtSlot(int)
    def on_action_name_changed(self, index: int):
        is_interaction = self.action_name.itemData(index) == "interaction"
        self.action_payload.setHidden(is_interaction)
        self.pid_input.setHidden(
            is_interaction
            or self.action_payload.itemData(self.action_payload.currentIndex())
            == "random_pid"
        )
        if is_interaction:
            self.pid_input.clear()

    @pyqtSlot(int)
    def on_action_payload_changed(self, index: int):
        is_random_pid = self.action_payload.itemData(index) == "random_pid"
        self.pid_input.setHidden(is_random_pid)
        if is_random_pid:
            self.pid_input.clear()

    def get_values(self):
        result = {
            "action_name": self.action_name.itemData(self.action_name.currentIndex()),
            "action_payload": self.action_payload.itemData(
                self.action_payload.currentIndex()
            ),
        }
        if self.pid_input.isVisible():
            result["pid"] = self.pid_input.text().strip()
        return result
