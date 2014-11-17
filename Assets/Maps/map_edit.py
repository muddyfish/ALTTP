import zipfile
import json
from Assets.button import *
from Assets.entry import *
import view_map
try:
  import cStringIO as StringIO
except ImportError:
  import StringIO
  
class Map(view_map.Map):
  def __init__(self, main, pygame):
    globals()["main"] = main
    globals()["pygame"] = pygame
    view_map.add_globals(main, pygame)
    self.screen = main.screen
    self.map_f = main.args[1]
    self.load_map(self.map_f)
    self.size = main.size
    main.screen=type(main.screen)(pygame.display.set_mode((main.size[0]+100, main.size[1]+200)))
    self.screen = main.screen
    self.tile_offset = [0,0]
    self.coll_surf = pygame.Surface((8,8), pygame.SRCALPHA)
    self.coll_surf.fill((128,0,0,128))
    self.button_text = ["Collision", "Exits", "Entities", "Layers", "Water"]
    self.buttons = []
    for b in range(len(self.button_text)):
      self.buttons.append(Button(pygame, self.screen, (0,0,128), main.size[0]+10, 9+48*b, 80, 32, 1, self.button_text[b], ((128,128,0))))
    self.subscreen_events = [self.collision_events, str, str, str, str]
    self.subscreen_blits =  [self.collision_blits, range, range, range, range]
    self.subscreen = 0
    
  def indexes(self, iterable, value):
    indexes = []
    for x, x_val in enumerate(iterable):
      for y, y_val in enumerate(x_val):
	if y_val == value:
	  indexes.append((x,y))
    return indexes
  
  def save(self):
    m = zipfile.ZipFile(self.map_f, "w", zipfile.ZIP_DEFLATED)
    m.writestr("collision", json.dumps(self.collision))
    m.writestr("position", json.dumps(self.position))
    image = StringIO.StringIO()
    pygame.image.save(self.tilesheet, image)
    m.writestr("tilesheet", image.getvalue())
    
  def collision_events(self, events):
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
	if event.pos[0] < main.size[0]:
	  x = event.pos[0]/16+self.tile_offset[0]+1
	  y = event.pos[1]/16+self.tile_offset[1]+1
	  x2 = (event.pos[0]/8)%2
	  y2 = (event.pos[1]/8)%2
	  self.screen.blit_all()
	  if event.button == 3:
	    self.collision[x*2+x2][y*2+y2]^=1
	  else:
	    for x,y in self.indexes(self.position, self.position[x][y]):
	      self.collision[x*2+x2][y*2+y2]^=1	      
  def collision_blits(self, x, y):
    pos = self.get_pos(x,y,(16,16),8)
    for x2 in range(2):
      for y2 in range(2):
	pos2 = [pos[0]+x2*8, pos[1]+y2*8]
	if self.collision[(x+self.tile_offset[0])*2+x2][(y+self.tile_offset[1])*2+y2]:
	  self.screen.blit_func(self.coll_surf, pos2)
    
  def run(self, events):
    for event in events:
      if event.type == pygame.KEYDOWN:
	if event.key == pygame.K_LEFT: self.tile_offset[0]-=1
	if event.key == pygame.K_RIGHT:self.tile_offset[0]+=1
	if event.key == pygame.K_UP:   self.tile_offset[1]-=1
	if event.key == pygame.K_DOWN: self.tile_offset[1]+=1
	if event.key == pygame.K_s: self.save()
	self.screen.blit_all()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.pos[0] > main.size[0]:
	  for b in range(len(self.buttons)):
	    if self.buttons[b].pressed(event.pos):
	      self.subscreen = b
	      self.screen.fill((0,0,0))
	      for button in self.buttons:
		button.draw()
	      self.screen.blit_all()
    self.subscreen_events[self.subscreen](events)
    for x in xrange(self.blit_tiles[0]):
      for y in xrange(self.blit_tiles[1]):
	pos = self.get_pos(x,y, (0,0))
	try:
	  self.screen.blit_func(self.tiles[x+self.tile_offset[0]][y+self.tile_offset[1]], pos)
	  self.subscreen_blits[self.subscreen](x, y)
	except IndexError: pass