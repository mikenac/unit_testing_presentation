import jsons
import json
import requests
from todo_module.model.todo import Todo

class TodoClient():

    def __init__(self, base_uri: str):
        self.base_uri = base_uri

    def get_todo(self, todo_id: int) -> Todo:
        
        uri = f"""{self.base_uri}/todos/{todo_id}"""
        response = requests.get(uri)
        if response.status_code != 200:
            raise requests.HTTPError(response.text)
        return Todo.from_json(json.loads(response.text))

    def put_todo(self, todo: Todo):
        data = todo.dump()
        uri = f"""{self.base_uri}/todos/{todo.id}"""
        response = requests.put(uri, data=data)
        if response.status_code != 200:
            raise requests.HTTPError(response.text)
       
                

            