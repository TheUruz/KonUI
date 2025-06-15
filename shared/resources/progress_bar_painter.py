from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QStyledItemDelegate


class ProgressBarPainter(QStyledItemDelegate):
    def __init__(self, progress_map, parent):
        super().__init__(parent)
        self.progress_map: dict[int, int] = progress_map

    def paint(self, painter, option, index):
        row = index.row()
        progress = self.progress_map.get(row, 0)
        rect = option.rect
        fill_width = int(rect.width() * progress / 100)
        painter.fillRect(rect.adjusted(0, 0, -rect.width() + fill_width, 0), QColor(0, 200, 0, 100))
        super().paint(painter, option, index)
