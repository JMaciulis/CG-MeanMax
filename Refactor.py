import sys
import math


MAP_RADIUS = 6000.0
TANKERS_BY_PLAYER
TANKERS_BY_PLAYER_MIN = 1
TANKERS_BY_PLAYER_MAX = 3

WATERTOWN_RADIUS = 3000.0

TANKER_THRUST = 500
TANKER_EMPTY_MASS = 2.5
TANKER_MASS_BY_WATER = 0.5
TANKER_FRICTION = 0.40
TANKER_RADIUS_BASE = 400.0
TANKER_RADIUS_BY_SIZE = 50.0
TANKER_EMPTY_WATER = 1
TANKER_MIN_SIZE = 4
TANKER_MAX_SIZE = 10
TANKER_MIN_RADIUS = TANKER_RADIUS_BASE + TANKER_RADIUS_BY_SIZE * TANKER_MIN_SIZE
TANKER_MAX_RADIUS = TANKER_RADIUS_BASE + TANKER_RADIUS_BY_SIZE * TANKER_MAX_SIZE
TANKER_SPAWN_RADIUS = 8000.0
TANKER_START_THRUST = 2000

MAX_THRUST = 300
MAX_RAGE = 300
WIN_SCORE = 50

REAPER_MASS = 0.5
REAPER_FRICTION = 0.20
REAPER_SKILL_DURATION = 3
REAPER_SKILL_COST = 30
REAPER_SKILL_ORDER = 0
REAPER_SKILL_RANGE = 2000.0
REAPER_SKILL_RADIUS = 1000.0
REAPER_SKILL_MASS_BONUS = 10.0

DESTROYER_MASS = 1.5
DESTROYER_FRICTION = 0.30
DESTROYER_SKILL_DURATION = 1
DESTROYER_SKILL_COST = 60
DESTROYER_SKILL_ORDER = 2
DESTROYER_SKILL_RANGE = 2000.0
DESTROYER_SKILL_RADIUS = 1000.0
DESTROYER_NITRO_GRENADE_POWER = 1000

DOOF_MASS = 1.0
DOOF_FRICTION = 0.25
DOOF_RAGE_COEF = 1.0 / 100.0
DOOF_SKILL_DURATION = 3
DOOF_SKILL_COST = 30
DOOF_SKILL_ORDER = 1
DOOF_SKILL_RANGE = 2000.0
DOOF_SKILL_RADIUS = 1000.0

LOOTER_RADIUS = 400.0
LOOTER_REAPER = 0
LOOTER_DESTROYER = 1
LOOTER_DOOF = 2

TYPE_TANKER = 3
TYPE_WRECK = 4
TYPE_REAPER_SKILL_EFFECT = 5
TYPE_DOOF_SKILL_EFFECT = 6
TYPE_DESTROYER_SKILL_EFFECT = 7
EPSILON = 0.00001
MIN_IMPULSE = 30.0
IMPULSE_COEFF = 0.5

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, point):
        return math.sqrt((self.x - point.x)*(self.x - point.x) + (self.y - point.y)*(self.y - point.y))
    

    def move(self, x, y):
        self.x = x
        self.y = y 
    
    def move_to(self, point, distance):
        d = self.distance(point)

        if d < EPSILON:
            return
        
        dx = point.x - self.x
        dy = point.y - self.y
        coef = distance/d

        self.x += dx * coef
        self.y += dy * coef

    def is_in_range(self, point, range_btwn):
        return point != self and self.distance(point) <= range_btwn


    def __eq__(self, obj):
        if (self == obj) return True
        if (obj == None) return False
        if self.x != obj.x return False
        if self.y != obj.y return False
        return True


