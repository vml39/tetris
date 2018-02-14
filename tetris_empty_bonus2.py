#tetris_empty.py

# Name: Katherine & Vivian 
# Collaborators:

# import modules
from random import *
from graphics import *
from time import *

class Block(Rectangle):
     BLOCK_SIZE=30 #class variables
     OUTLINE_WIDTH=3
     def __init__(self, pt, color):
        self.i=pt.getX()
        self.j=pt.getY()
        self.color=color
        self.update_coords()
     def update_coords(self): #update the x and y coordinates and rectangle object
        self.point1=Point(Block.BLOCK_SIZE*self.i,Block.BLOCK_SIZE*self.j)
        self.point2=Point(Block.BLOCK_SIZE*(self.i+1),Block.BLOCK_SIZE*(self.j+1))
        self.s=Rectangle(self.point1,self.point2) #creates an object "s", a Rectangle
     def draw(self,GraphWin):
        self.window=GraphWin
        self.s.draw(GraphWin)
        self.s.setFill(self.color)
        self.s.setOutline("black")
        self.s.setWidth(Block.OUTLINE_WIDTH)
     def move(self,dx,dy):
        self.i=self.i+dx
        self.j=self.j+dy
        self.s.undraw()
        self.update_coords()
        self.draw(self.window)
     def can_move(self,board,dx,dy): #???
          if 0<=self.i+dx<=9 and 0<=self.j+dy<=19:
               return True
          else:
               return False
    
class Shape(object):
     def __init__(self,coords,color):
        self.block0=Block(coords[0],color)
        self.block1=Block(coords[1],color)
        self.block2=Block(coords[2],color)
        self.block3=Block(coords[3],color)
        self.blocks=[self.block0,self.block1,self.block2,self.block3]
        self.rotation_dir=1
        shift_rotation_dir=False
     def move(self,dx,dy):
        for block in self.blocks:
            block.move(dx,dy)
     def draw(self,win):
        for block in self.blocks:
            block.draw(win)
     def get_blocks(self):
          return self.blocks
     def can_move(self,board,dx,dy):
          no_match = 0
          trues=0
          for block in self.blocks:
               i,j = block.i + dx,block.j + dy
               if board.can_move(i,j)==True:
                    no_match += 1
               status=block.can_move(board,dx,dy)
               if status==True:
                    trues+=1
          if trues==4 and no_match==4:
               return True
          else:
               return False
     def can_rotate(self,wtptetris): #parameter is board 
          centerx = wtptetris.current_shape.center_block.i
          centery = wtptetris.current_shape.center_block.j
          block_ok = 0
          if self.shift_rotation_dir == False:
               return False
          for block in self.blocks:
               block.x,block.y = block.i,block.j
               bdir = self.rotation_dir
               x = centerx + bdir*centery - bdir*block.y
               y = centery - bdir*centerx + bdir*block.x
               if block.can_move(wtptetris.board,x-block.i,y-block.j)==True and (x,y) not in wtptetris.board.grid:
                    block_ok+=1
          if block_ok == 4:
               return True
          else:
               return False 
     def rotate(self,board):
          # first change rotation_dir, then rotate according to that
          pass
class I_shape(Shape):
     def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x + 2, center.y)]
        Shape.__init__(self, coords, "red")
        self.center_block=self.blocks[1]
        self.rotation_dir = -1
        self.shift_rotation_dir=True
        self.t = 'i'
class J_shape(Shape):
     def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x + 1, center.y+1)]
        Shape.__init__(self, coords, "orange")
        self.center_block=self.blocks[1]
        self.rotation_dir = 1
        self.shift_rotation_dir=True
        self.t = 'j'
class L_shape(Shape):
     def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x -1, center.y+1)]
        Shape.__init__(self, coords, "yellow")
        self.center_block=self.blocks[1]
        self.rotation_dir = 1
        self.shift_rotation_dir=True
        self.t = 'l'
class O_shape(Shape):
     def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x , center.y),
                  Point(center.x - 1, center.y+1),
                  Point(center.x, center.y+1)]
        Shape.__init__(self, coords, "lime green")
        self.center_block=self.blocks[1]
        self.shift_rotation_dir=False
        self.t = 'o'
