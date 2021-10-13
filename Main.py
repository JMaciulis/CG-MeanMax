import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Point():
    def __init__(self, x, y):
        self.x = x 
        self.y = y

    def distance2(self, point):
        return (self.x - point.x)*(self.x - point.x) + (self.y - point.y)*(self.y - point.y)

    def distance(self, point):
        return math.sqrt(self.distance2(point))    

class Unit(Point):
    def __init__(self, unit_id, unit_type, player, mass, radius):
        super(Unit, self).__init__(x, y)
        self.unit_id = unit_id
        self.unit_type = unit_type
        self.player = player
        self.mass = mass
        self.radius = radius
        self.vx = 0
        self.vy = 0
        self.extra = 0
        self.extra_2 = 0
        self.score = 0

    def update(self, x, y, vx, vy, extra, extra_2):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.extra = extra
        self.extra_2 = extra_2
    
def sort_tankers(tankers, my_unit):
    for t in tankers:
        if t.extra == 0:
            t.score = -1
        else:
            t.score = (1-t.distance(my_unit)/12000)
            t.score += t.extra * 0.1
    tankers.sort(key=lambda x: x.score, reverse=True) 
    return tankers
    
def sort_wrecks(wrecks, me, enemy1, enemy2, pools):
    reaper = me[0]
    destroyer = me[1]
    enemy1_reaper = enemy1[0]
    enemy2_reaper = enemy2[0]

    enemy_reaper_distance_coeff = 0.3

    for w in wrecks:
        w.score = 2*score_by_distance(w,reaper)
        w.score -= score_by_distance(w, enemy1_reaper)*enemy_reaper_distance_coeff
        w.score -= score_by_distance(w, enemy2_reaper)*enemy_reaper_distance_coeff
        w.score += w.extra*0.05
        w.score += score_by_distance(w, destroyer)*0.25
        #todo add tar pool effect on score
    wrecks.sort(key=lambda x: x.score, reverse=True)  
    return wrecks

def score_by_distance(wreck, point):
    return  (1-wreck.distance(point)/12000)

def sort_wrecks_by_dist(wrecks, unit):
    for w in wrecks:
       w.score = w.distance(unit)
       
    wrecks.sort(key=lambda x : x.score, reverse=False)
    return wrecks
    
       
# game loop
while True:
    my_units = []
    enemy1_units = []
    enemy2_units = []
    wrecks = []
    tankers = []
    tar_pools = []

    my_score = int(input())
    enemy_score_1 = int(input())
    enemy_score_2 = int(input())
    my_rage = int(input())
    enemy_rage_1 = int(input())
    enemy_rage_2 = int(input())
    unit_count = int(input())
    for i in range(unit_count):
        unit_id, unit_type, player, mass, radius, x, y, vx, vy, extra, extra_2 = input().split()
        unit_id = int(unit_id)
        unit_type = int(unit_type)
        player = int(player)
        mass = float(mass)
        radius = int(radius)
        x = int(x)
        y = int(y)
        vx = int(vx)
        vy = int(vy)
        extra = int(extra)
        extra_2 = int(extra_2)

        unit = Unit(unit_id, unit_type, player, mass, radius)
        unit.update(x, y, vx, vy, extra, extra_2)
 
        if player == 0:
            my_units.append(unit)
        elif player == 1:
            enemy1_units.append(unit)
        elif player == 2:
            enemy2_units.append(unit)
        else:
            if unit_type == 4:
                wrecks.append(unit)
            elif unit_type == 3:
                tankers.append(unit)
            elif unit_type == 5:
                tar_pools.append(unit)

    my_units.sort(key=lambda x: x.unit_id, reverse=False)
    enemy1_units.sort(key=lambda x: x.unit_id, reverse=False)
    enemy2_units.sort(key=lambda x: x.unit_id, reverse=False)

    reaper = my_units[0]
    destr = my_units[1]
    doof = my_units[2]

    reaper_target = None
    tanker_target = None
    doof_target = None

    if wrecks == []:
        reaper_target = my_units[1]
        reaper_msg = 'DESTR'
    else:
        wrecks = sort_wrecks(wrecks, my_units, enemy1_units, enemy2_units, tar_pools)
        reaper_target = wrecks[0]
        reaper_msg = reaper_target.score
    
    if tankers == []:
        tanker_target = Point(0,0)
        tanker_msg = 'NO TARGET'
    else:
        tankers = sort_tankers(tankers, destr)
        tanker_target = tankers[0]
        tanker_msg = tanker_target.extra
        
    if enemy_score_1 >= enemy_score_2:
        main_enemy = enemy1_units[0]
        wrecks = sort_wrecks_by_dist(wrecks, main_enemy)
        if wrecks != [] :
            doof_target = wrecks[0]
        else:
            doof_target = main_enemy
        doof_msg = 'ONE'
    else:
        main_enemy = enemy1_units[0]
        wrecks = sort_wrecks_by_dist(wrecks, main_enemy)
        doof_target = wrecks[0]
        doof_msg = 'TWO'

        
    print(reaper_target.x - reaper.vx, reaper_target.y - reaper.vy, 300, reaper_msg)
    if my_rage >= 60 and int(destr.distance(Point(doof_target.x - doof_target.vx, doof_target.y - doof_target.vy))) <= 2000:
        print('SKILL', main_enemy.x-main_enemy.vx, main_enemy.y-main_enemy.vy)
        my_rage -= 60
    else:
        print(tanker_target.x - destr.vx, tanker_target.y - destr.vy, 300, tanker_msg)
      
    if my_rage >= 30 and doof_target.extra > 3 and doof.distance(doof_target) <= 2*doof_target.radius and doof.distance(main_enemy) < 3*doof_target.radius:
        print('SKILL', doof_target.x, doof_target.y)
    else:
        print(doof_target.x - doof.vx, doof_target.y - doof.vy, 300, doof_msg)
