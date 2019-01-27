class SomeObject:
    '''Some object.'''
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class NullHandler:
    '''A null handler (null chain link) that will pass the event to be
    processed by the next handler, if there is one.
    '''
    def __init__(self, successor=None):
        # Pass the next link.  
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            # Give to the next.  
            return self.__successor.handle(obj, event)


class EventGet:
    '''The class of the event that will occur.'''
    def __init__(self, value):
        self.kind = 'EventGet'
        self.value = value


class EventSet(EventGet):
    def __init__(self, value):
        super().__init__(value)
        self.kind = 'EventSet'


class IntHandler(NullHandler):

    def handle(self, obj, event):
        if type(event.value) is int or event.value is int:
            if event.kind == 'EventGet':
                return obj.integer_field
            elif event.kind == 'EventSet':
                obj.integer_field = event.value
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):

    def handle(self, obj, event):
        if type(event.value) is float or event.value is float:
            if event.kind == 'EventGet':
                return obj.float_field
            elif event.kind == 'EventSet':
                obj.float_field = event.value
        else:
            return super().handle(obj, event)


class StrHandler(NullHandler):

    def handle(self, obj, event):
        if type(event.value) is str or event.value is str:
            if event.kind == 'EventGet':
                return obj.string_field
            elif event.kind == 'EventSet':
                obj.string_field = event.value
        else:
            return super().handle(obj, event)


if __name__ == "__main__":
    obj = SomeObject()
    obj.integer_field = 42
    obj.float_field = 3.14
    obj.string_field = "some text"
    chain = IntHandler(FloatHandler(StrHandler(NullHandler)))
    print(chain.handle(obj, EventGet(int)))
    print(chain.handle(obj, EventGet(float)))
    print(chain.handle(obj, EventGet(str)))
    chain.handle(obj, EventSet(100))
    print(chain.handle(obj, EventGet(int)))
    chain.handle(obj, EventSet(0.5))
    print(chain.handle(obj, EventGet(float)))
    chain.handle(obj, EventSet('new text'))
    print(chain.handle(obj, EventGet(str)))
