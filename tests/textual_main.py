'''
Display content with textual
'''

import re
import time
from textual.app import App, ComposeResult
from textual.widgets import Static
from textual.widget import Widget
from textual.reactive import Reactive
from textual.timer import Timer
from pprint import pprint
import importlib.resources 

INIT_PERF_COUNT =  time.perf_counter()

class Clock(Static):
    '''
    Abandoned
    '''
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

class Details(Static):
    #data:dict =  {}
    title:str  = ''
    data:dict =  Reactive({})
    
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
    
    running_data = Reactive({'--':'no data'})
    finished_data = Reactive({})
    message_data = Reactive({})
    
    running_count =  Reactive(0)
    finished_count =  Reactive(0)
    
    def __init__(self):
        super().__init__(classes='content-view')
            
    def compose(self) -> ComposeResult:
        yield Details(self.running_data, 'Running')
        yield Details(self.finished_data, 'Finished')
        yield MessageView({'error': 'none','submit':'some task'}, 'Message')


class MessageView(Details):
    clock: Reactive[str] = Reactive("") 
    init_perf_count:float = INIT_PERF_COUNT
    now_perf_count:float = init_perf_count
    # data:dict =  Reactive({'time':'---'})

    def on_mount(self) -> None:
        self.update_time()
        # Set up a timer to update the clock every second
        self.set_interval(1, self.update_time)
        
    def update_time(self) -> None:
        """Update the time displayed."""
        self.now_perf_count = time.perf_counter() - self.init_perf_count
        ftime =  time.strftime("%H:%M:%S", time.gmtime(self.now_perf_count))

        self.clock = ftime
        self.border_title = f' {self.title}  {self.clock} '
        self.data = {'time':ftime}
        self.mutate_reactive(Details.data)
        # self.refresh()
        
        ws = []
        for widget in self.query():
            ws.append(str(widget))
        # self.data = {'widgets':'\n'.join(ws)}


class FloatView(Static):
    def __init__(self):
        super().__init__(classes='float-view')
    
    def compose(self) -> ComposeResult:
        yield Overview()

class Overview(Widget):
    id = 'overview'
    def __init__(self):
        super().__init__(id='overview')
        
    def compose(self):
        # yield Clock()
        yield Details({'count': 99999,'byte': '114g'})
        
        
class MainApp(App):
    def __init__(self, driver_class = None, css_path = None, watch_css = False):
        css_path = css_path or importlib.resources.files(__package__) / "style.css"
        super().__init__(driver_class, css_path, watch_css)
    
    def on_mount(self) -> None:
        # Set the app's theme
        self.theme = "nord"
        self.theme = "gruvbox"
        
        self.set_interval(3, self.check)
    
    def check(self):
        # TODO:
        print('MainApp: run check')
        # cv = self.query_one(".content-view")
        # cv.running_data = {'???':'mmm'}
            
        
    def compose(self) -> ComposeResult:
        yield MainView()
