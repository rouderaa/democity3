class Subject:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer_func):
        self._observers.append(observer_func)

    def remove_observer(self, observer_func):
        self._observers.remove(observer_func)

    def notify_observers(self, *args, **kwargs):
        for observer in self._observers:
            observer(*args, **kwargs)
