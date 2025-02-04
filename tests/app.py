import os
import time
from webmiss import textual_main
from webmiss import worker
from webmiss import task

tapp:textual_main.MainApp = None

def main():
    global tapp
    
    w = worker.Worker(task.SleepTask)
    w.emit = emit
    w.start()
    
    # time.sleep(10)
    tapp = textual_main.MainApp()
    tapp.run()
    
    

    
def emit(event, data):
    w:worker.Worker
    t:task.Task
    if event == 'worker:submit':
        w, t = data
        #set_state('tasks_running', w.tasks_running)
    if event == 'worker:done':
        w, t = data




def set_state(key, value):
    if tapp is None:
        return
   
    if key == 'tasks_running':
        cv = tapp.query_one(".content-view")
        print(cv.running_data )

