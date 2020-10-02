import jsons

class Todo(jsons.JsonSerializable):
    """ Todo class """

    def __init__(self, id: int, userId: int, title: str, completed: bool):
        self.id = id
        self.userId = userId
        self.title = title
        self.completed = completed
