human_image = 'human.png'
wait_human_image="waithuman.png"
flow_human_image="flowhuman.png"
bg = "bg2.png"
exit_image = "exit.png"
train_image = "train.png"

import pygame
import math
import random
from pygame.locals import *

SCREEN_SIZE = (1024, 720)
SCR_RECT = Rect(0, 0, SCREEN_SIZE[0], 920)
class Vector2(object):
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    @classmethod
    def from_points(cls, P1, P2):
        return cls(P2[0] - P1[0], P2[1] - P1[1])

    def get_magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalized(self):
        magnitude = self.get_magnitude()
        # print(magnitude)
        self.x /= magnitude
        self.y /= magnitude

    def change_x(self):
        return Vector2(-self.x, self.y)

    def change_y(self):
        return Vector2(self.x, -self.y)

    def back_x(self):
        return self.x

    def back_y(self):
        return self.y

    def back_v(self):
        return ((self.x), (self.y))

    def turn(self, dir):
        return Vector2((self.x * math.cos(math.radians(-dir)) - self.y * math.sin(math.radians(-dir))),
                       (self.x * math.sin(math.radians(-dir)) + self.y * math.cos(math.radians(-dir))))

    def __add__(self, rhs):
        return Vector2(self.x + rhs.x, self.y + rhs.y)

    def __sub__(self, rhs):
        return Vector2(self.x - rhs.x, self.y - rhs.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        return Vector2(self.x / scalar, self.y / scalar)
def cul_distance(vector):
    return math.sqrt(math.pow(vector.x,2)+math.pow(vector.y,2))

EXIT = [Vector2(0.0, 285.0), Vector2(974.0, 285.0)]

class Human(pygame.sprite.Sprite):
    def __init__(self, exit, time=0,dis=Vector2(0,0),self_v=1.0, r=15.0, x=1.0, y=1.0, ):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(human_image).convert_alpha()
        self.pos = Vector2(x, y)
        self.self_v = self_v
        self.exit=exit
        self.rect = Rect(self.pos.back_x(), self.pos.back_y(), self.image.get_width(), self.image.get_height())
        self.radius = r
        self.direction = Vector2.from_points(self.pos.back_v(), self.exit)
        self.direction.normalized()

        self.cout = 0
        self.wait_time = 0
        self.switch = False
        self.timecout=time
        self.distancecout=dis


    def redir(self):
        self.direction = Vector2.from_points(self.pos.back_v(), self.exit)
        self.direction.normalized()
        self.cout = 0
        self.wait_time=0
        self.switch = False

    def update(self):
        self.timecout+=1

        if self.switch == True:
            self.cout += 1
        if self.cout > 100:
            self.redir()
        if self.rect.left < 0 or self.rect.right > SCREEN_SIZE[0]:
            self.self_v = -self.self_v
            #self.direction.turn(180)
        if self.rect.top < 0+80 or self.rect.bottom > SCREEN_SIZE[1]-80:
            self.self_v = -self.self_v
            #self.direction.turn(180)
        self.pos += self.direction * self.self_v
        self.distancecout+=self.direction * self.self_v
        self.rect = Rect(self.pos.back_x(), self.pos.back_y(), self.image.get_width(), self.image.get_height())
        #self.rect = self.rect.clamp(SCR_RECT)
        screen.blit(self.image, self.pos.back_v())

class Flow_human(Human):
    def __init__(self, exit, time=0,dis=Vector2(0,0),self_v=1.0, r=15.0, x=1.0, y=1.0, ):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(flow_human_image).convert_alpha()
        self.pos = Vector2(x, y)
        self.self_v = self_v
        self.exit=exit
        self.midpoint = (self.pos.x, 360)
        """
        if self.exit[0]==0.0:
            self.midpoint=(self.pos.x,random.uniform(360,640))
        else:
            self.midpoint = (self.pos.x, random.uniform(80, 360))"""
        self.rect = Rect(self.pos.back_x(), self.pos.back_y(), self.image.get_width(), self.image.get_height())
        self.radius = r
        self.direction = Vector2.from_points(self.pos.back_v(), self.midpoint)
        self.direction.normalized()
        self.timecout=time
        self.distancecout=dis
        self.cout = 0
        self.switch = False

    def redir(self):
        self.direction = Vector2.from_points(self.pos.back_v(), self.midpoint)
        self.direction.normalized()
        self.cout = 0
        self.wait_time=0
        self.switch = False

    def change_mode(self):
        """
        if self.midpoint[1]-20<= self.pos.y and self.pos.y <=20+self.midpoint[1]:
            return True"""
        if self.exit[0] == 0.0:
            if 360-40 <= self.pos.y and self.pos.y <= 360+40:
                return True
        else:
            if 360-100 <= self.pos.y and self.pos.y <= 360+100:
                return True

    def update(self):
        self.timecout+=1
        if self.switch == True:
            self.cout += 1
        if self.cout > 100:
            self.redir()
        if self.rect.left < 0 or self.rect.right > SCREEN_SIZE[0]:
            self.self_v = -self.self_v
            #self.direction.turn(180)
        if self.rect.top < 0+80 or self.rect.bottom > SCREEN_SIZE[1]-80:
            self.self_v = -self.self_v
            #self.direction.turn(180)
        self.pos += self.direction * self.self_v
        self.distancecout+=self.direction * self.self_v
        self.rect = Rect(self.pos.back_x(), self.pos.back_y(), self.image.get_width(), self.image.get_height())
        #self.rect = self.rect.clamp(SCR_RECT)
        screen.blit(self.image, self.pos.back_v())

class Wait_human(Human):
    def __init__(self, exit, xy,v,d,time=0,dis=Vector2(0,0),self_v=0.0,r=20.0 ):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(wait_human_image).convert_alpha()
        self.pos = xy
        self.self_v = self_v
        self.old_v=v
        self.exit = exit
        self.rect = Rect(self.pos.back_x(), self.pos.back_y(), self.image.get_width(), self.image.get_height())
        self.radius = r
        self.direction=d
        self.wait_time = 0
        self.cout = 0
        self.cout2 = 0
        self.switch = False
        self.timecout = time
        self.distancecout = dis

    def change_mode(self,group,group2):
        list= pygame.sprite.spritecollide(self,group,False,collided =pygame.sprite.collide_circle)
        list2=pygame.sprite.spritecollide(self,group2,False,collided =pygame.sprite.collide_circle)
        if len(list)<=1 and len(list2)<2:
            self.cout += 1
        if len(list2)>1:
            self.cout2+=1
            self.self_v=0.7
            self.direction.turn(130)
        if self.cout>100 or self.cout2>200:
            self.cout=0
            self.cout2=0
            return True

    def update(self):
        self.timecout += 1
        if self.rect.left < 0 or self.rect.right > SCREEN_SIZE[0]:
            self.self_v = -self.self_v
        if self.rect.top < 0+80 or self.rect.bottom > SCREEN_SIZE[1]-80:
            self.self_v = -self.self_v

        self.pos += self.direction * self.self_v
        self.distancecout += self.direction * self.self_v
        self.rect = Rect(self.pos.back_x(), self.pos.back_y(), self.image.get_width(), self.image.get_height())
        screen.blit(self.image, self.pos.back_v())


class Exit(Human):
    def __init__(self, xy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(exit_image).convert_alpha()
        self.pos = xy
        self.rect = Rect(self.pos.back_x(), self.pos.back_y(), self.image.get_width(), self.image.get_height())

    def update(self):
        screen.blit(self.image, self.pos.back_v())

class Station(object):
    flow_human = []
    turn_human = []
    wait_human = []

    time_list=[]
    distance_list=[]
    time=0

    enters=[(341,130),(682,130),(341,590),(682,590)]
    turns=[15,30,45,60,75,90]
    def __init__(self):
        self.human = pygame.sprite.Group()
        self.wait_human = pygame.sprite.Group()
        self.flow_human = pygame.sprite.Group()
        self.exits = pygame.sprite.Group()
        self.cout=0
        self.cout2 = 200
        for x in EXIT:
            self.exits.add(Exit(x))

    def coming_train(self):
        if self.cout2 < 150:
            self.cout2 += 1
            screen.blit(train, (self.cout2 * 3, 0))
            screen.blit(train, (684 - self.cout2 * 3, 641))
        elif self.cout2<250:
            self.cout2 += 1
            screen.blit(train, (450, 0))
            screen.blit(train, (684 - 450, 641))
        elif self.cout2<400:
            self.cout2 += 1
            screen.blit(train, (self.cout2 * 3-300, 0))
            screen.blit(train, (684 - self.cout2 * 3+300, 641))
        else:
            self.cout2=0

    def arrival(self,x=341,y=40):
        for a in range(0, random.randint(1,2)):
            self.human.add(Human(EXIT[random.randint(0, 1)].back_v(), self_v=random.uniform(0.6,0.8),x=x-80+a*100, y=y))

    def arrival_flow(self,x=341,y=40):
        for a in range(0, random.randint(1,2)):
            self.flow_human.add(Flow_human(EXIT[random.randint(0, 1)].back_v(), self_v=random.uniform(0.6,0.8),x=x-80+a*100, y=y))


    def check_flow(self):
        human_list = []
        ########生成旅客
        if self.cout < 600:
            self.cout += 1
        else:
            self.cout=0
            for a in self.enters:
                self.arrival_flow(a[0],a[1])
        ###########普通旅客判定
        for a in self.flow_human:
            list = pygame.sprite.spritecollide(a, self.flow_human, False)
            if (len(list) > 1 or len(pygame.sprite.spritecollide(a, self.human, False))>0 or len(pygame.sprite.spritecollide(a, self.wait_human, False))>0):
                for b in list:
                    b.direction = b.direction.turn(self.turns[random.randint(0, 5)])
                a.switch = True

            if (a.change_mode()):
                self.flow_human.remove(a)
                self.human.add(Human(a.exit, x=a.pos.back_x(), y=a.pos.back_y(), self_v=a.self_v, time=a.timecout,dis=a.distancecout))

        for a in self.human:
            list = pygame.sprite.spritecollide(a, self.human, False)
            if (len(list) > 1 or len(pygame.sprite.spritecollide(a, self.flow_human, False))>0 or len(pygame.sprite.spritecollide(a, self.wait_human, False))>0):
                for b in list:
                    b.direction = b.direction.turn(self.turns[random.randint(0, 5)])
                a.switch = True
                a.wait_time+=1

                if (a.wait_time>10):
                    self.human.remove(a)
                    self.wait_human.add(Wait_human(a.exit, a.pos,a.self_v,a.direction,time=a.timecout,dis=a.distancecout))

        ###########等待旅客test
        for a in self.wait_human:
            if a.change_mode(self.human,self.wait_human):
                self.wait_human.remove(a)
                self.human.add(Human(a.exit, x=a.pos.back_x(),y=a.pos.back_y(),self_v=a.old_v,time=a.timecout,dis=a.distancecout))

        human_list+=pygame.sprite.groupcollide(self.human,self.exits,  True,False )
        human_list +=pygame.sprite.groupcollide(self.wait_human, self.exits,  True,False)
        for a in human_list:
            if len(self.time_list)<=10:
                self.time_list.append(a.timecout)
                self.distance_list.append(a.distancecout)
            else:
                self.time_list.pop(0)
                self.distance_list.pop(0)
                self.time_list.append(a.timecout)
                self.distance_list.append(a.distancecout)
    def check(self):
        human_list = []
        ########生成旅客
        if self.cout < 400:
            self.cout += 1
        else:
            self.cout=0
            for a in self.enters:
                self.arrival(a[0],a[1])
        ###########普通旅客判定
        for a in self.human:
            list = pygame.sprite.spritecollide(a, self.human, False)
            if (len(list) > 1 or len(pygame.sprite.spritecollide(a, self.wait_human, False))>0):
                for b in list:
                    b.direction = b.direction.turn(self.turns[random.randint(0, 5)])
                a.switch = True
                a.wait_time+=1

                if (a.wait_time>10):
                    self.human.remove(a)

                    self.wait_human.add(Wait_human(a.exit, a.pos,a.self_v,a.direction,time=a.timecout,dis=a.distancecout))

        ###########等待旅客test
        for a in self.wait_human:
            if a.change_mode(self.human,self.wait_human):
                self.wait_human.remove(a)
                self.human.add(Human(a.exit, x=a.pos.back_x(),y=a.pos.back_y(),self_v=a.old_v,time=a.timecout,dis=a.distancecout))

        human_list+=pygame.sprite.groupcollide(self.human,self.exits,  True,False )
        human_list +=pygame.sprite.groupcollide(self.wait_human, self.exits,  True,False)
        for a in human_list:
            if len(self.time_list)<=10:
                self.time_list.append(a.timecout)
                self.distance_list.append(a.distancecout)
            else:
                self.time_list.pop(0)
                self.distance_list.pop(0)
                self.time_list.append(a.timecout)
                self.distance_list.append(a.distancecout)

    def data_gra(self):
        length_human=len(self.human.sprites())
        length_waithuman=len(self.wait_human.sprites())

        total_dis = Vector2(0, 0)
        for a in self.distance_list:
            total_dis +=a
        ev_time = (sum(self.time_list)) *200/(10*1500)
        if ev_time>200:
            ev_time=200
        ev_dis = cul_distance(total_dis)*200/(10*500)


        self.time += 0.1
        if self.time > 720:
            self.time = 0
        #########柱状图
        pygame.draw.rect(screen, (255, 255, 255),
                         Rect(840, 720, 70, 200))
        pygame.draw.rect(screen, (189,253, 64),Rect(850, 920-ev_time, 30, ev_time))
        pygame.draw.rect(screen, (253, 135, 64),Rect(880, 920 - ev_dis, 30, ev_dis))
        #########曲线
        pygame.draw.rect(screen, (255, 255, 255),
                         Rect(0 + self.time, 720, 20, 200))
        pygame.draw.rect(screen, (0, 255, 0),
                         Rect(0 + self.time, 920 - 5 * (length_waithuman+length_human), 0.1, 7 * (length_waithuman+length_human)))
        pygame.draw.rect(screen, (0, 0, 255),
                         Rect(0 + self.time, 920 - 5 * length_human, 0.1, 7 * length_human))
        pygame.draw.rect(screen, (255, 0, 0),
                         Rect(0 + self.time, 920 - 5 * length_waithuman, 0.1,7 * length_waithuman))

    def show(self,mode):
        self.coming_train()
        if mode==1:
            self.check_flow()
        else:
            self.check()
        self.human.update()
        self.wait_human.update()
        self.flow_human.update()
        self.exits.update()
        self.data_gra()

########main
pygame.init()
screen = pygame.display.set_mode(SCR_RECT.size, 0, 32)
screen.fill((255, 255, 255))

background = pygame.image.load(bg).convert_alpha()
train = pygame.image.load(train_image).convert_alpha()

test=Station()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(background, (0, 0))

    test.show(0)

    pygame.display.update()
