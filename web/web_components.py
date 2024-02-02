from PyQt5.QtCore import QUrl, Qt, QThread, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage, QWebEngineSettings
from database.db_operations import register, login

class LoadUrlThread(QThread):
    load_url = pyqtSignal(QUrl)

    def run(self):
        self.load_url.emit(QUrl("https://user319183.github.io/"))

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        register(username, password)
        self.login()
        
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if login(username, password): # We also are calling the login function
            print("Login successful")
        else:
            print("Login failed")

class CustomWebEngineView(QWebEngineView):
    def __init__(self, address_bar, user_agent_dropdown, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.address_bar = address_bar
        self.user_agent_dropdown = user_agent_dropdown
        self.user_agent_dropdown.currentIndexChanged.connect(self.update_user_agent)

        self.load_url_thread = LoadUrlThread()
        self.load_url_thread.load_url.connect(self.load)
        self.load_url_thread.start()

        self.profile = QWebEngineProfile(self)
        self.setPage(QWebEnginePage(self.profile, self))

        self.profile.setCachePath("cache")

        # Enable hardware acceleration
        self.settings().setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)

        self.update_user_agent()

        # Set the zoom factor to be according to the user's screen DPI
        self.setZoomFactor(1 / self.logicalDpiX())

    def update_user_agent(self):
        user_agent = self.user_agent_dropdown.currentText()
        self.profile.setHttpUserAgent(user_agent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("Left mouse button clicked")
        elif event.button() == Qt.RightButton:
            print("Right mouse button clicked")
        super().mousePressEvent(event)
        
    def load(self, url):
        url_str = url.toString()
        if not url_str.startswith(("http://", "https://")):
            url = QUrl("https://www.google.com/search?q=" + url_str)
        if url.isValid():
            super().load(url)
        else:
            print(f"Invalid URL: {url.toString()}")

    def onLoadFinished(self, success):
        if success:
            self.address_bar.setText(self.url().toString())
        else:
            print(f"Failed to load: {self.url().toString()}")
            
    def set_zoom_factor(self, value):
        self.setZoomFactor(value / 100)