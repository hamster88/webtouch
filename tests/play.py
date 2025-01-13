import re
import time
from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.widget import Widget
from textual.reactive import Reactive
from textual.timer import Timer
from pprint import pprint
import importlib.resources 

class Clock(Static):
    text: Reactive[str] = Reactive("") 
    init_perf_count:float = time.perf_counter()
    now_perf_count:float = 0
    
    def on_mount(self) -> None:
        self.update_time()
        # Set up a timer to update the clock every second
        self.set_interval(1, self.update_time)
        
    def update_time(self) -> None:
        """Update the time displayed."""
        self.now_perf_count = time.perf_counter() - self.init_perf_count
        ftime =  time.strftime("%H:%M:%S", time.gmtime(self.now_perf_count))

        self.text = ftime
        self.update(self.text)
        
class Overview(Widget):
    # id = 'overview'
    def __init__(self):
        super().__init__(id='overview')
        
    def compose(self):
        yield Clock()
        yield Details({'count': 99999,'byte': '114g'})
        
    

class Details(Widget):
    data:dict 
    title:str 
    def __init__(self,  data:dict, title=None, classes=''):
        details_classes = 'details ' + (title and ' ' or 'no-title ')
        classes = details_classes + classes
        super().__init__(classes=classes)
        self.title = title
        self.border_title = f' {title} '
        self.data = data
    
    def compose(self):
        for k, v in self.data.items():
            yield Static(str(k), classes='details-item-label', markup=False)
            yield Static(str(v), classes='details-item-value', markup=False)


class MainView(Static):
    def __init__(self):
        super().__init__(classes='main-view')
    
            
    def compose(self) -> ComposeResult:
        yield FloatView()
        yield ContentView()
        
class ContentView(Static):
    def __init__(self):
        super().__init__(classes='content-view')
    
            
    def compose(self) -> ComposeResult:
        yield Details({'y':2,'zzz':123}, 'Running')
        yield Details({'y':2,'zzz':123}, 'Finished')
        yield Details({'error': 'none','submit':'some task'}, 'Message')



class FloatView(Static):
    def __init__(self):
        super().__init__(classes='float-view')
    
    def compose(self) -> ComposeResult:
        yield Overview()
        # yield Static('aaa')


        
class MainApp(App):
    CSS_PATH = 'style.css'
    def on_mount(self) -> None:
        # Set the app's theme
        self.theme = "gruvbox"
        
    def compose(self) -> ComposeResult:
        yield MainView()


MainApp().run()