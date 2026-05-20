# CRS Companion / CRSさん

A QGIS plugin that shows a dockable panel for the current project CRS.

The panel displays, from top to bottom:

1. CRS character image
2. Horizontal resize handle
3. CRS code such as `EPSG:4326`
4. CRS name
5. CRS explanation text

CRS data and most plugin UI strings are stored in `crs_companion/crs_data/crs_companion.json`.
Images are stored in `crs_companion/images/`.

Initial supported CRS:

- EPSG:4326
- EPSG:3857
- EPSG:4301
- EPSG:6668

## Image resizing

The image width follows the dock panel width.
The image height is changed only by dragging the horizontal line handle below the image. Dragging on the image itself does not resize it.
The explanation text area absorbs the remaining dock space.

## Localization

The plugin is designed for `en` and `ja` from the start.

- English display name: `CRS Companion`
- Japanese display name: `CRSさん`

Most visible strings are externalized in the `ui` section of `crs_companion/crs_data/crs_companion.json`.
Translation source files are also included in `crs_companion/i18n/` for future Qt-based UI strings.
Compile `.ts` files to `.qm` with Qt Linguist tools in your QGIS/Qt environment if needed.

## Install

Zip the `crs_companion` folder (**not repository root**), then install it from QGIS Plugin Manager using "Install from ZIP".
