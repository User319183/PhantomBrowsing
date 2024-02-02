from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QPushButton, QLineEdit, QWidget, QHBoxLayout, QLabel, QComboBox, QMessageBox, QSizePolicy, QSpacerItem, QSlider, QMainWindow
import sys
from forms.login_form import LoginForm
from web.web_components import CustomWebEngineView, LoadUrlThread

MAX_HEIGHT = 30
NAVBAR_HEIGHT = 100

def create_navbar():
    # Create navigation buttons and address bar
    back_button = QPushButton('Back')
    forward_button = QPushButton('Forward')
    reload_button = QPushButton('Reload')
    address_bar = QLineEdit()

    # Create a user agent dropdown
    user_agent_dropdown = QComboBox()
    user_agent_dropdown.addItem("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537")
    user_agent_dropdown.addItem("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0")
    user_agent_dropdown.addItem("Mozilla/5.0 (iPhone; CPU iPhone OS 13_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1")

    address_bar.setMaximumHeight(MAX_HEIGHT)
    user_agent_dropdown.setMaximumHeight(MAX_HEIGHT)

    # Create a layout for the navigation bar
    nav_layout = QHBoxLayout()

    # Add widgets to the navigation layout
    nav_layout.addWidget(back_button)
    nav_layout.addWidget(forward_button)
    nav_layout.addWidget(reload_button)
    nav_layout.addWidget(QLabel("URL:"))
    nav_layout.addWidget(address_bar)
    nav_layout.addWidget(QLabel("User Agent:"))
    nav_layout.addWidget(user_agent_dropdown)

    # Create a widget for the navigation bar and add the navigation layout to it
    navbar = QWidget()
    navbar.setLayout(nav_layout)
    navbar.setMaximumHeight(NAVBAR_HEIGHT) # Set maximum height
    navbar.hide() # Hide the navigation bar initially

    return navbar, back_button, forward_button, reload_button, address_bar, user_agent_dropdown, nav_layout


def create_app():
    app = QApplication(sys.argv)
    navbar, back_button, forward_button, reload_button, address_bar, user_agent_dropdown, nav_layout = create_navbar()

    # CSS styling for the navbar
    navbar.setStyleSheet("""
        background-color: #fff;
        border-bottom: 1px solid #ccc;
    """)

    # Create a CustomWebEngineView instance
    view = CustomWebEngineView(address_bar, user_agent_dropdown)

    # Create a zoom slider
    zoom_slider = QSlider(Qt.Horizontal)
    zoom_slider.setRange(50, 200) # Zoom range from 50% to 200%
    zoom_slider.setValue(100)
    zoom_slider.valueChanged.connect(view.set_zoom_factor)

    # Set maximum width and size policy for the zoom slider
    zoom_slider.setMaximumWidth(100)
    zoom_slider.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    # Add the zoom slider to the navigation layout
    nav_layout.addWidget(QLabel("Zoom:"))
    nav_layout.addWidget(zoom_slider)

    back_button.clicked.connect(view.back)
    forward_button.clicked.connect(view.forward)
    reload_button.clicked.connect(view.reload)
    address_bar.returnPressed.connect(lambda: view.load(QUrl(address_bar.text())))

    # Create a LoginForm instance
    login_form = LoginForm(navbar)

    # Create a layout and add the widgets
    layout = QVBoxLayout()
    layout.addWidget(navbar)
    layout.addWidget(view)
    layout.addWidget(login_form)

    # Create a widget to hold the layout
    container = QWidget()
    container.setLayout(layout)

    # Show the container
    container.show()

    # Check if the user is logged in or registered
    if login_form.is_user_logged_in() or login_form.is_user_registered():
        window = QMainWindow()

        view = CustomWebEngineView(address_bar, user_agent_dropdown)

        window.setCentralWidget(view)

        # Show the window maximized
        window.showMaximized()

    app.exec_()

if __name__ == "__main__":
    create_app()