class Unit(Point):
    def __init__(self, inputs):
        super().__init__(int(inputs[5]), int(inputs[6]))
        self.id = int(inputs[0])
        self.type = int(inputs[1])
        self.mass = float(inputs[3])
        self.radius = int(inputs[4])
        self.vx = int(inputs[7])
        self.vy = int(inputs[8])
        self.known = False
        self.friction = 0
    
    def thrust(self, p, power):
        distance = self.distance(p)

        if math.abs(distance) <= EPSILON:
            return
        
        coef = (power/mass)/distance

        self.vx += (p.x - self.x) * coef
        self.vy += (p.y - self.y) * coef

    def get_collision(self, u):
        # Check instant collision
        if (self.distance(u) <= self.radius + u.radius):
            return Collision(0, self, u)

        # Both units are motionless
        if (self.vx == 0.0 and self.vy == 0.0 and u.vx == 0.0 and u.vy == 0.0) :
            return False
        

        # Change referencial
        # Unit u is not at point (0, 0) with a speed vector of (0, 0)
        x2 = self.x - u.x
        y2 = self.y - u.y
        r2 = self.radius + u.radius
        vx2 = self.vx - u.vx
        vy2 = self.vy - u.vy

        # Resolving: sqrt((x + t*vx)^2 + (y + t*vy)^2) = radius <=> t^2*(vx^2 + vy^2) + t*2*(x*vx + y*vy) + x^2 + y^2 - radius^2 = 0
        # at^2 + bt + c = 0
        # a = vx^2 + vy^2
        # b = 2*(x*vx + y*vy)
        # c = x^2 + y^2 - radius^2 

        a = vx2 * vx2 + vy2 * vy2

        if (a <= 0.0):
            return False
        

        b = 2.0 * (x2 * vx2 + y2 * vy2)
        c = x2 * x2 + y2 * y2 - r2 * r2
        delta = b * b - 4.0 * a * c

        if (delta < 0.0) :
            return False

        t = (-b - math.sqrt(delta)) / (2.0 * a)

        if (t <= 0.0) :
            return False

        return Collision(t, self, u)

    # Bounce between 2 units
    def bounce(self, u):
        mcoeff = (self.mass + u.mass) / (self.mass * u.mass)
        nx = self.x - u.x
        ny = self.y - u.y
        nxnysquare = nx * nx + ny * ny
        dvx = vx - u.vx
        dvy = vy - u.vy
        product = (nx * dvx + ny * dvy) / (nxnysquare * mcoeff)
        fx = nx * product
        fy = ny * product
        m1c = 1.0 / self.mass
        m2c = 1.0 / u.mass

        self.vx -= fx * m1c
        self.vy -= fy * m1c
        u.vx += fx * m2c
        u.vy += fy * m2c

        fx = fx * IMPULSE_COEFF
        fy = fy * IMPULSE_COEFF

        #Normalize vector at min or max impulse
        impulse = math.sqrt(fx * fx + fy * fy)
        coeff = 1.0
        if (impulse > EPSILON and impulse < MIN_IMPULSE):
            coeff = MIN_IMPULSE / impulse
        

        fx = fx * coeff
        fy = fy * coeff

        self.vx -= fx * m1c
        self.vy -= fy * m1c
        u.vx += fx * m2c
        u.vy += fy * m2c

        diff = (self.distance(u) - self.radius - u.radius) / 2.0
        if (diff <= 0.0):
            #Unit overlapping. Fix positions.
            self.move_to(u, diff - EPSILON)
            u.move_to(self, diff - EPSILON)
        
class Looter(Unit):

    def __init__(self, inputs):
        super().__init__(inputs)

class Collision():

    def __init__(self, t, a, b):
        self.a = a
        self.b = b
        self.t = t

class Agent():

# game loop
while True:
    
    my_score = int(input())
    enemy_score_1 = int(input())
    enemy_score_2 = int(input())
    my_rage = int(input())
    enemy_rage_1 = int(input())
    enemy_rage_2 = int(input())
    unit_count = int(input())

    for i in range(unit_count):
        inputs = input().split()

    
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(f'{rtarget.x + steering_vector.x} {rtarget.y + steering_vector.y} {300}')
    print(f'{dtarget.x - me.destroyer.vx} {dtarget.y - me.destroyer.vy} 300')
    print(f'{ftarget.x - me.doof.vx} {ftarget.y - me.doof.vy} 300')