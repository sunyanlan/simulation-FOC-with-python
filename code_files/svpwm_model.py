'''
author : sunyan
'''

import math

class SVPWM(object):
    #input
    u_alpha = 0.0
    u_beta = 0.0
    Tpwm = 0.0
    Udc = 0.0
    
    #output
    Sa = 0
    Sb = 0
    Sc = 0
    
    N = 0
    X = 0.0
    Y = 0.0
    Z = 0.0
    T1 = 0.0
    T2 = 0.0
    Tcm1 = 0.0
    Tcm2 = 0.0
    Tcm3 = 0.0
    wave = 0.0
    min_step = 0.0
    up_flg = 1
    down_flg = 0
    
    Ua = 0.0
    Ub = 0.0
    Uc = 0.0
    
    def __init__(self):
        self.step_num = 1
        self.Tpwm = 0.0001
    
    def Sector_Caculate(self):
        if(self.u_beta >= 0):
            u1 = 1
        else:
            u1 = 0
        if((self.u_alpha * math.sqrt(3 / 4) - 0.5 * self.u_beta) >= 0):
            u2 = 1
        else:
            u2 = 0
        if((-self.u_alpha * math.sqrt(3 / 4) - self.u_beta * 0.5) >= 0):
            u3 = 1
        else:
            u3 = 0
        self.N = 4 * u3 + 2 * u2 + u1
        
    def XYZ_Caculate_no_pwm(self):
        self.X = self.u_beta * math.sqrt(3)
        self.Y = self.u_beta * math.sqrt(3) / 2 + self.u_alpha * 3 / 2
        self.Z = self.u_beta * math.sqrt(3) / 2 - self.u_alpha * 3 / 2
        
    def XYZ_Caculate(self):
        self.X = self.u_beta * math.sqrt(3) * self.Tpwm / self.Udc
        self.Y = (self.u_beta * math.sqrt(3) / 2 + self.u_alpha * 3 / 2) * self.Tpwm / self.Udc
        self.Z = (self.u_beta * math.sqrt(3) / 2 - self.u_alpha * 3 / 2) * self.Tpwm / self.Udc
        
    def T1T1_Caculate(self):
        if(self.N == 1):
            T1 = self.Z
        elif(self.N == 2):
            T1 = self.Y
        elif(self.N == 3):
            T1 = -self.Z
        elif(self.N == 4):
            T1 = -self.X
        elif(self.N == 5):
            T1 = self.X
        elif(self.N == 6):
            T1 = -self.Y
        else:
            T1 = -self.Y
            
        if(self.N == 1):
            T2 = self.Y
        elif(self.N == 2):
            T2 = -self.X
        elif(self.N == 3):
            T2 = self.X
        elif(self.N == 4):
            T2 = self.Z
        elif(self.N == 5):
            T2 = -self.Y
        elif(self.N == 6):
            T2 = -self.Z
        else:
            T2 = -self.Z
        
        if((self.Tpwm - T2 - T1) >= 0):
            self.T1 = T1
        else:
            self.T1 = (T1 * self.Tpwm) / (T1 + T2)
            
        if((self.Tpwm - T2 - T1) >= 0):
            self.T2 = T2
        else:
            self.T2 = (T2 * self.Tpwm) / (T1 + T2)
        
    def T1T1_Caculate_no_pwm(self):
        if(self.N == 1):
            T1 = self.Z
        elif(self.N == 2):
            T1 = self.Y
        elif(self.N == 3):
            T1 = -self.Z
        elif(self.N == 4):
            T1 = -self.X
        elif(self.N == 5):
            T1 = self.X
        elif(self.N == 6):
            T1 = -self.Y
        else:
            T1 = -self.Y
            
        if(self.N == 1):
            T2 = self.Y
        elif(self.N == 2):
            T2 = -self.X
        elif(self.N == 3):
            T2 = self.X
        elif(self.N == 4):
            T2 = self.Z
        elif(self.N == 5):
            T2 = -self.Y
        elif(self.N == 6):
            T2 = -self.Z
        else:
            T2 = -self.Z
        
        if((self.Udc - T2 - T1) >= 0):
            self.T1 = T1
        else:
            self.T1 = (T1 * self.Udc) / (T1 + T2)
            
        if((self.Udc - T2 - T1) >= 0):
            self.T2 = T2
        else:
            self.T2 = (T2 * self.Udc) / (T1 + T2)
        
    def Tcm_Caculate(self):
        te_u1 = (self.Tpwm - self.T1 - self.T2) / 4
        te_u2 = (self.Tpwm + self.T1 - self.T2) / 4
        te_u3 = (self.Tpwm + self.T1 + self.T2) / 4
        
        if((self.N == 1) or (self.N == 6)):
            self.Tcm1 = te_u2
        elif((self.N == 2) or (self.N == 3)):
            self.Tcm1 = te_u1
        elif((self.N == 4) or (self.N == 5)):
            self.Tcm1 = te_u3
        else:
            self.Tcm1 = te_u2
        
        if((self.N == 1) or (self.N == 5)):
            self.Tcm2 = te_u1
        elif((self.N == 2) or (self.N == 6)):
            self.Tcm2 = te_u3
        elif((self.N == 3) or (self.N == 4)):
            self.Tcm2 = te_u2
        else:
            self.Tcm2 = te_u3
        
        if((self.N == 1) or (self.N == 3)):
            self.Tcm3 = te_u3
        elif((self.N == 2) or (self.N == 5)):
            self.Tcm3 = te_u2
        elif((self.N == 4) or (self.N == 6)):
            self.Tcm3 = te_u1
        else:
            self.Tcm3 = te_u1
            
    def Tcm_Caculate_no_pwm(self):
        te_u1 = (self.Udc - self.T1 - self.T2)
        te_u2 = (self.Udc + self.T1 - self.T2)
        te_u3 = (self.Udc + self.T1 + self.T2)
        
        if((self.N == 1) or (self.N == 6)):
            self.Tcm1 = te_u2
        elif((self.N == 2) or (self.N == 3)):
            self.Tcm1 = te_u1
        elif((self.N == 4) or (self.N == 5)):
            self.Tcm1 = te_u3
        else:
            self.Tcm1 = te_u2
        
        if((self.N == 1) or (self.N == 5)):
            self.Tcm2 = te_u1
        elif((self.N == 2) or (self.N == 6)):
            self.Tcm2 = te_u3
        elif((self.N == 3) or (self.N == 4)):
            self.Tcm2 = te_u2
        else:
            self.Tcm2 = te_u3
        
        if((self.N == 1) or (self.N == 3)):
            self.Tcm3 = te_u3
        elif((self.N == 2) or (self.N == 5)):
            self.Tcm3 = te_u2
        elif((self.N == 4) or (self.N == 6)):
            self.Tcm3 = te_u1
        else:
            self.Tcm3 = te_u1
    
    def triangular_wave(self):
        if(self.up_flg):
            self.wave = self.wave + self.min_step
        elif(self.down_flg):
            self.wave = self.wave - self.min_step
            
        if(self.wave > (self.Tpwm / 2 - self.min_step)):
            self.up_flg = 0
            self.down_flg = 1
        elif(self.wave < self.min_step):
            self.up_flg = 1
            self.down_flg = 0
    
    def Tcm123_Sabc(self):
        if((self.wave - self.Tcm1) >= 0.0):
            self.Sa = 1
        else:
            self.Sa = 0
        if((self.wave - self.Tcm2) >= 0.0):
            self.Sb = 1
        else:
            self.Sb = 0
        if((self.wave - self.Tcm3) >= 0.0):
            self.Sc = 1
        else:
            self.Sc = 0
            
    def svpwm_synth_out_sa_sb_sc(self, u_alpha, u_beta, Tpwm, Udc, min_step):
        self.u_alpha = u_alpha
        self.u_beta = u_beta
        self.Tpwm = Tpwm
        self.Udc = Udc
        self.min_step = min_step
        self.Sector_Caculate()
        self.XYZ_Caculate()
        self.T1T1_Caculate()
        self.Tcm_Caculate()
        self.triangular_wave()
        self.Tcm123_Sabc()
        
    def svpwm_synth_out_ua_ub_uc(self, u_alpha, u_beta, Tpwm, Udc, min_step):
        self.svpwm_synth_out_sa_sb_sc(u_alpha, u_beta, Tpwm, Udc, min_step)
        self.Ua = (1 / 3) * self.Udc * (2 * self.Sa - self.Sb - self.Sc)
        self.Ub = (1 / 3) * self.Udc * (-self.Sa + 2 * self.Sb - self.Sc)
        self.Uc = (1 / 3) * self.Udc * (-self.Sa - self.Sb + 2 * self.Sc)
        
    def svpwm_synth_no_pwm(self, u_alpha, u_beta, Udc):
        self.u_alpha = u_alpha
        self.u_beta = u_beta
        self.Tpwm = 1.0
        self.Udc = Udc
        self.Sector_Caculate()
        self.XYZ_Caculate_no_pwm()
        self.T1T1_Caculate_no_pwm()
        self.Tcm_Caculate_no_pwm()
        self.Ua = (self.Udc - self.Tcm1) / 2.0
        self.Ub = (self.Udc - self.Tcm2) / 2.0
        self.Uc = (self.Udc - self.Tcm3) / 2.0
    
    