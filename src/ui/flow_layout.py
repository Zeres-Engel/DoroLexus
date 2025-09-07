from PySide6.QtWidgets import QLayout, QSizePolicy, QWidgetItem
from PySide6.QtCore import QPoint, QRect, QSize


class FlowLayout(QLayout):
    """A simple flow layout that wraps items and centers rows.
    Based on Qt's FlowLayout example, adapted for PySide6.
    """

    def __init__(self, parent=None, margin=0, spacing=10):
        super().__init__(parent)
        self._item_list = []
        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self._item_list.append(item)

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)
        return None

    def expandingDirections(self):
        return 0

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self._do_layout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        size += QSize(left + right, top + bottom)
        return size

    def _do_layout(self, rect, test_only):
        x = rect.x()
        y = rect.y()
        line_height = 0

        left, top, right, bottom = self.getContentsMargins()
        effective_rect = rect.adjusted(+left, +top, -right, -bottom)
        x = effective_rect.x()
        y = effective_rect.y()
        max_width = effective_rect.width()

        spacing_x = self.spacing()
        spacing_y = self.spacing()

        row_items = []
        row_width = 0
        total_height = 0

        def place_row(items, start_x, y_pos):
            for item in items:
                item_geom = item.geometry()
                item.setGeometry(QRect(start_x, y_pos, item_geom.width(), item_geom.height()))
                start_x += item_geom.width() + spacing_x

        for item in self._item_list:
            next_x = x + item.sizeHint().width() + spacing_x
            if next_x - spacing_x - effective_rect.x() > max_width and row_items:
                # Center current row
                extra_space = max_width - row_width + spacing_x
                start_x = effective_rect.x() + max(0, extra_space // 2)
                if not test_only:
                    place_row(row_items, start_x, y)
                y += line_height + spacing_y
                total_height += line_height + spacing_y
                x = effective_rect.x()
                row_items = []
                row_width = 0
                line_height = 0

            item_width = item.sizeHint().width()
            item_height = item.sizeHint().height()
            row_items.append(item)
            row_width += item_width + (spacing_x if row_items else 0)
            line_height = max(line_height, item_height)
            x = effective_rect.x() + row_width

        if row_items:
            extra_space = max_width - row_width + spacing_x
            start_x = effective_rect.x() + max(0, extra_space // 2)
            if not test_only:
                place_row(row_items, start_x, y)
            y += line_height
            total_height += line_height

        return total_height + top + bottom
