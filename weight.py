import argparse
from engine import weight_fix_angle, get_pred_img

def get_args_parser():
    parser = argparse.ArgumentParser('Set transformer detector', add_help=False)
    #particle filter
    parser.add_argument('--n_particles', default=500, type=int)
    parser.add_argument('--gamma', default=10, type=float,help="the parameter in equation 12")
    parser.add_argument('--n_resampling', default=50, type=int, help="how many steps when particle filter resampling")
    parser.add_argument('--batch_n_resampling', default=50, type=int, help="how many steps when particle filter resampling")


    #implement info
    parser.add_argument('--focal', default=0.8, type=float)
    parser.add_argument('--D', default=46.0, type=float)
    parser.add_argument('--map_info', default=(360,480), type=tuple)
    parser.add_argument('--G0', default=8, type=int)

    parser.add_argument('--interval', default=100000, type=int)
    # 100,000  500

    parser.add_argument('--N_normalize_weight', default=1, type=int)
    parser.add_argument('--N_HeatMap', default=1, type=int)

    parser.add_argument('--expand', action='store_true',help='expand the number of feature points')
    parser.add_argument('--only_pos', action='store_true', help='only use the positive events')

    return parser





if __name__ == '__main__':
    parser = argparse.ArgumentParser('SLAM with event camera', parents=[get_args_parser()])
    args = parser.parse_args()
    print(args)
    weight_fix_angle(args)
    get_pred_img()