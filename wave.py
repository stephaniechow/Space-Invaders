"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

Name: Harper Tooch(hat45) and Stephanie Chow(sac342)
Date 12/2/2018
"""
from game2d import *
from consts import *
from models import *
import random


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary. It
    also marches the aliens back and forth across the screen until they are all
    destroyed or they reach the defense line (at which point the player loses).
    When the wave is complete, you should create a NEW instance of Wave (in Invaders)
    if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not update.
    See subcontrollers.py from Lecture 24 for an example.  This class will be similar
    to than one in how it interacts with the main class Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None]
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]

    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that
    you need to access in Invaders.  Only add the getters and setters that you need for
    Invaders. You can keep everything else hidden.

    You may change any of the attributes above as you see fit. For example, may want to
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        rt:         Whether the alien is moving right [bool]
        dn:         Whether the alien had moved down during the last time interval
                    [0 <= int <= 2]
        boltFire:   Rate at which a bolt is fired from the alien [0 <= int <= BOLT_RATE]
        alienSteps: Number of steps taken by the alien before an alien shoots a bolt
                    [0 <= int <= BOLT_RATE]
        isWin:      Whether the player has won [bool]
        isFinish:   Whether the wave is finished [bool]
        score:      How many aliens you hit [int >= 0]
        pewShip:    Sound that the Ship makes when it shoots a bolt[Sound object]
        pewAlien:   Sound that an Alien makes when it shoots a bolt[Sound object]
        BlastShip:  Sound that the Ship makes when it gets hit by a bolt[Sound object]
        BlastAlien: Sound that an Alien makes when it gets hit by a bolt[Sound object]

    """

    def addTime(self,t):
        """
        Adds t to time

        This is a helper method to keep track of time.

        Parameter t: The time being added
        Preconditon: t is an int
        """
        assert type(t) == int or type(t) == float
        self._time += t

    def getRt(self):
        """
        Returns whether the ship is moving to the right

        A getter method that returns self.rt, to tell whether the player is
        moving to the right(True) or left(False)
        """
        return self.rt

    def setRt(self, t):
        """
        Sets self.rt to a boolean

        Sets self.rt to a boolean to see whether the wave is moving to the
        left(False) or to the right(True)

        Parameter t: The indicator whether the wave is moving to the left or right
        Precondition: t is a boolean
        """
        assert type(t) == bool
        self.rt = t

    def getDn(self):
        """
        Returns whether the ship moved down during the last update

        A getter method that returns self.dn, to tell whether the wave has moved
        down during the last update. If self.dn == 0, then the wave is moving
        to the right. If self.dn == 1, then the wave had just moved down. If
        self.dn == 2, then the wave is moving to the left.
        """
        return self.dn

    def setDn(self,t):
        """
        Sets self.dn to an int

        Sets self.dn to an int of whether the wave has moved down. See self.getDn()
        for more information

        Parameter t: The indicator of whether the wave has moved down
        Precondition: t is 0 <= int <= 2
        """
        assert type(t) == int and t >= 0 and t <= 2
        self.dn = t

    def getShip(self):
        """
        Returns the ship object

        Use this method to get the ship object or to indicate whehter the ship is gone
        if it returns None.
        """
        return self._ship

    def getLives(self):
        """
        Returns the amount of lives the player has left

        This method return the number of lives the player has left before the
        player gets a Game Over
        """
        return self._lives

    def getFinish(self):
        """
        Returns whether the game has finished or not

        This method returns a boolean of whether the game is finished(True) or
        not finished(False)
        """
        return self.isFinish

    def getWin(self):
        """
        Returns whether the player had won the wave or not

        This method returns true is the player has won the game, and returns
        false if the player has lost the game.
        """
        return self.isWin

    def getScore(self):
        """
        Returns the score

        This method returns the score that the player has in the game
        """
        return self.score

    def __init__(self):
        """
        Initializes the ship and the aliens in the wave.

        This method, creates the ship, the aliens and the defense line, initializes
        the bolt list, time, boltFire, alienSteps, dn, lives, score and the sounds. It
        also sets rt to True, isWin to False, and isFinish to False.
        """
        self._lives = SHIP_LIVES
        self._createAliens()
        self.createShip()
        self._bolts = []
        self._dline = GPath(points =[0, DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE]\
            ,linewidth = 2, linecolor = 'black')
        self._time = 0
        self.rt = True
        self.dn = 0
        self.boltFire = 0
        self.alienSteps = 0
        self.isWin = False
        self.isFinish = False
        self.score = 0
        self.pewShip = Sound('pew1.wav')
        self.pewAlien = Sound('pew2.wav')
        self.blastShip = Sound('blast1.wav')
        self.blastAlien = Sound('blast2.wav')

    def update(self,input,t):
        """
        Updates the ship, aliens, and laser bolts to move

        This method updates the aliens movement, the ship movement, adds time,
        creates the bolt for the alien and the ship, checks for collisions, deletes
        bolts that are offscreen, and checks for whether there are anymore aliens
        in the wave and whether the aliens have passed the defense line.
        It also sets self.boltFire for how many steps the Aliens should travel before
        shooting a bolt.

        Parameter input: indicates which keyi is being pressed by the user
        Preconditon: input is an instance of GInput

        Parameter t: the time being added
        Preconditon: t is an int or float (asserted in addTime())
        """
        if self.boltFire == 0:
            self.boltFire = random.randint(1,BOLT_RATE)
        self.moveShip(input)
        self.addTime(t)
        self.moveAlien()
        self.createBolt(input)
        self.createAlienBolt()
        self.moveBolts()
        self.collideBoltAlien()
        self.collideBoltPlayer()
        self.delBolts()
        self.isThereAlien()
        self.didAlienPass()

    def draw(self,view):
        """
        Draws the ship, aliens, defensive line and bolts

        This method draws the ship, aliens, defensive line and bolts. If the aliens
        are None the method does not draw that alien. If the ship is hit by an alien
        bolt and is None, then the ship is not drawn. The bolts are drawn for
        the aliens and the ship.
        """
        for q in range(len(self._aliens)):
            for w in range(len(self._aliens[q])):
                if self._aliens[q][w] is None:
                    continue
                self._aliens[q][w].draw(view)
        if not self._ship is None:
            self._ship.draw(view)
        self._dline.draw(view)
        for x in range(len(self._bolts)):
            self._bolts[x].draw(view)

    def moveShip(self, i):
        """
        Moves the ship when given the user input

        This method moves the ship to the left and to the right when i is supplied
        by the user

        Parameter i: indicates which key is being pressed by the user
        Preconditon: i is an instance of GInput
        """
        assert isinstance(i, GInput) == True
        da = 0
        if self._ship is None:
            return
        if i.is_key_down('left'):
            da -= SHIP_MOVEMENT
        if i.is_key_down('right'):
            da += SHIP_MOVEMENT
        old = self._ship.getX()
        new = old + da
        if new > (GAME_WIDTH - (SHIP_WIDTH/2)):
            return
        elif (new < SHIP_WIDTH/2):
            return
        self._ship.setX(old + da)

    def moveAlien(self):
        """
        Helper method to move all the aliens

        This method first finds the alien in the farthest left column and the top
        row, and the alien in the farthest right column and bottom row. Using
        these aliens, the aliens move down once it hits the edge of the game
        screen, and moves left and right depending on self.rt
        """
        for y in range(ALIENS_IN_ROW):
            if self.isEmptyColumn(y) == False:
                for x in range(len(self._aliens)):
                    if not self._aliens[x][y] is None:
                        wizz = self._aliens[x][y]
        for y in range(ALIENS_IN_ROW):
            h = ALIENS_IN_ROW - 1 - y
            if self.isEmptyColumn(h) == False:
                for x in range(len(self._aliens)):
                    if not self._aliens[x][h] is None:
                        queburt = self._aliens[x][h]
        if (self._time > ALIEN_SPEED):
            if (wizz.getX() > (GAME_WIDTH - ALIEN_H_SEP - ALIEN_WIDTH/2)) \
                and (self.getDn() == 0):
                self.downAlien()
            elif (queburt.getX() < (ALIEN_H_SEP + ALIEN_WIDTH/2)) \
                and (self.getDn() == 2):
                self.downAlien()
            elif self.getRt() == True:
                self.rightAlien()
            elif self.getRt() == False:
                self.leftAlien()
            self._time = 0
            self.alienSteps += 1

    def rightAlien(self):
        """
        Helper method to move all the aliens to the right

        This method moves all the aliens to the right by ALIEN_H_WALK and sets
        self.Dn to 0 to signify that the aliens are moving to the right
        """
        for x in range(len(self._aliens)):
            for y in range(len(self._aliens[x])):
                if self._aliens[x][y] is None:
                    continue
                old = self._aliens[x][y].getX()
                self._aliens[x][y].setX(old+ALIEN_H_WALK)
        self.setDn(0)

    def leftAlien(self):
        """
        Helper method to move all the aliens to the left

        This method moves all the aliens to the left by ALIEN_H_WALK and sets
        self.Dn to 2 to signify that the aliens are moving to the left
        """
        for x in range(len(self._aliens)):
            for y in range(len(self._aliens[x])):
                if self._aliens[x][y] is None:
                    continue
                old = self._aliens[x][y].getX()
                self._aliens[x][y].setX(old-ALIEN_H_WALK)
        self.setDn(2)

    def downAlien(self):
        """
        Helper method to move all the aliens down

        This method moves all the aliens down by ALIEN_V_WALK and sets
        self.Dn to 1 to signify that the aliens have just moved down
        """
        for x in range(len(self._aliens)):
            for y in range(len(self._aliens[x])):
                if self._aliens[x][y] is None:
                    continue
                old = self._aliens[x][y].getY()
                self._aliens[x][y].setY(old-ALIEN_V_WALK)
        self.setRt(not self.getRt())
        self.setDn(1)

    def createBolt(self, i):
        """
        Helper method to create a bolt for the player when the up key is pressed

        When the 'up' key is pressed by the player, and they are no other bolts
        that are fired by the ship in the game, then this method creates a bolt
        that is fired by the ship

        Parameter i: i is the key that is pressed
        Precondtion: i is a GInput object
        """
        assert isinstance(i, GInput) == True
        for x in self._bolts:
            if x.isPlayerBolt() == True:
                return
        if i.is_key_down('up'):
            self._bolts.append(Bolt(self._ship.getX(),\
                self._ship.getY() + SHIP_HEIGHT/2, BOLT_SPEED, True))
            self.pewShip.play()

    def createAlienBolt(self):
        """
        Helper method to create an alien bolt

        When self.alienSteps == self.boltFire (when the steps the alien has taken
        and the steps needed to take for the next alien bolt to be fired equal
        each other) then this method creates a bolt fired by an alien of the bottom
        row in a random column.
        """
        if self.alienSteps == self.boltFire:
            x = random.randint(0, ALIENS_IN_ROW-1)
            while self.isEmptyColumn(x) == True:
                x = random.randint(0, ALIENS_IN_ROW-1)
            for q in range(len(self._aliens)):
                r = ALIEN_ROWS - 1 - q
                if not self._aliens[r][x] is None:
                    break
            self._bolts.append(Bolt(self._aliens[r][x].getX(), self._aliens\
                [r][x].getY(), -BOLT_SPEED, False))
            self.alienSteps = 0
            self.boltFire = 0
            self.pewAlien.play()

    def isEmptyColumn(self,x):
        """
        Helper method to see whether column x is empty

        This method checks through column x of self._aliens to see if there are
        any more aliens in that column. it returns True if there are no more aliens
        in that column, and it returns False if there are aliens in that column

        Parameter x: The column being checked
        Preconditon: x is int < ALIENS_IN_ROW
        """
        assert type(x) == int and x < ALIENS_IN_ROW
        for q in range(ALIEN_ROWS):
            if not self._aliens[q][x] is None:
                return False
        return True

    def isEmptyRow(self,x):
        """
        Helper method to see whether row x of the aliens is empty

        This method checks through row x of self._aliens to see if there are any
        aliens in the row. It returns true if there are no aliens in the row,
        and it returns False if there are aliens in that row.

        Parameter x: The row being checked
        Preconditon: x is int < ALIEN_ROWS
        """
        assert type(x) == int and x < ALIEN_ROWS
        for q in range(ALIENS_IN_ROW):
            if not self._aliens[x][q] is None:
                return False
            return True

    def moveBolts(self):
        """
        Helper method to move the bolts

        This method moves all the bolts depending on their velocity
        """
        for x in self._bolts:
            old = x.getY()
            x.setY(old + x.getVelocity())

    def delBolts(self):
        """
        Helper method to delete the bolts once they go off screen

        This method checks through all the bolts in self._bolts to see if they
        go off screen, and when they do, they get deleted from the list.
        """
        x = 0
        while x < len(self._bolts):
            if self._bolts[x].getY() > (GAME_HEIGHT + BOLT_HEIGHT/2):
                del self._bolts[x]
            elif self._bolts[x].getY() < -BOLT_HEIGHT/2:
                del self._bolts[x]
            else:
                x += 1

    def collideBoltAlien(self):
        """
        Helper method to check whether the bolt fired by the player hit any aliens.

        This method first find the bolt fired by the player and checks through
        all the aliens to see if that bolt hit any of the aliens. If it hits an
        alien, then the alien is set to None and the bolt is removed. This method
        also accumalates the score. If the alien hit is within the bottom half
        rows, then score is increased by ten. If the alien hit is within the top
        half rows, then the score is increased by twenty.
        """
        for q in self._bolts:
            if q.isPlayerBolt() == True:
                for x in range(len(self._aliens)):
                    for y in range(len(self._aliens[x])):
                        if (not self._aliens[x][y] is None) and (self._aliens\
                            [x][y].collides(q) == True):
                            if ALIEN_ROWS/(x+1) >= ALIEN_ROWS/2:
                                self.score+=20
                            else:
                                self.score+=10
                            self._aliens[x][y] = None
                            self._bolts.remove(q)
                            self.blastAlien.play()
                            return

    def collideBoltPlayer(self):
        """
        Helper method to check whether any alien bolts collided with the ship

        This method checks the bolts in the list self._bolts to see if they
        collide with the player. Once it sees that a bolt has collided with the
        ship, then is sets the ship to None, deletes the bolt and decreases the
        lives of the ship by one.
        """
        for q in range(len(self._bolts)):
            if self._ship.collides(self._bolts[q]) == True:
                self.blastShip.play()
                self._ship = None
                del self._bolts[q]
                self._lives -=1
                if self._lives == 0:
                    self.isFinish = True
                return

    def isThereAlien(self):
        """
        Helper method to check if there are still aliens in the wave.

        This method checks through all the aliens in the self._aliens list to
        see if there are anymore aliens in the wave, If there are no more aliens,
        theb self.isFinish is set to True, and self.isWin is set to True.
        """
        for x in range(len(self._aliens)):
            for y in range(len(self._aliens[x])):
                if not self._aliens[x][y] is None:
                    return
        self.isFinish = True
        self.isWin = True

    def didAlienPass(self):
        """
        Helper method to check when the aliens have passed the defense line.

        This method checks through the aliens on the bottom row to see if they
        past the defense line. If the aliens pass the defense line, then self.isFinish
        is set to True.
        """
        for x in range(ALIEN_ROWS):
            need = ALIEN_ROWS - 1 - x
            if self.isEmptyRow(x) == False:
                for y in range(ALIENS_IN_ROW):
                    if (not self._aliens[need][y] is None) and ((self._aliens\
                        [need][y].getY() - ALIEN_HEIGHT/2) <= DEFENSE_LINE):
                        self.isFinish = True
                        return

    def createShip(self):
        """
        A helper method to create the ship object

        This method creates the ship object using the SHip constructor
        """
        self._ship = Ship(GAME_WIDTH/2 , SHIP_BOTTOM)

    def _createAliens(self):
        """
        A helper method that creates the _aliens 2D list.

        This method creates a 2d list of all the aliens in a wave with the
        dimensions ALIEN_ROWS by ALIENS_IN_ROW.
        """
        y = 0
        x = 0
        i = ''
        r = 0
        self._aliens = []
        for q in range(ALIEN_ROWS):
            t = []
            y = GAME_HEIGHT - (ALIEN_CEILING + q*(ALIEN_V_SEP) + q*(\
                ALIEN_HEIGHT))
            for w in range(ALIENS_IN_ROW):
                x = (w+2)*ALIEN_H_SEP + w*ALIEN_WIDTH
                t.append(Alien(x,y,i))
            self._aliens.append(t)
            x = 0
        for q in range(ALIEN_ROWS):
            r = q
            for w in range(ALIENS_IN_ROW):
                i = ALIEN_IMAGES[int(r%(len(ALIEN_IMAGES)*2)//2)]
                self._aliens[ALIEN_ROWS-q-1][w].setSource(i)
