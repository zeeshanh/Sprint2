from sets import Set


class Story:
    ownerID = ""
    text = ""
    displays = []

    upvoters = Set()
    downvoters = Set()

    def __init__(self, ownerId, text="", displays=[]):
        self.ownerID = ownerId
        self.text = text
        self.displays = displays
        self.upvoters = Set()
        self.downvoters = Set()

    def getOwnerID(self):
        return self.ownerID

    def getUpvoteNum(self):
        return self.upvoters.__len__()

    def getDownvoteNum(self):
        return self.downvoters.__len__()

    def getDisplays(self):
        return self.displays

    def addUpvote(self, user):
        if self.ownerID == user.id:
            print("One cannot", user.id, "vote for oneself.")
        elif self.upvoters.__contains__(user.id) or self.downvoters.__contains__(user.id):
            print("User:", user.id, "has already voted.")
        else:
            self.upvote += 1
            self.upvoters.add(user.id)

    def addDownvote(self, user):
        if self.ownerID == user.id:
            print("One cannot vote for oneself.")
        elif self.upvoters.__contains__(user.id) or self.downvoters.__contains__(user.id):
            print("User:", user.id, "has already voted.")
        else:
            self.downvote += 1
            self.downvoters.add(user.id)
