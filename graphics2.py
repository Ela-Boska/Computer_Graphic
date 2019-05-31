import matplotlib.pyplot as plt
import numpy as np
import pdb

class line():

    def __init__(self,point_1,point_2):
        if point_1[1]<point_2[1]:
            self.point_1=point_1
            self.point_2=point_2
        else:
            self.point_1=point_2
            self.point_2=point_1
        self.xmin = min(point_1[0],point_2[0])
        self.xmax = max(point_1[0],point_2[0])
        if (point_2[0]-point_1[0]) != 0:
            self.k = (point_2[1]-point_1[1])/(point_2[0]-point_1[0])
        else:
            self.k = np.inf
            self._k = 0
        if self.k == 0:
            self._k = np.inf
        else:
            self._k = 1/self.k

    def get_points(self):
        e = -0.5
        points = []
        x = int(self.point_1[0])
        for y in range(int(self.point_1[1]), int(self.point_2[1])):
            points.append([x,y])
            e += self._k
            tmp = int((e+1)//1)
            e -= tmp
            x += tmp
        #print(points)
        return points
    
    def draw(self,img):
        points = self.get_points()
        for point in points:
            img[point[0],point[1]] = 1
        return img

    def clip(self, xy_range: list):#实现Liang-Barsky 算法
        xmin, xmax, ymin, ymax = xy_range
        dx = self.point_2[0]-self.point_1[0]
        dy = self.point_2[1]-self.point_1[1]
        x0 = self.point_1[0]
        y0 = self.point_1[1]
        u_in = [0]
        u_out = [1]
        if dx!=0:
            us = [(xmin-x0)/dx, (xmax-x0)/dx]
            if dx>0:
                u_in.append(us[0])
                u_out.append(us[1])
            else:
                u_in.append(us[1])
                u_out.append(us[0])
        if dy!=0:
            us = [(ymin-y0)/dy, (ymax-y0)/dy]
            if dy>0:
                u_in.append(us[0])
                u_out.append(us[1])
            else:
                u_in.append(us[1])
                u_out.append(us[0])
        u_1 = np.max(u_in)
        u_2 = np.min(u_out)
        #pdb.set_trace()
        if u_1>u_2:
            return None
        x_1 = x0 + u_1*dx
        x_2 = x0 + u_2*dx
        y_1 = y0 + u_1*dy
        y_2 = y0 + u_2*dy
        return line((x_1,y_1),(x_2,y_2))


class polygon():

    def __init__(self, vertexs:list, color:list=[1,1,1]):
        self.vertexs = vertexs
        self.lines = []
        self.links = []
        for i in range(len(vertexs)):
            self.lines.append(line(vertexs[i], vertexs[(i+1)%len(vertexs)]))
            self.links.append([i,(i+1)%len(vertexs)])
        self.color = color
        self.ymin = np.inf
        self.ymax = 0
        self.xmin = np.inf
        self.xmax = 0
        for vertex in self.vertexs:
            if vertex[1]< self.ymin:
                self.ymin = vertex[1]
            elif vertex[1]> self.ymax:
                self.ymax = vertex[1]
            if vertex[0] < self.xmin:
                self.xmin = vertex[0]
            elif vertex[0] > self.xmax:
                self.xmax = vertex[0]

    def get_boundary(self):
        points = []
        for LINE in self.lines:
            points += LINE.get_points()
        return points
    
    def draw(self,img):
        # img should be (m,n,2). The 2nd layer is used to store the labels
        labels = np.zeros_like(img)
        for point in self.get_boundary():
            labels[point[0],point[1]] += 1
            

        for y in np.arange(int(self.ymin),int(self.ymax)):
            S = 0
            for x in np.arange(self.xmin,self.xmax):
                S += labels[x,y]
                if S % 2 == 1:
                    img[x,y] = 1
        return img

    def clip(self,xy_range: list): 
        def _clip(object:polygon, xy_value:int, x_or_y: int, flag: int):
            # x_or_y: 0 -> x, 1 -> y
            # flag: 0 -> xy >= xy_value, 1 -> xy < xy_value
            vertexs = []
            for link in object.links:
                
                if flag == 0:

                    if object.vertexs[link[0]][x_or_y] < xy_value and object.vertexs[link[1]][x_or_y] >= xy_value:
                        vertex1 = [None,None]
                        vertex1[x_or_y] = xy_value
                        vertex1[1-x_or_y] = int(0.5+object.vertexs[link[0]][1-x_or_y]+(xy_value-object.vertexs[link[0]][x_or_y])/
                            (object.vertexs[link[1]][x_or_y]-object.vertexs[link[0]][x_or_y])*
                            (object.vertexs[link[1]][1-x_or_y]-object.vertexs[link[0]][1-x_or_y]))
                        vertex2 = object.vertexs[link[1]]
                        vertexs.append(vertex1)
                        vertexs.append(vertex2)
                    elif object.vertexs[link[0]][x_or_y] >= xy_value and object.vertexs[link[1]][x_or_y] < xy_value:
                        vertex1 = [None,None]
                        vertex1[x_or_y] = xy_value
                        vertex1[1-x_or_y] = int(0.5+object.vertexs[link[0]][1-x_or_y]+(xy_value-object.vertexs[link[0]][x_or_y])/
                            (object.vertexs[link[1]][x_or_y]-object.vertexs[link[0]][x_or_y])*
                            (object.vertexs[link[1]][1-x_or_y]-object.vertexs[link[0]][1-x_or_y]))
                        vertexs.append(vertex1)
                    elif object.vertexs[link[0]][x_or_y] >= xy_value and object.vertexs[link[1]][x_or_y] >= xy_value:
                        vertexs.append(object.vertexs[link[1]])
                else:
                    if object.vertexs[link[0]][x_or_y] >= xy_value and object.vertexs[link[1]][x_or_y] < xy_value:
                        vertex1 = [None,None]
                        vertex1[x_or_y] = xy_value
                        vertex1[1-x_or_y] = int(0.5+object.vertexs[link[0]][1-x_or_y]+(xy_value-object.vertexs[link[0]][x_or_y])/
                            (object.vertexs[link[1]][x_or_y]-object.vertexs[link[0]][x_or_y])*
                            (object.vertexs[link[1]][1-x_or_y]-object.vertexs[link[0]][1-x_or_y]))
                        vertex2 = object.vertexs[link[1]]
                        vertexs.append(vertex1)
                        vertexs.append(vertex2)

                    elif object.vertexs[link[0]][x_or_y] < xy_value and object.vertexs[link[1]][x_or_y] >= xy_value:
                        vertex1 = [None,None]
                        vertex1[x_or_y] = xy_value
                        vertex1[1-x_or_y] = int(0.5+object.vertexs[link[0]][1-x_or_y]+(xy_value-object.vertexs[link[0]][x_or_y])/
                            (object.vertexs[link[1]][x_or_y]-object.vertexs[link[0]][x_or_y])*
                            (object.vertexs[link[1]][1-x_or_y]-object.vertexs[link[0]][1-x_or_y]))
                        vertexs.append(vertex1)

                    elif object.vertexs[link[0]][x_or_y] < xy_value and object.vertexs[link[1]][x_or_y] < xy_value:

                        vertexs.append(object.vertexs[link[1]])
            return polygon(vertexs)
        
        xmin, xmax, ymin, ymax = xy_range
        out = _clip(self,xmin,0,0)
        out = _clip(out,ymin,1,0)
        out = _clip(out,xmax,0,1)
        out = _clip(out,ymax,1,1)
        return out

    def draw_boundary(self,img):
        points = self.get_boundary()
        for point in points:
            img[point[0],point[1]] += 1
        return img
        




def show(img):
    tmp = img.T
    tmp = np.flip(tmp,0)
    plt.imshow(tmp,cmap=plt.cm.gray)
    plt.yticks(np.arange(img.shape[1]-1,-2,-img.shape[1]//5),np.arange(0,img.shape[1]+1,img.shape[1]//5))
    plt.xticks(np.arange(0,img.shape[0]+1,img.shape[0]//5))


if __name__=='__main__':
    a = polygon(
        [[25,31],[830,439],[700,900],[294,569]]
    )
    plt.subplot(221)
    img = np.zeros((1000,1000))
    b = a.clip([200,800,200,800])
    img= b.draw(img)
    
    show(img)
  

    plt.subplot(222)
    img = np.zeros((1000,1000))
    img= a.clip([200,800,200,800]).draw_boundary(img)
    show(img)

    plt.subplot(223)
    img = np.zeros((1000,1000))
    img= a.draw(img)
    show(img)

    plt.subplot(224)
    img = np.zeros((1000,1000))
    img= a.draw_boundary(img)
    show(img)
    plt.show()