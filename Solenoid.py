import vpython as vp
import numpy as np

class SolenoidClass():

    def __init__(self, pos, ori, rad, thi, I, no_of_seg, turns = 1):

        self.pos = pos
        self.ori = ori
        self.rad = rad
        self.thi = thi
        self.I= I
        self.no_of_seg = no_of_seg
        self.turns = turns

        self.ring = vp.ring(pos = self.pos, axis = self.ori, radius = self.rad, thickness = self.thi)
        element_length = (2 * np.pi * self.rad) / self.no_of_seg
        segments = [0]*(self.no_of_seg)

        for i in range(self.no_of_seg):
            theta = i * (2 * np.pi / self.no_of_seg)
            y = self.rad * np.cos(theta)
            z = self.rad * np.sin(theta)

            segments[i] = vp.cylinder(pos = vp.vec(self.pos.x, self.pos.y + y, self.pos.z + z), axis = element_length * vp.vec(0,-vp.sin(theta),vp.cos(theta)), radius = self.thi)
            segments[i].visible = False
        
        self.segments = segments
        print('done')


