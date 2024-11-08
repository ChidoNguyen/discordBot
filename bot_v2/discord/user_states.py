class UserStates :
    def __init__(self):
        self.task = None
        self.pick_options = []
        self.locked = False
    
    def isLocked(self):
        return self.locked
    
    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False