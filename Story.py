from sets import Set


class Story:
    ownerID = ""
    text = ""
    displays = []

    upvoters = Set()
    downvoters = Set()

    def __init__(self, name, ownerId, text="", displays=[], ):
        self.ownerID = ownerId
        self.text = text
        self.displays = displays
        self.upvoters = []
        self.downvoters = []
        self.name = name
        self.upvote = 0
    def getOwnerID(self):
        return self.ownerID

    def getUpvoteNum(self):
        return self.upvoters.__len__()

    def getDownvoteNum(self):
        return self.downvoters.__len__()

    def getDisplays(self):
        return self.displays

    def addUpvote(self, userID):
        print self.ownerID, userID
        if self.ownerID == userID:
            print("One cannot", userID, "vote for oneself.")
        elif self.upvoters.__contains__(userID) or self.downvoters.__contains__(userID):
            print("User:", userID, "has already voted.")
        else:
            self.upvote += 1
            self.upvoters.append(str(userID))

    def addDownvote(self, user):
        if self.ownerID == userID:
            print("One cannot vote for oneself.")
        elif self.upvoters.__contains__(userID) or self.downvoters.__contains__(userID):
            print("User:", userID, "has already voted.")
        else:
            self.downvote += 1
            self.downvoters.append(str(userID))
