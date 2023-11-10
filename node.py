class Node:
  def __init__(self, x: int, y: int, xSupport: bool = False, ySupport: bool = False):
    self.x = x
    self.y = y
    self.xSupport = xSupport
    self.ySupport = ySupport
  
  @classmethod
  def setSupports(self, xSupport: bool = False, ySupport: bool = False):
    self.xSupport = xSupport
    self.ySupport = ySupport
    
  @classmethod
  def print(self):
    return f"x: {self.x}, y: {self.y}, xSupport: {self.xSupport}, ySupport: {self.ySupport}"
