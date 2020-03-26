"""
Bresenham algorithm を参考に改良
"""
import numpy as np

class Painter():    
    def calculate_f_parameter(self,a_x,a_y,b_x,b_y):
        """
        y = dy/dx(x - x1) + y1
        """
        self.dy = a_y - b_y
        self.dx = a_x - b_x
        self.x1 = a_x
        self.y1 = a_y
    def get_f_value(self,x,y):
        """
        f(x,y) = 2{dy(x - x1) - dx(y - y1)}
        """
        return 2*(self.dy*(x - self.x1) - self.dx * (y - self.y1))
    
    def paint_segment(self,img , a_x,a_y,b_x,b_y,line_width = 1):
        a_x : float = float(a_x)
        a_y : float = float(a_y)
        b_x : float = float(b_x)
        b_y : float = float(b_y)
        self.calculate_f_parameter(a_x,a_y,b_x,b_y)
        
        if a_x < b_x:
            i_x = int(a_x + 0.5)
            i_y = int(a_y + 0.5)
            max_x = b_x
            #プロットしていく方向を決める
            if i_y < b_y :
                error_n_list = [[0,1],[1,1],[1,0]]
            else:
                error_n_list = [[1,0],[1,-1],[0,-1]]
                
        else:
            i_x = int(b_x + 0.5)
            i_y = int(b_y + 0.5)
            max_x = int(a_x)
            
            #プロットしていく方向を決める
            if i_y < a_y :
                error_n_list = [[0,1],[1,1],[1,0]]
            else:
                error_n_list = [[1,0],[1,-1],[0,-1]]
            
        if a_y < b_y:
            max_y = int(b_y)
            min_y = int(a_y)
        else:
            max_y = int(a_y)
            min_y = int(b_y)
        #エラー値が最も小さい点をプロットする
        while i_x <= max_x and i_y <= max_y and i_y >= min_y:
            img[i_y][i_x] = 1
            for i in range(line_width * (-1) ,line_width + 1):
                for j in range(line_width * (-1) ,line_width + 1):
                    img[i_y + i][i_x + j] = 1
            
            min_error = abs(self.get_f_value(i_x+error_n_list[0][0] , i_y + error_n_list[0][1]))
            plus_n = error_n_list[0]
            
            for i_list in error_n_list[1:]:
                if min_error > abs(self.get_f_value(i_x+i_list[0] , i_y + i_list[1])):
                    min_error = abs(self.get_f_value(i_x+i_list[0] , i_y + i_list[1]))
                    plus_n = i_list
                
            i_x += plus_n[0]
            i_y += plus_n[1]
        
        return img

if __name__ == '__main__':
    painter = Painter()
    painter.calculate_f_parameter(3,4,4,5)
    print("y = ",painter.dy,"/",painter.dx,"(x - ",painter.x1,") + ",painter.y1)
    print(painter.get_f_value(3,5))
    print(painter.get_f_value(3,4))
    print(painter.get_f_value(3,3))
    
    img = np.zeros((10,10))
    img = painter.paint_segment(img,1,2,7,5)
    print(img)
    
    img = np.zeros((10,10))
    img = painter.paint_segment(img,2,1,0,5)
    print(img)
    
    img = np.zeros((10,10))
    img = painter.paint_segment(img,3,1,3,6)
    print(img)
    
    img = np.zeros((10,10))
    img = painter.paint_segment(img,1,2,6,2)
    print(img)
    
    print("painter")