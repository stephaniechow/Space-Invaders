"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object. So technically Bolt, which has a velocity,
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you
add new features to your game, such as power-ups.  If you are unsure about whether to
make a new class or not, please ask on Piazza.

Name: Harper Tooch(hat45) and Stephanie Chow (sac342)
Date: 12.2.2018
"""
from consts import *
from game2d import *


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that Ships and Aliens collide with different bolts.  Ships
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    def getX(self):
        """
        Returns: the x coordinate of the center of the ship.

        A getter method that returns self.x, or the x coordinate of the center
        of the ship
        """
        return self.x

    def setX(self, x):
        """
        Sets the x coordinate of the center of the ship.

        A setter method that sets the x coordinate of the center of
        the ship to x

        Parameter x: the x coordinate of the center of the ship
        Preconditon: x is an float or int and x >= 0
        """
        assert (type(x) == int or type(x) == float) and x >= 0
        self.x = x

    def getY(self):
        """
        Return: the y coordinate of the center of the ship.

        A getter method that returns self.y, or the y coordinate of the center
        of the ship
        """
        return self.y

    def __init__(self,x,y):
        """
        Initializes the ship.

        With the coordinates supplied, it creates and draws the ship
        the same way you create an draw a GImage Object.

        Parameter x: the horizontal coordinate of the center of the ship image.
        Precondition: x is an int or float and x >= 0

        Parameter y: the vertical coordinate of the center of the ship image.
        Precondition: y is an int or float and y>=0
        """
        assert (type(x) == float or type(x) == int) and x >= 0
        assert (type(y) == float or type(y) == int) and y >= 0
        super().__init__(x=x,y=y,width = SHIP_WIDTH, height = SHIP_HEIGHT, \
            source = 'ship.png')

    def collides(self, bolt):
        """
        Returns: True if the bolt was fired by the alien and collides with the ship

        This method checks the coordinates of the four corners of the bolt to see
        if the Ship contains thoses coordinates. If it does, then the bolt collides
        with the Ship, and the method returns True. If not, it returns False

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt, Bolt) == True
        if bolt.isPlayerBolt() == True:
            return False
        if self.contains([bolt.getX() - (BOLT_WIDTH/2),bolt.getY() + \
            (BOLT_HEIGHT/2)]):
            return True
        elif self.contains([bolt.getX() - (BOLT_WIDTH/2),bolt.getY() - \
            (BOLT_HEIGHT/2)]):
            return True
        elif self.contains([bolt.getX() + (BOLT_WIDTH/2),bolt.getY() - \
            (BOLT_HEIGHT/2)]):
            return True
        elif self.contains([bolt.getX() + (BOLT_WIDTH/2),bolt.getY() + \
            (BOLT_HEIGHT/2)]):
            return True
        return False


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that Ships and Aliens collide with different bolts.  Ships
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    def setSource(self, i):
        """
        Sets the source of the imag eof the alien to i

        This is a helper function that sets the source of the image to i for an
        alien

        Parameter i: The image of the alien
        Preconditon: i is a str of a valid image
        """
        assert type(i) == str and (i in ALIEN_IMAGES or i == '')
        self.source = i

    def getX(self):
        """
        Return: the x coordinate of the center of an alien

        A getter method that returns self.x, or the x coordinate of the center
        of the alien
        """
        return self.x

    def setX(self, x):
        """
        Sets the x coordinate of the center of an alien.

        This is a helper function that changes the x coordinate of the center of
        an alien to x

        Parameter x: the x coordinate of the center of an alien
        Preconditon: x is an int or float and x >= 0
        """
        assert (type(x) == int or type(x) == float) and x >= 0
        self.x = x

    def getY(self):
        """
        Return: the y coordinate of the center of an alien.

        A gettor method that returns self.y, or the y coordinate of the center
        of the alien
        """
        return self.y

    def setY(self,y):
        """
        Sets the y coordinate of the center of an alien.

        This is a helper function that changes the y coordinate of the center of
        the alien

        Parameter y: the y coordinate of the center of an alien
        Preconditon: y is an int or float and y >= 0
        """
        assert (type(y) == int  or type(y) == float) and y >= 0
        self.y = y

    def __init__(self,x,y,i):
        """
        Initializes the aliens.

        With the coordinates and image supplied, it creates and draws the aliens
        the same way you create an draw a GImage Object.

        Parameter x: the horizontal coordinate of the center of the alien image.
        Precondition: x is an int and x >= 0

        Parameter y: the vertical coordinate of the center of the alien image.
        Precondition: y is an int and y>=0

        Parameter i: The image of the alien.
        Precondtion: i is a string and is in ALIEN_IMAGES
        """
        assert type(x) == int and x >= 0
        assert type(y) == int and x >= 0
        assert type(i) == str and (i in ALIEN_IMAGES or i =='')
        super().__init__(x=x,y=y,width = ALIEN_WIDTH, height = ALIEN_HEIGHT,\
            source = i)

    def collides(self, bolt):
        """
        Returns: True if the bolt was fired by the ship and collides with this alien

        This method checks the coordinates of the four corners of the bolt to see
        if the Alien contains thoses coordinates. If it does, then the bolt collides
        with the Alien, and the method returns True. If not, it returns False

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt, Bolt) == True
        if bolt.isPlayerBolt() == False:
            return False
        if self.contains([bolt.getX() - (BOLT_WIDTH/2), bolt.getY() + \
            (BOLT_HEIGHT/2)]):
            return True
        elif self.contains([bolt.getX() - (BOLT_WIDTH/2), bolt.getY() - \
            (BOLT_HEIGHT/2)]):
            return True
        elif self.contains([bolt.getX() + (BOLT_WIDTH/2), bolt.getY() - \
            (BOLT_HEIGHT/2)]):
            return True
        elif self.contains([bolt.getX() + (BOLT_WIDTH/2), bolt.getY() + \
            (BOLT_HEIGHT/2)]):
            return True
        return False


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles.  The size of the bolt is
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.

    The class Wave will need to look at these attributes, so you will need getters for
    them.  However, it is possible to write this assignment with no setters for the
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.

    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a
    helper.

    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.

    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        playerBolt: Whether the bolt is from the player or not [bool]
    """

    def isPlayerBolt(self):
        """
        Returns: Whether the bolt is from the player or not in the form of a
        bool

        This helper function returns if the bolt is from the player or not
        """
        return self.playerBolt

    def getVelocity(self):
        """
        Returns the velocity of the bolt

        This helper function returns the velocity of the bolt in the y coordinate
        """
        return self._velocity

    def getY(self):
        """
        Return: the y coordinate of the center of the bolt.

        A getter method that returns self.y, or the y coordinate of the
        center of the bolt
        """
        return self.y

    def setY(self,y):
        """
        Sets the y coordinate of the center of the bolt

        This is a helper function that changes the y coordinate of the center of
        the bolt

        Parameter y: the y coordinate of the center of the bolt
        Preconditon: y is an int or float
        """
        assert (type(y) == int or type(y) == float)
        self.y = y

    def getX(self):
        """
        Return: the x coordinate of the center of the bolt

        A getter method that returns self.x, or the x coordinate of the
        center of the bolt
        """
        return self.x

    def __init__(self, x, y, v, t):
        """
        Initializes the bolt.

        With the coordinates and velocity supplied, it creates and draws a bolt
        the same way you create and draw a GRectangle Object.

        Parameter x: the horizontal coordinate of the center of the bolt.
        Precondition: x is an int and x >= 0

        Parameter y: the vertical coordinate of the center of the bolt.
        Precondition: y is an int and y>=0

        Parameter v: The velocity of the bolt.
        Precondtion: v is an int or float

        Parameter t: Whether the bolt is from the player of the alien.
        Precondition: t is a bool
        """
        assert (type(x) == int or type(x) == float) and x >= 0
        assert (type(y) == int or type(y) == float) and y >= 0
        assert (type(v) == int) or (type(v) == float)
        assert type(t) == bool
        super().__init__(x = x, y = y, width = BOLT_WIDTH, height = BOLT_HEIGHT, \
            linecolor = 'black', fillcolor = 'black')
        self._velocity = v
        self.playerBolt = t
