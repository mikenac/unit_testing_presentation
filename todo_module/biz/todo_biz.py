import copy

from todo_module.model.todo import Todo
from todo_module.client.todo_client import TodoClient
from todo_module.biz.function_runner import FunctionRunner


class TodoBiz():
    """ Business logic for all things Todo """

    def __init__(self, todo_client: TodoClient):
        self.todo_client = todo_client

    def get_todo(self, todo_id: int) -> Todo:
        """ Simple getter passthrough """
        return self.todo_client.get_todo(todo_id)

    def complete_todo(self, todo: Todo):
        """ Simplest completion method possible """
        todo.completed = True
        self.todo_client.put_todo(todo)

    
    def complete_todo_with_complex_logic_bad(self, todo: Todo): #pragma: no cover

        # BAD because requires API call to test biz logic REFACTOR
        todo.completed = True
        if todo.id in (3, 4):
            todo.title = todo.title + " is a bad todo!"

        self.todo_client.put_todo(todo)

    def complete_todo_with_complex_logic_good(self, todo: Todo):

        # tested separately
        new_todo = this.do_complex_logic_on_todo(todo)

        # can be tested separately
        self.todo_client.put_todo(new_todo)


    def do_complex_logic_on_todo(self, todo: Todo) -> Todo:
        # PURE function: »-(¯`·.·´¯)->

        # create a new todo that we will modify
        new_todo = copy.deepcopy(todo)
        new_todo.completed = True
        if new_todo.id in (3, 4):
            new_todo.title = new_todo.title + " is a bad todo!"
        return new_todo


    def complete_todo_complex_with_retries_bad(self, todo: Todo): #pragma: no cover

        # BADNESS: ╭∩╮(Ο_Ο)╭∩╮ needs refactor
        # need to be able to test this separately
        todo.completed = True
        if todo.id in (3, 4):
            todo.title = todo.title + " is a bad todo!"

        # how do I test this retry logic?
        for tries in range(3):
            try:
                if (tries < 2):
                    print("will retry")
                    self.todo_client.put_todo(todo)
                else:
                    # now I have to have qeueu somewhere too
                    print("Put this in a failure queue now")
                    return
            except Exception as ex:
                print(f"Bad things have happened {ex}")
                pass


    def complete_todo_complex_with_retries_good(self, todo: Todo, retries: int):
        """ Now we are cooking with gas! """

        # tested separately
        new_todo = self.do_complex_logic_on_todo(todo)


        # tested separately, will raise on error
        results = FunctionRunner.do_a_thing_with_retries(self.todo_client.put_todo, retries, todo)










