import argparse
from engine import main, main_batch, weight_fix_angle, get_pred_img

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

    parser.add_argument('--interval', default=500, type=int)
    # 100,000  500

    parser.add_argument('--N_normalize_weight', default=1, type=int)
    parser.add_argument('--N_HeatMap', default=1, type=int)

    parser.add_argument('--data_root', default="/data1/zem/graduate_project/Data", type=str)
    parser.add_argument('--save_root', default="/data1/zem/graduate_project/Data/exp_3", type=str)

    parser.add_argument('--expand', action='store_true', help='expand the number of feature points')
    parser.add_argument('--only_pos', action='store_true', help='only use the positive events')


    return parser

# TODO: check angle (no problem), only positive (no effect), expanding feature points, adjust angle random walk



if __name__ == '__main__':

    parser = argparse.ArgumentParser('SLAM with event camera', parents=[get_args_parser()])
    args = parser.parse_args()
    print(args)
    # main(args)
    print('events data root is: ', args.data_root)
    print('image saved root is: ', args.save_root)
    main_batch(args)



    # feats = L.getFeaturePoints('triangle')
    # print(feats)
    # transform = tools.Transform(args)
    # pose = E.Pose(0,0,0)
    # x,y,z = transform.image2ref(3,4,5,pose)
    # print("x = {}, y={}, z={}".format(x,y,z))


