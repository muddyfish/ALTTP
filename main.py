#Import modules
import pygame
import sys
import glob
import os
import json
import inspect

import Assets.asset_loader as asset_loader
import Assets.PauseMenu.main as pause_menu
import Assets.Maps.to_collision as to_collision
import Assets.Maps.view_map as view_map

class Main:
    def __init__(self):
        self.load_settings()
        self.size = (320,240)
        self.fullscreen = 0
        if self.settings["fullscreen"]:
            self.fullscreen = pygame.FULLSCREEN
        self.fps_limit = self.settings["fps_limit"]

        #Init pygame
        pygame.init()
        pygame.key.set_repeat(100)
        self.screen = Screen(pygame.display.set_mode(tuple(self.size), self.fullscreen)) #Create the display
        pygame.display.set_caption("OOT 2D")
        self.clock = pygame.time.Clock()
        self.args = sys.argv

        self.title_font=pygame.font.SysFont("vervanda", 48)
        self.fps_font=pygame.font.SysFont("vervanda", 12)

        self.asset_loader = asset_loader.AssetLoader(pygame)
        self.controllers = {
          "pause": pause_menu.PauseMenu,
          "collision_edit": to_collision.Map,
          "map_view": view_map.Map}
        self.screen_control = None
        self.change_controller("map_view")

    def run(self):
        while 1:
            self.clock.tick(self.fps_limit)
            events = pygame.event.get()
            for event in events: #Events that are always done
                if event.type == pygame.QUIT: self.quit()
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_BACKSPACE: self.screenshot()
                    elif event.key == pygame.K_ESCAPE:  self.quit()
                        
            self.screen_control.run(events) #Other events
            fps = self.fps_font.render("FPS: %d" %(int(self.clock.get_fps())), True, (255,255,255))
            self.screen.blit(fps, (10, 30))
            pygame.display.update(self.screen.blit_rects_old)
            pygame.display.update(self.screen.blit_rects)
            self.screen.blit_rects_old = self.screen.blit_rects
            self.screen.blit_rects = []

    def screenshot(self):
        print("Screenshot")
        globs = glob.glob("./Screenshots/screenshot_*.png")
        latest_num=0
        if len(globs) != 0: latest_num = max([int(f.split("_")[-1][:-4]) for f in globs])
        pygame.image.save(self.screen.copy(), "Screenshots%sscreenshot_%i.png" %(os.sep, latest_num+1))

    def change_controller(self,new):
        self.screen.blit_rects.append(((0,0), self.screen.get_size()))
        self.screen_control_name=new
        self.screen_control=self.controllers[self.screen_control_name](self, pygame)
            
    def quit(self):
        pygame.quit()
        sys.exit()

    def load_settings(self):
        file_obj = open("settings.json")
        self.settings = json.load(file_obj)
        file_obj.close()

    def save_settings(self):
        file_obj = open("settings.json", "w")
        json.dump(file_obj, self.settings)
        file_obj.close()

class Screen(object):
    def __init__(self, surf):
        self.blit_rects = []
        self.blit_rects_old = []
        for name, val in inspect.getmembers(surf):
            if name != "blit":
                try: setattr(self, name, val)
                except TypeError: pass
            else:
                self.blit_func = val
        
    def blit(self, *args, **kargs):
        self.blit_rects.append(self.blit_func(*args, **kargs))
        
def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    Main().run()

if __name__ == "__main__":
    if "debug" in sys.argv:
        try: import cProfile as profile
        except ImportError: import profile
        profile.run('main()')
    else:
        main()
