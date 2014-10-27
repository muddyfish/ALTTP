import Assets.PauseMenu.equipment as equipment
import Assets.PauseMenu.map as map
import Assets.PauseMenu.quest as quest
import Assets.PauseMenu.select as select

subs = ["equipment", "map", "quest", "select"]
subscreens = dict(zip(subs, [globals()[i] for i in subs]))

class PauseMenu():
  def __init__(self, main, pygame):
    globals()["main"] = main
    globals()["pygame"] = pygame
    self.screen = main.screen
    self.orig = self.screen.copy()
    self.subscreens = []
    for subscreen in subs:
      self.subscreens.append(subscreens[subscreen].__dict__[subscreen.capitalize()](main, self, pygame))
    self.subscreen = 0
    
  def left(self):
    self.subscreen = (self.subscreen-1)%len(self.subscreens)
    self.subscreens[self.subscreen].pointer.set_point("R")
  def right(self):
    self.subscreen = (self.subscreen+1)%len(self.subscreens)
    self.subscreens[self.subscreen].pointer.set_point("L")
  
  def run(self, events):
    self.screen.blit(self.orig, (0,0))
    self.subscreens[self.subscreen].run(events)