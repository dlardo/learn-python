print("-- Lesson 1--")
def outer_function(message):
    def inner_function():
        print('The inner function inherits {}'.format(message)) # message in inherited from outer_function
    return inner_function # returns a function with the message var stored.

# First class means you can pass functions as variables. Add () to execute the
# function. Without it, you are just passing memory locations around.
first_class_citizen_function = outer_function("this message")
first_class_citizen_function()  # prints 'The inner function inherits this message'

first_class_citizen_function_two = outer_function("any message")
first_class_citizen_function_two() # prints 'The inner function inherits any message'

# Same code as above but renamed
print("-- Lesson 1 renamed --")
def var_decorator_function(message):
    def wrapper_function():
        print('The inner function inherits {}'.format(message))
    return wrapper_function # outer function returns the 'baked' inner function

my_var_decorator_function = var_decorator_function("my message")
my_var_decorator_function() # prints 'The inner function inherits my message'

# As functions can be passed around like variables, we can s/message/function/
print("-- Lesson 2--")
def accept_function_decorator(var_function):
    print('Baking: accept_function_decorator is running - this only runs during a bake')
    def wrapper_function():
        print('Wrapper executed this before {}'.format(var_function.__name__))
        run_original_function = var_function() # "run" the passed in func(). When baking this doesn't actually execute.
        return run_original_function
    return wrapper_function # outer function returns the 'baked' inner function

def hello_world():
    print('Running Hello World')

decorated_hello_world = accept_function_decorator(hello_world)
print("{} is what we are calling. "
      "It includes the variables (function) we passed in.\n".format(decorated_hello_world.__name__))
print("\nNow we will run decorated_hello_world():")
decorated_hello_world()

# Making hello_world always do the contents of hello world and the accept_function_decorator
print("-- Lesson 3--")
hello_world = accept_function_decorator(hello_world) # same at @syntax
print("\nNow we will run hello_world():")
hello_world()

print("-- Lesson 4: Using the @decorator syntax --")
@accept_function_decorator # exact same thing: hello_world_two = accept_function_decorator(hello_world_two)
def hello_world_two():
    print('Hello World two is running')

print("\nNow we will run hello_world_two():")
hello_world_two()

print("-- Lesson 5: passing arguments --")

@accept_function_decorator
def square(my_int):
    return my_int * my_int

print("\nNow we will run square():")
try:
    print(square(3))
except TypeError as e: # TypeError: wrapper_function() takes 0 positional arguments but 1 was given
    print(e)

def decorator_with_args(var_function):
    print('Baking: accept_function_decorator is running - this only runs during a bake')
    def wrapper_function(*args, **kwargs):
        print('Wrapper executed this before {}'.format(var_function.__name__))
        return var_function(*args, **kwargs)
    return wrapper_function

@decorator_with_args
def cube(my_int):
    return my_int * my_int * my_int

print("\nNow we will run cube():")
print(cube(3))

@decorator_with_args
def add_em_up(add_me_list):
    result = 0
    for x in add_me_list:
        result = result + x

    return result

print("\nNow we will run add_em_up:")
print(add_em_up([1, 3, 1]))


print("-- Lesson 6: Classes --")
# Function() is more popular, but this is another way to do it that allows for more features / control.
class DecoratorClass(object):

    def __init__(self, original_function):
        self.original_function = original_function

    def __call__(self, *args, **kwargs):
        # __call__() allows the class's instance to be called as a function
        # ex:
        # a = class   <-- __init__
        # a()         <-- __call__
        print('__call__ executed this before {}'.format(self.original_function.__name__))
        return self.original_function(*args, **kwargs)

@DecoratorClass
def display():
    print('I display things')

print("\nNow we will run display():")
display()

print("-- Lesson 7: Practical examples -- ")

def my_logger(orig_func):
    import logging
    my_format = '%(asctime)-15s %(message)s'
    logging.basicConfig(filename='{}.log'.format(orig_func.__name__),
                        level=logging.INFO,
                        format=my_format)
    logger = logging.getLogger(orig_func.__name__)
    logger.info("----------")
    # Will output a log to the filesystem
    # So practically, any time you want to add logging to a new function, you can use this.
    # Pros: One logging config to maintain, easy to apply.

    def wrapper(*args, **kwargs):
        logger.info('{}() ran with args: {} and kwargs: {}'.format(orig_func.__name__, args, kwargs))
        return orig_func(*args, **kwargs)

    return wrapper

@my_logger
def arg_heavy_example(stuff, pets, house='expensive'):
    if house == 'cheap':
        print("Great! You can get all the {} and {} you want".format(stuff, pets))
    else:
        print("You don't get to have {} and {}. The house is {}".format(stuff, pets, house))

print("\nNow we will run arg_heavy_example():")
arg_heavy_example('4k TV', 'Pixel', house='cheap')
arg_heavy_example('4k TV', 'Pixel')


def my_timer(orig_function):
    import time

    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_function(*args, **kwargs)  #actually run the function
        t2 = time.time() - t1
        print('{}() ran in {} sec'.format(orig_function.__name__, t2))
        return result  # return the result of the function

    return wrapper # return function, now with new functionality

@my_timer
def sleep_a_little(secs):
    import time
    time.sleep(secs)

print("\nNow we will run sleep_a_little(1):")
sleep_a_little(1)

print("-- Lesson 8: Stack Decorators -- ")

# Problem: stacking decorators causes a orig_function = top_most_decorator(second(orig_function) stack
# The stack is processed inside -> out. second(orig_function) is ran, then the result is passed to top_most()
# When this happens, the orig_function.__name__ is lost, as it's now not that any more, it's wrapper()

# To fix, there is a special module you can use. Best practice?
from functools import wraps

def my_functools_timer(orig_function):
    import time

    @wraps(orig_function) # preserves function name?
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_function(*args, **kwargs)  #actually run the function
        t2 = time.time() - t1
        print('{} ran in {} sec'.format(orig_function.__name__, t2))
        return result  # return the result of the function

    return wrapper # return function, now with new functionality


def my_functools_logger(orig_func):
    import logging
    logging.basicConfig(filename='{}.log'.format(orig_func.__name__), level=logging.INFO)
    logger = logging.getLogger(orig_func.__name__)
    print("Orig Func Name: {}".format(orig_func.__name__))
    # Will output a log to the filesystem
    # So practically, any time you want to add logging to a new function, you can use this.
    # Pros: One logging config to maintain, easy to apply.

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        logger.info('{} Ran with args: {} and kwargs: {}'.format(orig_func.__name__, args, kwargs))
        return orig_func(*args, **kwargs)

    return wrapper

@my_functools_logger
@my_functools_timer
def talk_in_your_sleep_a_little(secs):
    import time
    print("blah blah time to sleep for {}".format(secs))
    time.sleep(secs)

print("True name of sleep_a_little() (no @wraps applied): {}".format(sleep_a_little.__name__))  # prints "wrapper"
print("True name of talk_in_your_sleep_a_little() (@wraps applied): {}"
      .format(talk_in_your_sleep_a_little.__name__)) # prints the original name, which is nice.

print("\nNow we will run talk_in_your_sleep_a_little(1):")
talk_in_your_sleep_a_little(1)