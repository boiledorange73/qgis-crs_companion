import json
import os

class CrsCompanionConfig:
    """Loads plugin UI strings and CRS companion data from JSON."""

    def __init__(self, plugin_dir):
        self.plugin_dir = plugin_dir
        self.data = {}
        self.locale = self._current_locale()
        self.load()

    def load(self):
        path = os.path.join(self.plugin_dir, "crs_data", "crs_companion.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("root JSON must be an object")
            self.data = data
        except Exception:
            self.data = {}

    def text(self, key, **kwargs):
        value = self.localized(self.data.get("ui", {}), key)
        if kwargs:
            try:
                return value.format(**kwargs)
            except Exception:
                return value
        return value

    def localized(self, obj, key):
        if not isinstance(obj, dict):
            return ""
        # gets values
        values = obj.get(key, {})
        if isinstance(values, str):
            # values can be string if values is not required to be localized.
            return values
        if not isinstance(values, dict):
            # values is dict whose key is a lang and value is a localized text.
            return ""
        return (
            values.get(self.locale)
            or values.get(self.data.get("default_locale", "en"))
            or ""
        )

    def _current_locale(self):
        from qgis.PyQt.QtCore import QLocale
        from qgis.core import QgsApplication, QgsSettings
        settings = QgsSettings()
        override = settings.value("locale/overrideFlag", False, type=bool)
        user_locale = settings.value("locale/userLocale", "", type=str)
        if override and user_locale:
            return str(user_locale).split("_")[0].lower()
        app_locale = ""
        if hasattr(QgsApplication, "locale"):
            app_locale = QgsApplication.locale() or ""
        if app_locale:
            return str(app_locale).split("_")[0].lower()
        return QLocale.system().name().split("_")[0].lower()

