from graphics3 import *
import cv2
from time import time

D = 200
a = []
for i in range(100):
    tmp = plane_3d([[100*np.cos(np.pi*i/50),0,100*np.sin(np.pi*i/50)],
        [100*np.cos(np.pi*(i+1)/50),0,100*np.sin(np.pi*(1+i)/50)],
        [0,200,0]],[127,127,127])
    a.append(tmp)
bottom = plane_3d([[100*np.cos(np.pi*i/50),0,100*np.sin(np.pi*i/50)] for i in range(100)],[255,127,127])
a.append(bottom)
body = body_3d(a)
#M = rotate([0,1,1],np.pi/2)
M_scale = scale(2.)
M = move([-200,-200,-400])
M = rotate([1,1,1],np.pi/10).dot(M)
M = move([200,200,400]).dot(M)

plt.ion()
body.exeucute(M_scale)
body.exeucute(move([200,100,400]))
for i in range(20):
    body.exeucute(M)
    img = np.zeros([300,300,3],dtype='int')
    depth = np.zeros(img.shape[0:2],dtype='float')
    depth.fill(np.inf)
    a = time()
    img = body.draw(D,img,depth,MSAA=1)
    b = time()
    print(b-a)
    cv2.imwrite('pic\\cone{}.png'.format(i),img)
    show(img)
    plt.pause(0.1)
plt.ioff()
#show(img)
plt.show()