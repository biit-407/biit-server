import os

def mock_dev(return_value):
    """
    Decorator for mocking the return value of a function when
    in a dev environment

    Args:
        return_value (any): the value to have the function return  
            when run from inside a dev environment
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            stage = os.getenv("STAGE")
            if stage == "dev":
                return return_value

            result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator