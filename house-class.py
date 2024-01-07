import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class house:
    def __init__(self,params):
        self.matrix= {}
        self.home = np.zeros((101,101))
        for key in params["indexes"].keys():
            room = params["indexes"][key]
            ind_min_x = min(room[:,0])
            ind_max_x = max(room[:,0])
            ind_min_y = min(room[:,1])
            ind_max_y = max(room[:,1])
            self.matrix[key] = np.zeros(((ind_max_x-ind_min_x,ind_max_y-ind_min_y)))
            self.home[ind_min_x:ind_max_x,ind_min_y:ind_max_y] = 1
            self.home[ind_min_x,ind_min_y:ind_max_y]=2
            self.home[ind_max_x,ind_min_y:ind_max_y]=2
            self.home[ind_min_x:ind_max_x,ind_min_y]=2
            self.home[ind_min_x:ind_max_x,ind_max_y]=2
    def show(self):
        cmapmine = ListedColormap(['w','b','black'], N=3)
        plt.imshow(self.home,cmap=cmapmine)
        plt.show()
        print(self.home[0,:])


if __name__=="__main__":
    params = {"indexes":{"`I": np.array(((0,0),(0,35),(40,0),(40,35))),"II" : np.array(((40,0),(40,35),(100,0),(100,35))), "III":np.array(((40,35),(40,60),(100,35),(100,60))),"IV":np.array(((40,60),(40,100),(80,60),(80,100))),"V":np.array(((80,60),(80,100),(100,60),(100,100))) }}
    home = house(params)
    home.show()
