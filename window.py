
from core.base import Base


class Window(Base):
    def initialize(self):       
        print("Window terinisialisasi")

    def update(self):
        pass


Window().run()