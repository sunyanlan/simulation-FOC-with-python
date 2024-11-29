'''
author : sunyan
'''

import pmsm_model
import svpwm_model
import PI_model
import math_transforms_model
import matplotlib.pyplot as plt
import math


def pmsm_mode_sim():
    TS = 0.00001
    max_time = 1.0
    
    TL_turn = 0.1

    time = []
    
    plot_rpm = []
    
    plot_ia = []
    plot_ib = []
    plot_ic = []
    
    plot_theta = []
    
    plot_ua = []
    plot_ub = []
    plot_uc = []
    
    pm_pi = PI_model.PI()
    pm_tf = math_transforms_model.math_transforms()
    pm_sv = svpwm_model.SVPWM()
    pm_mo = pmsm_model.PMSM()
    
    pm_pi.spd_ref = 0.1
    pm_pi.TS = TS
    
    pm_pi.spd_fb = pm_mo.speed_rpm
    
    
    for i in range(0, int(max_time / TS)):
        t = i * TS
        time.append(t)
        
        if(pm_pi.spd_ref < 1000.0):
            pm_pi.spd_ref = pm_pi.spd_ref + 0.03
        else:
            pm_pi.spd_ref = 1000.0
        
        if((i > int(TL_turn / TS)) and (TL < 10.0)):
            TL = TL + 0.0002
        elif(i < int(TL_turn / TS)):
            TL = 0.5
        
        pm_pi.spd_fb = pm_mo.speed_rpm
        pm_pi.spd_pi_cal()
        pm_pi.i_q_ref = pm_pi.spd_pi_out
        pm_pi.i_q_fb = pm_tf.I_q
        pm_pi.I_q_pi_cal()
        pm_pi.i_d_ref = 0.0
        pm_pi.i_d_fb = pm_tf.I_d
        pm_pi.I_d_pi_cal()
            
        pm_tf.Ud = pm_pi.i_d_pi_out
        pm_tf.Uq = pm_pi.i_q_pi_out
        pm_tf.theta = pm_mo.theta
        pm_tf.ipark_cal()
        
        pm_sv.svpwm_synth_no_pwm(pm_tf.Ualpha, pm_tf.Ubeta, 311)
        
        pm_mo.pmsm_model_3s(pm_sv.Ua, pm_sv.Ub, pm_sv.Uc, TL, TS)
        pm_tf.I_a = pm_mo.ia
        pm_tf.I_b = pm_mo.ib
        pm_tf.I_c = pm_mo.ic
        pm_tf.current_3s_to_2r()
        
        plot_rpm.append(pm_mo.speed_rpm)
        plot_ia.append(pm_mo.ia)
        plot_ib.append(pm_mo.ib)
        plot_ic.append(pm_mo.ic)
        plot_theta.append(pm_mo.theta % (2 * math.pi))
        plot_ua.append(pm_sv.Ua)
        plot_ub.append(pm_sv.Ub)
        plot_uc.append(pm_sv.Uc)
    
    ig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
    ax1.plot(time, plot_rpm)
    ax1.grid()
    ax2.plot(time, plot_ia, label='ia')
    ax2.plot(time, plot_ib, label='ib')
    ax2.plot(time, plot_ic, label='ic')
    ax2.legend(loc='upper right')
    ax2.grid()
    ax3.plot(time, plot_theta)
    ax3.grid()
    
    #ig, (ax1) = plt.subplots(1, 1, sharex=True)
    #ax1.plot(time, plot_ua)
    #ax1.plot(time, plot_ub)
    #ax1.plot(time, plot_uc)
    #ax1.grid()
    
    plt.show()

def main():
    pmsm_mode_sim()

if __name__ == "__main__":
    main()
