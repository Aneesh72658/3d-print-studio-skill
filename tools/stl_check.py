import sys, trimesh, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
m = trimesh.load(sys.argv[1], force="mesh")
bed = float(sys.argv[2]) if len(sys.argv) > 2 else 256
ext = m.extents
print(f"size_mm: {ext[0]:.2f} x {ext[1]:.2f} x {ext[2]:.2f}")
print("watertight:", m.is_watertight, "| triangles:", len(m.faces))
print(f"volume_cm3: {m.volume/1000:.2f}")
print(f"fits bed ({bed:.0f}mm):", bool((ext <= bed).all()))
zmin = m.bounds[0][2]
down = (m.face_normals[:, 2] < -0.707) & (m.triangles_center[:, 2] > zmin + 0.3)
ov = m.area_faces[down].sum(); print(f"overhang_area_mm2 (>45deg, needs support): {ov:.0f} ({100*ov/m.area:.1f}% of surface)")
base = (m.face_normals[:, 2] < -0.99) & (m.triangles_center[:, 2] < zmin + 0.01)
print(f"bed_contact_mm2: {m.area_faces[base].sum():.0f}")
light = np.array([0.4, -0.5, 0.8]); light /= np.linalg.norm(light)
shade = 0.35 + 0.65 * np.clip(m.face_normals @ light, 0, 1)
col = np.c_[0.29*shade, 0.56*shade, 0.85*shade, np.ones_like(shade)]
col[down] = [0.9, 0.3, 0.2, 1]
out = sys.argv[1].rsplit(".", 1)[0] + "_preview.png"
fig = plt.figure(figsize=(12, 4.5))
for i, (el, az) in enumerate([(25, -60), (25, 120), (90, -90)]):
    ax = fig.add_subplot(1, 3, i + 1, projection="3d")
    ax.add_collection3d(Poly3DCollection(m.triangles, facecolors=col, edgecolor="none"))
    b = m.bounds; c = b.mean(0); r = (b[1] - b[0]).max() / 2
    ax.set_xlim(c[0]-r, c[0]+r); ax.set_ylim(c[1]-r, c[1]+r); ax.set_zlim(c[2]-r, c[2]+r)
    ax.view_init(el, az); ax.set_axis_off()
plt.tight_layout(); plt.savefig(out, dpi=110); print("preview:", out, "(red = needs support)")
