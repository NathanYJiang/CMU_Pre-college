from cmu_graphics import *

def updateMessages(app, curMessage):
    # add new message
    app.messages.append(curMessage)

    # too long
    if len(app.messages) > 12:
        app.messages.pop(0)