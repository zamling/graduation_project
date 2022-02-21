import argparse
from tqdm import tqdm
from localization.model.particle_filter import ParticleFilter
from util import tools
from util import event as E
from util import load_data as L
import numpy as np
from util.draw import draw_partiles, draw_angle
import matplotlib.pyplot as plt

def get_args_parser():
    parser = argparse.ArgumentParser('Set transformer detector', add_help=False)
    #particle filter
    parser.add_argument('--n_particles', default=500, type=int)
    parser.add_argument('--gamma', default=100, type=float,help="the parameter in equation 12")
    parser.add_argument('--n_resampling', default=100, type=int, help="how many steps when particle filter resampling")
    parser.add_argument('--batch_n_resampling', default=20, type=int, help="how many steps when particle filter resampling")


    #implement info
    parser.add_argument('--focal', default=0.8, type=float)
    parser.add_argument('--D', default=46.0, type=float)
    parser.add_argument('--map_info', default=(360,480), type=tuple)
    parser.add_argument('--G0', default=8, type=int)

    parser.add_argument('--B', default=5, type=int)

    return parser

def get_pose(particles):
    scores = []
    for particle in particles:
        score = particle.get_score()
        scores.append(score)
    max_index = np.argmax(scores)
    pose = particles[max_index].get_pose()
    x,y,r = pose.state
    position = [x,y,r]
    return position



def main(args):
    # loop
    events = L.dataLoader('triangle')
    feature_points = L.getFeaturePoints('triangle',expand=False)
    filter = ParticleFilter(arg=args,feature_points=feature_points)
    pre_particle = filter.get_particles()
    pose = get_pose(pre_particle)
    draw_partiles(pre_particle, (pose[0], pose[1]))
    draw_angle(pre_particle, pose[2])
    for event in tqdm(events):
        min_h = filter.update(event,pre_particle)
        pre_particle = filter.get_particles()


        if (filter.get_time_step() + 1) % args.n_resampling == 0:
            filter.resampling(noisy=True)
        if (filter.get_time_step() + 1) % 1000 == 0:
            drawParicle = filter.get_particles()
            pose = get_pose(drawParicle)
            print("\n[Time Step]: {}, min_h={}".format(filter.get_time_step(), min_h))
            print("current pose: {}".format(pose))
        if (filter.get_time_step() + 1) % 10000 == 0:
            drawParicle = filter.get_particles()
            pose = get_pose(drawParicle)
            draw_partiles(drawParicle, (pose[0], pose[1]))
            draw_angle(drawParicle,pose[2])

        filter.increment_time()

def main_batch(args):
    # loop
    events = L.dataLoader('triangle')
    event_loader = L.batch_data(args.B,events)
    event_iter = iter(event_loader)
    feature_points = L.getFeaturePoints('triangle',expand=False)
    filter = ParticleFilter(arg=args,feature_points=feature_points)
    pre_particle = filter.get_particles()
    pose = get_pose(pre_particle)
    draw_partiles(pre_particle, (pose[0], pose[1]))
    draw_angle(pre_particle, pose[2])
    for _ in tqdm(range(len(event_loader))):
        event_batch = next(event_iter)
        filter.update_with_batch(event_batch,pre_particle)
        pre_particle = filter.get_particles()
        if (filter.get_time_step() + 1) % args.batch_n_resampling == 0:
            filter.resampling(noisy=True)
        if (filter.get_time_step() + 1) % 200 == 0:
            drawParicle = filter.get_particles()
            pose = get_pose(drawParicle)
            print("\n[Time Step]: {}".format(filter.get_time_step()))
            print("current pose: {}".format(pose))
        if (filter.get_time_step() + 1) % 2000 == 0:
            drawParicle = filter.get_particles()
            pose = get_pose(drawParicle)
            draw_partiles(drawParicle, (pose[0], pose[1]))
            draw_angle(drawParicle,pose[2])

        filter.increment_time()




if __name__ == '__main__':
    parser = argparse.ArgumentParser('SLAM with event camera', parents=[get_args_parser()])
    args = parser.parse_args()
    #main(args)
    main_batch(args)



    # feats = L.getFeaturePoints('triangle')
    # print(feats)
    # transform = tools.Transform(args)
    # pose = E.Pose(0,0,0)
    # x,y,z = transform.image2ref(3,4,5,pose)
    # print("x = {}, y={}, z={}".format(x,y,z))


