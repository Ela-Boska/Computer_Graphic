from graphics3 import *
import cv2

D = 200
a = plane_3d([[0,0,0],[0,0,100],[0,100,100],[0,100,0]],[255,0,0])
b = plane_3d([[100,0,0],[100,0,100],[100,100,100],[100,100,0]],[0,255,0])
c = plane_3d([[0,0,0],[0,0,100],[100,0,100],[100,0,0]],[0,0,255])
d = plane_3d([[0,100,0],[0,100,100],[100,100,100],[100,100,0]],[127,127,0])
e = plane_3d([[0,0,0],[100,0,0],[100,100,0],[0,100,0]],[0,127,127])
f = plane_3d([[0,0,100],[100,0,100],[100,100,100],[0,100,100]],[127,0,127])
body = body_3d([d,b,c,f,a,e])
#M = rotate([0,1,1],np.pi/2)
M_scale = scale(2.)
M = move([-200,-200,-200])
M = rotate([1,1,1],np.pi/10).dot(M)
M = move([200,200,200]).dot(M)

plt.ion()
body.exeucute(M_scale)
body.exeucute(move([200,200,200]))
for i in range(20):
    body.exeucute(M)
    img = np.zeros([300,300,3],dtype='int')
    depth = np.zeros(img.shape[0:2],dtype='float')
    depth.fill(np.inf)
    img = body.draw(D,img,depth,MSAA=1)
    cv2.imwrite('pic\cubic{}.png'.format(i),img)
    show(img)
    plt.pause(0.5)
plt.ioff()
#show(img)
plt.show()