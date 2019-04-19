"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There
is no need for any additional classes in this module.  If you need more classes, 99% of
the time they belong in either the wave module or the models module. If you are unsure
about where a new class should go, post a question on Piazza.

Name:Harper Tooch(hat45) and Stephanie Chow(sac342)
Date: 12/2/18
"""
from consts import *
from game2d import *
from wave import *


class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for
    processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when the
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]

    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification for the
    method update.

    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be
    documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        lastkeys:   the number of keys pressed last frame [int >= 0] Credits to Professor White
        scoreCount: the text with a count of the score [GLabel]
        LivesCount: the text with a count of the score [GLabel]
    """

    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message
        (in attribute _text) saying that the user should press to play a game.
        """
        self._state = STATE_INACTIVE
        self._wave = None
        if self._state == STATE_INACTIVE:
            self._text = GLabel(x = GAME_WIDTH/2, y = GAME_HEIGHT/2, \
                text = "Press 'S' to Play", font_size = 50 )
        else:
            self._text = None
        self.scoreCount =  GLabel(x = 50, y = GAME_HEIGHT - ALIEN_CEILING/4, \
            text = "", font_size = 20 )
        self.LivesCount =  GLabel(x = 50, y = GAME_HEIGHT - ALIEN_CEILING/2, \
            text = "", font_size = 20 )

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.

        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these
        does its own thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.  It is a
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._determineState()
        if self._state == STATE_NEWWAVE:
            self._wave = Wave()
            self._state = STATE_ACTIVE
        if self._state == STATE_ACTIVE:
            self._wave.update(self.input,dt)
            self.scoreCount.text = "Score: " + str(self._wave.getScore())
            self.LivesCount.text = "Lives: " + str(self._wave.getLives())
        if self._state == STATE_ACTIVE and self._wave.getFinish() == True:
            self._state = STATE_COMPLETE
        if self._state == STATE_ACTIVE and self._wave.getShip() is None:
            self._state = STATE_PAUSED
        if self._state == STATE_PAUSED:
            self.pausedState()
        if self._state == STATE_CONTINUE:
            self._state = STATE_ACTIVE
            self._wave.createShip()
        if self._state == STATE_COMPLETE:
            self.finish()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw a GObject
        g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in
        Wave. In order to draw them, you either need to add getters for these attributes
        or you need to add a draw method to class Wave.  We suggest the latter.  See
        the example subcontroller.py from class.
        """
        if (self._state == STATE_INACTIVE) or (self._state == STATE_PAUSED) or\
            (self._state == STATE_COMPLETE):
            self._text.draw(self.view)
        if (not self._wave is None) and (self._state != STATE_COMPLETE):
            self._wave.draw(self.view)
        if (not self.scoreCount is None) and ((self._state!= STATE_INACTIVE) or\
            (self._state != STATE_NEWWAVE)):
            self.scoreCount.draw(self.view)
        if (not self.LivesCount is None) and ((self._state!= STATE_INACTIVE) or\
            (self._state != STATE_NEWWAVE)):
            self.LivesCount.draw(self.view)

    def pausedState(self):
        """
        Method for when the state is paused.

        When self._state == STATE_PAUSED, in other words when the player loses
        a life, then this method is used to prompt the player to press 'S' to
        continue.
        """
        self._text = GLabel(x = GAME_WIDTH/2, y = SHIP_BOTTOM, \
            text = "Press 'S' to Continue", font_size = 50 )

    def finish(self):
        """
        Method for when the game is finished.

        When self._state == STATE_COMPLETE, then this method is called to prompt
        the player whether they lost or won the game.
        """
        if self._wave.getWin() == True:
            self._text = GLabel(x = GAME_WIDTH/2, y = GAME_HEIGHT/2, \
                text = "You Win!!", font_size = 50 )
        if self._wave.getWin() == False:
            self._text = GLabel(x = GAME_WIDTH/2, y = GAME_HEIGHT/2, \
                text = "Game Over", font_size = 50 )

    def _determineState(self):
        """
        Determines the current state and assigns it to self.state

        This method checks for a key press, and if there is one, changes the state
        to the next value.  A key press is when a key is pressed for the FIRST TIME.
        We do not want the state to continue to change as we hold down the key.  The
        user must release the key and press it again to change the state.
        """
        curr_keys = self.input.key_count
        change = curr_keys > 0 and self.lastkeys == 0
        if change and self.input.is_key_down('s'):
            self._state = (self._state + 1) % NUM_STATES
        self.lastkeys= curr_keys
