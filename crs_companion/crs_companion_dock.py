import os

from qgis.PyQt.QtCore import Qt, QSize
from qgis.PyQt.QtGui import QPixmap
from qgis.PyQt.QtWidgets import (
    QDockWidget,
    QWidget,
    QLabel,
    QTextEdit,
    QVBoxLayout,
    QSizePolicy,
    QFrame,
)
from qgis.core import QgsProject


class CompanionImageLabel(QLabel):
    """Image width follows the dock width; height is controlled only by the handle."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pixmap_original = None
        self._image_height = 220

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setMinimumHeight(80)
        self.setFixedHeight(self._image_height)
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def set_image_height(self, height):
        self._image_height = max(80, min(600, int(height)))
        self.setFixedHeight(self._image_height)
        self._update_scaled_pixmap()

    def image_height(self):
        return self._image_height

    def set_companion_pixmap(self, pixmap):
        self._pixmap_original = pixmap
        self._update_scaled_pixmap()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_scaled_pixmap()

    def _update_scaled_pixmap(self):
        if not self._pixmap_original or self._pixmap_original.isNull():
            self.clear()
            return

        target_size = QSize(max(1, self.width()), self._image_height)
        scaled = self._pixmap_original.scaled(
            target_size,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.setPixmap(scaled)


class ImageResizeHandle(QFrame):
    """Horizontal handle that vertically resizes the companion image."""

    def __init__(self, image_label, parent=None):
        super().__init__(parent)
        self.image_label = image_label
        self._drag_start_y = None
        self._start_height = image_label.image_height()

        self.setObjectName("CrsCompanionImageResizeHandle")
        self.setFixedHeight(14)
        self.setCursor(Qt.CursorShape.SizeVerCursor)
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setStyleSheet(
            "QFrame#CrsCompanionImageResizeHandle {"
            "border-top: 2px solid palette(mid);"
            "margin: 4px 0;"
            "}"
            "QFrame#CrsCompanionImageResizeHandle:hover {"
            "border-top: 3px solid palette(highlight);"
            "}"
        )

    def _get_y(self, event):
        if hasattr(event, "position"):
            return event.position().y()
        return event.pos().y()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_y = self._get_y(event)
            self._start_height = self.image_label.image_height()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_start_y is None:
            super().mouseMoveEvent(event)
            return

        delta = self._get_y(event) - self._drag_start_y
        self.image_label.set_image_height(self._start_height + delta)
        event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_start_y = None
        event.accept()


class CrsCompanionDock(QDockWidget):
    def __init__(self, iface, plugin_dir, config):
        super().__init__()
        self.iface = iface
        self.plugin_dir = plugin_dir
        self.config = config
        self.data = config.data

        self.setObjectName("CrsCompanionDock")
        self.setWindowTitle(self.config.text("dock_title"))

        self.image_label = CompanionImageLabel()
        self.resize_handle = ImageResizeHandle(self.image_label)
        self.resize_handle.setToolTip(self.config.text("resize_handle_tooltip"))
        self.code_label = QLabel()
        self.name_label = QLabel()
        self.description_text = QTextEdit()

        self.description_text.setReadOnly(True)
        self.description_text.setAcceptRichText(False)
        self.description_text.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.code_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.name_label.setWordWrap(True)

        self._setup_layout()

    def default_area(self):
        return Qt.DockWidgetArea.RightDockWidgetArea

    def _setup_layout(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        layout.addWidget(self.image_label)
        layout.addWidget(self.resize_handle)
        layout.addWidget(self.code_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.description_text, 1)

        container.setLayout(layout)
        self.setWidget(container)

    def refresh(self):
        # Reload JSON on refresh so UI/CRS text edits are picked up without restarting QGIS.
        self.config.load()
        self.data = self.config.data
        self.setWindowTitle(self.config.text("dock_title"))
        self.resize_handle.setToolTip(self.config.text("resize_handle_tooltip"))

        crs = QgsProject.instance().crs()
        authid = crs.authid() if crs and crs.isValid() else ""

        items = self.data.get("items", {})
        #
        item = items.get(authid)
        # if items has alias, alias is applued
        if item and "alias" in item:
            item = items.get(item["alias"])
        # If item not found
        if not item:
            item = self._unknown_item(authid)

        self._apply_item(authid, item)

    def _unknown_item(self, authid):
        code = authid or self.config.text("unknown_crs_code")
        return {
            "image": self.data.get("fallback_image", "unknown.png"),
            "name": {
                self.config.locale: self.config.text("unsupported_crs_name"),
            },
            "description": {
                self.config.locale: self.config.text(
                    "unsupported_crs_description",
                    code=code,
                ),
            },
        }

    def _localized_value(self, obj, key):
        return self.config.localized(obj, key)

    def _check_file_in_dir(self, dir_path, relfile_path):
        if relfile_path is None:
            return None
        dir_path = os.path.realpath(dir_path)
        file_path = os.path.realpath(os.path.join(dir_path, relfile_path))
        try:
            if os.path.commonpath([dir_path, file_path]) != dir_path:
                return None
        except ValueError:
            return None
        if not os.path.isfile(file_path):
            return None
        return file_path

    def _apply_item(self, authid, item):
        image_name = None
        if "image" in item:
            image_name = item["image"]
        if image_name is None:
            image_name = self.data.get("fallback_image", "unknown.png")
        # checks whether
        image_path = self._check_file_in_dir( os.path.join(self.plugin_dir, "images"), image_name)
        pixmap = QPixmap(image_path) if image_path is not None else None
        if pixmap is None or pixmap.isNull():
            fallback = os.path.join(
                self.plugin_dir,
                "images",
                self.data.get("fallback_image", "unknown.png"),
            )
            pixmap = QPixmap(fallback)

        self.image_label.set_companion_pixmap(pixmap)
        self.code_label.setText(authid or self.config.text("unknown_crs_code"))
        self.name_label.setText(self._localized_value(item, "name"))
        self.description_text.setPlainText(self._localized_value(item, "description"))
