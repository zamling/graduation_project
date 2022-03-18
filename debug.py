import argparse
from engine import main, main_batch, weight_fix_angle
import os.path
from tqdm import tqdm
from localization.model.particle_filter import ParticleFilter
from localization.model.check_weight import WeightChecker
from util import tools
from util import event as E
from util import load_data as L
import numpy as np
from util.draw import draw_partiles, draw_angle, draw_HeatMap, save_HeatMap

def get_args_parser():
    parser = argparse.ArgumentParser('Set transformer detector', add_help=False)
    #particle filter
    parser.add_argument('--n_particles', default=500, type=int)
    parser.add_argument('--gamma', default=100, type=float,help="the parameter in equation 12")
    parser.add_argument('--n_resampling', default=100, type=int, help="how many steps when particle filter resampling")
    parser.add_argument('--batch_n_resampling', default=50, type=int, help="how many steps when particle filter resampling")
    #implement info
    parser.add_argument('--focal', default=0.8, type=float)
    parser.add_argument('--D', default=46.0, type=float)
    parser.add_argument('--map_info', default=(360,480), type=tuple)
    parser.add_argument('--G0', default=8, type=int)

    parser.add_argument('--interval', default=100000, type=int)

    parser.add_argument('--N_normalize_weight', default=1, type=int)
    parser.add_argument('--N_HeatMap', default=1, type=int)
    parser.add_argument('--debug_type', default='transform', type=str)
    return parser

def check_transform(args,pixel_pos,img_pos=None,pose=None):
    transform = tools.Transform(args)
    pix_x, pix_y = pixel_pos
    img_ = transform.pixel2image(pix_x,pix_y)
    print('img: {}'.format(img_))
    if img_pos is not None:
        img_ = img_pos
    if pose is None:
        pose = E.Pose(0,0,0)
    img_x, img_y, img_z = img_
    x,y,z = transform.image2ref(img_x,img_y,img_z,pose)
    print("Refer: x = {}, y={}, z={}".format(x,y,z))

# TODO: cost function

def cost_matrix(args):
    events = L.dataLoader('triangle2')
    events_number = len(events)
    event_loader = L.TimeDataIter(events,args.interval)
    feature_points = L.getFeaturePoints('triangle',expand=False)
    checker = WeightChecker(arg=args,feature_points=feature_points)
    outputs = np.zeros((100,51,51),dtype=np.float64)
    event_batch = event_loader.iter_data()
    min_h_map,each_update_map,update_map = checker.check_costMatrix(event_batch)
    print(f'FOR min_h_map: max: {min_h_map.max()}, min: {min_h_map.min()}, shape: {min_h_map.shape}')
    print(f'FOR each_update_map: max: {each_update_map.max()}, min: {each_update_map.min()}, shape: {each_update_map.shape}')
    print(f'FOR update_map: max: {update_map.max()}, min: {update_map.min()}, shape: {update_map.shape}')



if __name__ == "__main__":
    parser = argparse.ArgumentParser('SLAM with event camera', parents=[get_args_parser()])
    args = parser.parse_args()
    if args.debug_type == 'transform':
        pose = E.Pose(0,0,np.pi/2)
        check_transform(args,(0,0),(3,4,5),pose)
    if args.debug_type == 'cost':
        cost_matrix(args)

