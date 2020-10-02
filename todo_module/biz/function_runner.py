from typing import Any

class FunctionFailedException(Exception):

    def __init__(self, message: str, func_run_data: Any):
        super().__init__(message)
        self.func_run_data = func_run_data


class FunctionRunner():

    @staticmethod
    def do_a_thing_with_retries(function, max_tries: int, *args: Any) -> Any:
            """ Simple retry function runner. """

            run_results = {}
            func_return = None
            has_fails = False

            for tries in range(max_tries):
                try:
                    if(tries < max_tries):
                        if (args):
                            func_return = function(*args)
                        else:
                            func_return = function()
                        run_results[tries] = {"status": "success", "error": ""}
                        break
                except Exception as ex:
                    run_results[tries] = {"status": "fail", "error": ex}
                    has_fails = True
                    next
            
            if has_fails:
                raise FunctionFailedException("Failed", run_results)
            return func_return