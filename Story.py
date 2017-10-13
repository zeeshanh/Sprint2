class Story:
    ownerID = ""
    upvote = 0
    downvote = 0
    text = ""
    displays = []

    upvoters = []
    downvoters = []

    def __init__(self, ownerId, upvote=0, downvote=0, text="", displays=[]):
        self.ownerID = ownerId
        self.upvote = upvote
        self.downvote = downvote
        self.text = text
        self.displays = displays
        self.upvoters = []
        self.downvoters = []

    def getOwnerID(self):
        return self.ownerID

    def getUpvote(self):
        return self.upvote

    def getDownvote(self):
        return self.downvote

    def getDisplays(self):
        return self.displays

    def addUpvote(self, user):
        self.upvote += 1
        self.upvoters.append(user)

    def addDownvote(self, user):
        self.downvote += 1
        self.downvoters.append(user)
