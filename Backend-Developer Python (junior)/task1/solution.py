def strict(func):
    def wrapper(*args):
        annotations = func.__annotations__
        for arg_value, (arg_name, arg_type) in zip(args, annotations.items()):
            if not isinstance(arg_value, arg_type):
                raise TypeError(
                    f"Argument '{arg_name}' must be of type {arg_type.__name__}, got {type(arg_value).__name__}"
                )
        return func(*args)
    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


print(sum_two(1, 2))     # >>> 3
print(sum_two(1, 2.4))   # >>> TypeError