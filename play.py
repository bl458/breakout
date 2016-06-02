# play.py
# Byungchan Lim bl458
# 12/11/15
# From professor's arrows.py, function updatePaddle was used
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _score          [int]:
                    Measures the score that goes up from destroying bricks
    _scoreMultiple  [int]:
                    Multiply this to how much each brick is worth to get how much score
                    would go up after each brick gets destroyed. Depends on how faster ball
                    became. Since ball gets faster each time it hits the paddle, the attribute
                    is equal to how many times the ball hit the paddle
    _soundDetermin  [int]:
                    Determines the sound of the ball hitting the brick
    _level          [int]:
                    Current level of the game
    """
    
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getLevel(self):
        """Return: current level of the game""" 
        
        return self._level
    
    def getTries(self):
        """Return: number of tries left"""
        
        return self._tries
    
    def getBricks(self):
        """Return: the list of bricks still remaining""" 
        
        return self._bricks
    
    def getScore(self):
        """Return: the score in the game so far"""
        
        return self._score
       
    def setScoreMultiple(self, value):
        """Sets score to a new value
        
        Parameter value: new scoreMultiple
        Precondition: int>=0"""
        
        assert type(value)==int and value>=0
        
        self._scoreMultiple=value
    
    def decreaseScore(self, value):
        """Decrease the score by value
        
        Parameter value: how much the score decreases by
        Precondition: int >0"""
        
        assert type(value)==int and value>0
        
        self._score-=value
        self._score=max(0,self._score)
    
    def levelUp(self):
        """Increases the level by one""" 
        
        self._level+=1
        
    def setLevel(self, value):
        """Sets level to value
        
        Parameter value: new level
        Precondition: int larger than 0 and smaller than equal to 4"""
        
        self._level=value
    
    def setTries(self, value):
        """Sets tries to value
        
        Parameter value: new tries
        Precondition: int larger than or equal to 0 and smaller than equal to 3"""
        
        self._tries=value
    
    def setScore(self, value):
        """Sets level to value
        
        Parameter value: new level
        Precondition: int larger than 0"""
        
        self._score=value
    

    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """Initializes a single game.
        
        Initializes paddle, bricks, ball, tries, score, scoreMultiple, and soundDeterminant"""
        
        self._bricks=[]
        
        for r in range(BRICK_ROWS):
            for c in range(BRICKS_IN_ROW):
                x=BRICK_SEP_H/2.0 + BRICK_SEP_H*c + BRICK_WIDTH/2.0 + BRICK_WIDTH*c
                y=GAME_HEIGHT - BRICK_Y_OFFSET - BRICK_HEIGHT/2.0 - BRICK_SEP_V*r - BRICK_HEIGHT*r
                color=self._determineBrickColor(r)
                self._bricks.append(Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT,
                                          color, color,BRICK_ROWS-r))    
    
        self._paddle=Paddle(GAME_WIDTH/2.0, PADDLE_OFFSET, PADDLE_WIDTH,
                            PADDLE_HEIGHT,colormodel.BLACK,colormodel.BLACK)
        
        self._ball=None
        
        self._reset=True
        
        self._score=0
        
        self._tries=3
        
        self._level=1
        
        self._scoreMultiple=0
        
        self._soundDetermin=1
        
        self._reset=False

    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def updatePaddle(self,input1):
        """Updates the paddle location after keyboard input
        
        Parameter input1: keyboard input
        Precondition: valid key input
        
        Used Professor White's code from arrows.py"""
        
        if input1.is_key_down('left'):
            self._paddle.movePaddle(-1*PADDLE_ANIMATION_STEP)
        if input1.is_key_down('right'):
            self._paddle.movePaddle(PADDLE_ANIMATION_STEP)
        
        self._paddle.x=min(self._paddle.x, GAME_WIDTH-PADDLE_WIDTH/2.0)
        self._paddle.x=max(self._paddle.x, PADDLE_WIDTH/2.0)
    
    def serveBall(self):
        """Creates a Ball object and serves it
        
        The speed depends on the level you are in."""
        
        self._ball=Ball(x=GAME_WIDTH/2.0, y=GAME_HEIGHT/2.0, width=BALL_DIAMETER/2.0,
                        height=BALL_DIAMETER/2.0, fillcolor=colormodel.RED)
        if self._level==2:
            self._ball.setVx(BALL_XVELOCITY*2)
        if self._level==3:
            self._ball.setVx(BALL_XVELOCITY*4)
        if self._level==4:
            self._ball.setVx(BALL_XVELOCITY*6)
        
    def updateBall(self):
        """Updates ball's position whenever update() is called in Breakout.
        
        In other words, this moves the ball based on random velocity in x and y direction.
        The method also makes the ball bounce off the boundaries of the view, paddle, and bricks
        after collision. When ball collides with the bottom, player's number of tries go down."""
        
        self._ball.moveBall(self._ball.getVx(),self._ball.getVy())
        
        self._ball.bounceBall()
        
        self._determineCollisionPaddle()
        
        self._determineCollisionBricks()
                    
        if self._ball.bottom<=0:
            self._tries-=1
              
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def drawBricks(self,view):
        """Draws the bricks to the view
        
        Parameter view: view to draw on
        Precondition: instance of GView"""
        
        for b in self._bricks:
            b.draw(view)
    
    def drawPaddle(self,view):
        """Draws the paddles to the view
        
        Parameter view: view to draw on
        Precondition: instance of GView"""
        
        self._paddle.draw(view)
        
    def drawBall(self, view):
        """Draws the ball to the view
        
        Parameter view: view to draw on
        Precondition: instance of GView"""
        
        self._ball.draw(view)
    
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def _determineCollisionPaddle(self):
        """Determines if ball collided with any of the bricks and if it did,
        executes necessary operations.
        
        If ball did collide, function modifies velocity of the ball, adds sound effect, and
        updates scoreMultiple. Velocity in x direction gets faster each time ball hits the paddle.
        Velocity in y direction changes to itself multiplied by -1.
        The soundDeterminant also resets to 0"""
        
        if self._paddle.collides(self._ball):
            self._soundDetermin=1
            self._scoreMultiple+=1
            if self._ball.getVy()<0:
                soundEffect=Sound('bounce.wav')
                self._ball.setVy(self._ball.getVy()*-1)
                self._ball.setVx(self._ball.getVx()*XVELOCITY_UP_CONSTANT)
                soundEffect.play()
               
    def _determineCollisionBricks(self):
        """Determines if ball collided with any of the bricks and if it did,
        executes necessary operations.
        
        If ball did collide, function erases the bricks, changes ball velocity,
        increases score, and adds sound effect. Velocity in y direction changes
        to itself multiplied by -1. """
        
        brickToBeRemoved=[]
        for brick in self._bricks:
            if brick.collides(self._ball):
                soundEffect=Sound(self._determineSound(self._soundDetermin))
                soundEffect.play()
                self._ball.setVy(self._ball.getVy()*-1)
                self._updateScore(brick)
                brickToBeRemoved.append(brick)
                self._soundDetermin+=1
        
        for brick in brickToBeRemoved:
            self._bricks.remove(brick)
                    
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
    def _determineBrickColor(self, r):
        """Determines the brick color for different rows
        
        Parameter r: the row number of a brick
        Precondition: int>=0"""
        assert type(r)==int and r>=0
        
        if r%10==0 or r%10==1:
            return colormodel.RED
        if r%10==2 or r%10==3:
            return colormodel.ORANGE
        if r%10==4 or r%10==5:
            return colormodel.YELLOW
        if r%10==6 or r%10==7:
            return colormodel.GREEN
        if r%10==8 or r%10==9:
            return colormodel.CYAN
    
    def _updateScore(self, brick):
        """Updates score based on current speed of ball and the
        brick's score worth
        
        The points increase by  for each brick destroyed.
        The higher the speed is, the more points
        The closer the brick is to the top of the screen, the more points
        
        Parameter brick: the brick that collided with the ball
        Precondition: Brick object"""
        assert isinstance(brick, Brick)
        
        self._score+=self._scoreMultiple*brick.getBrickScore()
    
    def _determineSound(self, num):
        """Returns: sound that will be played depending on number of bricks hit
        
        Parameter num: number of bricks hit
        Precondition: int >0"""
        assert type(num)==int and num>0
        
        if num%4==1:
            return "saucer1.wav"
        if num%4==2:
            return "saucer2.wav"
        if num%4==3:
            return "plate1.wav"
        if num%4==0:
            return "plate2.wav"
