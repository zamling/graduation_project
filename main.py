import argparse
from localization.model.particle_filter import ParticleFilter
def get_args_parser():
    parser = argparse.ArgumentParser('Set transformer detector', add_help=False)
    #particle filter
    parser.add_argument('--n_particles', default=2000, type=int)
    parser.add_argument('--gamma', default=0.5, type=float,help="the parameter in equation 12")
    parser.add_argument('--n_resampling', default=100, type=int, help="how many steps when particle filter resampling")


    #implement info
    parser.add_argument('--focal_d', default=100.0, type=float)
    parser.add_argument('--D', default=100.0, type=float)
    parser.add_argument('--map_info', default=(100,100), type=tuple)
    return parser



def main(args):
    # loop
    filter = ParticleFilter(arg=args)

    while True:
        filter.update_event(event)
        filter.update_poses(delta_r=delta_r,delta_theta=delta_theta)
        filter.update_scores()  # here the time step + 1
        if filter.get_time_step() % args.n_resampling == 0:
            filter.resampling()
        filter.increment_time()




if __name__ == '__main__':
    parser = argparse.ArgumentParser('SLAM with event camera', parents=[get_args_parser()])
    args = parser.parse_args()
    main(args)