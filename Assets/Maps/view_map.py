import zipfile
import json
import warnings
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
    self.tile_offset = [40,40]
    self.view_offset = [0,0]
    self.move_directions = {pygame.K_LEFT: (0,-1),
			    pygame.K_RIGHT:(0, 1),
			    pygame.K_UP:   (1,-1),
			    pygame.K_DOWN: (1, 1)}
    self.pos = [[(self.get_pos(x,y)) \
      for y in range(self.blit_tiles[1])] \
      for x in range(self.blit_tiles[0])]
    
  def load_map(self, map_f):
    self.map = zipfile.ZipFile(map_f, "r")
    self.position = json.load(self.map.open("position"))
    self.tilesheet = pygame.image.load(StringIO.StringIO(self.map.read("tilesheet")), ".tga")
    self.collision = json.load(self.map.open("collision"))
    self.map.close()
    self.tile_size = self.tilesheet.get_height()
    self.tile_ims = []
    for tile in range(self.tilesheet.get_width()//self.tile_size):
      self.tile_ims.append(pygame.Surface((self.tile_size, self.tile_size)))
      self.tile_ims[-1].blit(self.tilesheet, (0,0), (tile*self.tile_size,0,(tile+1)*self.tile_size,16))
    self.tiles = [[self.tile_ims[self.position[x][y]] \
      for y in range(len(self.position[0]))] \
      for x in range(len(self.position))]
    self.blit_tiles = [i//self.tile_size+1 for i in self.screen.get_size()]
  
  def get_pos(self, x, y):
    return ((x-1)*self.tile_size+self.view_offset[0], (y-1)*self.tile_size+self.view_offset[1])
  def col_pos(self, x, y):
    return (x*8+self.view_offset[0], y*8+self.view_offset[1])

  def collide(self, d, a):
    offset = [self.tile_offset[i]*2-(self.view_offset[i]>>3)+self.blit_tiles[i] for i in range(2)]
    offset[d]+=a
    return self.collision[offset[0]][offset[1]]^1

  def move(self, d, a):
    if self.collide(d,a):
      self.view_offset[d]^=8
      if len({(self.view_offset[d], a), (0,-1), (8,1)})==2: self.tile_offset[d]+=a
      self.screen.blit_rects.append(((0,0), self.screen.get_size()))
      self.pos = [[(self.get_pos(x,y)) \
        for y in range(self.blit_tiles[1])] \
        for x in range(self.blit_tiles[0])]
  
  def run(self, events):
    for event in events:
      if event.type == pygame.KEYDOWN:
        if event.key in self.move_directions:
	  self.move(*self.move_directions[event.key])
    for x in range(self.blit_tiles[0]):
      for y in range(self.blit_tiles[1]):
        try:
          self.screen.blit_func(self.tiles[x+self.tile_offset[0]][y+self.tile_offset[1]], self.pos[x][y])
        except IndexError: warnings.warn("The border has been breached at: %r"%(self.tile_offset), UserWarning)