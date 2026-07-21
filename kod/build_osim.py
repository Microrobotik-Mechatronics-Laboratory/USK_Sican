import opensim as osim, numpy as np, xml.etree.ElementTree as ET, rig, wrap
root=ET.parse('rat_hindlimb_0.2.osim').getroot()
def t3(e): return np.fromstring(e.text.strip(),sep=' ')
BINF={}
for body in root.iter('Body'):
    n=body.get('name'); mass=body.findtext('mass')
    if mass is None: continue
    BINF[n]=dict(mass=float(mass), com=t3(body.find('mass_center')),
        I=[float(body.findtext(k)) for k in ['inertia_xx','inertia_yy','inertia_zz','inertia_xy','inertia_xz','inertia_yz']])
INNER={w.get('name'):float(w.findtext('inner_radius')) for w in root.iter('WrapTorus')}
def make_func(entry):
    axis,kind,data,coord=entry
    if kind=='identity': return osim.LinearFunction(1.0,0.0)
    sp=osim.SimmSpline()
    for x,y in zip(data[0],data[1]): sp.addPoint(float(x),float(y))
    return sp
def fill_axes(st, used, is_rot):
    base=0 if is_rot else 3; assigned=[]
    for i in range(3):
        ax=st.updTransformAxis(base+i)
        if i<len(used):
            e=used[i]; v=np.array(e[0],float); ax.set_axis(osim.Vec3(*v))
            ar=osim.ArrayStr(); ar.append(e[3]); ax.setCoordinateNames(ar); ax.set_function(make_func(e))
            assigned.append(v/np.linalg.norm(v))
        else:
            for cand in [np.array([1.,0,0]),np.array([0,1.,0]),np.array([0,0,1.])]:
                if all(abs(cand@a)<0.98 for a in assigned):
                    ax.set_axis(osim.Vec3(*cand)); assigned.append(cand); break

def build(with_muscles=True):
    m=osim.Model(); m.setName('rat'); G=m.getGround(); bod={}
    for n in ['spine','pelvis','femur','tibia','foot']:
        bi=BINF[n]; b=osim.Body(n,bi['mass'],osim.Vec3(*bi['com']),osim.Inertia(*bi['I'])); m.addBody(b); bod[n]=b
    for bdef in rig.bodies:
        n=bdef['name']
        if bdef['parent'] is None: continue
        pf=G if bdef['parent']=='ground' else bod[bdef['parent']]
        st=osim.SpatialTransform(); fill_axes(st,bdef['rots'],True); fill_axes(st,bdef['trans'],False)
        jt=osim.CustomJoint(n+'_j',pf,osim.Vec3(*bdef['loc']),osim.Vec3(0,0,0),bod[n],osim.Vec3(0,0,0),osim.Vec3(0,0,0),st)
        m.addJoint(jt)
    # wrap objects
    for name,o in wrap.WOBJ.items():
        if o['typ']=='WrapCylinder':
            w=osim.WrapCylinder(); w.set_radius(o['radius']); w.set_length(o['length'])
        elif o['typ']=='WrapSphere':
            w=osim.WrapSphere(); w.set_radius(o['radius'])
        else:
            w=osim.WrapTorus(); w.set_inner_radius(INNER[name]); w.set_outer_radius(o['outer'])
        w.setName(name); w.set_xyz_body_rotation(osim.Vec3(*o['rot'])); w.set_translation(osim.Vec3(*o['tr'])); w.set_quadrant(o['quad'])
        bod[o['body']].addWrapObject(w)
    if with_muscles:
        for mm in wrap.MUS:
            mu=osim.Thelen2003Muscle(mm['name'],10.0,mm['ofl'] or 0.05, mm['tsl'] or 0.001, 0.0)
            for i,(b,loc) in enumerate(mm['pts']):
                mu.addNewPathPoint(f"{mm['name']}_p{i}", bod[b], osim.Vec3(*loc))
            gp=mu.updGeometryPath()
            for wn in mm['wraps']:
                o=wrap.WOBJ[wn]; wo=bod[o['body']].getWrapObject(wn)
                gp.addPathWrap(wo)
            m.addForce(mu)
    return m,bod

if __name__=='__main__':
    m,bod=build(True); s=m.initSystem()
    cs=m.getCoordinateSet()
    for i in range(cs.getSize()):
        c=cs.get(i); nm=c.getName()
        if nm in rig.defaults: c.setValue(s,rig.defaults[nm],False)
    m.assemble(s); m.realizePosition(s)
    W=rig.fk(rig.defaults)
    print("coords",cs.getSize(),"muscles",m.getMuscles().getSize(),"| FK check:")
    for n in ['femur','tibia','foot']:
        p=bod[n].getPositionInGround(s); po=np.array([p.get(0),p.get(1),p.get(2)])*1000
        print(f"  {n:6s} OSim={np.round(po,1)} rig={np.round(W[n][:3,3]*1000,1)}")
    # test a muscle length changes with knee
    mu=m.getMuscles().get('BFp'); L0=mu.getLength(s)
    cs.get('knee_flx').setValue(s, -1.0); m.realizePosition(s); L1=mu.getLength(s)
    print(f"BFp length knee=-2.09 -> {L0*1000:.1f}mm ; knee=-1.0 -> {L1*1000:.1f}mm (changes: {abs(L1-L0)>1e-4})")
    m.printToXML('rat_rebuilt.osim'); print("saved rat_rebuilt.osim")
