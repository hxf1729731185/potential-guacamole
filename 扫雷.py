#-*-coding:utf-8-*-
from graphics import*
from random import*
from time import*
from button import*
class item:
    def __init__(self,win,position,x,y,_type=3,number=3,condition=0,flagcondition=0):
        self.p=position
        self.x=self.p.getX()
        self.y=self.p.getY()
        self.t=_type   #1为雷 0为空
        self.n=number  #空地周围雷的个数
        self.c=condition  # 0为未知  1为已点开
        self.coo=[x,y]      # self 在地图上的坐标
        self.flag=Circle(Point(self.x,self.y),0.5)
        self.flag.setFill("red")
        self.flagcon=flagcondition #0为没有插旗 1为已经插旗
        self.back=Rectangle(Point(self.x-0.5,self.y-0.5),Point(self.x+0.5,self.y+0.5))
        self.back.setFill("light pink")
        if self.t !=3:
            self.back.draw(win)
            
    def display(self):
        if self.flagcon==0:
            if self.t!=3 and self.c==0:
                if self.t ==0:
                    self.back.undraw()
                    self.c=1
                    if self.n != 0:
                        Text(self.p,str(self.n)).draw(win)
                    else:
                        for i in around(self):
                            i.display()
                if self.t==1:
                    self.back.setFill("red")
                    self.c=1
def creat_array(win): 
    array = []
    edge=[]
    for i in range(12):
        __item=item(win,Point(0,0),0,0)
        edge.append(__item)
    array.append(edge)
    for i in range(10):
        rol=[item(win,Point(0,0),0,0)]
        for j in range(10):
            mine=item(win,Point(i+1.5,j+7.5),i,j,0,0,0)
            rol.append(mine)
        rol.append(item(win,Point(0,0),0,0))
        array.append(rol)
    array.append(edge)
    return array
def setmine(n):  
    minelist=[]
    while len(minelist)!=n:
        p=Point(randrange(10),randrange(10))
        if p not in minelist:
            minelist.append(p)
    return minelist
def around(_item):  #返回一个格子周围其余八个格子组成的列表
    around=[]
    for k in [-1,0,1]:
        for l in [-1,0,1]:
            around.append(field[_item.coo[0]+k+1][_item.coo[1]+l+1])
    return around
def countmine(_item):   #更新空地上要显示的数字
    n=0
    for i in around(_item):
        if i !=0 and i.t==1:
            n+=1
    _item.n=n
win=GraphWin("Minesweeper",400,600)
win.setCoords(0,0,12,18)
def remove(_item):
    p1=win.getMouse()
    x=int(p1.getX())
    y=int(p1.getY())
    if 1<=x<=11 and 7<=y<=17:
                if field[x][y-6].flagcon==1:
                    field[x][y-6].flag.undraw()
                    field[x][y-6].flagcon=0
    
while 1:
    #draw back and button
    back=Rectangle(Point(0,0),Point(12,18))
    back.setFill("light yellow")
    back.draw(win)
    Text(Point(4,5),"Enter a number(5~25) to start:").draw(win)
    _input=Entry(Point(8,5),5)
    _input.draw(win)
    start=Button(win,Point(10,5),1.5,0.8,"Start")
    start.activate()
    c=Circle(Point(2,4),0.5)
    c.setFill("red")
    c.draw(win)
    _quit=Button(win,Point(8,4),1.5,0.8,"Quit")
    _quit.activate()
    end_game=Button(win,Point(10,4),1.5,0.8,"End")
    end_game.activate()
    flag=Button(win,Point(3.2,4),1,0.8,"Flag")
    remove=Button(win,Point(5,4),1.8,0.8,"Remove")
    for i in range(1,12):
        Line(Point(i,7),Point(i,17)).draw(win)
        Line(Point(1,i+6),Point(11,i+6)).draw(win)
    
    p=win.getMouse()
    if _quit.clicked(p):
            break 
    while (not start.clicked(p) or  _input.getText()==""):
        p=win.getMouse()
    else:
        start.deactivate()
        m=eval(_input.getText())
        if m<=4:
            message=Text(Point(6,9),"It is too easy,please enter \na number bigger than 4")
            message.setFill("red")
            message.setSize(20)
            message.draw(win)
            win.getMouse()
            message.undraw()
            continue
        
        flag.activate()
        remove.activate()
    minelist=setmine(m)
    field=creat_array(win)
    
    for mine in minelist:
        field[mine.getX()+1][mine.getY()+1].t=1
    for i in range(1,11):
            for j in range(1,11):
                _item = field[i][j]
                countmine(_item)

    start.deactivate()
    t1=time.time()
    while 1 :
        p=win.getMouse()
        x=int(p.getX())
        y=int(p.getY())
        if 1<=x<=11 and 7<=y<=17:
            field[x][y-6].display()
            if field[x][y-6].flagcon==0 and field[x][y-6].t==1:
                message=Text(Point(6,9),"YOU FAIL.")
                message.setSize(30)
                message.draw(win)
                win.getMouse()
                message.undraw()
                break
        elif _quit.clicked(p):
            break 
        elif end_game.clicked(p):
            break
        elif flag.clicked(p):
            #c.undraw()
            c1=Circle(Point(2,4),0.3)
            c1.setFill("black")
            c1.draw(win)
            p1=win.getMouse()
           # x=int(p1.getX())
           # y=int(p1.getY())
            while not flag.clicked(p1):
                p1=win.getMouse()
                x=int(p1.getX())
                y=int(p1.getY())
                if 1<=x<=11 and 7<=y<=17:
                    if field[x][y-6].flagcon==0 and field[x][y-6].c != 1:
                        field[x][y-6].flag.draw(win)
                        field[x][y-6].flagcon=1
                if flag.clicked(p1):
                    c1.undraw()
                    break
                if remove.clicked(p1):
                    c1.undraw()
                    remove.deactivate()
                    p1=win.getMouse()
                    x=int(p1.getX())
                    y=int(p1.getY())
                    if 1<=x<=11 and 7<=y<=17:
                        if field[x][y-6].flagcon==1:
                            field[x][y-6].flag.undraw()
                            field[x][y-6].flagcon=0
                    remove.activate()
                    break
                            #c1.undraw()
                            #break
            
            
                
            #c.draw(win)
        
        #if remove.clicked(p):
            #remove()
            """remove.deactivate()
            p1=win.getMouse()
            x=int(p1.getX())
            y=int(p1.getY())
            if 1<=x<=11 and 7<=y<=17:
                if field[x][y-6].flagcon==1:
                    field[x][y-6].flag.undraw()
                    field[x][y-6].flagcon=0"""
            #remove.activate()
        youwin=True
        for i in range(1,11):
            for j in range(1,11):
                _item = field[i][j]
                if _item.t==0 and _item.c==0:
                    youwin=False
        if  youwin:
            t2=time.time()
            for i in range(1,11):
                for j in range(1,11):
                    _item = field[i][j]
                    _item.display()
            message=Text(Point(6,11),"YOU WIN.\ncongratulations\n You use\n%0.3f seconds."%(t2-t1))
            message.setSize(30)
            message.setFill("black")
            message.draw(win)
            win.getMouse()
            message.undraw()
            break
    if _quit.clicked(p):
            break 
win.close()
