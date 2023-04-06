from functools import wraps


def utildecorator(func):
    """
    Example decorator which can be used to alter the lambda handler's runtime
    """
    @wraps(func)
    def wrapper(event, context):
        print('Hellloooooo from your lambda layer!')
        result = func(event, context)

        return result
    return wrapper
