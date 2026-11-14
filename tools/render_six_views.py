import sys, trimesh, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
m = trimesh.load(sys.argv[1], force="mesh")
views = [(20,-35,"Front 3/4"),(20,145,"Rear 3/4"),(0,-90,"Side"),(-60,-35,"Underside"),(0,0,"Front"),(90,-90,"Top")]
light = np.array([0.5,-0.6,0.7]); light/=np.linalg.norm(light)
fig = plt.figure(figsize=(16,10))
for i,(el,az,t) in enumerate(views):
    ax = fig.add_subplot(2,3,i+1, projection="3d")
    # light follows camera a bit
    e,a=np.radians(el),np.radians(az)
    cam=np.array([np.cos(e)*np.cos(a),np.cos(e)*np.sin(a),np.sin(e)])
    l=0.6*cam+0.4*light; l/=np.linalg.norm(l)
    sh=0.25+0.75*np.clip(m.face_normals@l,0,1)
    col=np.c_[0.75*sh,0.78*sh,0.82*sh,np.ones_like(sh)]
    ax.add_collection3d(Poly3DCollection(m.triangles, facecolors=col, edgecolor="none"))
    b=m.bounds;c=b.mean(0);r=(b[1]-b[0]).max()/2*0.62
    ax.set_xlim(c[0]-r,c[0]+r);ax.set_ylim(c[1]-r,c[1]+r);ax.set_zlim(c[2]-r,c[2]+r)
    ax.view_init(el,az);ax.set_axis_off();ax.set_title(t)
    try: ax.set_box_aspect((1,1,1))
    except: pass
plt.tight_layout();plt.savefig(sys.argv[2],dpi=110)
