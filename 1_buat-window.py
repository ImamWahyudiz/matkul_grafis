from core.base import Base 
class Test(Base):
    def initialize(self):
        print("init...")

    def update(self):
        pass

Test().run()
