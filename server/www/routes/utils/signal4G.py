class Signal():
    def __init__(self):
        self.signal = -1

    def update(self, signal):
        self.signal = signal

    def get(self):
        return self.signal

signal4G = Signal()