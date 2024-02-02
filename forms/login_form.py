import random
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QMessageBox, QGraphicsOpacityEffect
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, pyqtProperty, QTimer
from database.db_operations import register, login
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtProperty

from PyQt5.QtGui import QPainter

class ScalableWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scale = 1.0

    def getScale(self):
        return self._scale

    def setScale(self, scale):
        self._scale = scale
        self.update()

    scale = pyqtProperty(float, getScale, setScale)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.scale(self._scale, self._scale)
        super().paintEvent(event)

    scale = pyqtProperty(float, getScale, setScale)
    
class WelcomeLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.welcome_messages = [
            "Welcome to Phantom Browser",
            "Experience the web like never before",
            "Join our open-source community",
            "Developed with love by User319183",
            "Please sign in or register to get started"
        ]
        self.message_index = 0
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)

        self.fade_in_animation = QPropertyAnimation(self.opacity_effect, b'opacity')
        self.fade_in_animation.setDuration(2000)
        self.fade_in_animation.setStartValue(0)
        self.fade_in_animation.setEndValue(1)
        self.fade_in_animation.setEasingCurve(QEasingCurve.OutCubic)

        self.fade_out_animation = QPropertyAnimation(self.opacity_effect, b'opacity')
        self.fade_out_animation.setDuration(2000)
        self.fade_out_animation.setStartValue(1)
        self.fade_out_animation.setEndValue(0)
        self.fade_out_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_out_animation.finished.connect(self.fade_in)

    def update_message(self):
        self.message_index = (self.message_index + 1) % len(self.welcome_messages)
        self.fade_out_animation.start()

    def fade_in(self):
        self.setText(self.welcome_messages[self.message_index])
        self.fade_in_animation.start()

    def getOpacity(self):
        return self._opacity

    def setOpacity(self, opacity):
        self._opacity = opacity
        self.update()

    opacity = pyqtProperty(float, getOpacity, setOpacity)
    
class LoginForm(ScalableWidget):
    def __init__(self, navbar):
        super().__init__()
        
        # Set default width and height
        self.setFixedWidth(1000)
        self.setFixedHeight(400)
        
        self.navbar = navbar
        self.user_is_logged_in = False
        self.user_is_registered = False

        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton('Register', self)
        self.register_button.clicked.connect(self.register)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Username:'))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.login_button)

        self.welcome_label = WelcomeLabel(self)
        self.welcome_label.setFont(QFont("Arial", 20))
        self.welcome_label.setWindowFlags(Qt.FramelessWindowHint)
        self.welcome_label.setAttribute(Qt.WA_TranslucentBackground)
        layout.addWidget(self.welcome_label)

        self.setLayout(layout)

        # Check if the user is logged in or not
        if not self.is_user_logged_in() and not self.is_user_registered():
            QTimer.singleShot(0, self.welcome_label.fade_in)
            self.message_timer = QTimer(self)
            self.message_timer.timeout.connect(self.welcome_label.update_message)
            self.message_timer.start(5000) # update the message every 5 seconds
            
    def show_welcome_animation(self):
        self.opacity_effect = QGraphicsOpacityEffect(self.welcome_label)
        self.welcome_label.setGraphicsEffect(self.opacity_effect)

        self.animation = QPropertyAnimation(self.opacity_effect, b'opacity')
        self.animation.setDuration(2000) # 2 seconds for a slower transition
        self.animation.setStartValue(0) # start from fully transparent
        self.animation.setEndValue(1) # end at fully opaque
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

        self.animation.start()
        
    def hide_form(self):
        self.hide()

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username == "" or password == "":
            QMessageBox.warning(self, 'Registration', 'Please enter a username and password.')
            return
        register(username, password)
        QMessageBox.information(self, 'Registration', 'Registration successful. You are now logged in.')
        self.hide_form()
        self.navbar.show()
        self.user_is_registered = True
        self.user_is_logged_in = True

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if login(username, password):
            QMessageBox.information(self, 'Login', 'Login successful.')
            self.hide_form()
            self.navbar.show()
            self.user_is_logged_in = True
        else:
            QMessageBox.warning(self, 'Login', 'Login failed.')

    def is_user_logged_in(self):
        return self.user_is_logged_in
    
    def is_user_registered(self):
        return self.user_is_registered