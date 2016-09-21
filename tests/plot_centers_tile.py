import glob, os, sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy

oriFolder = sys.argv[1]
box = sys.argv[2]

images = glob.glob('*JPG')
points= []
for image in images:
    points.append([float(e) for e in os.popen('cat ' + oriFolder + '/Orientation-' + image + '.xml | grep "<Centre>"').read().strip().replace('<Centre>','').replace('</Centre>','').split()])
points = numpy.array(points)

minx,miny,maxx,maxy = [float(e) for e in box.split(',')]

fig = plt.figure()
ax = fig.add_subplot(111,aspect='equal')
ax.add_patch(patches.Rectangle((minx,miny), maxx-minx, maxy-miny, fill=False))
ax.scatter(points[:,0], points[:,1], color='g')
if len(sys.argv) == 3:
    plt.show()
else:
    fig.savefig(sys.argv[3])
