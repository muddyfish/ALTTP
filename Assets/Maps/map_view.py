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
    self.noclip = 'noclip' in main.args
    self.screen = main.screen
    self.map_f = main.args[1]
    self.load_map(self.map_f)
    self.tile_offset = [0,0]
    self.view_offset = [0,0]
    self.coll_surf = pygame.Surface((16,8), pygame.SRCALPHA)
    self.coll_surf.fill((0,128,0,128))
    self.move_directions = {pygame.K_LEFT: (0,-1),
			    pygame.K_RIGHT:(0, 1),
			    pygame.K_UP:   (1,-1),
			    pygame.K_DOWN: (1, 1)}
    self.pos = [[[[(self.get_pos(x,y, [x2,y2])) \
      for y in range(self.blit_tiles[1])] \
      for x in range(self.blit_tiles[0])] \
      for y2 in range(16)] \
      for x2 in range(16)]

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
  
  def get_pos(self, x, y, view_offset):
    return ((x-1)*16+view_offset[0], (y-1)*16+view_offset[1])

  def collide(self, d, a):
    if self.noclip: return True
    offset = [self.tile_offset[i]*2-(self.view_offset[i]>>3)+self.blit_tiles[i] for i in range(2)]
    offset[d]+=a
    return not (self.collision[offset[0]][offset[1]] or self.collision[offset[0]-1][offset[1]])

  def move(self, d, a):
    if self.collide(d,a):
      self.view_offset[d]^=8
      if len({(self.view_offset[d], a), (0,-1), (8,1)})==2:
	self.tile_offset[d]+=a
      self.screen.blit_all()
  
  def run(self, events):
    for event in events:    
      if event.type == pygame.KEYDOWN:
        if event.key in self.move_directions:
	  self.move(*self.move_directions[event.key])
    player_pos = [self.screen.get_width()/2-16, self.screen.get_height()/2-8]
    blit_x = self.tile_offset[0]
    blit_y = self.tile_offset[1]
    view_x = self.view_offset[0]
    view_y = self.view_offset[1]
    
    if self.tile_offset[0] <= 0:
      blit_x = 0
      view_x = 0
      player_pos[0] += self.tile_offset[0]*16-self.view_offset[0]
    if self.tile_offset[0]+self.blit_tiles[0]-1 >= len(self.tiles):
      blit_x = len(self.tiles)-self.blit_tiles[0]
      view_x = 0
      player_pos[0] -= (len(self.tiles)-self.blit_tiles[0]-self.tile_offset[0])*16+self.view_offset[0]
    if self.tile_offset[1] <= 0:
      blit_y = 0
      view_y = 0
      player_pos[1] += self.tile_offset[1]*16-self.view_offset[1]
    if self.tile_offset[1]+self.blit_tiles[1]-1 >= len(self.tiles[0]):
      blit_y = len(self.tiles[0])-self.blit_tiles[1]
      view_y = 0
      player_pos[1] -= (len(self.tiles)-self.blit_tiles[1]-self.tile_offset[1])*16+self.view_offset[1]
 
    for x in range(self.blit_tiles[0]):
      for y in range(self.blit_tiles[1]):
	self.screen.blit_func(self.tiles[blit_x+x][blit_y+y], self.pos[view_x][view_y][x][y])
    self.screen.blit_func(self.coll_surf, player_pos)