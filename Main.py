import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

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

class Target(Object):

    def __init__(self, input_string):
        super().__init__(input_string)
        self.owner = None
        self.owner_dist = 0

class Agent():

    def __init__(self, pid, score, rage):
        self.id = pid
        self.score = score
        self.rage = rage

        self.reaper = None
        self.destroyer = None
        self.doof = None

        self.close_wrecks = []

    def append_car(self, obj):
        if obj.unit_type == 0:
            self.reaper = obj
        elif obj.unit_type == 1:
            self.destroyer = obj
        elif obj.unit_type == 2:
            self.doof = obj

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
            me.append_car(obj)
        elif obj.player == 1:
            enemy1.append_car(obj)
        elif obj.player == 2:
            enemy2.append_car(obj)
        
        
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

    my_wrecks = [x for x in wrecks if x.owner.player == 0]
    rspeed = 300
    if my_wrecks != []:
        my_wrecks = sorted(my_wrecks, key = lambda x: x.owner_dist, reverse = False)
        if my_wrecks[0].owner_dist <= my_wrecks[0].radius:
            rspeed = 0
            rtarget = my_wrecks[0]
        else:
            my_wrecks = sorted(my_wrecks, key = lambda x: x.extra, reverse = True)
            rtarget = my_wrecks[0]
    else:
        rtarget = me.destroyer
    
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
    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    print(f'{rtarget.x} {rtarget.y} {rspeed}')
    print(f'{dtarget.x} {dtarget.y} 300')
    print(f'{ftarget.x} {ftarget.y} 300')
