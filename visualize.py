import pygame
from pygame.locals import *
import time
import mohr

XSHIFT = 500
YSHIFT = 400
MARKERRADIUS = 7

class MohrModel:
    def __init__(self, sx, sy, sz, txy, tyz, txz):
        self.sx = sx
        self.sy = sy
        self.sz = sz
        self.txy = txy
        self.tyz = tyz
        self.txz = txz

        [sxp, syp, szp] = mohr.calc_sigp(sx, sy, sz, txy, tyz, txz)
        self.principals = [int(sxp), int(syp), int(szp)]

        circ1 = mohr.define_circle(sxp, syp)
        circ2 = mohr.define_circle(sxp, szp)
        circ3 = mohr.define_circle(syp, szp)

        circles = [circ1, circ2, circ3]
        circles = sorted(circles, key=lambda tup: tup[1])

        # for tracking which principal is moving (if one is)
        self.movingPrincipal = None

        # the circles themselves
        self.circles = [Circle(*circles[2]), Circle(*circles[1]), Circle(*circles[0])]

    def update(self):
    	[sxp, syp, szp] = self.principals
        circ1 = mohr.define_circle(sxp, syp)
        circ2 = mohr.define_circle(sxp, szp)
        circ3 = mohr.define_circle(syp, szp)

        circles = [circ1, circ2, circ3]
        circles = sorted(circles, key=lambda tup: tup[1])

        self.circles = [Circle(*circles[2]), Circle(*circles[1]), Circle(*circles[0])]


class Circle:
    def __init__(self, sig, radius):
        self.sig = int(sig) # tuple
        self.radius = int(radius) # number

    def update(self, sig=None, radius=None):
        if sig:
            self.sig = int(sig)
        if radius:
            self.radius = int(radius)


class MohrView:
    def __init__(self, model, screen):
        self.model = model # class Mohr
        self.screen = screen

    def draw(self):
        self.screen.fill(pygame.Color(0,0,0)) # fill with black

        # draw circles
        grays = [75,125,200]
        for i,c in enumerate(self.model.circles):
            g = grays[i]
            pygame.draw.circle(self.screen, pygame.Color(g,g,g), (c.sig+XSHIFT, YSHIFT), c.radius)
    
        # mark & label the principal stresses
        for i,p in enumerate(self.model.principals):
            color = [0,0,0]
            color[i] = 255

            label = myfont.render("%s" %(p), 1, color) #*****FIX***go through intersections
            self.screen.blit(label,(50,690 + 20*i))

            if i == self.model.movingPrincipal: # different color if moving
                pygame.draw.circle(self.screen, pygame.Color(255,255,255), (p+XSHIFT, YSHIFT), MARKERRADIUS)
            else:
                pygame.draw.circle(self.screen, pygame.Color(*color), (p+XSHIFT, YSHIFT), MARKERRADIUS)

        # label the max shears
        for i, l in enumerate(self.model.circles):
            color = [255,255,255]
            color[i] = 0

            label2 = myfont.render("%s" %(l.radius), 1, color)
            self.screen.blit(label2,(50,610 + 20*i))

            if i == self.model.movingMaxShear: # different color if moving
                pygame.draw.circle(self.screen, pygame.Color(255,255,255), (l.sig+XSHIFT, l.radius+YSHIFT), MARKERRADIUS)
            else:
                pygame.draw.circle(self.screen, pygame.Color(*color), (l.sig+XSHIFT, l.radius+YSHIFT), MARKERRADIUS)

        label3 = myfont.render("Principal Stresses", 1, (255,255,255))
        self.screen.blit(label3,(50,670))

        label4 = myfont.render("Maximum Shear Stresses", 1, (255,255,255))
        self.screen.blit(label4,(50,590))

        pygame.display.update()
   

class MohrController:
    def __init__(self, model):
        self.model = model
        self.model.movingPrincipal = None
        self.model.movingMaxShear = None
        self.model.oldRadius = None
        self.model.oldPrincipals = None

    def handleEvent(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.model.movingPrincipal = self.inPrincipalMarker(event.pos)
            self.model.movingMaxShear = self.inMaxShearMarker(event.pos)

            # save the radius, if changing max shear
            if self.model.movingMaxShear != None:
                self.model.oldRadius = self.model.circles[self.model.movingMaxShear].radius
                self.model.oldPrincipals = self.model.principals

        elif event.type == MOUSEBUTTONUP:
            self.model.movingPrincipal = None
            self.model.movingMaxShear = None
            self.model.oldRadius = None
            self.model.oldPrincipals = None

        elif event.type == MOUSEMOTION:
            if self.model.movingPrincipal != None:
                self.model.principals[self.model.movingPrincipal] = event.pos[0]-XSHIFT
                self.model.update()

            if self.model.movingMaxShear != None:
                newRadius = event.pos[1]-YSHIFT
                ratio = newRadius/float(self.model.oldRadius)
                self.model.principals = [int(op*ratio) for op in self.model.oldPrincipals]
                self.model.circles[self.model.movingMaxShear].update(radius=newRadius)
                self.model.update()

    def inPrincipalMarker(self, pos):
        # default to no marker
        inMarker = None

        # check each intersection point
        for i, p in enumerate(self.model.principals):
            dist = ((pos[0]-p-XSHIFT)**2 + (pos[1]-0-YSHIFT)**2)**0.5
            if dist < MARKERRADIUS: # in this point?
                inMarker = i

        return inMarker

    def inMaxShearMarker(self, pos):
    	# default to no marker
        inMarker = None

        # check each intersection point
        for i, l in enumerate(self.model.circles):
            dist = ((pos[0]-l.sig-XSHIFT)**2 + (pos[1]-l.radius-YSHIFT)**2)**0.5
            if dist < MARKERRADIUS: # in this point?
                inMarker = i

        return inMarker

    
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

    myfont=pygame.font.SysFont("monospace", 15)

    running = True # on/off switch

    while running:
        view.draw()
        time.sleep(.001) #game speed limit
        for event in pygame.event.get():
       	    if event.type == QUIT: # player closed window
                running = False
            if event.type in [MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION]: # arrow key press
                controller.handleEvent(event)

    pygame.quit() # closes open pygame window once game is over