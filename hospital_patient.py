import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib import animation
from itertools import combinations
import statistics
import matplotlib
import matplotlib.gridspec as gridspec

class Hospital:

    def __init__(self, beds):
        '''
        Initialize a hospital with given number of beds
        '''
        self.totals_beds = beds
        self.avail_beds = beds

    def admit_patient(self, patient):
        if patient.health == -1:
            if self.avail_beds > 0:
                patient.admitted = 1
                self.avail_beds -= 1

    def free_bed(self):
        self.avail_beds += 1


class Person:
    """A class representing a two-dimensional person position ad health status."""

    def __init__(self, x, y, vx, vy, radius=0.01, styles=None, box_length=1, recovery_time=1000):
        """Initialize the person's position, velocity, and radius.

        Any key-value pairs passed in the styles dictionary will be passed
        as arguments to Matplotlib's Circle patch constructor.

        """

        self.r = np.array((x, y))
        self.v = np.array((vx, vy))
        self.radius = radius
        self.box_length = box_length
        self.recovery_time = recovery_time
        self.health = 1    #1 for healthy, -1 for sick, -100 for dead, 2 for recovered
        self.sick_time = 0
        self.social_dist = 0 # 0 for moving freely, 1 for sicial distancing
        self.admitted = 0 #0 if not admitted in hospital, 1 if admitted in hospital
        self.styles = styles
        '''if not self.styles:
            # Default circle styles
            self.styles = {'edgecolor': 'b', 'fill': False}'''

    # For convenience, map the components of the person's position and
    # velocity vector onto the attributes x, y, vx and vy.
    @property
    def x(self):
        return self.r[0]
    @x.setter
    def x(self, value):
        self.r[0] = value
    @property
    def y(self):
        return self.r[1]
    @y.setter
    def y(self, value):
        self.r[1] = value
    @property
    def vx(self):
        return self.v[0]
    @vx.setter
    def vx(self, value):
        self.v[0] = value
    @property
    def vy(self):
        return self.v[1]
    @vy.setter
    def vy(self, value):
        self.v[1] = value

    def overlaps(self, other):
        """Does the circle of this person overlap that of other?"""

        return np.hypot(*(self.r - other.r)) < self.radius + other.radius

    def draw(self, ax):
        """Add this person's Circle patch to the Matplotlib Axes ax."""
        color = 'tomato' if self.health==-1 else 'cornflowerblue'

        circle = Circle(xy=self.r, radius=self.radius, **self.styles, color=color)
        ax.add_patch(circle)
        return circle

    def recover_health(self, hospital):
        if self.health == -1:
            self.sick_time += 1
            if self.admitted == 0:
                hospital.admit_patient(self)
            if self.sick_time > self.recovery_time and self.admitted == 1:
                self.sick_time = 0
                self.health = 2
                hospital.free_bed()
            elif self.sick_time > self.recovery_time and self.admitted == 0:
                self.dead()

    def dead(self):
        self.v = 0
        self.health = -100

    def advance(self, dt):
        """Advance the person's position forward in time by dt."""

        self.r += self.v * dt

        # Make the persons bounce off the walls
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = -self.vx
        if self.x + 1.5*self.radius > self.box_length:
            self.x = self.box_length-1.5*self.radius
            self.vx = -self.vx
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = -self.vy
        if self.y + 1.5*self.radius > self.box_length/2:
            self.y = self.box_length/2-1.5*self.radius
            self.vy = -self.vy

        '''
        code to add shelfs/lines/obstacles inside the room
        if self.y <= 0.7 and self.y >= (0.7-self.radius) and self.x < 0.7:
            self.y = 0.7 - self.radius
            self.vy = -self.vy

        if self.y >= 0.7 and self.y <= (0.7+self.radius)and self.x < 0.7:
            self.y = 0.7 + self.radius
            self.vy = -self.vy

        if self.y <= 0.3 and self.y >= (0.3-self.radius) and self.x > 0.3:
            self.y = 0.3 - self.radius
            self.vy = -self.vy

        if self.y >= 0.3 and self.y <= (0.3+self.radius)and self.x > 0.3:
            self.y = 0.3 + self.radius
            self.vy = -self.vy'''
