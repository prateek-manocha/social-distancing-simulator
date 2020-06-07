import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib import animation
from itertools import combinations
import statistics
import matplotlib
import matplotlib.gridspec as gridspec
from hospital_patient import *


class Simulation:
    """A class for a simple hard-circle molecular dynamics simulation.

    The simulation is carried out on a square domain: 0 <= x < 1, 0 <= y < 1.

    """

    def __init__(self, n, sick_init, social_dist, radius=0.01, styles=None, total_beds=10, box_length=1, recovery_time=1000):
        """Initialize the simulation with n persons with radii radius.

        radius can be a single value or a sequence with n values.

        Any key-value pairs passed in the styles dictionary will be passed
        as arguments to Matplotlib's Circle patch constructor when drawing
        the persons.

        """

        self.init_persons(n, sick_init, social_dist, radius, box_length, recovery_time, total_beds, styles)
        self.init_hospital(total_beds)

    def init_hospital(self, total_beds):
        self.hospital = Hospital(total_beds)

    def init_persons(self, n, sick_init, social_dist, radius, box_length, recovery_time, total_beds, styles=None):
        """Initialize the n persons of the simulation.

        Positions and velocities are chosen randomly; radius can be a single
        value or a sequence with n values.

        """

        try:
            iterator = iter(radius)
            assert n == len(radius)
        except TypeError:
            # r isn't iterable: turn it into a generator that returns the
            # same value n times.
            def r_gen(n, radius):
                for i in range(n):
                    yield radius
            radius = r_gen(n, radius)

        self.n = n
        self.collisions = 0
        self.counter = 0
        self.box_length = box_length
        self.recovery_time = recovery_time
        self.total_beds = total_beds
        self.social_dist = social_dist
        self.sick_init = sick_init
        self.n_persons = n
        self.persons = []
        for i, rad in enumerate(radius):
            # Try to find a random initial position for this person.
            while True:
                # Choose x, y so that the person is entirely inside the
                # domain of the simulation.
                x, y = rad + (self.box_length - 2*rad) * np.random.random(2)
                y /= 2
                # Choose a random velocity (within some reasonable range of
                # values) for the person.
                vr = 0.1 * np.random.random() + 0.2
                vphi = 2*np.pi * np.random.random()
                vx, vy = vr * np.cos(vphi), vr * np.sin(vphi)
                if i < self.sick_init:
                    person = Person(x, y, vx, vy, rad, styles, self.box_length, self.recovery_time)
                    person.health = -1
                elif i>self.sick_init and i<=(self.sick_init + self.social_dist):
                    person = Person(x, y, 0, 0, rad, styles, self.box_length, self.recovery_time)
                    person.social_dist = 1
                else:
                    person = Person(x, y, vx, vy, rad, styles, self.box_length, self.recovery_time)
                # Check that the person doesn't overlap one that's already
                # been placed.
                for p2 in self.persons:
                    if p2.overlaps(person):
                        break
                else:
                    self.persons.append(person)
                    break

    def handle_collisions(self):
        """Detect and handle any collisions between the persons.

        When two persons collide, they do so elastically: their velocities
        change such that both energy and momentum are conserved.

        """

        def change_velocities(p1, p2):
            """
            persons p1 and p2 have collided elastically: update their
            velocities.

            """

            m1, m2 = p1.radius**2, p2.radius**2
            M = m1 + m2
            r1, r2 = p1.r, p2.r
            d = np.linalg.norm(r1 - r2)**2
            v1, v2 = p1.v, p2.v
            u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
            u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
            if p1.health == -100 or p1.social_dist == 1:
                p2.v *= -1
            elif p2.health == -100 or p2.social_dist == 1:
                p1.v *= -1
            else:
                p1.v = u1
                p2.v = u2


        def update_health(p1, p2):
            '''
            If collision between two persons, change their health status depending on health of both
            the persons that collided
            '''
            if p1.health == -1 and p2.health == 1:
                p2.health = -1
            elif p2.health == -1 and p1.health == 1:
                p1.health = -1

        # We're going to need a sequence of all of the pairs of persons when
        # we are detecting collisions. combinations generates pairs of indexes
        # into the self.persons list of persons on the fly.
        pairs = combinations(range(self.n), 2)

        for i,j in pairs:
            if self.persons[i].overlaps(self.persons[j]):
                change_velocities(self.persons[i], self.persons[j])
                update_health(self.persons[i], self.persons[j])
                self.collisions += 1

    def advance_animation(self, dt):
        """Advance the animation by dt, returning the updated Circles list."""

        for i, p in enumerate(self.persons):
            p.advance(dt)
            self.circles[i].center = p.r
            if p.health == 1:
                self.circles[i].set_color('forestgreen')
            elif p.health == -1:
                p.recover_health(self.hospital)
                self.circles[i].set_color('orangered')
                #if p.admitted == 1:
                #    self.circles[i].set_edgecolor('black')
            elif p.health == 2:
                self.circles[i].set_color('deepskyblue')
            elif p.health == -100:
                self.circles[i].set_color('black')
            if p.social_dist == 1:
                self.circles[i].set_edgecolor('black')
                self.circles[i].set_linewidth(0.5)

        self.handle_collisions()
        return self.circles

    def advance(self, dt):
        """Advance the animation by dt."""
        for i, p in enumerate(self.persons):
            p.advance(dt)
        self.handle_collisions()

    def init(self):
        """Initialize the Matplotlib animation."""

        self.circles = []
        for person in self.persons:
            dummy = person.draw(self.ax)
            self.circles.append(dummy)
        self.healthy = []
        self.sick = []
        self.recovered = []
        self.dead = []
        self.get_status()
        #self.ax2.plot(self.health_count)
        self.ax2.stackplot(range(0, len(self.healthy)),self.sick, self.healthy, self.recovered, self.dead, labels=['Healthy','Sick','Recovered', 'Dead'], colors=['orangered','forestgreen', 'deepskyblue', 'black'])
        self.ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),ncol=3, fancybox=True, shadow=True)
        self.ax3.plot(range(0, len(self.healthy)), self.healthy,'forestgreen', self.sick, 'orangered', self.recovered, 'deepskyblue', self.dead, 'black')
        #return self.circles

    def get_status(self):
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        for person in self.persons:
            if person.health == 1:
                count1 += 1
            elif person.health == -1:
                count2 += 1
            elif person.health == 2:
                count3 += 1
            elif person.health == -100:
                count4 += 1
        self.healthy.append(count1)
        self.sick.append(count2)
        self.recovered.append(count3)
        self.dead.append(count4)

    def exit_animate(self):
        #print(self.sick[-1])
        if self.sick[-1] == 0:
            self.counter += 1
            if self.counter >= 50:
                exit()

    def animate(self, i):
        """The function passed to Matplotlib's FuncAnimation routine."""
        self.advance_animation(0.01)
        self.get_status()
        self.ax2.clear()
        self.ax3.clear()
        self.ax2.plot(np.ones(len(self.healthy))*self.total_beds, 'k--')
        samples = range(0, len(self.healthy))
        self.ax2.stackplot(samples, self.sick, self.healthy, self.recovered, self.dead, labels=['Sick: ' +str(self.sick[-1]),'Healthy: '+str(self.healthy[-1]),'Recovered: '+str(self.recovered[-1]), 'Dead: '+str(self.dead[-1])], colors=['orangered','forestgreen', 'deepskyblue', 'black'])
        #self.ax2.legend(bbox_to_anchor=(1.04,0), loc="lower left", borderaxespad=0)
        self.ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=2, fancybox=True, fontsize=6, shadow=True)
        self.ax2.xaxis.set_ticks([])
        self.ax2.set_ylim(0, self.n+30)
        self.ax3.plot(samples, self.healthy,'forestgreen', label = 'Healthy')
        self.ax3.plot(samples, self.sick, 'orangered', label = 'Sick')
        self.ax3.plot(samples, self.recovered, 'deepskyblue', label = 'Recovered')
        self.ax3.plot(samples, self.dead, 'black', label = 'Dead')
        self.ax3.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=2, fancybox=True, fontsize=6, shadow=True)
        self.ax3.set_ylim(0, self.n+30)
        self.ax3.xaxis.set_ticks([])
        self.ax2.yaxis.set_ticks([])
        self.ax2.set_xlabel('Change over time')
        self.ax3.set_xlabel('Change over time')
        self.ax.set_title('Social Distancing Followed By '+str(self.social_dist)+'% People.')
        self.ax2.set_title('Stacked area graph for each category', fontsize = 8)
        self.ax3.set_title('Percentage graph for each category', fontsize = 8)
        self.exit_animate()


    def do_animation(self, save=False):
        """Set up and carry out the animation of the molecular dynamics.

        To save the animation as a MP4 movie, set save=True.
        """

        #fig, self.ax = plt.subplots()
        fig1 = plt.figure(constrained_layout=False)
        spec1 = gridspec.GridSpec(ncols=11, nrows=12, figure=fig1)
        self.ax = fig1.add_subplot(spec1[0:6, :])
        self.ax2 = fig1.add_subplot(spec1[7:, 0:5])
        self.ax3 = fig1.add_subplot(spec1[7:, 6:])
        #self.ax3 = fig1.add_subplot(spec1[3, ])
        for s in ['top','bottom','left','right']:
            self.ax.spines[s].set_linewidth(2)
        self.ax.set_aspect('equal', 'box')
        self.ax.set_xlim(0, self.box_length)
        self.ax.set_ylim(0, self.box_length/2)
        self.ax2.set_xlim(0, 10000)
        self.ax2.set_ylim(0, self.n+10)
        self.ax3.set_xlim(0, 10000)
        self.ax3.set_ylim(0, self.n+10)
        self.ax.xaxis.set_ticks([])
        self.ax.yaxis.set_ticks([])
        self.ax2.xaxis.set_ticks([])
        self.ax2.yaxis.set_ticks([])
        self.ax3.yaxis.set_ticks([50,100,150])
        self.ax3.xaxis.set_ticks([])

        #self.ax3.yaxis.set_ticks([50,100,150])
        #followed by '+str(social_dist)+'% people.
        anim = animation.FuncAnimation(fig1, self.animate, init_func=self.init, frames=10000, interval=2, blit=False)

        if save:
            Writer = animation.writers['ffmpeg']
            writer = Writer(fps=100, bitrate=1800)
            anim.save('Final_'+str(self.social_dist)+'_social.mp4', writer=writer)
            plt.close()
        else:
            plt.show()
