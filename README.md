# QClickEdit

## Description

This module creates click-to-input text that switches to a Qt input widget when clicked upon, and reverts back to text when the widget loses focus.

Input widgets currently supported: QSpinBox, QLineEdit, QTimeEdit, and QComboBox.

## Using this Module

Values can be set for QClickEdit widgets, regardless of the type of input widget used, with the function setValue(), and values can be returned with getValue(). QLineEdit and QComboBox return as a string, QSpinBox returns as an integer, and QTimeEdit returns as a QTime Object.

See Examples.py for basic use.

## How it functions

Self.input_widget holds the Qt user input widget. Any of the functions inherent to the widget can be executed through self.input_widget, though compatability with this module cannot be guaranteed. Self.text holds the value displayed when a QClickEdit object goes out of focus. Text is displayed as a QPushButton widget with flat text. When a QClickEdit widget is clicked on, it hides the text and displays the underlying Qt user input widget. When the user clicks elseware or the input widget loses focus, a QClickEdit widget reverts back to the flat text in self.text, displaying the current value of the underlying input widget.
