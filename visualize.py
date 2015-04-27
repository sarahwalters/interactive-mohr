import pygame
from pygame.locals import *
import time
import mohr

class MohrModel:
    def __init__(self, sx, sy, sz, txy, tyz, txz):
        self.sx = sx
        self.sy = sy
        self.sz = sz
        self.txy = txy
        self.tyz = tyz
        self.txz = txz

        [sxp, syp, szp] = mohr.calc_sigp(sx, sy, sz, txy, tyz, txz)

        circ1 = mohr.define_circle(sxp, syp)
        circ2 = mohr.define_circle(sxp, szp)
        circ3 = mohr.define_circle(syp, szp)

        circles = [circ1, circ2, circ3]
        circles = sorted(circles, key=lambda tup: tup[1])

        self.circles = [Circle(*circles[2]), Circle(*circles[1]), Circle(*circles[0])]

    def update(self):
        pass

class Circle:
    def __init__(self, sig, radius):
        self.sig = int(sig) # tuple
        self.radius = int(radius) # number

    def update(self, sig, radius):
        self.sig = int(sig)
        self.radius = int(radius)

class MohrView:
    def __init__(self, model, screen):
        self.model = model # class Mohr
        self.screen = screen

    def draw(self):
        self.screen.fill(pygame.Color(0,0,0)) # fill with black

        grays = [50, 100, 150]
        for i, c in enumerate(self.model.circles):
            g = grays[i]
            pygame.draw.circle(self.screen, pygame.Color(g,g,g), (c.sig+500, 500), c.radius)
    
        pygame.display.update()
    
class MohrController:
    def __init__(self, model):
        self.model = model

    def handleEvent(self, event):
        pass
        #''' Responds to player arrow key input '''
        #if event.type != KEYDOWN: # catchall for events which are not arrow presses
        #    return
        #for box in self.model.boxes:
        #    # check whether box is in target range
        #    if box.centery > self.model.sy - 5*self.model.side/2 and box.centery < self.model.sy - 2*self.model.side:
        #        # check whether key pressed was correct key
        #        if event.key == self.arrowEventDict[box.arrow]:
        #            # remove and update score
        #            self.model.boxes.remove(box)
        #            self.model.score += 1

    
if __name__ == '__main__':
    '''
        This is where the game runs. Creates screen, builds MVC, controls whether game is running.
    '''
    pygame.init()

    size = (1000,800) #make sure sx-10 is multiple of 20
    screen = pygame.display.set_mode(size)
    
    model = MohrModel(80,50,20,20,40,40) 
    view = MohrView(model, screen)
    controller = MohrController(model)

    running = True # on/off switch

    while running:
        model.update()
        view.draw()
        time.sleep(.001) #game speed limit

    pygame.quit() # closes open pygame window once game is over