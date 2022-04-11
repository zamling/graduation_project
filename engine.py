import os.path

from tqdm import tqdm
from localization.model.particle_filter import ParticleFilter
from localization.model.check_weight import WeightChecker
from util import tools
from util import event as E
from util import load_data as L
import numpy as np
from util.draw import draw_partiles, draw_angle, draw_HeatMap, save_HeatMap, save_partiles,save_angle
import matplotlib.pyplot as plt
import scipy.io as scio
'''
mydata_v3: gamma 100
mydata_gamma50 : gamma 50
mydata_gamma50_tr: gamma 50, translation first, followed by rotation
'''
save_file = "/data1/zem/graduate_project/Data/mydata_Expand_5.mat"


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
    events = L.dataLoader('triangle2')
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
    # load all of events
    events = L.dataLoader('triangle2')
    events_number = len(events)
    # generate the events iterator in a certain time interval args.interval
    event_loader = L.TimeDataIter(events,args.interval,is_positive=args.only_pos)
    feature_points = L.getFeaturePoints('triangle',expand=args.expand)
    filter = ParticleFilter(arg=args,feature_points=feature_points)
    # get the initial particles
    pre_particle = filter.get_particles()
    count = 1
    for i in tqdm(range(20000)):
        event_batch = event_loader.iter_data()
        filter.update_with_batch(event_batch,pre_particle)
        pre_particle = filter.get_particles()
        if (filter.get_time_step() + 1) % args.batch_n_resampling == 0:
            filter.resampling(noisy=True)
        if (filter.get_time_step() + 1) % 200 == 0:
            drawParicle = filter.get_particles()
            pose = get_pose(drawParicle)
            current = event_loader.currentEvent()
            print("\n[Time Step]: {}, current event: [{}/{}]".format(filter.get_time_step(),current,events_number))
            print("current pose: {}".format(pose))
        # save the particle results
        if (filter.get_time_step() + 1) % 200 == 0:
            drawParicle = filter.get_particles()
            pose = get_pose(drawParicle)
            name = f'{count:04}.jpg'
            name_angle = f'A{count:04}.jpg'
            save_partiles(drawParicle, (pose[0], pose[1]),name)
            count += 1
            # save_angle(drawParicle,pose[2],name_angle)
        # if (filter.get_time_step() + 1) % 2000 == 0:
        #     drawParicle = filter.get_particles()
        #     pose = get_pose(drawParicle)
        #     # name = f'{count:04}.jpg'
        #     draw_partiles(drawParicle, (pose[0], pose[1]))
        #     # count += 1
        #     draw_angle(drawParicle,pose[2])

        filter.increment_time()

def weight_fix_angle(args):
    # load all of events
    events = L.dataLoader('triangle2')
    # generate the events iterator in a certain time interval args.interval
    event_loader = L.TimeDataIter(events,args.interval,is_positive=args.only_pos)
    # get feature points
    feature_points = L.getFeaturePoints('triangle',expand=args.expand)
    checker = WeightChecker(arg=args,feature_points=feature_points)
    # grid the whole map 51 by 51 [-25,25] for each coordinate
    outputs = np.zeros((100,51,51),dtype=np.float64)
    for i in tqdm(range(100)):
        event_batch = event_loader.iter_data()
        checker.fix_angle_update(event_batch)
        if (checker.get_time_step() + 1) % args.N_normalize_weight == 0:
            checker.normalize_weight()

        outputs[i,:,:] = checker.CurrentWeight

    scio.savemat(save_file,{'mydata':outputs})
    print(f'done in {save_file}')


def get_pred_img():
    data = scio.loadmat(save_file)
    mydata = data['mydata']
    for i in tqdm(range(mydata.shape[0])):
        weightmap = mydata[i,:,:]
        save_name = f'{i+1:04}.jpg'
        save_root = "/data1/zem/graduate_project/Data/data_Expand_5"
        save_path = os.path.join(save_root,save_name)
        save_HeatMap(weightmap,save_path)


if __name__ == "__main__":
    get_pred_img()
