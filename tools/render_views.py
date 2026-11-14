import sys, trimesh, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
m = trimesh.load(sys.argv[1], force="mesh")
views=[(18,-38,"Front 3/4"),(15,215,"Rear 3/4"),(2,-90,"Side")]
fig=plt.figure(figsize=(18,6.5))
for i,(el,az,t) in enumerate(views):
    ax=fig.add_subplot(1,3,i+1,projection="3d")
    e,a=np.radians(el),np.radians(az); cam=np.array([np.cos(e)*np.cos(a),np.cos(e)*np.sin(a),np.sin(e)])
    l=0.55*cam+0.45*np.array([0.3,-0.3,0.9]); l/=np.linalg.norm(l)
    sh=0.18+0.82*np.clip(m.face_normals@l,0,1)**1.3
    ax.add_collection3d(Poly3DCollection(m.triangles,facecolors=np.c_[0.82*sh,0.83*sh,0.86*sh,np.ones_like(sh)],edgecolor="none"))
    b=m.bounds;c=b.mean(0);r=(b[1]-b[0]).max()/2*0.52
    ax.set_xlim(c[0]-r,c[0]+r);ax.set_ylim(c[1]-r,c[1]+r);ax.set_zlim(c[2]-r,c[2]+r)
    ax.view_init(el,az);ax.set_axis_off();ax.set_title(t,fontsize=14)
plt.subplots_adjust(0,0,1,0.95,0,0);plt.savefig(sys.argv[2],dpi=110)
