import argparse
from localization.model.particle_filter import ParticleFilter
from util import tools
from util import event as E
from util import load_data as L
import numpy as np
def get_args_parser():
    parser = argparse.ArgumentParser('Set transformer detector', add_help=False)
    #particle filter
    parser.add_argument('--n_particles', default=100, type=int)
    parser.add_argument('--gamma', default=0.5, type=float,help="the parameter in equation 12")
    parser.add_argument('--n_resampling', default=100, type=int, help="how many steps when particle filter resampling")


    #implement info
    parser.add_argument('--focal', default=0.8, type=float)
    parser.add_argument('--D', default=46.0, type=float)
    parser.add_argument('--map_info', default=(360,480), type=tuple)
    parser.add_argument('--G0', default=1, type=int)

    # file path
    parser.add_argument('--file_path', default=r"C:\git\graduation_project\Data\tone_dots.txt",type=str)
    return parser

def get_pose(particles):
    scores = []
    for particle in particles:
        score = particle.get_score()
        scores.append(score)
    max_index = np.argmax(scores)
    pose = particles[max_index].get_pose()
    return pose



def main(args):
    # loop
    events = L.dataLoader('random')
    filter = ParticleFilter(arg=args,feature_points=feature_points)
    pre_particle = filter.get_particles()
    trajectory = []
    for event in events:
        filter.update(event,pre_particle)
        pre_particle = filter.get_particles()
        pose = get_pose(pre_particle)
        trajectory.append(pose)
        if filter.get_time_step() % args.n_resampling == 0:
            filter.resampling()
        filter.increment_time()




if __name__ == '__main__':
    parser = argparse.ArgumentParser('SLAM with event camera', parents=[get_args_parser()])
    args = parser.parse_args()
    transform = tools.Transform(args)
    pose = E.Pose(0,0,90)
    x,y,z = transform.image2ref(3,4,5,pose)
    print("x = {}, y={}, z={}".format(x,y,z))


