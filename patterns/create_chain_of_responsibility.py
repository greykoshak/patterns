# Необходимо реализовать:
#
# EventGet(<type>) создаёт событие получения данных соответствующего типа
# EventSet(<value>) создаёт событие изменения поля типа type(<value>)
# Необходимо реализовать классы NullHandler, IntHandler, FloatHandler, StrHandler так, чтобы можно было создать цепочку:

# chain = IntHandler(FloatHandler(StrHandler(NullHandler())))

# chain.handle(obj, EventGet(int)) — вернуть значение obj.integer_field
# chain.handle(obj, EventGet(str)) — вернуть значение obj.string_field
# chain.handle(obj, EventGet(float)) — вернуть значение obj.float_field
# chain.handle(obj, EventSet(1)) — установить значение obj.integer_field =1
# chain.handle(obj, EventSet(1.1)) — установить значение obj.float_field = 1.1
# chain.handle(obj, EventSet("str")) — установить значение obj.string_field = "str"

class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class EventGet:
    def __init__(self, get_type):
        self.get_type = get_type


class EventSet:
    def __init__(self, value):
        self.value = value


class NullHandler:
    def __init__(self, successor=None):
        self.__successor = successor  # Преемник

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)


class IntHandler(NullHandler):

    def handle(self, some_obj, event):
        if isinstance(event, EventGet) and event.get_type == int:
            return some_obj.integer_field
        elif isinstance(event, EventSet) and isinstance(event.value, int):
            some_obj.integer_field = event.value
        else:
            # print("Передаю событие дальше")
            return super().handle(some_obj, event)


class FloatHandler(NullHandler):

    def handle(self, some_obj, event):
        if isinstance(event, EventGet) and event.get_type == float:
            return some_obj.float_field
        elif isinstance(event, EventSet) and isinstance(event.value, float):
            some_obj.float_field = event.value
        else:
            # print("Передаю событие дальше")
            return super().handle(some_obj, event)


class StrHandler(NullHandler):

    def handle(self, some_obj, event):
        if isinstance(event, EventGet) and event.get_type == str:
            return some_obj.string_field
        elif isinstance(event, EventSet) and isinstance(event.value, str):
            some_obj.string_field = event.value
        else:
            # print("Передаю событие дальше")
            return super().handle(some_obj, event)


# Testing Space

chain = IntHandler(FloatHandler(StrHandler(NullHandler())))
obj = SomeObject()

print(chain.handle(obj, EventGet(int)))  # — вернуть значение obj.integer_field
print(chain.handle(obj, EventGet(str)))  # — вернуть значение obj.string_field
print(chain.handle(obj, EventGet(float)))  # — вернуть значение obj.float_field
chain.handle(obj, EventSet(1))  # — установить значение obj.integer_field =1
print(obj.integer_field)
chain.handle(obj, EventSet(1.1))  # — установить значение obj.float_field = 1.1
print(obj.float_field)
chain.handle(obj, EventSet("str"))  # — установить значение obj.string_field = "str"
print(obj.string_field)
