import xml.etree.ElementTree as ET, numpy as np, rig
root=ET.parse('rat_hindlimb_0.2.osim').getroot()
def _t(e): return np.fromstring(e.text.strip(),sep=' ')

# ---- parse wrap objects ----
WOBJ={}
for body in root.iter('Body'):
    bn=body.get('name'); ws=body.find('.//WrapObjectSet/objects')
    if ws is None: continue
    for w in list(ws):
        rot=_t(w.find('xyz_body_rotation')); tr=_t(w.find('translation'))
        WOBJ[w.get('name')]=dict(body=bn,typ=w.tag,rot=rot,tr=tr,
            quad=(w.findtext('quadrant') or 'all').strip(),
            radius=float(w.findtext('radius')) if w.find('radius') is not None else None,
            length=float(w.findtext('length')) if w.find('length') is not None else None,
            outer=float(w.findtext('outer_radius')) if w.find('outer_radius') is not None else None)
# ---- parse muscles (points + wrap assignments + params) ----
MUS=[]
for mus in root.iter('Thelen2003Muscle'):
    n=mus.get('name')
    if n=='default': continue
    mps=mus.find('.//MusclePointSet/objects'); pts=[]
    for pp in list(mps):
        b=pp.findtext('body'); loc=pp.find('location')
        if b is not None and loc is not None: pts.append((b.strip(),_t(loc)))
    ws=mus.find('.//MuscleWrapSet/objects')
    assigns=[w.findtext('wrap_object').strip() for w in list(ws)] if ws is not None else []
    MUS.append(dict(name=n,pts=pts,wraps=assigns,
                    ofl=float(mus.findtext('optimal_fiber_length')),
                    tsl=float(mus.findtext('tendon_slack_length'))))
MUSD={m['name']:m for m in MUS}

def euler_xyz(r):
    cx,cy,cz=np.cos(r); sx,sy,sz=np.sin(r)
    Rx=np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]]); Ry=np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]]); Rz=np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]])
    return Rx@Ry@Rz

def wobj_world(name, W):
    o=WOBJ[name]; Tb=W[o['body']]
    R=Tb[:3,:3]@euler_xyz(o['rot']); p=Tb[:3,:3]@o['tr']+Tb[:3,3]
    return R,p,o

def _wrap_circle_2d(A,B,r,ndisc=12):
    dA=np.linalg.norm(A); dB=np.linalg.norm(B)
    if dA<=r or dB<=r: return None
    AB=B-A; t=np.clip(-A@AB/(AB@AB),0,1); 
    if np.linalg.norm(A+t*AB)>=r: return None       # no penetration
    thA=np.arctan2(A[1],A[0]); thB=np.arctan2(B[1],B[0])
    phA=np.arccos(np.clip(r/dA,-1,1)); phB=np.arccos(np.clip(r/dB,-1,1))
    best=None
    for d in (1,-1):
        tA=thA-d*phA; tB=thB+d*phB
        TA=r*np.array([np.cos(tA),np.sin(tA)]); TB=r*np.array([np.cos(tB),np.sin(tB)])
        sweep=((tB-tA)*d)%(2*np.pi)
        s=np.linspace(0,sweep,ndisc); arc=[r*np.array([np.cos(tA+d*si),np.sin(tA+d*si)]) for si in s]
        L=np.linalg.norm(A-TA)+r*sweep+np.linalg.norm(TB-B)
        if best is None or L<best[0]: best=(L,[A]+arc+[B])
    return best[1]

def _quad_ok(p, quad):
    if quad=='all': return True
    ax={'x':0,'y':1,'z':2}[quad[-1]]; sgn=-1.0 if quad.startswith('-') else 1.0
    return p[ax]*sgn > 0

def wrap_cylinder(A,B,R,c,o,K=24):
    # robust surface-projection wrap: push penetrating samples out to cylinder surface (axis=z in obj frame)
    r=o['radius']; a=R.T@(A-c); b=R.T@(B-c); pts=[]; hit=False
    for t in np.linspace(0,1,K):
        p=a+(b-a)*t; dxy=np.hypot(p[0],p[1])
        if 0<t<1 and dxy<r and _quad_ok(p,o['quad']):
            p=np.array([p[0]*r/dxy,p[1]*r/dxy,p[2]]); hit=True
        pts.append(p)
    if not hit: return [A,B]
    return [R@p+c for p in pts]

def wrap_sphere(A,B,R,c,o,K=24):
    r=o['radius'] if o['radius'] is not None else o['outer']   # torus approx = sphere of outer radius
    a=R.T@(A-c); b=R.T@(B-c); pts=[]; hit=False
    for t in np.linspace(0,1,K):
        p=a+(b-a)*t; d=np.linalg.norm(p)
        if 0<t<1 and d<r and _quad_ok(p,o['quad']):
            p=p*(r/d); hit=True
        pts.append(p)
    if not hit: return [A,B]
    return [R@p+c for p in pts]

def muscle_path(name,coords):
    W=rig.fk(coords); m=MUSD[name]
    path=[W[b][:3,:3]@loc+W[b][:3,3] for b,loc in m['pts']]
    for wn in m['wraps']:
        R,c,o=wobj_world(wn,W)
        newpath=[path[0]]
        for i in range(len(path)-1):
            A,Bp=path[i],path[i+1]
            if o['typ']=='WrapCylinder': seg=wrap_cylinder(A,Bp,R,c,o)
            else: seg=wrap_sphere(A,Bp,R,c,o)   # sphere & torus(approx)
            newpath.extend(seg[1:])
        path=newpath
    return path

def muscle_length(name,coords,wrap=True):
    if wrap: p=muscle_path(name,coords)
    else:
        W=rig.fk(coords); m=MUSD[name]; p=[W[b][:3,:3]@loc+W[b][:3,3] for b,loc in m['pts']]
    return sum(np.linalg.norm(np.array(p[i+1])-np.array(p[i])) for i in range(len(p)-1))

def moment_arm(name,coord,coords,d=1e-3):
    c1=dict(coords); c2=dict(coords); c1[coord]+=d; c2[coord]-=d
    return -(muscle_length(name,c1)-muscle_length(name,c2))/(2*d)

if __name__=='__main__':
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    W=rig.fk(rig.defaults)
    # diagnostic: BFp over femur_prox, plot in cylinder 2D frame
    m=MUSD['BFp']; R,c,o=wobj_world('femur_prox',W)
    path0=[W[b][:3,:3]@loc+W[b][:3,3] for b,loc in m['pts']]
    A,Bp=path0[0],path0[1]
    seg=wrap_cylinder(A,Bp,R,c,o)
    a=R.T@(A-c); b=R.T@(Bp-c); segl=[R.T@(P-c) for P in seg]
    fig,ax=plt.subplots(figsize=(4,4))
    th=np.linspace(0,2*np.pi,100); ax.plot(o['radius']*np.cos(th),o['radius']*np.sin(th),'k')
    ax.plot([a[0],b[0]],[a[1],b[1]],'r--',label='straight')
    ax.plot([p[0] for p in segl],[p[1] for p in segl],'b.-',label='wrapped')
    ax.set_aspect('equal'); ax.legend(); ax.set_title('BFp over femur_prox (cyl frame xy)')
    plt.savefig('wrap_diag.png',dpi=90,bbox_inches='tight')
    print('BFp straight=%.1fmm wrapped=%.1fmm'%(muscle_length('BFp',rid:=rig.defaults,False)*1000, muscle_length('BFp',rig.defaults,True)*1000))
    print('knee moment arm BFp = %.2f mm'%(moment_arm('BFp','knee_flx',rig.defaults)*1000))
