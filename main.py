from cmu_graphics import *
import random
import math

def onAppStart(app):
    marginX = app.width * 0.1
    marginY = app.height * 0.25
    boardWidth  = app.width  - (2 * marginX)
    boardHeight = app.height - (marginY + 50)
    app.board = Board(marginX, marginY, boardWidth, boardHeight)
    app.modes = [ Mode('Standard Blue Dot', 'blue', Dot),
                  Mode('Big Slow Red Dot', 'red', BigSlowRedDot),
                  Mode('Fast Sienna Dot', 'sienna', FastSiennaDot)
                ]
    app.modeIndex = 0

def onResize(app):
    # margin ratios to keep board roughly centered
    marginX = app.width * 0.1
    marginY = app.height * 0.25

    newWidth  = app.width  - (2 * marginX)
    newHeight = app.height - (marginY + 50)  # leave top UI space

    app.board.left   = marginX
    app.board.top    = marginY
    app.board.width  = newWidth
    app.board.height = newHeight

    for dot in app.board.dots:
        xmin = app.board.left + dot.r
        xmax = app.board.left + app.board.width - dot.r
        ymin = app.board.top + dot.r
        ymax = app.board.top + app.board.height - dot.r
        dot.x = max(xmin, min(dot.x, xmax))
        dot.y = max(ymin, min(dot.y, ymax))

def onStep(app):
    app.board.moveDots()

def redrawAll(app):
    drawLabel('Dot Classes App', app.width/2, app.board.top -120, size=16, bold=True)
    drawLabel('Click to place a new dot', app.width/2, app.board.top -100, size=14)
    drawLabel('Press m to change dot mode', app.width/2, app.board.top -80, size=14)
    drawLabel('Press c to clear all dots', app.width/2, app.board.top -60, size=14)
    drawLabel(f'Gravity: {app.board.gravityMode.upper()}', app.width/2, app.board.top -40, size=14, fill='gray')
    mode = app.modes[app.modeIndex]
    drawLabel(f'Current mode: {mode.name}', app.width/2, app.board.top - 20, size=14, fill=mode.color)
    app.board.draw(app)

def onKeyPress(app, key):
    if key == 'm':
        app.modeIndex = (app.modeIndex + 1) % len(app.modes)
    elif key == 'c':
        app.board.clearDots()
    elif key == 'g':
        order = ['none', 'mutual', 'fall']
        i = order.index(app.board.gravityMode)
        app.board.gravityMode = order[(i + 1) % len(order)]

def onMousePress(app, mouseX, mouseY):
    if app.board.contains(mouseX, mouseY):
       mode = app.modes[app.modeIndex]
       dot = mode.ModeClass(mouseX, mouseY, app.board)
class Spark:
    def __init__(self, x, y, angle, speed, lifetime=10):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.life = lifetime
        self.maxLife = lifetime

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.speed *= 0.95  # slows down slightly
        self.life -= 1

    def draw(self):
        # fade out as life decreases
        alpha = max(0, self.life / self.maxLife)
        fade = int(255 * alpha)
        color = rgb(255, fade, 100)  # more red when fading out
        drawCircle(self.x, self.y, 2, fill=color)

