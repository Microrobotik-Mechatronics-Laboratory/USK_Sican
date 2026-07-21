"""vtp (OpenSim Geometry) -> obj (MuJoCo). Run once to create obj/ from Geometry/."""
import xml.etree.ElementTree as ET, numpy as np, meshio, os
def parse_vtp(path):
    r=ET.parse(path).getroot(); piece=r.find('.//Piece')
    pts=np.fromstring(piece.find('Points').find('DataArray').text.replace('\n',' '),sep=' ').reshape(-1,3)
    conn=off=None
    for da in piece.find('Polys').findall('DataArray'):
        v=np.fromstring(da.text.replace('\n',' '),sep=' ').astype(int)
        if da.get('Name')=='connectivity': conn=v
        elif da.get('Name')=='offsets': off=v
    tris=[]; s=0
    for o in off:
        poly=conn[s:o]; s=o
        for k in range(1,len(poly)-1): tris.append([poly[0],poly[k],poly[k+1]])
    return pts, np.array(tris,int)
if __name__=='__main__':
    os.makedirs('obj',exist_ok=True)
    for f in ['ground','spine','pelvis','femur','tibia','foot']:
        p,tr=parse_vtp(f'Geometry/{f}.vtp'); meshio.write_points_cells(f'obj/{f}.obj',p,[('triangle',tr)])
        print(f,len(p),'verts')
