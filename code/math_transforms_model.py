'''
author : sunyan
'''

import math

class math_transforms(object):
    #ipark input
    theta = 0.0
    Ud = 0.0
    Uq = 0.0
    #clark input
    I_a = 0.0
    I_b = 0.0
    I_c = 0.0
    #plark input
    
    #ipark output
    Ualpha = 0.0
    Ubeta = 0.0
    #clark output
    I_alpha = 0.0
    I_beta = 0.0
    #plark output
    I_d = 0.0
    I_q = 0.0
    
    
    def ipark_cal(self):
        self.Ualpha = math.cos(self.theta) * self.Ud - math.sin(self.theta) * self.Uq
        self.Ubeta = math.sin(self.theta) * self.Ud + math.cos(self.theta) * self.Uq
        
    def clark_cal(self):
        self.I_alpha = (self.I_a - 0.5 * (self.I_b + self.I_c)) * 2 / 3
        self.I_beta = math.sqrt(3) / 2 * (self.I_b - self.I_c) * 2 / 3
        
    def plark_cal(self):
        self.I_d = self.I_alpha * math.cos(self.theta) + self.I_beta * math.sin(self.theta)
        self.I_q = -self.I_alpha * math.sin(self.theta) + self.I_beta * math.cos(self.theta)
        
    def current_3s_to_2r(self):
        self.clark_cal()
        self.plark_cal()