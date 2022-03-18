import os.path

from tqdm import tqdm
from localization.model.particle_filter import ParticleFilter
from localization.model.check_weight import WeightChecker
from util import tools
from util import event as E
from util import load_data as L
import numpy as np
from util.draw import draw_partiles, draw_angle, draw_HeatMap, save_HeatMap
import matplotlib.pyplot as plt
import scipy.io as scio
'''
mydata_v3: gamma 100
mydata_gamma50 : gamma 50
mydata_gamma50_tr: gamma 50, translation first, followed by rotation
'''
save_file = "/data1/zem/graduate_project/Data/mydata_gamma10_tr.mat"


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
    # loop
    events = L.dataLoader('triangle2')
    events_number = len(events)
    event_loader = L.TimeDataIter(events,args.interval)
    feature_points = L.getFeaturePoints('triangle',expand=False)
    filter = ParticleFilter(arg=args,feature_points=feature_points)
    pre_particle = filter.get_particles()
    pose = get_pose(pre_particle)
    draw_partiles(pre_particle, (pose[0], pose[1]))
    draw_angle(pre_particle, pose[2])
    while event_loader.not_end():
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
        if (filter.get_time_step() + 1) % 3000 == 0:
            drawParicle = filter.get_particles()
            pose = get_pose(drawParicle)
            draw_partiles(drawParicle, (pose[0], pose[1]))
            draw_angle(drawParicle,pose[2])

        filter.increment_time()

def weight_fix_angle(args):
    # loop
    events = L.dataLoader('triangle2')
    events_number = len(events)
    event_loader = L.TimeDataIter(events,args.interval)
    feature_points = L.getFeaturePoints('triangle',expand=False)
    checker = WeightChecker(arg=args,feature_points=feature_points)
    outputs = np.zeros((100,51,51),dtype=np.float64)
    for i in tqdm(range(100)):
        event_batch = event_loader.iter_data()
        checker.fix_angle_update(event_batch)
        if (checker.get_time_step() + 1) % args.N_normalize_weight == 0:
            checker.normalize_weight()
        # if (checker.get_time_step() + 1) % args.N_HeatMap == 0:
        #     draw_HeatMap(checker.CurrentWeight)

        outputs[i,:,:] = checker.CurrentWeight

    scio.savemat(save_file,{'mydata':outputs})
    print(f'done in {save_file}')



        #checker.increment_time()

def get_pred_img():
    data = scio.loadmat(save_file)
    mydata = data['mydata']
    for i in tqdm(range(mydata.shape[0])):
        weightmap = mydata[i,:,:]
        save_name = f'{i+1:04}.jpg'
        save_root = "/data1/zem/graduate_project/Data/data_gamma10_tr"
        save_path = os.path.join(save_root,save_name)
        save_HeatMap(weightmap,save_path)


if __name__ == "__main__":
    get_pred_img()
