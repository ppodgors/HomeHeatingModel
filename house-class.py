import numpy as np 

class house:
    def __init__(self,params):
        self.matrix= {}
        for key in params["indexes"].keys():
            ind_min_x = min(key[:,0])
            ind_max_x = max(key[:,0])
            ind_min_y = min(key[:,1])
            ind_max_y = max(key[:,1])
            self.matrix[key] = np.zeros(((ind_max_x-ind_min_x,ind_max_y-ind_min_y)))

if __name__=="__main__":
  params = {"indeksy":{"`I": np.array(((0,0),(0,35),(20,35),(20,0))),"II" : np.array(((20,0),(20,35),(100,35),(100,0)))}}


  home = house(params)
