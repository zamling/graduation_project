import util.event as E
import numpy as np

def distance(p,q):
    p_x,p_y = p
    q_x, q_y = q
    return np.sqrt(np.square((p_x-q_x))+np.square((p_y-q_y)))

def get_alpha():

    pass

class ParticleFilter:
    def __init__(self,arg,feature_points):
        self.n_particles = arg.n_particles
        self.map_info = arg.map_info
        self.particles = E.Particle()
        self.time_step = 0
        self.events = []
        self.gamma = arg.gamma
        self.D = arg.D
        self.feature_points = feature_points
        self.f = arg.focal_d
        #format of feature points [(1,2),(2,3),...]

        self.init_particle()

    def init_particle(self):
        h_max,w_max = self.map_info
        particles = []
        for i in range(self.n_particles):
            x = np.random.rand() * h_max
            y = np.random.rand() * w_max
            new_particle = E.Pose(x,y)
            particles.append(new_particle)
        scores = self.update_scores()

        self.particles.update_Pose(0,particles)
        self.particles.update_Score(0, scores)

    def find_min(self,r,e):
        #F_H(r)
        cur_min = None
        for feature_ in self.feature_points:
            x = distance(feature_,e)
            h = x*self.D/r

            if cur_min is None:
                cur_min = h
            else:
                if h < cur_min:
                    cur_min = h
        return cur_min

    def update_scores(self):
        pre_scores = self.particles.get_k_Particle(self.time_step)["scores"]
        new_scores = np.zeros((self.n_particles))
        # min d_{ray}(r,h)
        '''
        we have known all of feature points in this map, and here, we compare the event
        '''
        r = np.zeros((self.n_particles,))
        params = self.events[-1].get_param
        e_x = params['x']
        e_y = params['y']
        current_poses = self.particles.get_k_Particle(self.time_step+1)["poses"]
        assert len(current_poses)==self.n_particles, "some wrong in _history"
        for i,p in enumerate(current_poses):
            p_x,p_y = p.state
            p_e_d = distance((e_x,e_y),(p_x,p_y))
            Wpx = p_e_d/self.f
            r = np.sqrt((np.square(self.D)+np.square(p_e_d)))
            min_h = self.find_min(r,(e_x,e_y))
            update_number = np.exp(-1/2*np.square(min_h/(self.gamma*Wpx)))
            alpha = 0.5 #need to change!!!!!!!
            new_scores[i] = pre_scores[i] + alpha* update_number
        self.particles.update_Score(self.time_step+1, new_scores)
        return new_scores


    def increment_time(self):
        self.time_step += 1
        pass

    def update_poses(self,delta_r):
        pre_pose = self.particles.get_k_Particle(self.time_step)["poses"]
        Poses = []
        for i in range(self.n_particles):
            M_x = np.random.normal(loc=0, scale=delta_r)
            M_y = np.random.normal(loc=0, scale=delta_r)
            pre_x,pre_y = pre_pose[i].state
            x = pre_x + M_x
            y = pre_y + M_y
            new_Pose = E.Pose(x, y)
            Poses.append(new_Pose)
        self.particles.update_Pose(self.time_step+1,Poses)
        return Poses

    def get_time_step(self):
        return self.time_step


    def update_event(self,event):
        new_event = event
        self.events.append(new_event)

# if __name__ == "__name__":
#
# #loop
#     filter = ParticleFilter(arg=)
#
#     filter.update_event(event)
#
#     filter.update_poses()
#
#     filter.update_scores() # here the time step + 1



