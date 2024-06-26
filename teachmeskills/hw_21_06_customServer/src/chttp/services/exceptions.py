import functools
import traceback

def catch_exception(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            print(f'Exception in {func.__name__}: {e}')
            traceback.print_exc()
            return
    return wrapper