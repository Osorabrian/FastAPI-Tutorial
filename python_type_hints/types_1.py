#type hints or type annotations are special syntax in python that declare types of variables

def get_names(first_name: str, last_name:str) -> str:
    return f"{first_name} {last_name}"

print(get_names("John", "Doe")) # John Doe

#type annotations not only help with auto-completion but also help with static type checking using tools like mypy, which can catch type-related errors before runtime.

def get_age(name: str, age:  int) -> str:
    return name + " is " + str(age)

print(get_age("Alice", 30)) # Alice is 30

#you can declare all python types int, str, float, bool, list, dict, tuple, set, bytes

#Typing Module

from typing import Any

#Any is a special type hint that indicates that a variable can be of any type. It is often used when the type of a variable is not known or when you want to allow for flexibility in the types that can be passed to a function.
def process_data(data: Any) -> None:
    print("Processing data:", data)

process_data({"key": "value"}) # Processing data: {'key': 'value'}

#Generic types allow you to specify types that can be used with a variety of data structures, such as lists, dictionaries, and tuples. This is useful for creating reusable code that can work with different types of data.

#list
def process_list(items: list[int]) -> None:
    for item in items:
        print("Processing item:", item)

process_list([1, 2, 3]) # Processing item: 1, Processing item: 2, Processing item: 3

#tuple and set
def letters_and_numbers(lettters: tuple[str, str, str], numbers: set[int])-> None:
    print("Letters:", lettters)
    print("Numbers:", numbers)

print(letters_and_numbers(("a", "b", "c"), {1, 2, 3})) # Letters: ('a', 'b', 'c'), Numbers: {1, 2, 3}

#dictionaries - to define a dict you pass 2 type parameters seperated by a comma
def process_dict(data: dict[str, int]) -> None:
    for key, value in data.items():
        print(f"Key: {key}, Value: {value}")

process_dict({"a": 1, "b": 2, "c": 3}) # Key: a, Value: 1
                                         # Key: b, Value: 2
                                         # Key: c, Value: 3

#Union it allows you to specify types that can be one of several options. This is symbolized by the | operator, which is used to separate the different types that can be accepted.
def process_value(value: int | str) -> None:
    if isinstance(value, int):
        print("Processing integer:", value)
    elif isinstance(value, str):
        print("Processing string:", value)

print(process_value("Brian")) # Processing integer: 42

#Possibly None
def process_optional(value: int | None = None) -> None:
    if value is not None:
        print("Processing value:", value)
    else:
        print("No value provided")

print(process_optional()) # No value provided

#Classes as types

class Person:

    def __init__(self, name: str) -> None:
        self.name = name

#one_person is an instance of the person class
def greet(one_person: Person) -> str:
    return f"hello, {person.name}!  Welcome to the world of type hints."

person = Person("Alice")
print(greet(person)) # hello, Alice!  Welcome to the world of type hints.


#pydantic is a python library to perform data validation
#you delcare the shape of data as class with attributes
from pydantic import BaseModel

class School(BaseModel):
    id: int
    name: str
    location: str


def describe_school(one_school: School) -> str:
    return f"{one_school.name} is located in {one_school.location}."

#python has a feture that allows adding metadata to type hint known as Annotated

from typing import Annotated

def describe_user(name: Annotated[str | None, "The user's name is Brian"] = None)  -> str:
    if name is not None:
        return f"Hello, {name}!"
    else:
        return "Hello, guest!"
    
print(describe_user(None)) # Hello, Brian!


import os
name = os.getenv("MY_NAME", "World") # if the environment variable MY_NAME is not set, it will default to "guest"Eorl
print(name) # Hello, my guest!