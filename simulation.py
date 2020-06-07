
from simulator import *
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--ground_size', '--g', type=int, help='To change the area of the box movement is confined to.', default = 4)
parser.add_argument('--population', '--p', type=int, help='To control the total number of healthy population at the start of simulation.', default = 101)
parser.add_argument('--init_sick', '--i', type=int, help='Initial sick people at the start.', default = 1)
parser.add_argument('--recovery_time', '--rt', type=int, help='Constant recovery time, after which an infected person will become recovered.', default = 1000)
parser.add_argument('--radii', '--r', type=float, help='Safe social distancing distance each person needs to maintain.', default = 0.04)
parser.add_argument('--hospital_beds', '--b', type=int, help='Total nu,ber of available hospital beds.', default = 25)
parser.add_argument('--social_dist', '--s', type=int, help='Total number of people following social distancing.', default = 25)



args = parser.parse_args()
print(args)
if __name__ == '__main__':

#    for i in range(100):
    total_frames = 100000
    box_length = args.ground_size
    npersons = args.population
    social_dist = args.social_dist
    recovery_time = args.recovery_time
    sick_people = args.init_sick
    radii = args.radii
    total_beds = args.hospital_beds
    styles = {'linewidth': 2, 'fill': 1}
    sim = Simulation(npersons, sick_people, social_dist, radii, styles, total_beds, box_length, recovery_time)
    sim.do_animation(save=True)
