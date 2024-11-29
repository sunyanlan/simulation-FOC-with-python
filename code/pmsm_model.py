'''
author : sunyan
'''

import math

class PMSM(object):
    id = 0.0
    iq = 0.0
    
    wm = 0.0
    theta = 0.0
    
    ia = 0.0
    ib = 0.0
    ic = 0.0
    
    TS = 0.001
    TL = 0.0
    
    ud = 0.0
    uq = 0.0
    
    ua = 0.0
    ub = 0.0
    uc = 0.0
    
    speed_rpm = 0.0
    
    R = 0.0
    Ld = 0.0
    Lq = 0.0
    Pn = 0.0
    Phi = 0.0
    J = 0.0
    B = 0.0
    
    
    def __init__(self):
        self.R = 2.875
        self.Ld = 0.0085
        self.Lq = 0.0085
        self.Pn = 4.0
        self.Phi = 0.175
        self.J = 0.001
        self.B = 0.008
        
    def pmsm_model_i_dq(self):
        self.id = self.id + ((1 / self.Ld) * self.ud - (self.R / self.Ld) * self.id + (self.Lq / self.Ld) * self.Pn * self.iq * self.wm) * self.TS
        self.iq = self.iq + ((1 / self.Lq) * self.uq - (self.R / self.Lq) * self.iq - (self.Ld / self.Lq) * self.Pn * self.wm * self.id - (self.Phi * self.Pn / self.Lq) * self.wm) * self.TS
        self.wm = self.wm + ((1 / self.J) * (1.5 * self.Pn * (self.Phi * self.iq + (self.Ld - self.Lq) * self.iq * self.id) - self.B * self.wm - self.TL)) * self.TS
        self.theta = self.theta + self.wm * self.Pn * self.TS
        self.speed_rpm = self.wm * 30.0 / math.pi
        
    def pmsm_model_i_dq2abc(self):
        self.ia = self.id * (2 / 3) * math.cos(self.theta) - self.iq * (2 / 3) * math.sin(self.theta)
        self.ib = self.id * ((-math.cos(self.theta) / 2) + (math.sqrt(3) / 2 * math.sin(self.theta))) * (2 / 3) + self.iq * ((math.sin(self.theta) / 2)+(math.sqrt(3) / 2 * math.cos(self.theta))) * (2 / 3)
        self.ic = self.id * ((-math.cos(self.theta) / 2) - (math.sqrt(3) / 2 * math.sin(self.theta))) * (2 / 3) + self.iq * ((math.sin(self.theta) / 2) - (math.sqrt(3) / 2 * math.cos(self.theta))) * (2 / 3)
        
    def pmsm_u_abc2dq(self):
        self.ud = self.ua * math.cos(self.theta) * 2 / 3 + self.ub * (-0.5 * math.cos(self.theta) + (math.sqrt(3) / 2) * math.sin(self.theta)) * 2 / 3 + self.uc * (-0.5 * math.cos(self.theta) - (math.sqrt(3) / 2) * math.sin(self.theta)) * 2 / 3
        self.uq = self.ua * -math.sin(self.theta) * 2 / 3 + self.ub * (0.5 * math.sin(self.theta) + (math.sqrt(3) / 2) * math.cos(self.theta)) * 2 / 3 + self.uc * (0.5 * math.sin(self.theta) - (math.sqrt(3) / 2) * math.cos(self.theta)) * 2 / 3
        
    def pmsm_model_3s(self, ua, ub, uc, TL, TS):
        self.ua = ua
        self.ub = ub
        self.uc = uc
        self.TL = TL
        self.TS = TS
        self.pmsm_u_abc2dq()
        self.pmsm_model_i_dq()
        self.pmsm_model_i_dq2abc()





