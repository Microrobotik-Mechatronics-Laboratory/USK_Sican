import numpy as np, opensim as osim, build_osim, rig
DEG=np.pi/180.0
m,bod=build_osim.build(True); s=m.initSystem()
cs=m.getCoordinateSet(); musc=m.getMuscles()
def setc(d):
    for k,v in d.items():
        for i in range(cs.getSize()):
            if cs.get(i).getName()==k: cs.get(i).setValue(s,v,False)
    m.assemble(s); m.realizePosition(s)
def L(n): return musc.get(n).getLength(s)*1000.0
base={k:v for k,v in rig.defaults.items()}
# central difference knee moment arm at default knee, holding others fixed
h=2.0*DEG
def knee_ma(n):
    d=dict(base); k0=base.get('knee_flx',-1.0)
    d['knee_flx']=k0+h; setc(d); Lp=L(n)
    d['knee_flx']=k0-h; setc(d); Lm=L(n)
    return -(Lp-Lm)/(2*h)  # mm/rad -> mm (since r=-dL/dtheta, theta in rad, L in mm => mm)
print("knee_flx default =",base.get('knee_flx'))
print("muscle  knee moment arm (mm)  [+ = extensor-side]")
for n in ['RF','VL','VI','VM','BFp','SM','STa','STp']:
    try: print(f"  {n:4s}  {knee_ma(n):+6.2f}")
    except Exception as e: print(f"  {n:4s}  ERR {e}")
