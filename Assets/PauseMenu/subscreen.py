import math

class Pointer():
  def __init__(self, subscreen):
    self.subscreen = subscreen
    self.screen = self.subscreen.screen
    self.point_im = self.subscreen.load_image("PauseMenu/cursor.png")
    self.point_ims = [pygame.transform.rotate(self.point_im, i*90) for i in range(4)]
    self.points = self.subscreen.get_points()
    self.points["L"] = (-10,80,30,30)
    self.points["R"] = (240,80,30,30)
    self.set_point("R")
    
  def set_point(self, point):
    self.point = point
    rect = self.points[point]
    self.rect = list(rect[:2])
    self.rect.extend([sum(rect[i::2])-10 for i in range(2)])
    self.rect = [r+30 for r in self.rect]
    self.p_rects = (self.rect[:2], self.rect[::3], self.rect[2:], self.rect[2:0:-1])
  
  def change(self, l, u):
    c_point = self.points[self.point]
    self.distances = []
    for point in self.points:
      p_val = self.points[point]
      if p_val != c_point:
#	print point, \
#	  ((l !=-1 and p_val[0] - c_point[0] > 0) or \
#	   (l != 1 and p_val[0] - c_point[0] < 0) or \
#	   (u!=0 and p_val[0] - c_point[0] == 0)) and \
#	  ((u !=-1 and p_val[1] - c_point[1] > 0) or \
#	   (u != 1 and p_val[1] - c_point[1] < 0) or \
#	   (l!=0 and p_val[1] - c_point[1] == 0)), p_val[0] - c_point[0], p_val[1] - c_point[1], l, u
	
	if((l !=-1 and p_val[0] - c_point[0] > 0) or \
	   (l != 1 and p_val[0] - c_point[0] < 0) or \
	   (u != 0 and p_val[0] - c_point[0] == 0)) and \
	  ((u !=-1 and p_val[1] - c_point[1] > 0) or \
	   (u != 1 and p_val[1] - c_point[1] < 0) or \
	   (l != 0 and p_val[1] - c_point[1] == 0)):
	  self.distances.append((point, p_val, math.sqrt((c_point[0]-p_val[0])**2+(c_point[1]-p_val[1])**2)))
    self.distances.sort(key=lambda x: x[2])
#    print self.distances
    if len(self.distances) != 0:
      self.set_point(self.distances[0][0])
  
  def blit(self):
    map(self.screen.blit, self.point_ims, self.p_rects)

class Subscreen():
  def __init__(self, main, pausemenu, pygame):
    globals()["main"] = main
    globals()["pygame"] = pygame
    self.screen = main.screen
    self.pausemenu = pausemenu
    self.load_image = main.asset_loader.load_image
    
    self.im = self.load_image("PauseMenu/"+self.__class__.__name__.lower()+".png")
    self.im_text = self.load_image("PauseMenu/nes_text/"+self.__class__.__name__+".png")
    self.im.blit(self.im_text, (self.im.get_width()/2-self.im_text.get_width()/2, 0))
    self.l = self.load_image("PauseMenu/L.png")
    self.r = self.load_image("PauseMenu/R.png")
    
    self.pointer = Pointer(self)
    
  def get_points(self): return {}
  
  def run(self, events):
    self.screen.blit(self.im, (40,40))
    self.screen.blit(self.l, (20,111))
    self.screen.blit(self.r, (274,111))
    self.pointer.blit()
    for event in events:
      if event.type == pygame.KEYDOWN:
	if event.key == pygame.K_LEFT:
	  if self.pointer.point == "L": self.pausemenu.left()
	  else: self.pointer.change(-1, 0)
	if event.key == pygame.K_RIGHT: 
	  if self.pointer.point == "R": self.pausemenu.right()
	  else: self.pointer.change(1, 0)
	if event.key == pygame.K_UP:
	  self.pointer.change(0, -1)
	if event.key == pygame.K_DOWN:
	  self.pointer.change(0, 1)
	
 