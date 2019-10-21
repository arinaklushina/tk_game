#часть кода отвечает за передвижение,
#часть - за создание шариков,
# часть - за отражение, за клики и  итд

import tkinter as tk
import random
import sys


WIDTH = 800
HEIGHT = 600

score = 0

results = []

colors = ['yellow', 'red', 'orange']

class Ball:
    def __init__(self):
        #(x,y) - centre
        #creates a ball
        global colors
        self.R = random.randint(20, 50)
        self.x = random.randint(self.R, WIDTH - self.R)
        self.y = random.randint(self.R, HEIGHT - self.R)
        self.dx, self.dy = (+2, +3)
        self.ball_id = canvas.create_oval(self.x - self.R, self.y - self.R,
                                     self.x + self.R, self.y + self.R,
                                     fill=random.choice(colors))
    
    def move(self):
        #moves ball and changes coords
        self.x += self.dx
        self.y += self.dy
        if self.x + self.R > WIDTH and self.dx > 0 or self.x - self.R <= self.R and self.dx < 0:
            self.dx = -self.dx
        if self.y + self.R > HEIGHT and self.dy >0 or self.y - self.R <= self.R and self.dy <0:
            self.dy = -self.dy
            
    def show(self):
        #draws ball and calls movement
        canvas.move(self.ball_id, self.dx, self.dy)
        
    def check_inside(self, event):
        if (event.x - self.x)**2+(event.y - self.y)**2 <= self.R ** 2:
            #score += 1
            return True
        else:
            return False
            
    

def canvas_click_handler(event):
    global  score,  balls
    for ball in balls:
        if ball.check_inside(event):
            score += 1

def show_score():
    global score
    w = tk.Tk()
    w.geometry('200x100')
    sc = tk.Label(w, text='Your score is ' + str(score))
    sc.pack()

def new_player():
    global score

    f = open('results.txt', 'r+')
    f.write(str(score))
    score = 0
    f.close()

def show_table():
    with open('results.txt') as f:
        f_contents = f.readlines()
        print(f_contents)
        i = 1
        for elem in f_contents:
            print('player #', i, ' : ', elem, '\n')
            i+=1

def tick():
    for  ball in balls:
        ball.move()
        ball.show()
        
    root.after(50, tick)

    
    


def main():
    global root, canvas, balls
    
    root = tk.Tk()
    root.geometry(str(WIDTH) + "x" + str(HEIGHT))
    canvas = tk.Canvas(root, width=int(WIDTH), height=int(HEIGHT))
    canvas.pack(anchor="nw", fill=tk.BOTH)
    canvas.bind('<Button-1>', canvas_click_handler)
    root2 = tk.Tk()
    root2.geometry('200x100')
    b = tk.Button(root2, text="show my score!", command=show_score)
    b.pack()
    root3 = tk.Tk()
    root3.geometry('200x100')
    c = tk.Button(root3, text="new player", command=new_player)
    c.pack()

    root4 = tk.Tk()
    root4.geometry('200x100')
    d = tk.Button(root4, text="show scores", command=show_table)
    d.pack()
    
    balls = [Ball() for i in range(7)]
    tick()

    root.mainloop()


if __name__ == "__main__":
    main()