class S_shape(Shape):
     def __init__(self, center):
        coords = [Point(center.x - 1, center.y+1),
                  Point(center.x , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x, center.y+1)]
        Shape.__init__(self, coords, "dodger blue")
        self.center_block=self.blocks[1]
        self.rotation_dir = 1
        self.shift_rotation_dir=True
        self.t = 's'
class T_shape(Shape):
     def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x, center.y+1)]
        Shape.__init__(self, coords, "medium orchid")
        self.center_block=self.blocks[1]
        self.rotation_dir = 1
        self.shift_rotation_dir=True
        self.t = 't'
class Z_shape(Shape):
     def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x , center.y),
                  Point(center.x + 1, center.y+1),
                  Point(center.x, center.y+1)]
        Shape.__init__(self, coords, "hot pink")
        self.center_block=self.blocks[1]
        self.rotation_dir = 1
        self.shift_rotation_dir=True
        self.t = 'z'
class ScoreBoard(object):
     def __init__(self,win,width,height):
          self.width=width
          self.height=height
          #create a canvas
          self.canvas=CanvasFrame(win,self.width*Block.BLOCK_SIZE,self.height*Block.BLOCK_SIZE)
          self.canvas.setBackground("azure")
          # create score
          self.score=0
          self.draw_score()
          # create level
          self.level=int(self.score)/int(150)+1
          self.draw_level()
          #create next shape
          #self.draw_next_shape(WTPtetris.game)
     def draw_score(self):
          sqw = self.width*Block.BLOCK_SIZE
          sqh = self.height*Block.BLOCK_SIZE
          self.sc=Text(Point(4*sqw/5,sqh/4),"Score:")
          self.sc.draw(self.canvas)
          self.sc.setSize(15)
          self.sc.setStyle('bold')
          self.sc.setTextColor('black')
          self.sc.setFace('helvetica')
          self.scor=Text(Point(4*sqw/5,sqh/2),self.score)
          self.scor.draw(self.canvas)
          self.scor.setSize(15)
          self.scor.setTextColor('black')
          self.scor.setFace('helvetica')
     def draw_level(self):
          sqw = self.width*Block.BLOCK_SIZE
          sqh = self.height*Block.BLOCK_SIZE
          self.l=Text(Point(sqw/2,sqh/4),"Level:")
          self.l.draw(self.canvas)
          self.l.setSize(15)
          self.l.setStyle('bold')
          self.l.setTextColor('black')
          self.l.setFace('helvetica')
          self.lev=Text(Point(sqw/2,sqh/2),self.level)
          self.lev.draw(self.canvas)
          self.lev.setSize(15)
          self.lev.setTextColor('black')
          self.lev.setFace('helvetica')
     def update_score(self):
          self.scor.undraw()
          self.draw_score()
     def update_level(self):
          self.lev.undraw()
          self.level=int(self.score)/int(150)+1
          self.draw_level()
##     def draw_next_shape(self,wtptetris):
##          #self.game=wtptetris
##          sqw = self.width*Block.BLOCK_SIZE
##          sqh = self.height*Block.BLOCK_SIZE
##          self.n=Text(Point(sqw/5,sqh/4),"Next Shape:")
##          self.n.draw(self.canvas)
##          self.n.setSize(15)
##          self.n.setStyle('bold')
##          self.n.setTextColor('black')
##          self.n.setFace('helvetica')
##          self.next=wtptetris.next_shape
##          self.next.draw(self.canvas)
##     def update_next_shape(self,wtptetris):
##          self.draw_next_shape(wtptetris)
##          self.next.undraw(self.canvas)
##          self.draw_next_shape(wtptetris)
     
