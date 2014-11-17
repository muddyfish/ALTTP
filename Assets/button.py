class Button():
  def __init__(self, pygame, surface, color, x, y, length, height, width, text, text_color):
    globals()['pygame'] = pygame
    self.surface, self.color, self.x, self.y, self.length, self.height, self.width, self.text, self.text_color = surface, color, x, y, length, height, width, text, text_color
    self.draw()
    
  def draw(self):
    surface = self.draw_button(self.surface, self.color, self.length, self.height, self.x, self.y, self.width)
    surface = self.write_text( self.surface, self.text, self.text_color, self.length, self.height, self.x, self.y)
    self.rect = pygame.Rect(self.x,self.y, self.length, self.height)

  def write_text(self, surface, text, text_color, length, height, x, y):
    myFont = pygame.font.SysFont("velvenda", 18)
    myText = myFont.render(text, 1, text_color)
    surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
    return surface

  def draw_button(self, surface, color, length, height, x, y, width):       
    for i in range(1,10):
      s = pygame.Surface((length+(i*2),height+(i*2)))
      s.fill(color)
      alpha = (255/(i+2))
      if alpha <= 0:
        alpha = 1
      s.set_alpha(alpha)
      surface.blit(s, (x-i,y-i))
    return surface

  def pressed(self, mouse):
    if mouse[0] > self.rect.topleft[0]:
      if mouse[1] > self.rect.topleft[1]:
        if mouse[0] < self.rect.bottomright[0]:
          if mouse[1] < self.rect.bottomright[1]:
            return True
          else: return False
        else: return False
      else: return False
    else: return False
 
