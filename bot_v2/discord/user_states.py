class UserStates :
    def __init__(self):
        self.task = None
        self.urls = []
        self.pick_thread = None
        self.locked = False
    
    def book_urls(self,links,thread_id):
        self.urls = links
        self.pick_thread = thread_id

    def cancel(self):
        self.urls = []
        self.pick_thread = None

    def isLocked(self):
        return self.locked
    
    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False