from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window

from jnius import autoclass, cast, PythonJavaClass, java_method

Window.clearcolor = (1, 1, 1, 1)

# Java Callback for AuthenticationResult
class BiometricCallback(PythonJavaClass):
    __javainterfaces__ = ['androidx/biometric/BiometricPrompt$AuthenticationCallback']
    __javacontext__ = 'app'

    def __init__(self, label):
        super().__init__()
        self.label = label

    @java_method('(Landroidx/biometric/BiometricPrompt$AuthenticationResult;)V')
    def onAuthenticationSucceeded(self, result):
        self.label.text = "✅ Fingerprint Scanned Successfully"

    @java_method('(Landroidx/biometric/BiometricPrompt$AuthenticationFailure;)V')
    def onAuthenticationFailed(self):
        self.label.text = "❌ Authentication Failed"

    @java_method('(Landroidx/biometric/BiometricPrompt$AuthenticationError;Ljava/lang/CharSequence;)V')
    def onAuthenticationError(self, errorCode, errString):
        self.label.text = f"❌ Error: {errString}"


class FingerprintApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        self.label = Label(text="Scan your fingerprint", font_size='24sp', color=(0, 0, 0, 1))
        self.layout.add_widget(self.label)
        Clock.schedule_once(self.setup_biometric, 1)
        return self.layout

    def setup_biometric(self, dt):
        activity = autoclass('org.kivy.android.PythonActivity').mActivity
        BiometricPrompt = autoclass('androidx.biometric.BiometricPrompt')
        BiometricPromptBuilder = autoclass('androidx.biometric.BiometricPrompt$Builder')
        Executor = autoclass('java.util.concurrent.Executors').newSingleThreadExecutor()

        callback = BiometricCallback(self.label)

        promptInfoBuilder = autoclass('androidx/biometric/BiometricPrompt$PromptInfo$Builder')()
        promptInfoBuilder.setTitle("Fingerprint Authentication")
        promptInfoBuilder.setSubtitle("Authenticate using your fingerprint")
        promptInfoBuilder.setNegativeButtonText("Cancel")
        promptInfo = promptInfoBuilder.build()

        biometricPrompt = BiometricPrompt(activity, Executor, callback)
        biometricPrompt.authenticate(promptInfo)

if __name__ == '__main__':
    FingerprintApp().run()
