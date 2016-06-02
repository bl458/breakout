# breakout.py
# Byungchan Lim bl458
# 12/11/15
# From professor's state.py, function _determineState and instance attributes last_keys, factor were taken
"""Primary module for Breakout application

This module contains the main controller class for the Breakout application. There is no
need for any any need for additional classes in this module.  If you need more classes, 
99% of the time they belong in either the play module or the models module. If you 
are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from game2d import *
from play import *

# setters are ok or no in play?
# specifications are specific enough?
# bounceball() not sure?? 

# PRIMARY RULE: Breakout can only access attributes in play.py via getters/setters
# Breakout is NOT allowed to access anything in models.py

class Breakout(GameApp):
    """Instance is the primary controller for the Breakout App
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Play.
    Play should have a minimum of two methods: updatePaddle(input) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
                the current state of the game represented a value from constants.py
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle, ball, and bricks
        _mssg   [GLabel, or None if there is no message to display]
                the currently active message
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _game is only None if _state is STATE_INACTIVE.
        Attribute _mssg is only None if  _state is STATE_ACTIVE or STATE_COUNTDOWN.
    
    For a complete description of how the states work, see the specification for the
    method update().
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _timeDelay  [int]:
                Measures how much time has passed in the countdown
    _level      [int]:
                the level player is in
    _mssgLives  [int]:
                message that displays tries
    _mssgScore  [int]:
                message that displays score
    _mssgLevel  [int]:
                meesage that displays level
    _realLevel  [int]:
                same as level in play. Made to save level value when going
                on to new level into STATE_NEWGAME
    _realTries  [int]:
                same as tries in play. Made to save number of tries left when going
                on to new level into STATE_NEWGAME
    _realScore  [int]:
                same as score in play. Made to save score value when going
                on to new level into STATE_NEWGAME          
    """
    
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _mssg) saying that the user should press to play a game."""
        # IMPLEMENT ME
        self._state=STATE_INACTIVE
        self._mssgScore=None
        self._mssgLives=None
        self._mssgLevel=None
        self._realLevel=1
        self._realTries=3
        self._realScore=0
        
        if self._state!=STATE_INACTIVE:
            self._mssg=None
        
        else:
            self._game=None
            self._mssg=GLabel(x=GAME_WIDTH/2.0, y=GAME_HEIGHT/2.0, text='Press any key to play', font_size=40,
                          font_name="ComicSans.ttf", bold=False, halign="center", valign="middle")
            self._timeDelay=0

    def update(self,dt):
        """Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Play.  The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Play object _game to play the game.
        
        As part of the assignment, you are allowed to add your own states.  However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWGAME,
        STATE_COUNTDOWN, STATE_PAUSED, and STATE_ACTIVE.  Each one of these does its own
        thing, and so should have its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It is a 
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen.
        
        STATE_NEWGAME: This is the state creates a new game and shows it on the screen.  
        This state only lasts one animation frame before switching to STATE_COUNTDOWN.
        
        STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball is 
        served.  The player can move the paddle during the countdown, but there is no
        ball on the screen.  Paddle movement is handled by the Play object.  Hence the
        Play class should have a method called updatePaddle()
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Play (NOT in this class).  Hence
        the Play class should have methods named updatePaddle() and updateBall().
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        The rules for determining the current state are as follows.
        
        STATE_INACTIVE: This is the state at the beginning, and is the state so long
        as the player never presses a key.  In addition, the application switches to 
        this state if the previous state was STATE_ACTIVE and the game is over 
        (e.g. all balls are lost or no more bricks are on the screen).
        
        STATE_NEWGAME: The application switches to this state if the state was 
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        
        STATE_COUNTDOWN: The application switches to this state if the state was
        STATE_NEWGAME in the previous frame (so that state only lasts one frame).
        
        STATE_ACTIVE: The application switches to this state after it has spent 3
        seconds in the state STATE_COUNTDOWN.
        
        STATE_PAUSED: The application switches to this state if the state was 
        STATE_ACTIVE in the previous frame, the ball was lost, and there are still
        some tries remaining.
        
        STATE_NEWLEVEL: The application switches to this state if the state was
        STATE_ACTIVE in the previous frame, the person destroyed all the bricks in
        any levels below 4
        
        STATE_COMPLETE: The application switches to this state if the state was
        STATE_PAUSED in the previous frame. After switching, either the ball was lost
        and there are no tries remaining or there were no bricks remaining.  
        
        You are allowed to add more states if you wish. Should you do so, you should 
        describe them here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        # IMPLEMENT ME
        assert type(dt)==float or type(dt)==int
        
        self._determineState()
            
        if self._state==STATE_NEWGAME:
            self._startNewGame()
            
        if self._state==STATE_COUNTDOWN:
            self._doCountdown()
            
        if self._state==STATE_PAUSED:
            self._pausedGame()
            
        if self._state==STATE_ACTIVE:
            self._playGame()
            
        if self._state==STATE_COMPLETE:
            self._endGame()
        
        if self._state==STATE_NEWLEVEL:
            self._newLevel()
            
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are attributes in Play. 
        In order to draw them, you either need to add getters for these attributes or you 
        need to add a draw method to class Play.  We suggest the latter.  See the example 
        subcontroller.py from class."""
        # IMPLEMENT ME
        if self._state==STATE_INACTIVE:
            self._mssg.draw(self.view)
            
        if self._state==STATE_COUNTDOWN:
            self._mssg.draw(self.view)
            self._game.drawBricks(self.view)
            self._game.drawPaddle(self.view)
            
        if self._state==STATE_ACTIVE:
            self._game.drawBricks(self.view)
            self._game.drawPaddle(self.view)
            self._game.drawBall(self.view)
            self._mssg.draw(self.view)
            self._mssgLives.draw(self.view)
            self._mssgScore.draw(self.view)
        
        if self._state==STATE_PAUSED:
            self._mssg.draw(self.view)
            self._game.drawPaddle(self.view)
            self._game.drawBricks(self.view)
            self._mssgLives.draw(self.view)
            self._mssgScore.draw(self.view)
        
        if self._state==STATE_NEWLEVEL:
            self._mssg.draw(self.view)
            
        if self._state==STATE_COMPLETE:
            self._mssg.draw(self.view)
            
    # HELPER METHODS FOR THE STATES GO HERE
    def _determineState(self):
        """Determines the state. 
        
        When the state is inactive,
        this method checks for a key press, and if there is one, changes the state 
        to the next value.  A key press is when a key is pressed for the FIRST TIME.
        When the state is active,
        this method transitions to STATE_NEWLEVEL if there are no bricks and
        the level is less than 4.
        If the player beats the game when the level is 4, the state becomes
        STATE_COMPLETE. 
    
        Used Professor White's function _determineState in state.py for if statement
        for when the state is inactive. """
        
        if self._state==STATE_INACTIVE:
            keyInput = self.input.key_count
            change = keyInput > 0
            
            if change:
                self._state = STATE_NEWGAME
        
        if self._state==STATE_ACTIVE:
            if self._game.getBricks()==[] and self._game.getLevel()<4:
                self._state=STATE_NEWLEVEL
            if self._game.getBricks()==[] and self._game.getLevel()==4:
                self._state=STATE_COMPLETE
        
    def _startNewGame(self):
        """Starts new game and then changes state to the next one
        
        This method makes ball, paddle, and bricks appear on the view for
        the first time. It also erases the welcome screen message. It also
        initializes the lives (tries) message and score message"""
        
        self._mssg=None
        self._game=Play()
        self._mssgLives=GLabel(x=GAME_WIDTH-30, y=GAME_HEIGHT-BRICK_Y_OFFSET/2.0, text='Lives: '
                              +str(self._game.getTries()),
                              font_size=10, font_name="ComicSans.ttf",
                              bold=False, halign="center", valign="middle")
        self._mssgScore=GLabel(x=30, y=GAME_HEIGHT-BRICK_Y_OFFSET/2.0, text='Score: '
                              +str(self._game.getScore()),
                              font_size=10, font_name="ComicSans.ttf",
                              bold=False, halign="center", valign="middle")
        self._mssgLevel=GLabel(x=GAME_WIDTH/2.0, y=GAME_HEIGHT-BRICK_Y_OFFSET/2.0, text='Level: '
                              +str(self._game.getLevel()),
                              font_size=10, font_name="ComicSans.ttf",
                              bold=False, halign="center", valign="middle")
        self._game.setLevel(self._realLevel)
        self._game.setTries(self._realTries)
        self._game.setScore(self._realScore)
        self._state=STATE_COUNTDOWN
    
    def _doCountdown(self):
        """Shows the countdown from 3 to 1 for 3 seconds and then
        transitions to playable state.
        
        After reaching a playable state, the ball is served.
        Keeps track of the time by using the attribute timeDelay. """
        
        if 0<=self._timeDelay<60:
            self._mssg=GLabel(x=GAME_WIDTH/2.0, y=GAME_HEIGHT/2.0, text='3',
                              font_size=40, font_name="ComicSans.ttf",
                              bold=False, halign="center", valign="middle")
            self._game.updatePaddle(self.input)
            
        if 60<=self._timeDelay<120:
            self._mssg.text='2'
            self._game.updatePaddle(self.input)
            
        if 120<=self._timeDelay<180:
            self._mssg.text='1'
            self._game.updatePaddle(self.input)
            
        if self._timeDelay==180:
            self._game.updatePaddle(self.input)
            self._state=STATE_ACTIVE
            self._timeDelay=0
            self._game.serveBall()
        
        self._timeDelay+=1    
     
    def _playGame(self):
        """Called when game is ongoing after countdown ends
        
        When the ball is lost and tries remaining decreases, state moves on to a paused one.
        Changes message to display score."""
        
        originalTries=self._game.getTries()
        
        self._game.updatePaddle(self.input)
        self._game.updateBall()
        
        self._mssg.y=GAME_HEIGHT-BRICK_Y_OFFSET/2.0
        self._mssg.text='Level '+str(self._game.getLevel())
        
        self._mssgLives.text='Lives: '+str(self._game.getTries())
        
        self._mssgScore.text='Score: '+str(self._game.getScore())
        
        if originalTries!=self._game.getTries():
            self._state=STATE_PAUSED

    def _pausedGame(self):
        """Calld when game is paused when ball falls out of bounds. 
        
        Sets scoreMultiple back to 0. Since the ball fell, there is a penalty that makes the
        score goes down by a value. If the tries or bricks remaining reach 0,
        the state transitions from paused to complete. If the game is not complete yet,
        a click on the mouse starts the game again.
        """
        
        self._game.setScoreMultiple(0)
        
        if self._game.getTries()==0:
            self._state=STATE_COMPLETE
            self._game.decreaseScore(SCORE_PENALTY_3)
            
        else: 
            self._mssg.text='Too hard? Y/N'
            self._mssg.font_size=30
            self._mssg.y=GAME_HEIGHT/2.0
            self._ball=None
            
            if self._game.getTries()==2:
                self._game.decreaseScore(SCORE_PENALTY_1)
            if self._game.getTries()==1:
                self._game.decreaseScore(SCORE_PENALTY_2)
            
            if self.input.is_key_down('n'):
                self._state=STATE_COUNTDOWN
            elif self.input.is_key_down('y'):
                self._state=STATE_COMPLETE
    
    def _newLevel(self):
        """Called when game is going on to new level.
        
        Shows a message depending on what level the player beat. Also
        goes onto the next level or goes to the losing screen depending
        on the user input.
        """
        
        self._mssg.y=GAME_HEIGHT/2.0
        if self._game.getLevel()==1:
            self._mssg.text='Meh. Next level? Y/N'
            self._mssg.font_size=20
        if self._game.getLevel()==2:
            self._mssg.text='Hm.\nBut can you handle THIS? Y/N'
            self._mssg.font_size=20
        if self._game.getLevel()==3:
            self._mssg.text='Dang. But the next one\'s impossible! Y/N'
            self._mssg.font_size=20
        
        if self.input.is_key_down('y'):
            self._game.setLevel(self._game.getLevel()+1)
            self._realLevel=self._game.getLevel()
            self._realScore=self._game.getScore()
            self._realTries=self._game.getTries()
            self._state=STATE_NEWGAME
        elif self.input.is_key_down('n'):
            self._state=STATE_COMPLETE
        
    def _endGame(self):
        """Called when the game is ending after the player runs out of
        tries or hit all the bricks.
        
        Puts a message up depending on whether the player won or not."""
        
        if self._game.getBricks()==[] and self._game.getTries()>0 and self._game.getLevel()==4:
            self._mssg.text='GG :P Score: ' +str(self._game.getScore())
            self._mssg.font_size=20
            self._mssg.y=GAME_HEIGHT/2.0
            
        else:
            self._mssg.text='Too hard eh? Score: '+str(self._game.getScore())
            self._mssg.font_size=20
            self._mssg.y=GAME_HEIGHT/2.0
