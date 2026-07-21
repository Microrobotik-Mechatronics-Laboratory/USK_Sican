import os; os.environ.setdefault('MUJOCO_GL','egl')
import numpy as np, mujoco, imageio.v2 as imageio, rig
BONES=['spine','pelvis','femur','tibia','foot']
Rg=np.array([[1,0,0],[0,0,-1],[0,1,0]],float)
footV=__import__('meshio').read('obj/foot.obj').points
TOE=footV[np.argmax(footV[:,0])]            # most anterior foot vertex (toe)
CTRL=['hip_flx','knee_flx','ankle_flx']     # controlled DOFs (sagittal)
RANGES={}
import xml.etree.ElementTree as ET
for c in ET.parse('rat_hindlimb_0.2.osim').getroot().iter('Coordinate'):
    r=c.find('range'); RANGES[c.get('name')]=np.fromstring(r.text.strip(),sep=' ')

def toe_world(coords):
    W=rig.fk(coords); R=W['foot'][:3,:3]; p=W['foot'][:3,3]
    return Rg@(R@TOE+p)

def hip_world(coords):
    return Rg@rig.fk(coords)['femur'][:3,3]

def ik(target_xz, seed, iters=60, lam=3e-3):
    c=dict(seed); q=np.array([c[k] for k in CTRL])
    for _ in range(iters):
        for i,k in enumerate(CTRL): c[k]=q[i]
        cur=toe_world(c); err=np.array([target_xz[0]-cur[0], target_xz[1]-cur[2]])
        if np.linalg.norm(err)<2e-5: break
        J=np.zeros((2,len(CTRL))); eps=1e-5
        for i,k in enumerate(CTRL):
            c2=dict(c); c2[k]=q[i]+eps; w=toe_world(c2)
            J[:,i]=np.array([w[0]-cur[0], w[2]-cur[2]])/eps
        dq=J.T@np.linalg.solve(J@J.T+lam*np.eye(2),err)
        q=q+dq
        for i,k in enumerate(CTRL): q[i]=np.clip(q[i],RANGES[k][0]+1e-3,RANGES[k][1]-1e-3)
    for i,k in enumerate(CTRL): c[k]=q[i]
    return c, np.linalg.norm(err)

# gait/target params
L=0.8/27.0; BETA=0.6; H=0.010
FLOOR=-0.016; ZG=FLOOR+0.0015
def smoother(t): return t*t*t*(t*(6*t-15)+10)
def target(phi, x0):
    if phi<=BETA:                      # stance: planted, moves back with belt
        return np.array([x0 - L*phi, ZG])
    t=(phi-BETA)/(1-BETA)              # swing: return forward + lift
    x=(x0-L*BETA)+ (L*BETA)*smoother(t)
    z=ZG + H*np.sin(np.pi*t)
    return np.array([x,z])

def solve_cycle(N):
    base=dict(rig.defaults); x0=hip_world(base)[0]+0.012
    seed=dict(base); out=[]; errs=[]
    for i in range(N):
        phi=i/N; c,e=ik(target(phi,x0),seed); seed=c; out.append(c); errs.append(e)
    return out, float(np.max(errs))

if __name__=='__main__':
    cs,me=solve_cycle(6)
    print('max IK error mm', round(me*1000,3))
    for i,c in enumerate(cs):
        print(i, {k:round(c[k],2) for k in CTRL}, 'toe_mm',np.round(toe_world(c)*1000,1))
