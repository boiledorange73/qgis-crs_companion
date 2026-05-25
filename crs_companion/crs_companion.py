import os

from qgis.PyQt.QtCore import QCoreApplication, QTranslator
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject

from .crs_companion_config import CrsCompanionConfig
from .crs_companion_dock import CrsCompanionDock


class CrsCompanionPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.config = CrsCompanionConfig(self.plugin_dir)
        self.translator = None
        self.action = None
        self.dock = None

        self._install_translator()

    def _install_translator(self):
        qm_path = os.path.join(
            self.plugin_dir,
            "i18n",
            f"crs_companion_{self.config.locale}.qm",
        )

        if os.path.exists(qm_path):
            self.translator = QTranslator()
            if self.translator.load(qm_path):
                QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        menu_text = self.tr("CRS Companion")
        menu_toggle_text = self.tr("Toggle CRS Companion")
        icon_path = os.path.join(self.plugin_dir, "crs_companion-32x32.png")
        self.action = QAction(QIcon(icon_path), menu_toggle_text, self.iface.mainWindow())
        self.action.triggered.connect(self.toggle_dock)

        self.iface.addPluginToMenu(menu_text, self.action)
        self.iface.addToolBarIcon(self.action)

        self.dock = CrsCompanionDock(self.iface, self.plugin_dir, self.config)
        self.iface.addDockWidget(self.dock.default_area(), self.dock)
        self.dock.hide()

        QgsProject.instance().crsChanged.connect(self.dock.refresh)
        self.dock.refresh()

    def unload(self):
        if self.dock:
            try:
                QgsProject.instance().crsChanged.disconnect(self.dock.refresh)
            except Exception:
                pass

        if self.action:
            menu_text = self.tr("CRS Companion")
            self.iface.removePluginMenu(menu_text, self.action)
            self.iface.removeToolBarIcon(self.action)
            self.action = None

        if self.dock:
            self.iface.removeDockWidget(self.dock)
            self.dock.deleteLater()
            self.dock = None

        if self.translator:
            QCoreApplication.removeTranslator(self.translator)
            self.translator = None

    def toggle_dock(self):
        if not self.dock:
            return

        self.dock.setVisible(not self.dock.isVisible())
        if self.dock.isVisible():
            self.dock.raise_()
            self.dock.refresh()

    def tr(self, message):
        return QCoreApplication.translate("CrsCompanion", message)