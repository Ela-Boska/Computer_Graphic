from graphics3 import *
from time import time
import cv2

D = 500
ka = [0.2,0.2,0.2]
kd = [0.3,0.3,0.3]
ks = [0.5,0.5,0.5]
planes = []
l = 100
for i in range(l):
    tmp = plane_3d([[100*np.cos(i*np.pi*2/l),100*np.sin(i*np.pi*2/l),0],
        [100*np.cos((i+1)*np.pi*2/l),100*np.sin((i+1)*np.pi*2/l),0],
        [0,0,100]
    ],ka,kd,ks)
    planes.append(tmp)
bottom = plane_3d([[100*np.cos(i*np.pi*2/l),100*np.sin(i*np.pi*2/l),0] for i in range(l,0,-1)],ka,kd,ks)
planes.append(bottom)
body = body_3d(planes)
#M = rotate([0,1,1],np.pi/2)
M_scale = scale(1.)
M = move([-200,-200,300])
M = rotate([1,1,1],np.pi/10).dot(M)
M = move([200,200,-300]).dot(M)
Ika = np.array([255,255,255],dtype='float')*1
Ikd = np.array([255,255,255],dtype='float')*1
Iks = np.array([255,255,255],dtype='float')*1
KL = np.array([0.,0.,1.])
n = 2
parameters = [Ika,Ikd,Iks,KL,n]
plt.ion()
body.exeucute(M_scale)
body.exeucute(move([200,200,-300]))
for i in range(20):
    img = np.zeros([300,300,3],dtype='int')
    depth = np.zeros(img.shape[0:2],dtype='float')
    depth.fill(-np.inf)
    a = time()
    
    img = body.draw(D,img,depth,parameters,MSAA=1)
    body.exeucute(M)
    b = time()
    print(b-a)
    cv2.imwrite('pic\\cone{}.png'.format(i),img)
    show(img)
    plt.pause(0.5)
plt.ioff()
#show(img)
plt.show()