from abc import ABC, abstractmethod


class A(ABC):
    @abstractmethod
    def do_something(self):
        print("Hello!")


class B(A):
    def do_something_else(self):
        print("Hi!")

    def do_something(self):
        print("hello!!")


b = B()
b.do_something()
b.do_something_else()
