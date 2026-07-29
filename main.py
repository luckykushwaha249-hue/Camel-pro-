from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

SUBJECTS = ["Hindi", "English", "Maths", "GK", "Poem", "Drawing", "Writing Practice"]

TOPICS = {
    "Hindi": ["Varnamala", "Fill in Blanks", "Match Letter"],
    "English": ["Alphabet A-Z", "Vowels", "Fill in Blanks", "Circle Correct Letter"],
    "Maths": ["Counting 1-100", "Before/After", "Backward Counting"],
    "GK": ["Fruits & Vegetables", "Body Parts", "My Self"],
    "Poem": ["Thank You God", "Teddy Bear Teddy Bear", "Jisne Sara Jagat Banaya", "Ek Do Teen Char"],
    "Drawing": ["Shapes", "Coloring"],
    "Writing Practice": ["Letters", "Numbers"],
}

QUESTIONS = {
    "Alphabet A-Z": [("Which letter comes after B?", ["A", "C", "D"], "C")],
    "Counting 1-100": [("What comes after 7?", ["6", "8", "9"], "8")],
    "Vowels": [("Which is a vowel?", ["B", "E", "K"], "E")],
}


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        root.add_widget(Label(text="Camel Pro", font_size=dp(28), size_hint_y=None, height=dp(50)))
        scroll = ScrollView()
        grid = GridLayout(cols=2, spacing=dp(12), size_hint_y=None, padding=dp(8))
        grid.bind(minimum_height=grid.setter("height"))
        for subject in SUBJECTS:
            btn = Button(text=subject, size_hint_y=None, height=dp(100), font_size=dp(18))
            btn.bind(on_release=lambda inst, s=subject: self.open_subject(s))
            grid.add_widget(btn)
        scroll.add_widget(grid)
        root.add_widget(scroll)
        self.add_widget(root)

    def open_subject(self, subject):
        app = App.get_running_app()
        app.root.get_screen("subject").load_subject(subject)
        app.root.current = "subject"


class SubjectScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(10))
        self.add_widget(self.layout)

    def load_subject(self, subject):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text=subject, font_size=dp(24), size_hint_y=None, height=dp(50)))
        back = Button(text="Back", size_hint_y=None, height=dp(44))
        back.bind(on_release=self.go_back)
        self.layout.add_widget(back)
        scroll = ScrollView()
        grid = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))
        for topic in TOPICS.get(subject, []):
            btn = Button(text=topic, size_hint_y=None, height=dp(70), font_size=dp(16))
            btn.bind(on_release=lambda inst, t=topic: self.open_topic(t))
            grid.add_widget(btn)
        scroll.add_widget(grid)
        self.layout.add_widget(scroll)

    def open_topic(self, topic):
        app = App.get_running_app()
        app.root.get_screen("topic").load_topic(topic)
        app.root.current = "topic"

    def go_back(self, *a):
        App.get_running_app().root.current = "home"


class TopicScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(10))
        self.add_widget(self.layout)
        self.score = 0
        self.total = 0

    def load_topic(self, topic):
        self.topic = topic
        self.score = 0
        self.total = 0
        self.questions = QUESTIONS.get(topic, [])
        self.index = 0
        self.render()

    def render(self):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text=self.topic, font_size=dp(22), size_hint_y=None, height=dp(44)))
        if self.index >= len(self.questions):
            self.layout.add_widget(Label(text=f"Done! Score: {self.score}/{self.total}", font_size=dp(20)))
            back = Button(text="Back", size_hint_y=None, height=dp(50))
            back.bind(on_release=self.go_back)
            self.layout.add_widget(back)
            return
        q, options, correct = self.questions[self.index]
        self.correct = correct
        self.layout.add_widget(Label(text=q, font_size=dp(18), size_hint_y=None, height=dp(60)))
        for opt in options:
            btn = Button(text=opt, size_hint_y=None, height=dp(60), font_size=dp(16))
            btn.bind(on_release=lambda inst, o=opt: self.check(o))
            self.layout.add_widget(btn)
        back = Button(text="Back", size_hint_y=None, height=dp(44))
        back.bind(on_release=self.go_back)
        self.layout.add_widget(back)

    def check(self, answer):
        self.total += 1
        if answer == self.correct:
            self.score += 1
        self.index += 1
        self.render()

    def go_back(self, *a):
        App.get_running_app().root.current = "subject"


class CamelProApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(SubjectScreen(name="subject"))
        sm.add_widget(TopicScreen(name="topic"))
        return sm


if __name__ == "__main__":
    CamelProApp().run()
