from lab2.algorithms.scan import Scan


class CScan(Scan):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, cycled=True)

    def tick_chamber(self):
        self.next_chamber()
