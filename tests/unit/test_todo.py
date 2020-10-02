import unittest
import json
import requests
from unittest.mock import MagicMock, patch
from requests import Response
import todo_module
from todo_module.model.todo import Todo
from todo_module.client.todo_client import TodoClient
from todo_module.biz.todo_biz import TodoBiz
from todo_module.biz.function_runner import FunctionRunner, FunctionFailedException


class SomeTests(unittest.TestCase):


    def test_complex_logic_for_bad_todos(self):

        """ Test to make sure todos id's 3,4 are marked bad"""

        todo3_json = """
        {
            "userId": 1,
            "id": 3,
            "title": "delectus aut autem",
            "completed": false
        }
        """
        todo3 = Todo.from_json(json.loads(todo3_json))

        todo4_json = """
        {
            "userId": 1,
            "id": 4,
            "title": "delectus aut autem",
            "completed": false
        }
        """
        todo4 = Todo.from_json(json.loads(todo4_json))


        client = TodoClient('https://jsonplaceholder.typicode.com')
        biz_logic = TodoBiz(client)

        new_todo3 = biz_logic.do_complex_logic_on_todo(todo3)
        assert "bad todo" in new_todo3.title
        assert new_todo3.completed == True

        new_todo4 = biz_logic.do_complex_logic_on_todo(todo4)
        assert "bad todo" in new_todo4.title
        assert new_todo4.completed == True


    def test_complex_logic_good_todo(self):

        """ Test to make sure ids that are not 3,4, are not bad """

        todo1_json = """
        {
            "userId": 1,
            "id": 1,
            "title": "delectus aut autem",
            "completed": false
        }
        """
        todo1 = Todo.from_json(json.loads(todo1_json))

        client = TodoClient('https://jsonplaceholder.typicode.com')
        biz_logic = TodoBiz(client)

        new_todo1 = biz_logic.do_complex_logic_on_todo(todo1)
        assert "bad todo" not in new_todo1.title
        assert new_todo1.completed == True


    def test_update_todo(self):

        """ Test with low value. I don't need to test remote API """
        todo_json = """
        {
            "userId": 1,
            "id": 1,
            "title": "delectus aut autem",
            "completed": false
        }
        """
        todo = Todo.from_json(json.loads(todo_json))

        client = TodoClient('https://jsonplaceholder.typicode.com')
        biz_logic = TodoBiz(client)

        biz_logic.complete_todo(todo)


    def test_do_a_thing_with_retries_pass(self):

        client = TodoClient('https://jsonplaceholder.typicode.com')
        biz_logic = TodoBiz(client)
        FunctionRunner.do_a_thing_with_retries(print, 3, "foobar")


    def test_do_a_thing_with_retries_fail_all(self):

        client = TodoClient('https://jsonplaceholder.typicode.com')
        biz_logic = TodoBiz(client)
        failer = lambda: (_ for _ in ()).throw(Exception('foobar'))
        with self.assertRaises(FunctionFailedException) as ex:
            result = FunctionRunner.do_a_thing_with_retries(failer, 3)
            print(ex)
            
        
    def test_todo_from_json(self):

        todo_json = """
        {
            "userId": 1,
            "id": 1,
            "title": "delectus aut autem",
            "completed": false
        }
        """

        todo = Todo.from_json(json.loads(todo_json))
        assert todo.id == 1


if __name__ == '__main__':
    unittest.main()
