'''
author : sunyan
'''

import math

class PI(object):
    TS = 0.0
    #speed pi
    spd_ref = 0.0
    spd_fb = 0.0
    
    spd_kp = 0.0
    spd_ki = 0.0
    spd_Ba = 0.0
    
    spd_up_limit = 0.0
    spd_low_limit = 0.0
    
    spd_ki_out = 0.0
    
    spd_pi_out = 0.0
    
    #id pi
    i_d_ref = 0.0
    i_d_fb = 0.0
    
    i_d_kp = 0.0
    i_d_ki = 0.0
    
    i_d_up_limit = 0.0
    i_d_low_limit = 0.0
    
    i_d_ki_out = 0.0
    
    i_d_pi_out = 0.0
    
    #id pi
    i_q_ref = 0.0
    i_q_fb = 0.0
    
    i_q_kp = 0.0
    i_q_ki = 0.0
    
    i_q_up_limit = 0.0
    i_q_low_limit = 0.0
    
    i_q_ki_out = 0.0
    
    i_q_pi_out = 0.0
    
    
    def __init__(self):
        self.spd_kp = 0.14
        self.spd_ki = 0.14 * 50
        self.spd_Ba = 0.013
        self.spd_up_limit = 30
        self.spd_low_limit = -30
        self.spd_ki_out = 0.0
        self.i_d_kp = 0.0085 * 1100
        self.i_d_ki = 2.875 * 1100
        self.i_d_up_limit = 311 * 0.9 * math.sqrt(1 / 3)
        self.i_d_low_limit = -311 * 0.9 * math.sqrt(1 / 3)
        self.i_d_ki_out = 0.0
        self.i_q_kp = 0.0085 * 1100
        self.i_q_ki = 2.875 * 1100
        self.i_q_up_limit = 311 * 0.9 * math.sqrt(1 / 3)
        self.i_q_low_limit = -311 * 0.9 * math.sqrt(1 / 3)
        self.i_q_ki_out = 0.0
        
    def spd_pi_cal(self):
        err = self.spd_ref - self.spd_fb
        kp_out = err * self.spd_kp
        self.spd_ki_out = self.spd_ki_out + err * self.spd_ki * self.TS
        pi_out_tmp = kp_out + self.spd_ki_out - err * self.spd_Ba
        if(pi_out_tmp > self.spd_up_limit):
            self.spd_pi_out = self.spd_up_limit
        elif(pi_out_tmp < self.spd_low_limit):
            self.spd_pi_out = self.spd_low_limit
        else:
            self.spd_pi_out = pi_out_tmp
            
    def I_d_pi_cal(self):
        err = self.i_d_ref - self.i_d_fb
        kp_out = err * self.i_d_kp
        self.i_d_ki_out = self.i_d_ki_out + err * self.i_d_ki * self.TS
        pi_out_tmp = kp_out + self.i_d_ki_out
        if(pi_out_tmp > self.i_d_up_limit):
            self.i_d_pi_out = self.i_d_up_limit
        elif(pi_out_tmp < self.i_d_low_limit):
            self.i_d_pi_out = self.i_d_low_limit
        else:
            self.i_d_pi_out = pi_out_tmp
        
    def I_q_pi_cal(self):
        err = self.i_q_ref - self.i_q_fb
        kp_out = err * self.i_q_kp
        self.i_q_ki_out = self.i_q_ki_out + err * self.i_q_ki * self.TS
        pi_out_tmp = kp_out + self.i_q_ki_out
        if(pi_out_tmp > self.i_q_up_limit):
            self.i_q_pi_out = self.i_q_up_limit
        elif(pi_out_tmp < self.i_q_low_limit):
            self.i_q_pi_out = self.i_q_low_limit
        else:
            self.i_q_pi_out = pi_out_tmp