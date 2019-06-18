from Solenoid import SolenoidClass
import vpython as vp
import numpy as np
import _thread

start = False

solenoid_list = []

def Standard():
    solenoid_list.append(SolenoidClass(vp.vec(-30,0,0), vp.vec(1,0,0), 10, 1, 1000, 100))
    solenoid_list.append(SolenoidClass(vp.vec(30,0,0), vp.vec(1,0,0), 10, 1, 1000, 100))

vp.button(bind = Standard, text= 'standard for testing')



Electrons = []
elec_vel = 1e6

def Electron():
    
    e = vp.sphere(pos = vp.vec(0,5,0), radius = 0.3, color=vp.color.red, make_trail = True, retain = 250)
    e.velocity = elec_vel * vp.vec(1,.3,.3)  #need to do angle thing
    Electrons.append(e)
    print('done')

vp.button(bind = Electron, text = 'create Electron')


total_steps = 10000
q = -1.6e-19    
m = 9.11e-31 
dt = 1e-8
mu_0 = 2*np.pi*1e-7
paths = []

def Path_Calc():
    global paths
    paths = [[0]*total_steps]*len(Electrons)
    for i in range(len(Electrons)):
        paths[i][0] = Electrons[i].pos
        velocity = Electrons[i].velocity
        for j in range(1, total_steps):
            
            B = vp.vec(0,0,0)
            for solenoid in solenoid_list:
                for k in range(solenoid.no_of_seg):
                    r = paths[i][j-1] - solenoid.segments[k].pos
                    dB = (mu_0 * solenoid.I /(4*np.pi)) * solenoid.segments[k].axis.cross(r) / r.mag**3
                    B = B + dB
            
            
            F = q * velocity.cross(B)
            velocity += (F * dt) / m
            
            paths[i][j] = paths[i][j-1] + velocity*dt
    
    #print(paths)
    print('done')

def new_thread():
    _thread.start_new_thread(Path_Calc)

vp.button(bind = new_thread, text = 'Path Calc')


start = False

def Go():
    global start
    start = True

vp.button(bind = Go, text = 'go')

time = 0
while time < total_steps:
    if start == False:
        vp.sleep(1)
        continue
    vp.rate(300)
    
    for j in range(len(Electrons)):
        Electrons[j].pos = paths[j][time]
    
    time += 1
    #print('step')
            




        