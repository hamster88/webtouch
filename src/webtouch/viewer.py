from collections import deque
import os
from pprint import pprint
import textwrap  
from webtouch.reporter import Reporter



class BaseViewer():
    def __init__(self):
        self.putlog:callable = lambda s:None
        self.errlog:callable = lambda s:None
        self.reporter:Reporter = None

    def show(self):
        print(f'{__class__.__name__}.show() is not implemented.')

    def loop(self):
        try:
            while True:
                input()
        except KeyboardInterrupt:
            pass
        finally:
            # os._exit(0)
            return

class NothingViewer(BaseViewer):
    def __init__(self):
        super().__init__()
    
    def show(self):
       self.loop()

class LogViewer(BaseViewer):
    def __init__(self):
        super().__init__()
        self.putlog = print
        
    def show(self):
       self.loop()

class SheetViewer(BaseViewer):
    def __init__(self):
        super().__init__()
        
    def show(self):
        return super().show()
    

class RichViewer(BaseViewer):
    def __init__(self):
        from webtouch.textual_main import MyTextualApp
        self.tapp = MyTextualApp()
        super().__init__()
    
    def show(self):
        self.tapp.run()
        
    
    