class Board(object):
     def __init__(self, win, width, height):
          self.width=width
          self.height=height
          #create a canvas to draw shapes on
          self.canvas=CanvasFrame(win,self.width*Block.BLOCK_SIZE,self.height*Block.BLOCK_SIZE)
          self.canvas.setBackground("deep sky blue")
          #create an empty dictionary
          self.grid={}
          self.draw_grid_lines(self.canvas)
     def draw_grid_lines(self, win):
          sqw = self.width*Block.BLOCK_SIZE/10
          sqh = self.height*Block.BLOCK_SIZE/20
          lnw=2
          lncol="white smoke"
          for a in range(0,11):
               l=Line(Point(sqw,0),Point(sqw,self.height*Block.BLOCK_SIZE))
               l.draw(win)
               l.setFill(lncol)
               l.setWidth(lnw)
               sqw += Block.BLOCK_SIZE
          for b in range(0,21):
               l=Line(Point(0,sqh),Point(self.width*Block.BLOCK_SIZE,sqh))
               l.draw(win)
               l.setFill(lncol)
               l.setWidth(lnw)
               sqh += Block.BLOCK_SIZE
          pass
     def draw_shape(self,shape):
          x = shape.center_block.i
          y = shape.center_block.j
          if shape.can_move(self,0,0)==True:
               shape.draw(self.canvas)
               return True
          else:
               return False
          # use can move or get blocks
        # run boundaries function to determine whether a block has reached the
        # "bottom" (or another block)
        # if so, find the coordinates of the shape's blocks and change list so
        # the coordinates are occupied
        # stop shape movement
     def can_move(self,x,y): #useless 
          if (x,y) in self.grid:
               return False
          else:
               return True
     def add_shape_dict(self,shape):
          for block in shape.get_blocks():
               x,y=block.i,block.j
               self.grid[(x,y)]=block
     def delete_row(self,y): 
          for x in range(0,10):
               self.grid[(x,y)].s.undraw() #undrawing too many. check function
               del self.grid[(x,y)]
     def is_row_complete(self,y): #checked!
          cnt=0
          for x in range(0,10):
               if (x,y) in self.grid:
                    cnt+=1
          if cnt==10:
               return True
          self.cntdraw=True
          return False
     def move_down_rows(self,y_start): #physically moves blocks above it. phantom blocks
          keys=self.grid.keys()
          for y in range(y_start,-1,-1):
               for x in range(0,10):
                    if (x,y) in keys:
                         self.grid[(x,y)].move(0,1)
                         self.grid[(x,y+1)]=self.grid[(x,y)]
                         del self.grid[(x,y)]
                         self.grid[(x,y+1)].i=x
                         self.grid[(x,y+1)].j=y+1
     def remove_complete_rows(self): # last step
          rows_removed=0
          for y in range (20):
               if self.is_row_complete(y)==True:
                    self.delete_row(y)
                    self.move_down_rows(y-1)
                    rows_removed+=1
          game.sb.score+=(50*rows_removed)
          if rows_removed%4==0:
               game.sb.score+=75*(rows_removed/4)
          game.sb.update_score()
          game.sb.update_level()
     def game_over(self):
          sqw = self.width*Block.BLOCK_SIZE
          sqh = self.height*Block.BLOCK_SIZE
          go=Text(Point(sqw/2,sqh/2),"Game Over")
          go.draw(self.canvas)
          go.setSize(30)
          go.setStyle('bold italic')
          go.setTextColor('white')
          go.setFace('helvetica')
          game.win.bind_all("<Key>",game.key_pressed_over)

class WTPTetris(object):
     SHAPES=[I_shape,J_shape,L_shape,O_shape,S_shape,T_shape,Z_shape]
     DIRECTION={"Left":(-1,0),"Right":(1,0),"Down":(0,1)}
     BOARD_WIDTH=10
     BOARD_HEIGHT=20
     def __init__(self, win):
          self.board=Board(win,self.BOARD_WIDTH,self.BOARD_HEIGHT)
          self.sb=ScoreBoard(win,self.BOARD_WIDTH,self.BOARD_HEIGHT/4)
          self.n=PiecePreview(self)
          self.win=win
          self.delay=1000 #ms
          #sets up keyboard events. Key pressed-->method key_pressed is called
          self.win.bind_all("<Key>", self.key_pressed)
          #set current c=shape to random new shape
##          self.next_shape=self.create_new_shape()
          self.current_shape=self.create_new_shape()
          self.next=self.n.next
          #our code
          #draw current_shape on board(board methods)
          self.board.draw_shape(self.current_shape)
          #animate shape
          self.animate_shape()
     def animate_shape (self):
          if self.current_shape.can_move(self.board,0,1)==True:
               self.update_speed()
               self.win.after(self.delay,self.animate_shape)
               self.do_move((0,1))
          elif self.current_shape.can_move(self.board,0,1)==False:
               # not useless, do not delete- when it just falls down by itself.
               self.key="Down"
               self.board.add_shape_dict(self.current_shape)
               #update scoreboard
               self.sb.score+=20
               self.sb.update_score()
               self.sb.update_level()
               #remove rows
               self.board.remove_complete_rows()
               #create new shapes
               self.current_shape=self.create_new_shape()
               self.board.draw_shape(self.current_shape)
               #update shapes