class Dot: 
    def __init__(self, x, y, board):
        self.x = x
        self.y = y
        self.r = 8
        self.color = "blue"
        self.board = board
        self.maxHealth = 5
        self.health = 5
        self.iframes = 0
        self.cracks = []  # list of (angle, length) tuples

        #set dx and dy
        while True:
            self.dx = random.randrange(-3, 3)
            self.dy = random.randrange(-3, 3)
            if (self.dx != 0) or (self.dy != 0):
                break
        board.dots.append(self)

    def integrate(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt

    def handleWalls(self, board):
        #default = bounce
        xmin = board.left + self.r
        ymin = board.top + self.r
        xmax = board.left + board.width - self.r
        ymax = board.top + board.height - self.r

        if self.x < xmin:
            self.x = xmin
            self.dx = -self.dx
        if self.x > xmax:
            self.x = xmax
            self.dx = -self.dx
        if self.y < ymin:
            self.y = ymin
            self.dy = -self.dy
        if self.y > ymax:
            self.y = ymax
            self.dy = -self.dy

    @property
    def mass(self):
        # mass ∝ area in 2D -> r^2 is a good approximation
        return self.r **2

    def takeDamage(self):
        self.health -= 1
        # Add 1–2 new cracks
        for i in range(random.randint(1,2)):
            self.cracks.append((random.random() * 2*math.pi,
                                random.randint(self.r//2, self.r)))
    
    def draw(self, app):
        drawCircle(self.x, self.y, self.r, fill=self.color)

        for angle, length in self.cracks:
            midAngle = angle + random.uniform(-0.1, 0.1)
            midLen = length * 0.5
            midX = self.x + midLen * math.cos(midAngle)
            midY = self.y + midLen * math.sin(midAngle)
            endX = self.x + length * math.cos(angle)
            endY = self.y + length * math.sin(angle)
            drawLine(self.x, self.y, midX, midY, fill='white', lineWidth=1)
            drawLine(midX, midY, endX, endY, fill='white', lineWidth=1)
class BigSlowRedDot(Dot):
    def __init__(self, x, y, board):
        super().__init__(x, y, board)
        self.r = 20
        self.color = "red"
        self.dx = self.dx / 3
        self.dy = self.dy / 3
        self.health = 10
        self.maxHealth = 10
class FastSiennaDot(Dot):
    def __init__(self, x, y, board):
        super().__init__(x, y, board)
        self.r = 8
        self.color = "sienna"
        self.dx = self.dx * 3
        self.dy = self.dy * 3
        self.health = 3
        self.maxHealth = 3  

    def handleWalls(self, board):
        xmin = self.board.left + self.r
        ymin = self.board.top + self.r
        xmax = self.board.left + self.board.width - self.r
        ymax = self.board.top + self.board.height - self.r

        if self.x < xmin:
            self.x = xmax
            self.dx = self.dx
        if self.y < ymin:
            self.y = ymax
            self.dy = self.dy
        if self.x > xmax:
            self.x = xmin
            self.dx = self.dx
        if self.y > ymax:
            self.y = ymin
            self.dy = self.dy
class Mode:
    def __init__(self, name, color, ModeClass):
        self.name = name
        self.color = color
        self.ModeClass = ModeClass
class Board:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.gravityEnabled = True

        # Tunables
        self.SUBSTEPS = 4
        self.G = 0.001
        self.G_DOWN = 0.2
        self.MAX_SPEED = 12
        self.RESTITUTION = 1.0
        self.SEPARATION_BIAS = 0.02
        self.POS_CORRECT_PERCENT = 0.9
        self.POS_CORRECT_SLOP = 0.005
        self.DAMAGE_COOLDOWN = 6  # frames

        self.dots = []
        self.sparks = []
        self.activeContacts = set()
        self.gravityMode = 'mutual'

    def clearDots(self):
        self.dots.clear()

    def moveDots(self):
        # substepped physics
        for _ in range(self.SUBSTEPS):
            # Planetary Gravity
            if self.gravityMode == 'mutual':
                for i in range(len(self.dots)):
                    for j in range(i + 1, len(self.dots)):
                        d1 = self.dots[i]; d2 = self.dots[j]
                        dx = d2.x - d1.x
                        dy = d2.y - d1.y
                        dist = math.hypot(dx, dy)
                        if dist > 1:
                            force = self.G * (d1.mass * d2.mass) / (dist * dist)
                            fx = force * dx / dist
                            fy = force * dy / dist
                            d1.dx += (fx / d1.mass) / self.SUBSTEPS
                            d1.dy += (fy / d1.mass) / self.SUBSTEPS
                            d2.dx -= (fx / d2.mass) / self.SUBSTEPS
                            d2.dy -= (fy / d2.mass) / self.SUBSTEPS
            
            # On Planet Gravity
            elif self.gravityMode == 'fall':
                ay = self.G_DOWN / self.SUBSTEPS
                for d in self.dots:
                    d.dy += ay

            # Speed cap
            for d in self.dots:
                s = math.hypot(d.dx, d.dy)
                if s > self.MAX_SPEED:
                    scale = self.MAX_SPEED / s
                    d.dx *= scale
                    d.dy *= scale

            # Integrate + walls (polymorphic; no extra generic clamp here)
            dt = 1 / self.SUBSTEPS
            for d in self.dots:
                d.integrate(dt)
                d.handleWalls(self)

            # Collisions each substep
            self.checkForCollisions()

        # Sparks once per frame
        for s in self.sparks:
            s.move()
        self.sparks = [s for s in self.sparks if s.life > 0]

        # Decrement i-frames
        for d in self.dots:
            if d.iframes > 0:
                d.iframes -= 1

        # Prune stale contacts (dots removed this frame)
        ids = {id(d) for d in self.dots}
        self.activeContacts = {p for p in self.activeContacts if p[0] in ids and p[1] in ids}

    def contains(self, x, y):
        return (self.left <= x <= self.left + self.width and
                self.top  <= y <= self.top  + self.height)

    def draw(self, app):
        drawRect(self.left, self.top, self.width, self.height, fill=None, border='black', borderWidth=4)
        for d in self.dots:
            d.draw(app)
        for s in self.sparks:
            s.draw()

    def checkForCollisions(self):
        for i in range(len(self.dots)):
            for j in range(i + 1, len(self.dots)):
                d1 = self.dots[i]; d2 = self.dots[j]
                dx = d2.x - d1.x
                dy = d2.y - d1.y
                dist = math.hypot(dx, dy)
                minDist = d1.r + d2.r

                if dist < minDist:
                    # Normal
                    if dist > 1e-8:
                        nx = dx / dist; ny = dy / dist
                    else:
                        nx, ny = 1.0, 0.0
                        dist = 0.0

                    # Positional correction
                    penetration = minDist - dist
                    inv1 = 1.0 / d1.mass
                    inv2 = 1.0 / d2.mass
                    invSum = inv1 + inv2

                    if penetration > 0:
                        corrMag = self.POS_CORRECT_PERCENT * max(penetration - self.POS_CORRECT_SLOP, 0.0) / max(invSum, 1e-12)
                        corrX = corrMag * nx; corrY = corrMag * ny
                        d1.x -= corrX * inv1; d1.y -= corrY * inv1
                        d2.x += corrX * inv2; d2.y += corrY * inv2

                    # Impulse (only if moving together)
                    vx = d1.dx - d2.dx
                    vy = d1.dy - d2.dy
                    vn = vx * nx + vy * ny
                    if vn < 0:
                        impulse = (-(1 + self.RESTITUTION) * vn) / max(invSum, 1e-12)
                        jx = impulse * nx; jy = impulse * ny
                        d1.dx += jx * inv1; d1.dy += jy * inv1
                        d2.dx -= jx * inv2; d2.dy -= jy * inv2

                        #--Anti-sticking Bias--
                        vn_after = (d1.dx - d2.dx) * nx + (d1.dy - d2.dy) * ny
                        sep = self.SEPARATION_BIAS
                        if vn_after > -sep:
                            biasImpulse = (-sep - vn_after) / max(invSum, 1e-12)
                            bjx = biasImpulse * nx; bjy = biasImpulse * ny
                            d1.dx += bjx * inv1; d1.dy += bjy * inv1
                            d2.dx -= bjx * inv2; d2.dy -= bjy * inv2

                    # Damage & sparks on first contact and if not invulnerable
                    pair = tuple(sorted((id(d1), id(d2))))
                    firstContact = pair not in self.activeContacts
                    self.activeContacts.add(pair)

                    if firstContact and d1.iframes == 0 and d2.iframes == 0:
                        d1.takeDamage(); d2.takeDamage()
                        d1.iframes = self.DAMAGE_COOLDOWN
                        d2.iframes = self.DAMAGE_COOLDOWN

                        cx = (d1.x + d2.x) / 2; cy = (d1.y + d2.y) / 2
                        for _ in range(random.randint(6, 12)):
                            angle = random.uniform(0, 2 * math.pi)
                            speed = random.uniform(2, 5)
                            self.sparks.append(Spark(cx, cy, angle, speed))
                else:
                    # Not colliding this substep → clear active contact
                    pair = tuple(sorted((id(d1), id(d2))))
                    self.activeContacts.discard(pair)

        # Remove destroyed dots after handling all pairs (safe compact)
        self.dots = [d for d in self.dots if d.health > 0]

def main():
    runApp(width=800, height=600)


main()