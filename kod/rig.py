import xml.etree.ElementTree as ET, numpy as np, os

OSIM='rat_hindlimb_0.2.osim'
tree=ET.parse(OSIM); root=tree.getroot()

def txt3(e): return np.fromstring(e.text.strip(),sep=' ')
def spline_eval(xs,ys,q): return float(np.interp(q,xs,ys))  # natural-ish; monotone x

# ---- parse bodies (tree order) ----
bodies=[]  # dict: name,parent,loc_in_parent, rot_axes[(axis,kind,data,coord)], trans_axes[...], mesh
for body in root.iter('Body'):
    name=body.get('name')
    joint=body.find('./Joint/*')  # CustomJoint
    if joint is None:  # ground has empty <Joint/>
        bodies.append(dict(name=name,parent=None,loc=np.zeros(3),rots=[],trans=[],mesh=None)); continue
    parent=joint.findtext('parent_body').strip()
    loc=txt3(joint.find('location_in_parent'))
    rots=[];trans=[]
    for ta in joint.findall('./TransformAxisSet/objects/TransformAxis'):
        axis=txt3(ta.find('axis')); coord=ta.findtext('coordinate').strip()
        is_rot=ta.findtext('is_rotation').strip()=='true'
        fn=ta.find('function')
        spl=ta.find('.//natCubicSpline') if fn is not None else None
        if spl is not None:
            xs=txt3(spl.find('x')); ys=txt3(spl.find('y')); entry=(axis,'spline',(xs,ys),coord)
        else:
            entry=(axis,'identity',None,coord)
        (rots if is_rot else trans).append(entry)
    mesh=body.findtext('.//VisibleObject/geometry_files')
    mesh=mesh.strip() if mesh and mesh.strip() else None
    bodies.append(dict(name=name,parent=parent,loc=loc,rots=rots,trans=trans,mesh=mesh))

# default coords
defaults={}
for c in root.iter('Coordinate'):
    defaults[c.get('name')]=float(c.findtext('default_value'))

def axis_angle(axis,ang):
    a=axis/np.linalg.norm(axis); x,y,z=a; c=np.cos(ang); s=np.sin(ang); C=1-c
    return np.array([[c+x*x*C, x*y*C-z*s, x*z*C+y*s],
                    [y*x*C+z*s, c+y*y*C, y*z*C-x*s],
                    [z*x*C-y*s, z*y*C+x*s, c+z*z*C]])

def val(entry,coords):
    axis,kind,data,coord=entry; q=coords[coord]
    return q if kind=='identity' else spline_eval(data[0],data[1],q)

def joint_T(b,coords):
    R=np.eye(3)
    for e in b['rots']: R=R@axis_angle(e[0],val(e,coords))
    t=np.zeros(3)
    for e in b['trans']: t=t+val(e,coords)*e[0]
    T=np.eye(4); T[:3,:3]=R; T[:3,3]=t
    O=np.eye(4); O[:3,3]=b['loc']
    return O@T

def fk(coords):
    W={}
    for b in bodies:
        if b['parent'] is None: W[b['name']]=np.eye(4)
        else: W[b['name']]=W[b['parent']]@joint_T(b,coords)
    return W

def mat2quat(R):
    m=R; t=np.trace(m)
    if t>0:
        s=np.sqrt(t+1)*2; w=0.25*s; x=(m[2,1]-m[1,2])/s; y=(m[0,2]-m[2,0])/s; z=(m[1,0]-m[0,1])/s
    elif m[0,0]>m[1,1] and m[0,0]>m[2,2]:
        s=np.sqrt(1+m[0,0]-m[1,1]-m[2,2])*2; w=(m[2,1]-m[1,2])/s; x=0.25*s; y=(m[0,1]+m[1,0])/s; z=(m[0,2]+m[2,0])/s
    elif m[1,1]>m[2,2]:
        s=np.sqrt(1+m[1,1]-m[0,0]-m[2,2])*2; w=(m[0,2]-m[2,0])/s; x=(m[0,1]+m[1,0])/s; y=0.25*s; z=(m[1,2]+m[2,1])/s
    else:
        s=np.sqrt(1+m[2,2]-m[0,0]-m[1,1])*2; w=(m[1,0]-m[0,1])/s; x=(m[0,2]+m[2,0])/s; y=(m[1,2]+m[2,1])/s; z=0.25*s
    q=np.array([w,x,y,z]); return q/np.linalg.norm(q)

if __name__=='__main__':
    W=fk(defaults)
    for n in ['spine','pelvis','femur','tibia','foot']:
        print(f'{n:7s} origin_mm={np.round(W[n][:3,3]*1000,1)}')
