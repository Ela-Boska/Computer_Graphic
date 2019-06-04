from graphics3 import *
from time import time
import cv2

D = 500
ka = [0.2,0.2,0.2]
kd = [0.3,0.3,0.3]
ks = [0.5,0.5,0.5]
a = plane_3d([[0,0,0],[50,50*3**0.5,0],[100,0,0]],ka,kd,ks)
b = plane_3d([[0,0,0],[100,0,0],[50,50/3**0.5,100*(2/3)**0.5]],ka,kd,ks)
c = plane_3d([[0,0,0],[50,50/3**0.5,100*(2/3)**0.5],[50,50*3**0.5,0]],ka,kd,ks)
d = plane_3d([[50,50/3**0.5,100*(2/3)**0.5],[100,0,0],[50,50*3**0.5,0]],ka,kd,ks)
body = body_3d([a,b,c,d])
#M = rotate([0,1,1],np.pi/2)
M_scale = scale(2.)
M = move([-100,-100,300])
M = rotate([1,1,1],np.pi/20).dot(M)
M = move([100,100,-300]).dot(M)
Ika = np.array([255,255,255],dtype='float')*1
Ikd = np.array([255,255,255],dtype='float')*1
Iks = np.array([255,255,255],dtype='float')*1
KL = np.array([0.,0.,1.])
n = 2
parameters = [Ika,Ikd,Iks,KL,n]
plt.ion()
body.exeucute(M_scale)
body.exeucute(move([100,100,-300]))
for i in range(20):
    img = np.zeros([300,300,3],dtype='int')
    depth = np.zeros(img.shape[0:2],dtype='float')
    depth.fill(-np.inf)
    a = time()
    
    img = body.draw(D,img,depth,parameters,MSAA=1)
    body.exeucute(M)
    b = time()
    print(b-a)
    cv2.imwrite('pic\\tetrahedron{}.png'.format(i),img)
    show(img)
    plt.pause(0.5)
plt.ioff()
#show(img)
plt.show()