import unittest
import json
import requests
from unittest.mock import MagicMock, patch
import todo_module
from todo_module.model.todo import Todo
from todo_module.client.todo_client import TodoClient
from todo_module.biz.todo_biz import TodoBiz
from requests import Response

class MocksTests(unittest.TestCase):


    def test_biz_get_todo_mock(self):

        # with mocks, but what does this tell me? NOTHING
        client = TodoClient("foobar")
        client.get_todo = MagicMock(return_value = Todo(id=1, userId=3, title="foobar", completed=False))
        biz = TodoBiz(client)
        todo = biz.get_todo(1)
        assert todo.id == 1


    @patch("requests.get")
    def test_biz_get_todo_patch(self, mocked_get):

        # lower level mocks that might get me some value, but this method does not
        # show the value as it is not testing the forks in the actual client method
        # which is what matters
        mocked_get.return_value = MagicMock(status_code=200, text="""
         {
            "userId": 1,
            "id": 1,
            "title": "delectus aut autem",
            "completed": false
        }
        """)

        client = TodoClient("foobar")
        biz = TodoBiz(client)
        todo = biz.get_todo(1)
        assert todo.id == 1

    @patch("requests.get")
    def test_biz_get_todo_patch_good(self, mocked_get):

        # NOW WE ARE COOKING WITH GAS!
        # This single mocked test tests the exception fork in the client code
        # and the happy path. No other tests are needed
        mocked_get.return_value = MagicMock(status_code=500, text="""
         {
            "userId": 1,
            "id": 1,
            "title": "delectus aut autem",
            "completed": false
        }
        """)

        client = TodoClient("foobar")
        
        with self.assertRaises(requests.HTTPError):
            client.get_todo(1)

        mocked_get.return_value = MagicMock(status_code=200, text="""
         {
            "userId": 1,
            "id": 1,
            "title": "delectus aut autem",
            "completed": false
        }
        """)
        # DOES THIS PROVIDE VALUE? Only in so far as it shows the non-error code fork
        todo = client.get_todo(1)
        assert todo.id == 1


    @patch("requests.put")
    def test_biz_put_todo_patch_good(self, mocked_get):
        mocked_get.return_value = MagicMock(status_code=500, text="""
         {
            "userId": 1,
            "id": 1,
            "title": "delectus aut autem",
            "completed": false
        }
        """)
        client = TodoClient("foobar")
        
        with self.assertRaises(requests.HTTPError):
            client.put_todo(Todo(id=1, userId=1, title="foobar", completed=False))



