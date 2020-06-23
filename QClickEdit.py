import datetime
from functools import partial

from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtWidgets import QHBoxLayout, QPushButton, QLabel
from PySide2.QtCore import Qt, QTime

from PySide2.QtWidgets import QSpinBox as SpinBox
from PySide2.QtWidgets import QLineEdit as LineEdit
from PySide2.QtWidgets import QTimeEdit as TimeEdit
from PySide2.QtWidgets import QComboBox as ComboBox


class QClickEdit(QWidget):
    """Displays text, changes to the specified user input field when clicked
    on, then reverts to text again when the widget loses focus.

    Self.input_widget holds the Qt user input widget. Any of the functions
    inherent to the widget can be executed, though compatability with this
    module cannot be guaranteed. Self.text holds the value displayed when a
    QClickEdit object is out of focus. Text is displayed as a QPushButton
    widget with flat text. When a QClickEdit widget is clicked on, it hides
    the text and displays the underlying Qt user input widget. When the user
    clicks elseware or the input widget loses focus, a QClickEdit widget
    reverts back to the flat text in self.text, displaying the current value
    of the underlying widget.

    Input widgets currently supported: QSpinBox, QLineEdit, QTimeEdit, and
    QComboBox.

    Values can be set for QClickEdit widgets, regardless of the type of input
    widget used, with the function setValue(), and values can be returned with
    getValue(). QLineEdit and QComboBox return as a string, QSpinBox returns
    as an integer, and QTimeEdit returns as a QTime Object.

    """

    # Registry saves instances of this class to iterate through them and
    # determine when to freeze edit fields
    _registry = []

    # Registry to keep track of which widgets have modified mousePressEvent()
    # functions, so they don't get rewritten every time a new QClickEdit object
    # is created.
    _top_widgets_modified = []

    def __init__(self, current_value, type_of_field=False, suffix=False,
                 parent=None):
        """Arguments:

        current_value -- The desired default value of the input widget
        type_of_field -- Optional argument - This string will precede the
                         displayed current value
        suffix -- suffix to follow current value displayed when self.text is
                  visible.
        """
        if not (isinstance(type_of_field, str) or (type_of_field is False)):
            raise TypeError("type_of_field argument is a descriptive prefix and must be a string")
        if not (isinstance(suffix, str) or (suffix is False)):
            raise TypeError("Suffix must be a string")

        QWidget.__init__(self)

        self.suffix = suffix

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setMargin(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        if type_of_field:
            self.layout.addWidget(QLabel(type_of_field + ": ", self))

        self.destroyed.connect(lambda: self._registry.remove(self))
        self._registry.append(self)

        self._createInputWidget()
        self._createTextWidget()
        self.setValue(current_value)

        top_widgets = QApplication.topLevelWidgets()

        for tw in top_widgets:
            if tw in self._top_widgets_modified:
                continue
            self._top_widgets_modified.append(tw)
            original_MPE = tw.mousePressEvent
            MPE = partial(self._topWidgetMousePressEvent, tw, original_MPE)
            tw.mousePressEvent = MPE

    # Private Functions #

    def _topWidgetMousePressEvent(self, parent, original_mousePressEvent,
                                  event):
        """Overrides a class's mouse press event while still triggering the
        original mouse press event. self._freezeInputPrecheck() runs
        afterwards.
        """
        original_mousePressEvent(event)

        self._freezeInputPrecheck()

    def _setToEdit(self):
        """When the text of this QClickEdit object is clicked upon, this
        function is triggered, which reverts the input field of any other
        QClickEdit object in the window to flat text with
        _freezeInputPrecheck(), then displays the input field of this object
        """
        self._freezeInputPrecheck()
        self._showInputField()

    def _freezeInputPrecheck(self):
        """Runs _showText() for any input widgets not under mouse"""
        for ClickEdit_widget in self._registry:
            if (ClickEdit_widget.input_widget.isVisible()) and \
               (not ClickEdit_widget.input_widget.underMouse()):

                ClickEdit_widget._showText()

    def _createTextWidget(self):
        """Creates QPushButton widget that will display the current value as
        text when self.input_widget is not displayed."""
        self.text = QPushButton("-", self)
        self.text.setStyleSheet("text-align: left; margin: 2")
        self.text.setFlat(True)
        text = self._addSuffix(self.getValue())
        self.text.setText(text)

        self.text.clicked.connect(self._setToEdit)

        self.layout.addWidget(self.text)

    def _createInputWidget(self):
        """Creates the user input widget as determined by the child class,
        changes this object's focusOutEvent function, then hides the input
        widget."""
        self.input_widget = self.widget_()
        self.input_widget.focusOutEvent = self.focusOutEvent
        self.layout.addWidget(self.input_widget)
        self.input_widget.hide()

    def _addSuffix(self, current_value):
        """Adds specified suffix to displayed text"""
        if self.suffix:
            text = str(current_value) + ' ' + self.suffix
        else:
            text = str(current_value)
        return text

    def _showInputField(self):
        """Hides self.text and displays the input widget"""
        self.text.hide()
        self.input_widget.show()

    def _showText(self):
        """Hides the input widget and displays self.text"""
        self.input_widget.hide()
        self.text.show()

    ##########################################
    # Public Functions (modified inherited) ###
    ##########################################
    def focusOutEvent(self, event):
        """Runs the original Qt focusOutEvent function, then runs
        self._freezeInputPrecheck, which determines the display state of each
        QClickEdit object in the window.

        The original focusOutEvent function is executed to ensure that any
        modifications to it from outside the QClickEdit module will still run.
        """
        super(QClickEdit, self).focusOutEvent(event)
        self._freezeInputPrecheck()


class QSpinBox(QClickEdit):
    """QSpinBox QClickEdit object.

    Text displayed becomes QSpinBox field when clicked upon and back to 'flat'
    text when clicked away from.
    """

    def __init__(self, current_value, type_of_field=False, suffix=False):
        self.widget_ = SpinBox
        QClickEdit.__init__(self, current_value, type_of_field, suffix,
                            parent=None)

    # Private Functions #

    def _createInputWidget(self):
        QClickEdit._createInputWidget(self)
        self.input_widget.setFocusPolicy(Qt.StrongFocus)
        self.input_widget.valueChanged.connect(self._updateCurrentValue)

    def _updateCurrentValue(self):
        self.text.setText(self._addSuffix(self.input_widget.value()))

    ####################
    # Public Functions #
    ####################
    def getValue(self):
        """Returns the current value"""
        return self.input_widget.value()
    def setValue(self, value):
        """Sets the current value"""
        text = self._addSuffix(value)
        self.text.setText(text)

        self.input_widget.setValue(value)


class QLineEdit(QClickEdit):
    """QLineEdit QClickEdit object.

    Text displayed becomes QLineEdit field when clicked upon and back to 'flat'
    text when clicked away from.
    """

    def __init__(self, current_value, type_of_field=False, suffix=False):
        self.widget_ = LineEdit

        self._current_value = current_value
        QClickEdit.__init__(self, current_value, type_of_field, suffix,
                            parent=None)

    # Private Functions #

    def _createInputWidget(self):
        QClickEdit._createInputWidget(self)

        self.input_widget.setFocusPolicy(Qt.StrongFocus)
        self.input_widget.textChanged.connect(self._updateCurrentValue)

    def _updateCurrentValue(self):
        self.text.setText(self._addSuffix(self.input_widget.text()))

    ####################
    # Public Functions #
    ####################
    def getValue(self):
        """Returns the current value"""
        return self.input_widget.text()
    def setValue(self, value):
        """Sets the current text"""
        current_value = str(value)
        self.input_widget.setText(current_value)


class QTimeEdit(QClickEdit):
    """QTimeEdit QClickEdit object.

    Text displayed becomes QTimeEdit field when clicked upon and back to 'flat'
    text when clicked away from.
    """

    def __init__(self, current_time, type_of_field=False,
                 display_format='h:mm:ss a'):
        self._inputCheck(current_time)

        self._display_format = display_format

        self.widget_ = TimeEdit
        QClickEdit.__init__(self, self._current_value, type_of_field,
                            parent=None)

        self.setMinimumWidth(100)
        self.setMaximumWidth(100)

        self.setStyleSheet('margin-left: 0;')
        if type_of_field:
            type_of_field_space = len(type_of_field) * 5
            self.setMaximumWidth(type_of_field_space + 200)

    # Private Functions #

    def _createInputWidget(self):
        QClickEdit._createInputWidget(self)

        self.input_widget.setFocusPolicy(Qt.StrongFocus)
        self.input_widget.timeChanged.connect(self._updateCurrentValue)

    def _setToEdit(self):
        QClickEdit._setToEdit(self)

        self.input_widget.setDisplayFormat(self._display_format)

    def _updateCurrentValue(self):
        current_value = self.input_widget.time()
        self.text.setText(current_value.toString(self._display_format))

    def _inputCheck(self, value):
        """Checks if given time is proper type"""
        if isinstance(value, datetime.time):
            self._current_value = QTime(value)
        elif isinstance(value, QTime):
            self._current_value = value
        elif value is False:
            self._current_value = QTime(0, 0, 0, 0)
        else:
            raise TypeError("current_time must be datetime.time or QTime object, or set to False")

    ####################
    # Public Functions #
    ####################
    def getValue(self):
        """Returns the currently selected time"""
        return self.input_widget.time()
    def setValue(self, value):
        """Set the current time"""
        self._inputCheck(value)

        self.text.setText(value.toString('h:mm:ss a'))
        self.input_widget.setTime(value)

    def setDisplayFormat(self, format_string):
        """Sets format of time displayed in flattened text and QTimeEdit.

        Arguments:

        format_string -- Use the same formatting for the string as
                         QTimeEdit.setDisplayFormat()
        """
        self.text.setText(self.input_widget.time().toString(format_string))
        self.input_widget.setDisplayFormat(format_string)

        self._display_format = format_string


class QComboBox(QClickEdit):
    """QComboBox QClickEdit object.

    __init__ function argument accepts a list, of which the items will become
    the selectable items of the QComboBox. It also accepts a single string or
    number, or any other object that can be passed to a str() function, which
    will become the sole item of the QComboBox. Additional items may be added
    with the addItem() function. Or, more directly, with
    self.input_widget.addItem().
    """

    def __init__(self, items):
        items = self._inputCheck(items)

        self.widget_ = ComboBox
        QClickEdit.__init__(self, self._current_value, False, parent=None)

        for item in items:
            self.input_widget.addItem(item)

    # Private Functions #

    def _createInputWidget(self):
        QClickEdit._createInputWidget(self)
        self.input_widget.setFocusPolicy(Qt.StrongFocus)
        self.input_widget.currentIndexChanged.connect(self._updateCurrentValue)

    def _inputCheck(self, values):
        items = []

        if isinstance(values, list):
            self._current_value = str(values[0])
            for v in values:
                item = str(v)
                items.append(item)
        else:
            items.append(str(values))

        return items

    def _updateCurrentValue(self):
        self.text.setText(self.input_widget.currentText())

    ####################
    # Public Functions #
    ####################
    def getValue(self):
        """Returns the current item in QComboBox input widget"""
        return self.input_widget.currentText()
    def setValue(self, v):
        """Set current item of QComboBox by value"""
        value = str(v)

        self.input_widget.setCurrentIndex(self.input_widget.findText(value))
        self.text.setText(value)

    def setIndex(self, index):
        """Set value of QComboBox by Index"""
        self.input_widget.setCurrentIndex(index)
        self.text.setText(self.input_widget.currentText())
    def getCurrentIndex(self):
        return self.input_widget.currentIndex()
    def removeIndex(self, index):
        self.input_widget.removeItem(index)

    def addItem(self, item):
        """Adds an item to the QComboBox"""
        item = str(item)
        self.input_widget.addItem(item)
    def removeItem(self, item):
        item = str(item)

        self.input_widget.removeItem(self.input_widget.findText(item))
