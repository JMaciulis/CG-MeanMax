import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Object():
    
    def __init__(self, input_string):
        inputs = input_string.split()
        self.unit_id = int(inputs[0])
        self.unit_type = int(inputs[1])
        self.player = int(inputs[2])
        self.mass = float(inputs[3])
        self.radius = int(inputs[4])
        self.x = int(inputs[5])
        self.y = int(inputs[6])
        self.vx = int(inputs[7])
        self.vy = int(inputs[8])
        self.extra = int(inputs[9])
        self.extra_2 = int(inputs[10])
    
    def distance(self, point):
        return math.sqrt((self.x - point.x)*(self.x - point.x) + (self.y - point.y)*(self.y - point.y))

class Target(Object):

    def __init__(self, input_string):
        super().__init__(input_string)
        self.owner = None
        self.owner_dist = 0

class Looter(Object):
    def __init__(self, input_string):
        super().__init__(input_string)

    def simulate_movement(self, power, target):
        distance = dist_btw_obj(self, target)

        coef = power/self.mass/ distance
        
        vx = self.vx + (target.x - self.x) * coef
        vy = self.vy  + (target.y - self.y) * coef

        return Point(self.x + vx, self.y + vy)
    
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
        elif obj.unit_type == 1:
            destroyers.append(obj)
        elif obj.unit_type == 3:
            tankers.append(Target(input_string))
        elif obj.unit_type == 4:
            wrecks.append(Target(input_string))

    voronoi_diagram(reapers, wrecks)
    voronoi_diagram(destroyers, tankers)

    rtarget = None
    closest_dist = 0
    for wreck in wrecks:
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

    dist = 100000
    for throtle in range(0, 300, 20):
        p = me.reaper.simulate_movement(throtle, rtarget)
        sim_dist = rtarget.distance(p) 
        if dist > sim_dist:
            print(f'{p.x} {p.y} sim_dist {sim_dist} power {throtle}', file=sys.stderr, flush=True)
            dist = sim_dist
            rspeed = throtle
   
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(f'{rtarget.x} {rtarget.y} {rspeed}')
    print(f'{dtarget.x} {dtarget.y} 300')
    print(f'{ftarget.x} {ftarget.y} 300')
