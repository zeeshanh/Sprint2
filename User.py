import uuid

class User:
    id = ""
    fname = ""
    lname = ""
    username = ""
    stories = []
    password = ""

    def __init__(self, fname, lname, username, password):
        self.id = uuid.uuid1()
        self.fname = fname
        self.lname = lname
        self.username = username
        self.password = password

    def getID(self):
        return str(self.id)

    def getUname(self):
        return self.username

    def getName(self):
        return self.fname

    def getStories(self):
        return self.stories

    def addStory(self, story):
        try:
            self.stories.append(story)
            return True
        except(Exception, e):
            print(e)
            return False

    def getPassword():
        return self.password
