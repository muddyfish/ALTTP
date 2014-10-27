import zipfile
import json
try:
  import cStringIO as StringIO
except ImportError:
  import StringIO
  
class Map():
  def __init__(self, main, pygame):
    globals()["main"] = main
    globals()["pygame"] = pygame
    self.screen = main.screen
    self.map_f = main.args[1]
    self.load_map(self.map_f)
    self.tile_offset = [1,1]
    self.view_offset = [0,0]
    self.coll_surf = pygame.Surface((8,8), pygame.SRCALPHA)
    self.coll_surf.fill((128,0,0,128))
    
  def load_map(self, map_f):
    self.map = zipfile.ZipFile(map_f, "r")
    self.position = json.load(self.map.open("position"))
    self.tilesheet = pygame.image.load(StringIO.StringIO(self.map.read("tilesheet")), ".tga")
    self.tile_size = self.tilesheet.get_height()
    self.tile_ims = []
    for tile in range(self.tilesheet.get_width()/self.tile_size):
      self.tile_ims.append(pygame.Surface((self.tile_size, self.tile_size)))
      self.tile_ims[-1].blit(self.tilesheet, (0,0), (tile*self.tile_size,0,(tile+1)*self.tile_size,16))
    self.tiles = [[self.tile_ims[self.position[x][y]] \
      for y in range(len(self.position[0]))] \
      for x in range(len(self.position))]
    self.blit_tiles = [i/self.tile_size+1 for i in self.screen.get_size()]
    if "collision" in self.map.namelist():
      self.collision = json.load(self.map.open("collision"))
    else:
      self.collision = [[int(0) \
	for y in range(len(self.position[0]))] \
	for x in range(len(self.position))]
    self.map.close()
  
  def pos(self, x, y):
    return ((x-1)*self.tile_size+self.view_offset[0], (y-1)*self.tile_size+self.view_offset[1])
    
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
    
  def run(self, events):
    for event in events:
      if event.type == pygame.KEYDOWN:
	if event.key == pygame.K_LEFT: self.tile_offset[0]-=1
	if event.key == pygame.K_RIGHT:self.tile_offset[0]+=1
	if event.key == pygame.K_UP:   self.tile_offset[1]-=1
	if event.key == pygame.K_DOWN: self.tile_offset[1]+=1
	if event.key == pygame.K_s: self.save()
      if event.type == pygame.MOUSEBUTTONDOWN:
	x = event.pos[0]/self.tile_size+self.tile_offset[0]+1
	y = event.pos[1]/self.tile_size+self.tile_offset[1]+1
	if event.button == 3:
	  self.collision[x][y]^=1
	else:
	  for x,y in self.indexes(self.position, self.position[x][y]):
	    self.collision[x][y]^=1
    for x in range(self.blit_tiles[0]):
      for y in range(self.blit_tiles[1]):
	pos = self.pos(x,y)
	try:
	  self.screen.blit(self.tiles[x+self.tile_offset[0]][y+self.tile_offset[1]], pos)
	  if self.collision[x+self.tile_offset[0]][y+self.tile_offset[1]]:
	    self.screen.blit(self.coll_surf, pos)
	except IndexError: pass