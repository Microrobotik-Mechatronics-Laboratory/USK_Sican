import os; os.environ.setdefault('MUJOCO_GL','egl')
import numpy as np, mujoco, imageio.v2 as imageio, walk, rig
from PIL import Image
BONES=walk.BONES; Rg=walk.Rg; L=walk.L
BCOL='.93 .90 .83 1'
assets="".join(f'<mesh name="{b}" file="{b}.obj"/>' for b in BONES)
mocaps="".join(f'<body name="{b}" mocap="true"><geom type="mesh" mesh="{b}" rgba="{BCOL}"/></body>' for b in BONES)
TR=2*0.4/L   # texrepeat so one tile == one stride L (seamless scroll)
xml=f'''<mujoco><compiler meshdir="obj" angle="radian"/>
<visual><global offwidth="{{S}}" offheight="{{S}}"/>
<headlight ambient="0.42 0.42 0.44" diffuse="0.55 0.55 0.55" specular="0.15 0.15 0.15"/><quality shadowsize="4096"/></visual>
<asset>
<texture name="sky" type="skybox" builtin="gradient" rgb1="0.16 0.17 0.20" rgb2="0.05 0.05 0.07" width="256" height="256"/>
<texture name="grid" type="2d" builtin="checker" rgb1="0.22 0.23 0.26" rgb2="0.17 0.18 0.21" width="512" height="512"/>
<material name="grid" texture="grid" texrepeat="{TR:.4f} {TR:.4f}" reflectance="0.05"/>
{assets}</asset>
<worldbody><light pos="0.06 0.05 0.4" dir="-0.1 -0.1 -1" diffuse="0.6 0.6 0.6" specular="0.2 0.2 0.2"/>
<geom name="floor" type="plane" pos="0 0 {walk.FLOOR}" size="0.5 0.5 0.01" material="grid"/>
{mocaps}</worldbody></mujoco>'''

def render(N,S,fps,gifname,stillname=None):
    cs,me=walk.solve_cycle(N)
    m=mujoco.MjModel.from_xml_string(xml.replace('{S}',str(S)))
    d=mujoco.MjData(m)
    fid=mujoco.mj_name2id(m,mujoco.mjtObj.mjOBJ_GEOM,'floor')
    # camera centered on hip/stride
    hp=walk.hip_world(rig.defaults); ctrx=hp[0]-L*0.3
    cam=mujoco.MjvCamera(); cam.type=mujoco.mjtCamera.mjCAMERA_FREE
    cam.lookat[:]=[ctrx, hp[1], (hp[2]+walk.FLOOR)/2+0.004]; cam.distance=0.125; cam.azimuth=90; cam.elevation=-6
    r=mujoco.Renderer(m,S,S); frames=[]
    for i in range(N):
        phi=i/N
        m.geom_pos[fid][0]=-L*phi           # scroll belt backward
        W=rig.fk(cs[i])
        for j,b in enumerate(BONES):
            T=W[b]; d.mocap_pos[j]=Rg@T[:3,3]; d.mocap_quat[j]=rig.mat2quat(Rg@T[:3,:3])
        mujoco.mj_forward(m,d); r.update_scene(d,cam); frames.append(r.render())
    del r
    imageio.mimsave(gifname,frames,duration=1/fps,loop=0)
    if stillname: Image.fromarray(frames[N//3]).resize((500,500),Image.LANCZOS).save(stillname)
    return frames,me

if __name__=='__main__':
    fr,me=render(8,560,10,'walk_strip_tmp.gif')
    import numpy as np
    Image.fromarray(np.concatenate(fr,axis=1)).save('walk_strip.png')
    print('strip frames',len(fr),'max IK err mm',round(me*1000,3))
