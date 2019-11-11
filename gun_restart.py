from random import randrange as rnd, choice
import tkinter as tk
import math
import time



class Ball():
    def __init__(self, x=40, y=450):
        """ Конструктор класса Ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 1
        self.vy = 1
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 30

    def set_coords(self):#merges object Ball to its coords
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
        if (self.x+self.vx<800 and self.y-self.vy<550):
            self.vy-=1
        elif (self.x+self.vx>800 or self.x+self.vx<0):
            self.vx=-self.vx
        elif (self.y-self.vy>550):
            self.vy=-int(0.6*self.vy)
            self.vx=int(0.6*self.vx)
        self.x += self.vx
        self.y -= self.vy
        self.set_coords()
        if (self.vx*self.vx+self.vx*self.vx<10):
            self.live -= 1
        if (self.live <0):
            canv.delete(self.id)
            self.x=0
        
        
    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (obj.x-self.x)*(obj.x-self.x)+(obj.y-self.y)*(obj.y-self.y)<(self.r+obj.r)*(self.r+obj.r):
            return True
        else:
            return False


class Gun():
    def __init__(self): 
        self.fire_power = 10#how big is the bang?
        self.fire_on = 0#is fire on?
        self.angle = 1
        self.id = canv.create_line(20,450,50,420,width=7) 

    def fire_start(self, event):#inits firing
        self.fire_on = 1

    def fire_end(self, event):#ends firing
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball()#first create a ball
        new_ball.r += 5
        self.angle = math.atan((event.y-new_ball.y) / (event.x-new_ball.x))
        new_ball.vx = self.fire_power * math.cos(self.angle)
        new_ball.vy = - self.fire_power * math.sin(self.angle)
        balls += [new_ball]
        self.fire_on = 0
        self.fire_power = 10

    def targetting(self, event=0):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.angle = math.atan((event.y-450) / (event.x-20))
        if self.fire_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.fire_power, 20) * math.cos(self.angle),
                    450 + max(self.fire_power, 20) * math.sin(self.angle)
                    )

    def power_up(self):#if fire's on, the gun is orange and increasing in length, else - black and stationary
        if self.fire_on:
            if self.fire_power < 100:
                self.fire_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class Target():
    def __init__(self): 
        self.points = 0
        self.live = 1
        self.vx=rnd(-10, 10)
        self.vy=rnd(-10, 10)
        self.id = canv.create_oval(0,0,0,0)
        self.id_points = canv.create_text(30,30,text = self.points,font = '28')
        self.new_target()#can we delete that?

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = rnd(600, 780)
        y = self.y = rnd(0, 550)
        r = self.r = rnd(20, 50)
        color = self.color = 'red'
        canv.coords(self.id, x-r, y-r, x+r, y+r)
        canv.itemconfig(self.id, fill=color)
        self.vx=rnd(-10, 10)
        self.vy=rnd(-10, 10)
    
    def move(self):
        self.x=self.x+self.vx
        self.y=self.y+self.vy
        if (self.x+self.vx>800 or self.x+self.vx<500):
            self.vx=-self.vx
        if (self.y+self.vy>550 or self.y+self.vy<0):
            self.vy=-self.vy
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r)

    def hit(self):
        """Попадание шарика в цель."""
        canv.coords(self.id, -10, -10, -10, -10)
        self.x=-10000
        self.points += 1
        canv.itemconfig(self.id_points, text=self.points)

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)
screen = canv.create_text(400, 300, text='', font='28')


bullet = 0
balls = []

def target_all_live():#if at least 1 target is alive, returns 1
    global targets
    u=0
    for t in targets:
        if t.live==1:
            u=1
    return u


def new_game(event=''):
    global screen,  targets, gun, bullet, balls
    gun = Gun()
    bullet = 0
    balls = []
    targets=[Target() for i in range(3)]
    for target in targets:
        target.new_target()
    canv.bind('<Button-1>', gun.fire_start)
    canv.bind('<ButtonRelease-1>', gun.fire_end)
    canv.bind('<Motion>', gun.targetting)

    while target_all_live():
        for target in targets:
            target.move()
        for ball in balls:
            ball.move()
            for target in targets:
                if ball.hittest(target) and target.live:
                    target.live = 0
                    target.hit()
        canv.update()
        time.sleep(0.03)
        gun.targetting()
        gun.power_up()
    print('DEAD')
    canv.delete('all')
    print('DELETED')
    canv.bind('<Button-1>', '')
    canv.bind('<ButtonRelease-1>', '')
    canv.bind('<Motion>', '')
    #canv.itemconfig(screen, text='')
    canv.itemconfig(screen, text='Вы уничтожили цели за ' + str(bullet) + ' выстрелов')
    canv.bind('<Button-1>', new_game)

new_game()
tk.mainloop()
