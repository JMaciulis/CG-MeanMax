import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __mul__(self, other):
        x = self.x * other
        y = self.y * other
        return Point(x, y)
    
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Point(x, y)
    
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Point(x, y)

class Object(Point):
    
    def __init__(self, input_string):
        inputs = input_string.split()
        super().__init__(int(inputs[5]), int(inputs[6]))
        self.unit_id = int(inputs[0])
        self.unit_type = int(inputs[1])
        self.player = int(inputs[2])
        self.mass = float(inputs[3])
        self.radius = int(inputs[4])
        #self.x = int(inputs[5])
        #self.y = int(inputs[6])
        self.vx = int(inputs[7])
        self.vy = int(inputs[8])
        self.extra = int(inputs[9])
        self.extra_2 = int(inputs[10])
    
    def distance(self, point):
        return math.sqrt((self.x - point.x)*(self.x - point.x) + (self.y - point.y)*(self.y - point.y))

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
        # at^2 + bt + c = 0;
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

class Collision():

    def __init__(self, t, a, b):
        self.a = a
        self.b = b
        self.t = t

class Target(Object):

    def __init__(self, input_string):
        super().__init__(input_string)
        self.owner = None
        self.owner_dist = 0

class Looter(Object):
    def __init__(self, input_string):
        super().__init__(input_string)

    def simulate_movement(self, power, target):
        dist = self.distance(Point(target.x - self.vx, target.y - self.vy))

        coef = power/self.mass/ dist
        
        vx = math.floor(self.vx + (target.x - self.vx - self.x) * coef)
        vy = math.floor(self.vy  + (target.y - self.vy - self.y) * coef)

        return Point(vx, vy)
    
    def get_friction(self):
        if self.unit_type == 0:
            return 0.2
        elif self.unit_type == 1:
            return 0.3
        elif self.unit_type == 2:
            return 0.25

class Agent():

    def __init__(self, pid, score, rage):
        self.id = pid
        self.score = score
        self.rage = rage

        self.reaper = None
        self.destroyer = None
        self.doof = None

        self.close_wrecks = []

    def append_looter(self, looter):
        if looter.unit_type == 0:
            self.reaper = looter
        elif looter.unit_type == 1:
            self.destroyer = looter
        elif looter.unit_type == 2:
            self.doof = looter

def dist_btw_obj(obj1, obj2):
    return math.sqrt((obj2.x - obj1.x)**2 + (obj2.y - obj1.y)**2)

def voronoi_diagram(atackers, targets):
    for target in targets:
        for atacker in atackers:
            dist = dist_btw_obj(target, atacker)
            if (target.owner == None) or (dist < target.owner_dist):
                target.owner = atacker
                target.owner_dist = dist

# game loop
while True:
    
    my_score = int(input())
    enemy_score_1 = int(input())
    enemy_score_2 = int(input())
    my_rage = int(input())
    enemy_rage_1 = int(input())
    enemy_rage_2 = int(input())
    unit_count = int(input())
    
    me = Agent(0, my_score, my_rage)
    enemy1 = Agent(1, enemy_score_1, enemy_rage_1)
    enemy2 = Agent(2, enemy_score_2, enemy_rage_2)

    wrecks = []
    tankers = []
    oil_fields = []
    reapers = []
    destroyers = []
    doofs = []
    coliders = []
    for i in range(unit_count):
        input_string = input()
        obj = Object(input_string)
        if obj.player == 0:
            me.append_looter(Looter(input_string))
        elif obj.player == 1:
            enemy1.append_looter(Looter(input_string))
        elif obj.player == 2:
            enemy2.append_looter(Looter(input_string))
        
        
        if obj.unit_type == 0:
            reapers.append(obj)
            coliders.append(obj)
        elif obj.unit_type == 1:
            destroyers.append(obj)
            coliders.append(obj)
        elif obj.unit_type == 3:
            tankers.append(Target(input_string))
            coliders.append(obj)
        elif obj.unit_type == 4:
            wrecks.append(Target(input_string))

    voronoi_diagram(reapers, wrecks)
    voronoi_diagram(destroyers, tankers)

    rtarget = None
    closest_dist = 0
    for wreck in wrecks:
        evaluate = True
        for obstacle in coliders:
            if (obstacle.player != 0) and (obstacle.unit_type != 0):
                if (wreck.distance(obstacle) < wreck.radius): # and (wreck.distance(me.reaper)) > wreck.radius:
                    evaluate = False
                    continue

        if not evaluate:
            continue
            
        distance = wreck.distance(me.reaper)
        if (rtarget == None) or (closest_dist > distance):
            rtarget = wreck
            closest_dist = distance
    
    my_tankers = [x for x in tankers if x.owner.player == 0]
    if my_tankers != []:
        my_tankers = sorted(my_tankers, key = lambda x: x.extra, reverse = True)
        dtarget = my_tankers[0]
    else:
        dtarget = me.destroyer
    
    if enemy1.score > enemy2.score:
        ftarget = enemy1.reaper
    else:
        ftarget = enemy2.reaper
   
    rspeed = 300
    if rtarget == None:
        rtarget = me.destroyer

    max_ahead = 2
    simv = me.reaper.simulate_movement(300, rtarget)
    #print(f'{simv.x} {simv.y}', file=sys.stderr, flush=True)
    ahead = simv*max_ahead
    #print(f'{ahead.x} {ahead.y}', file=sys.stderr, flush=True)
    ahead2 = simv*(max_ahead/2)
    #print(f'{ahead2.x} {ahead2.y}', file=sys.stderr, flush=True)
    obstacles_in_path = []
    avoid_this = None
    old_v = Point(me.reaper.vx, me.reaper.vy)
    me.reaper.vx = simv.x
    me.reaper.vy = simv.y

    for obstacle in coliders:
        if (obstacle.player == 0) and (obstacle.unit_type == 0):
            continue
        
        collision = me.reaper.get_collision(obstacle)
        if collision != False and collision.t <= 1 and (avoid_this == None or collision.t < avoid_this.t):
            avoid_this = collision
    
    print(f'target {rtarget.unit_id} ', file=sys.stderr)
    
    avoidance_force = Point(0,0)
    if avoid_this != None:
        print(f'avoid : {avoid_this.b.unit_id}', file= sys.stderr, flush= True)
        avoidance_force = me.reaper + simv - Point(avoid_this.b.x, avoid_this.b.y)
        MAX_AVOID_FORCE = 4
        avoidance_force = avoidance_force * MAX_AVOID_FORCE

    steering_vector = Point(-old_v.x, -old_v.y)
    if rtarget.radius < closest_dist:
        steering_vector = steering_vector + avoidance_force
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(f'{rtarget.x + steering_vector.x} {rtarget.y + steering_vector.y} {300}')
    print(f'{dtarget.x - me.destroyer.vx} {dtarget.y - me.destroyer.vy} 300')
    print(f'{ftarget.x - me.doof.vx} {ftarget.y - me.doof.vy} 300')