##               self.sb.update_next_shape(self)
               if self.current_shape.can_move(self.board,0,1)==True:
                    self.animate_shape()
##               if self.board.cntdraw==True:
##                    
               else:
                    #print "animating"
                    self.board.game_over()
                    #self.animate_shape() useless?
          

     def create_new_shape(self):
          r=randint(0,6)
          r_s=WTPTetris.SHAPES[r](Point(5,0))
          return r_s
     def do_move(self,direction):#physically moves
          x,y=direction 
          if self.current_shape.can_move(self.board,x,y)==True:
               self.current_shape.move(x,y)
          elif self.key=="Down":
               self.board.add_shape_dict(self.current_shape)
               #print self.board.grid
               #update scoreboard
               self.sb.score+=20
               self.sb.update_score()
               self.sb.update_level()
               #remove rows
               self.board.remove_complete_rows()
               #create new shapes
               self.current_shape=self.create_new_shape()
               self.board.draw_shape(self.current_shape)
               #update shapes
##               self.sb.update_next_shape(self)
     def update_speed(self):
          self.delay=1000/(self.sb.level)
     def do_rotate(self):
          if self.current_shape.can_rotate(self)== True:
               centerx = self.current_shape.center_block.i
               centery = self.current_shape.center_block.j
               for block in self.current_shape.blocks:
                    pbj=block.j
                    pbi=block.i
                    bdir = self.current_shape.rotation_dir
                    block.i = centerx + bdir*centery - bdir*pbj
                    block.j = centery - bdir*centerx + bdir*pbi
                    block.s.undraw()
                    block.update_coords()
                    block.draw(self.board.canvas)
               if self.current_shape.t == 's' and self.current_shape.rotation_dir == -1:
                    self.current_shape.rotation_dir = 1
               elif self.current_shape.t == 's' and self.current_shape.rotation_dir == 1:
                    self.current_shape.rotation_dir = -1
               elif self.current_shape.t == 'z' and self.current_shape.rotation_dir == -1:
                    self.current_shape.rotation_dir = 1
               elif self.current_shape.t == 'z' and self.current_shape.rotation_dir == 1:
                    self.current_shape.rotation_dir = -1
               elif self.current_shape.t == 'i' and self.current_shape.rotation_dir == -1:
                    self.current_shape.rotation_dir = 1
               elif self.current_shape.t == 'i' and self.current_shape.rotation_dir == 1:
                    self.current_shape.rotation_dir = -1                

     def key_pressed_over(self,event):
          pass

     def key_pressed(self,event):
          self.key=event.keysym
          if self.key=="space":
               while self.current_shape.can_move(self.board,0,1):
                    self.do_move((0,1))
               self.key="Down"
               self.do_move((0,1)) # this is important to starting at the top!
          elif self.key=="Up":
               self.do_rotate()
          else:
               d=WTPTetris.DIRECTION[self.key]
               self.do_move(d)
##               if self.current_shape.can_move(self.board,0,1)==False:
##                    self.board.add_shape_dict(self.current_shape)
##                    self.current_shape=self.create_new_shape()
##                    self.board.draw_shape(self.current_shape)
##                    print "this section is not useless!!!"

class PiecePreview(object):
     def __init__(self,wtptetris):
          self.next=wtptetris.create_new_shape()
     def draw_next_shape(self,wtptetris):
          #self.game=wtptetris
          sqw = self.width*Block.BLOCK_SIZE
          sqh = self.height*Block.BLOCK_SIZE
          self.n=Text(Point(sqw/5,sqh/4),"Next Shape:")
          self.n.draw(self.canvas)
          self.n.setSize(15)
          self.n.setStyle('bold')
          self.n.setTextColor('black')
          self.n.setFace('helvetica')
          self.next.draw(self.canvas)
##     def draw(self, canvasframe,x,y):
##          self.Rectangle.draw(Point(x,y),Point
     def update_next_shape(self,wtptetris):
          self.next.undraw(self.canvas)                             
          self.next=wtptetris.create_new_shape()
          self.draw_next_shape(wtptetris)
     def return_old(self,wtptetris):
          prev=self.next
          return prev 
     

               
# keep at end!
win=Window("WTP Tetris")
game=WTPTetris(win)
win.mainloop()
