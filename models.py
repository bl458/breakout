# models.py
# Byungchan Lim bl458
# 12/11/15
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything except the module constants.py.
# If you need extra information from Play, then it should be a parameter in your method, 
# and Play should pass it as a argument when it calls the method.


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A NEW PADDLE
    def __init__(self, x,y,width,height,linecolor,fillcolor):
        """Initializes a Paddle object.
        
        Parameter x: the horizontal coordinate of the object's center
        Precondition: int or float
        
        Parameter y: the vertical coordinate of the object's center
        Precondition: int or float
        
        Parameter width: the horizontal width of this shape 
        Precondition: int or float >0
        
        Parameter height: the vertical width of this shape
        Precondition: int or float >0
        
        Parameter linecolor: the object line color
        Precondition: valid color object 
        
        Parameter fillcolor: the object's fill color
        Precondition: valid color object """
        
        GRectangle.__init__(self,x=x,y=y,width=width,height=height,
                            linecolor=linecolor,fillcolor=fillcolor)
    
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    def movePaddle(self, step):
        """Moves the paddle to the left or right depending on step
        
        Parameter step: the amount of horizontal movement of Paddle
        Precondition: int or float"""
        
        self.x+=step
    
    def collides(self, ball):
        """Returns: True if the ball collides with this paddle
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball
        
        Got specification from Professor White's a7 description"""
        
        if self.contains(ball.x-BALL_DIAMETER/2.0,ball.y-BALL_DIAMETER/2.0):
            return True
        if self.contains(ball.x-BALL_DIAMETER/2.0,ball.y+BALL_DIAMETER/2.0):
            return True
        if self.contains(ball.x+BALL_DIAMETER/2.0,ball.y-BALL_DIAMETER/2.0):
            return True
        if self.contains(ball.x+BALL_DIAMETER/2.0,ball.y+BALL_DIAMETER/2.0):
            return True
        return False
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    

class Brick(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball.  You may wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _brickScore     [int]:
                    how much score go up when this brick is hit
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getBrickScore(self):
        """Return: how much this brick is worth in terms of score"""
        
        return self._brickScore
    
    # INITIALIZER TO CREATE A BRICK
    def __init__(self, x,y,width,height,linecolor,
                 fillcolor,brickScore):
        """Initializes a Brick object.
        
        Parameter x: the horizontal coordinate of the object's center
        Precondition: int or float
        
        Parameter y: the vertical coordinate of the object's center
        Precondition: int or float
        
        Parameter width: the horizontal width of this shape 
        Precondition: int or float >0
        
        Parameter height: the vertical width of this shape
        Precondition: int or float >0
        
        Parameter linecolor: the object line color
        Precondition: valid color object 
        
        Parameter fillcolor: the object's fill color
        Precondition: valid color object
        
        Parameter brickScore: score worth of this brick
        Precondition: int >0"""
        
        GRectangle.__init__(self,x=x,y=y,width=width,height=height,
                            linecolor=linecolor,fillcolor=fillcolor)
        self._brickScore=brickScore
        
    # METHOD TO CHECK FOR COLLISION
    def collides(self, ball):
        """Returns: True if the ball collides with this brick
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball
        
        Got specification from Professor White's a7 description"""
        
        if self.contains(ball.x-BALL_DIAMETER/2.0,ball.y-BALL_DIAMETER/2.0):
            return True
        if self.contains(ball.x-BALL_DIAMETER/2.0,ball.y+BALL_DIAMETER/2.0):
            return True
        if self.contains(ball.x+BALL_DIAMETER/2.0,ball.y-BALL_DIAMETER/2.0):
            return True
        if self.contains(ball.x+BALL_DIAMETER/2.0,ball.y+BALL_DIAMETER/2.0):
            return True
        return False
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVx(self):
        """Returns: Velocity in x direction"""
        
        return self._vx
    
    def getVy(self):
        """Returns: Velocity in y direction"""
        
        return self._vy
    
    def setVx(self, vx):
        """Sets velocity in x direction to vx
        
        Parameter vx: new velocity in x direction
        Precondition: int or float""" 
        
        self._vx=vx
    
    def setVy(self, vy):
        """Sets velocity in y direction to vy
        
        Parameter vy: new velocity in y direction
        Precondition: int or float""" 
        
        self._vy=vy
    
    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self,x,y,width,height,fillcolor):
        """Initializes a Ball object and assigns velocity in x and y directions
        
        Parameter: x: the horizontal coordinate of the object's center
        Precondition: int or float
        
        Parameter: y: the vertical coordinate of the object's center
        Precondition: int or float
        
        Parameter: width: the horizontal width of this shape 
        Precondition: int or float >0
        
        Parameter: width: the vertical width of this shape
        Precondition: int or float >0
        
        Parameter: linecolor: The object line color
        Precondition: valid color object 
        
        Parameter: fillcolor: the object's fill color
        Precondition: valid color object"""
        
        GEllipse.__init__(self,x=x,y=y,width=width,height=height,fillcolor=fillcolor)
        self._vx = BALL_XVELOCITY
        self._vx = self._vx * random.choice([-1, 1])
        self._vy= BALL_YVELOCITY
        
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
    def moveBall(self, xShift, yShift):
        """Moves the ball in x direction by xShift and in y direction by yShift
        
        Parameter xShift: amount of shift in horizontal direction
        Precondition: int or float
        
        Parameter yShift: amount of shift in vertical direction
        Precondition: int or float"""
        
        self.x+=xShift
        self.y+=yShift
    
    def bounceBall(self):
        """Bounces ball when it hits the walls and changes its direction"""
        
        if self.getVy()>=0:
            if self.top>=GAME_HEIGHT:
                self._vy=-1*self._vy
        
        if self.getVx()>=0:
            if self.left>=GAME_WIDTH:
                self._vx=-1*self._vx
        else:
            if self.right<=0:
                self._vx=-1*self._vx
        
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE

