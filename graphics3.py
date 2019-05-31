import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import pinv,inv
import time

class line_3d():

    def __init__(self,points):
        self.points = []
        for point in points:
            if len(point) == 3:
                self.points.append(np.array(point+[1], dtype='float').reshape(4,1))
            else:
                self.points.append(point)
        if points[0][1] < points[1][1]:
            self.flag = 0
        else:
            self.flag = 1
        if (points[0][1]-points[1][1])!=0:
            self._k = (points[0][0]-points[1][0])/(points[0][1]-points[1][1])
        else:
            self._k = np.inf
        

    def get_points(self):
        flag = self.flag
        points = np.zeros([int(self.points[1-flag][1])-int(self.points[flag][1]),2],dtype='int')
        points[:,1] = np.arange(int(self.points[flag][1]),int(self.points[1-flag][1])).astype('int')
        points[:,0] = np.linspace(self.points[flag][0],self.points[1-flag][0],len(points)+1).astype('int')[:-1]
        #print(points)
        return points

class plane_3d():

    def __init__(self, vertices, color):
        for i in range(len(vertices)):
            ans = np.ones([4,1], dtype='float')
            ans[0:3,0] = vertices[i]
            vertices[i] = ans
        self.vertices = vertices
        self.color = np.array(color,dtype='float')
        
        
    def form(self):
        p0 = self.vertices[1][0:3]
        dp1 = self.vertices[0][0:3] - self.vertices[1][0:3]
        dp2 = self.vertices[2][0:3] - self.vertices[1][0:3]
        self.a, self.b, self.c = np.cross(dp1[:,0],dp2[:,0])
        self.d = -p0.T.dot(np.cross(dp1[:,0],dp2[:,0]))
        self.lines = []
        vertices = self.projected_vertices
        for i in range(len(vertices)):
            self.lines.append(line_3d([vertices[i], vertices[(i+1)%len(vertices)]]))

    def project(self,d):
        self.projected_vertices = []
        for i in range(len(self.vertices)):
            new_point = project(d).dot(self.vertices[i])
            new_point /= new_point[3]
            new_point[2] = self.vertices[i][2]
            self.projected_vertices.append(new_point)
            #print(new_point)
        self.xmin = np.inf
        self.ymin = np.inf
        self.xmax = 0
        self.ymax = 0
        for vertex in self.projected_vertices:
            if vertex[1]< self.ymin:
                self.ymin = vertex[1]
            if vertex[1]> self.ymax:
                self.ymax = vertex[1]
            if vertex[0] < self.xmin:
                self.xmin = vertex[0]
            if vertex[0] > self.xmax:
                self.xmax = vertex[0]

    def draw(self, d, img, depth):

        self.project(d)
        self.form()
        points = np.zeros([0,2],dtype='int')
        for i in range(len(self.lines)):
            
            points = np.concatenate([points,self.lines[i].get_points()],0)
        labels = np.zeros(img.shape[0:2])
        for point in points:
            labels[point[0],point[1]] += 1

        for y in range(int(self.ymin), int(self.ymax)):
            S = 0
            for x in np.arange(int(self.xmin), int(self.xmax)):
                if labels[x,y] == 1 and S == 0:
                    S = 1
                    axby = self.a*x + self.b*y
                    z = (-self.d-axby)/(self.c+axby/d)
                    if z < depth[x,y]:
                        depth[x,y] = z
                        img[x,y] = 255
                elif labels[x,y] == 1 and S == 1:
                    S = 0
                    axby += self.a
                    z = (-self.d-axby)/(self.c+axby/d)
                    if z < depth[x,y]:
                        depth[x,y] = z
                        img[x,y] = 255
                elif S == 1:
                    axby += self.a
                    z = (-self.d-axby)/(self.c+axby/d)
                    if z<depth[x,y]:
                        img[x,y,:] = self.color
                        depth[x,y] = z
                    if labels[x,y] == 1:
                        S = 0

        return img

    def exeucute(self, Matrix):
        for i in range(len(self.vertices)):
            self.vertices[i] = Matrix.dot(self.vertices[i])
            self.vertices[i] /= self.vertices[i][3]

class body_3d():
    def __init__(self,planes):
        self.planes = planes

    def exeucute(self, Matrix):
        for i in range(len(self.planes)):
            self.planes[i].exeucute(Matrix)

    def draw(self, d, img, depth,MSAA=0):
        if MSAA:
            M = scale(3)
            M_ = scale(1/3)
            X,Y,_ = img.shape
            img = extend(img,3)
            depth = extend(depth,3)
            for i in range(len(self.planes)):
                self.planes[i].exeucute(M)
        for plane in self.planes:
            plane.draw(d*3, img, depth)
        if MSAA:
            for i in range(len(self.planes)):
                self.planes[i].exeucute(M_)
            Filters = np.array([[1,2,1],[2,4,2],[1,2,1]],dtype='float').reshape(3,3,1,1,1)/16
            img = img.reshape(X,3,Y,3,3).transpose(1,3,0,2,4).astype('float')
            img = (Filters*img).sum(0).sum(0).astype('int')
        return img

        
def scale(alpha):
    ans = np.eye(4, dtype='float')
    ans[3,3] = 1/alpha
    return ans

def project(d):
    ans = np.eye(4, dtype='float')
    ans[3,2] = 1/d
    ans[2,2] = 0
    return ans
        
def move(xyz):
    xyz = np.array(xyz, dtype='float')
    ans = np.eye(4, dtype='float')
    ans[0:3,3] = xyz
    return ans
    
def rotate_x(theta):
    ans = np.eye(4, dtype='float')
    ans[1,1] = np.cos(theta)
    ans[1,2] = -np.sin(theta)
    ans[2,1] = np.sin(theta)
    ans[2,2] = np.cos(theta)
    return ans

def rotate_y(theta):
    ans = np.eye(4, dtype='float')
    ans[0,0] = np.cos(theta)
    ans[0,2] = np.sin(theta)
    ans[2,0] = -np.sin(theta)
    ans[2,2] = np.cos(theta)
    return ans

def rotate_z(theta):
    ans = np.eye(4, dtype='float')
    ans[0,0] = np.cos(theta)
    ans[0,1] = -np.sin(theta)
    ans[1,0] = np.sin(theta)
    ans[1,1] = np.cos(theta)
    return ans

def rotate(dirc, theta):
    dirc = np.array(dirc, dtype='float')
    dirc /= np.sum(dirc**2)**0.5
    Theta = np.arccos(dirc[2])
    if Theta != 0:
        Fai = np.arccos(dirc[0]/np.sin(Theta))
        ans = rotate_z(-Fai)
        ans = rotate_y(np.pi/2-Theta).dot(ans)
        ans = rotate_x(theta).dot(ans)
        ans = rotate_y(Theta-np.pi/2).dot(ans)
        ans = rotate_z(Fai).dot(ans)
    else:
        ans = rotate_z(theta)
    return ans

def show(img):
    if img.ndim == 3:
        tmp = img.transpose([1,0,2])
    else:
        tmp = img.T
    tmp = np.flip(tmp,0)
    plt.imshow(tmp,cmap=plt.cm.gray)
    plt.yticks(np.arange(img.shape[1]-1,-2,-img.shape[1]//5),np.arange(0,img.shape[1]+1,img.shape[1]//5))
    plt.xticks(np.arange(0,img.shape[0]+1,img.shape[0]//5))

def extend(M,alpha):
    return M.repeat(alpha,0).repeat(alpha,1)