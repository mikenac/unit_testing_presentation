
import unittest
from todo_module.model.todo import Todo
from todo_module.client.todo_client import TodoClient


class TestTodoIntegration(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        cls.client = TodoClient('https://jsonplaceholder.typicode.com')

    def test_todo_get(self):
        """ Simple TODO getter integration test """

        todo = self.client.get_todo(1)
        assert todo.id == 1

    def test_todo_put(self):
        """ Simple TODO put integration test """

        todo = Todo(id=2, userId=2, title="Sandy", completed=False)
        self.client.put_todo(todo)
        
