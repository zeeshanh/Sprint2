import uuid

class User:
    id = ""
    name = ""
    balance = 0.0
    stories = []

    def __init__(self, name="", balance=0.0, stories=[]):
        self.id = uuid.uuid1()
        self.name = name
        self.balance = balance
        self.stories = stories

    def getID(self):
        return str(self.id)

    def getName(self):
        return self.name

    def getBalance(self):
        return self.balance

    def getStories(self):
        return self.stories

    def addBalance(self, inmoney):
        try:
            self.balance += inmoney
            return True
        except Exception, e:
            print e
            return False

    def removeBalance(self, outmoney):
        try:
            if self.balance < outmoney:
                return False
            else:
                self.balance -= outmoney
                return True
        except Exception, e:
            print e
            return False

    def addStory(self, story):
        try:
            self.stories.append(story)
            return True
        except Exception, e:
            print e
            return False
