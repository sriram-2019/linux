from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import os
from iris import capture_iris_image, compare_iris

class IrisAuthApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.status_label = Label(text="Press a button to proceed.", font_size=20)
        scan_btn = Button(text="Scan and Authenticate", size_hint=(1, 0.3), on_press=self.authenticate)
        save_btn = Button(text="Register Iris", size_hint=(1, 0.3), on_press=self.register_iris)

        layout.add_widget(self.status_label)
        layout.add_widget(scan_btn)
        layout.add_widget(save_btn)

        if not os.path.exists("user_data"):
            os.makedirs("user_data")

        return layout

    def register_iris(self, instance):
        self.status_label.text = "Capturing iris..."
        path = capture_iris_image('user_data/registered.jpg')
        if path:
            self.status_label.text = "Iris registered successfully."
        else:
            self.status_label.text = "Failed to capture iris."

    def authenticate(self, instance):
        self.status_label.text = "Scanning iris for authentication..."
        captured = capture_iris_image('user_data/current.jpg')
        if not captured or not os.path.exists('user_data/registered.jpg'):
            self.status_label.text = "Authentication failed. No registered iris."
            return

        result = compare_iris('user_data/current.jpg', 'user_data/registered.jpg')
        self.status_label.text = "Access Granted" if result else "Access Denied"

if __name__ == "__main__":
    IrisAuthApp().run()
