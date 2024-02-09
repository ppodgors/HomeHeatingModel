import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import copy

class House:
    def __init__(self,params):
        self.params = params
        self.initial_rooms= {}
        self.rooms_with_objects = {}
        self.walls_in_rooms = {'I': [], 'II': [], 'III': [], 'IV': [], 'V': []}
        self.home = np.zeros((101,101))
        self.result_matrix = np.zeros((101,101))
        self.build_initial_matrices()
        #abcd = self.build_result_matrix(self.rooms_with_objects,1)
        #plt.imshow(abcd)
        #plt.show()
        #print(self.rooms_with_objects["V"][-2,:])
        #print(self.rooms_with_objects["V"][-1,:])
    def outside_temp(self, t):
        T_srednia = -2.5  
        A = 4.5           
        T_okres = 24*60   
        return T_srednia + A * np.sin(2 * np.pi / T_okres * t) + 273

        
    def build_initial_matrices(self, show = True):
        room_windows = {'I': [], 'II': [], 'III': [], 'IV': [], 'V': []}
        room_heaters = {'I': [], 'II': [], 'III': [], 'IV': [], 'V': []}
        room_doors = {'I': [], 'II': [], 'III': [], 'IV': [], 'V': []}
        for window in self.params["windows"]:
            room_windows[window.room_nr()].append(window)
        for heater in self.params["heaters"]:
            room_heaters[heater.room_nr()].append(heater)
        for door in self.params["doors"]:
            room_doors[door.room_nr()].append(door)
        for key, room in self.params["rooms"].items():
            self.initial_rooms[key] = np.zeros((room.x_len()+1, room.y_len()+1))
            self.rooms_with_objects[key] = np.zeros((room.x_len()+1, room.y_len()+1))
            self.initial_rooms[key] = room.init_fun()(self.initial_rooms[key])
           # adding windows to each room
            for window in room_windows[key]:
                if not window.is_horizontal():
                    x_min, x_max, y = window.coordinates()
                    self.rooms_with_objects[key][(x_min-room.x_min()):(x_max-room.x_min()), (y - room.y_min())] = 1
                    self.initial_rooms[key][(x_min-room.x_min()):(x_max-room.x_min()), (y - room.y_min())] = self.outside_temp(0)
                else:
                    y_min, y_max, x = window.coordinates()
                    self.rooms_with_objects[key][(x-room.x_min()), (y_min-room.y_min()):(y_max-room.y_min())] = 1
                    self.initial_rooms[key][(x-room.x_min()), (y_min-room.y_min()):(y_max-room.y_min())] = self.outside_temp(0)
            for dict in [self.rooms_with_objects, self.initial_rooms]:
                #dict[key] = dict[key][:-1,:-1]
                dict[key][:,-2] = dict[key][:,-1]
                dict[key][:,1] = dict[key][:,0]
                dict[key][-2,:] = dict[key][-1,:]
                dict[key][1,:] = dict[key][0,:]
            for door in room_doors[key]:
                if not door.is_horizontal():
                    x_min, x_max, y = door.coordinates()
                    self.rooms_with_objects[key][(x_min-room.x_min()):(x_max-room.x_min()), (y - room.y_min())] = 2
                else:
                    y_min, y_max, x = door.coordinates()
                    self.rooms_with_objects[key][(x-room.x_min()), (y_min-room.y_min()):(y_max-room.y_min())] = 2

            # adding heaters, values in [0.1, ... , 0.5]

            for heater in room_heaters[key]:
                if not heater.is_horizontal():
                    x_min, x_max, y = heater.coordinates()
                    self.rooms_with_objects[key][(x_min-room.x_min()):(x_max-room.x_min()), (y - room.y_min())] = heater.get_level()/10
                else:
                    y_min, y_max, x = heater.coordinates()
                    self.rooms_with_objects[key][(x-room.x_min()), (y_min-room.y_min()):(y_max-room.y_min())] = heater.get_level()/10
            

            if key != "III":
                self.rooms_with_objects[key][:,-4] = self.rooms_with_objects[key][:,-3]
                self.rooms_with_objects[key][:,3] = self.rooms_with_objects[key][:,2]
                self.rooms_with_objects[key][-4,:] = self.rooms_with_objects[key][-3,:]
                self.rooms_with_objects[key][3,:] = self.rooms_with_objects[key][2,:]
            else:
                self.rooms_with_objects[key][:,-3] = self.rooms_with_objects[key][:,-2]
        self.room_doors = room_doors
            #self.initial_rooms[key] = self.initial_rooms[key][1:,1:]
        if not show:
            #cmapmine = ListedColormap(['lightgray','dodgerblue',"red"], N=3),,cmap=cmapmine
            plt.imshow(self.rooms_with_objects["IV"])
            plt.show()
    def build_partial_matrices(self,t):
        doors = self.params["doors"]
        for key, room in self.initial_rooms.items():
            top = room[:,0]
            if self.params["walls"][key][2]:
                room[:,0] = room[:,1]
            else:
                for i in range(len(top)):
                    if self.rooms_with_objects[key][i,0] == 1:
                        room[i,0:1] = self.outside_temp(t)
                    else:
                        room[i,0:1] = room[i,2]
            bottom = room[:,-1]
            if self.params["walls"][key][3]:
                room[:,-1] = room[:,-2]
            else:
                for i in range(len(bottom)):
                    if self.rooms_with_objects[key][i,-1] == 1:
                        room[i,-2] = self.outside_temp(t)
                        room[i,-1] = self.outside_temp(t)
                    else:
                        room[i,-2] = room[i,-3]
                        room[i,-1] = room[i,-3]
            left = room[0,1:-1]
            if self.params["walls"][key][0]:
                room[0,1:-1] = room[1,1:-1]
            else:
                for i in range(1, len(left)):
                    if self.rooms_with_objects[key][0,i] == 1:
                        room[0:1,i] = self.outside_temp(t)
                    else:
                        room[0:1,i] = room[2,i]
            right = room[-1,1:-1]
            if self.params["walls"][key][1]:
                room[-1,1:-1] = room[-1,1:-1]
            else:
                for i in range(1, len(right)):
                    if self.rooms_with_objects[key][-1,i] == 1:
                        room[-2,i] = self.outside_temp(t)
                        room[-1,i] = self.outside_temp(t)
                    else:
                        room[-2,i] = room[-3,i]
                        room[-1,i] = room[-3,i]        
        for key, room in self.params["rooms"].items():
            self.result_matrix[room.x_min():room.x_max()+1, room.y_min():room.y_max()+1] = self.initial_rooms[key]
        for x in range(0, len(doors),2):
            door1 = doors[x]
            door2 = doors[x+1]
            if not door1.is_horizontal():
                x_min, x_max, y1 = door1.coordinates()
                x_min, x_max, y2 = door2.coordinates()
                y_min = min(y1,y2)
                y_max = max(y1,y2)
                self.initial_rooms[door1.room_nr()][(x_min-self.params["rooms"][door1.room_nr()].x_min()):(x_max-self.params["rooms"][door1.room_nr()].x_min()),
                                                     (y1 - self.params["rooms"][door1.room_nr()].y_min())] = np.mean(self.result_matrix[x_min:x_max, y_min:y_max])
                self.initial_rooms[door2.room_nr()][(x_min-self.params["rooms"][door2.room_nr()].x_min()):(x_max-self.params["rooms"][door2.room_nr()].x_min()),
                                                     (y2 - self.params["rooms"][door2.room_nr()].y_min())] = np.mean(self.result_matrix[x_min:x_max, y_min:y_max])
            else:
                y_min, y_max, x1 = door1.coordinates()
                y_min, y_max, x2 = door2.coordinates()
                x_min = min(x1,x2)
                x_max = max(x1,x2)
                self.initial_rooms[door1.room_nr()][(x1-self.params["rooms"][door1.room_nr()].x_min()),
                                                     (y_min - self.params["rooms"][door1.room_nr()].y_min()):(y_max - self.params["rooms"][door1.room_nr()].y_min())] = np.mean(self.result_matrix[x_min:x_max, y_min:y_max])
                self.initial_rooms[door2.room_nr()][(x2-self.params["rooms"][door2.room_nr()].x_min()),
                                                     (y_min - self.params["rooms"][door2.room_nr()].y_min()):(y_max - self.params["rooms"][door2.room_nr()].y_min())] = np.mean(self.result_matrix[x_min:x_max, y_min:y_max])



    def build_result_matrix(self,t):
        self.result_matrix[:,:] = self.outside_temp(t)
        for key, room in self.params["rooms"].items():
            self.result_matrix[room.x_min():room.x_max()+1, room.y_min():room.y_max()+1] = self.initial_rooms[key]
    def matrix_to_plot(self):
        for key, room in self.params["rooms"].items():
            self.home[room.x_min():room.x_max(), room.y_min():room.y_max()] = 1
            self.home[room.x_min(), room.y_min():room.y_max()]=2
            self.home[room.x_max(), room.y_min():room.y_max()]=2
            self.home[room.x_min():room.x_max(), room.y_min()]=2
            self.home[room.x_min():room.x_max(), room.y_max()]=2
        for window in self.params["windows"]:
            if window.is_horizontal():
                y_min, y_max, x = window.coordinates()
                self.home[x, y_min:y_max] = 3
            else:
                x_min, x_max, y = window.coordinates()
                self.home[x_min:x_max, y] = 3
        for heater in self.params["heaters"]:
            if heater.is_horizontal():
                y_min, y_max, x = heater.coordinates()
                self.home[x, y_min:y_max] = 4
            else:
                x_min, x_max, y = heater.coordinates()
                self.home[x_min:x_max, y] = 4
        for door in self.params["doors"]:
            if door.is_horizontal():
                y_min, y_max, x = door.coordinates()
                self.home[x, y_min:y_max] = 1
            else:
                x_min, x_max, y = door.coordinates()
                self.home[x_min:x_max, y] = 1
        
    def solution(self, D):
        dt = 1
        dx = 1
        self.build_result_matrix(0)
        result_matrices = [self.result_matrix.copy()-273]
        #plt.imshow(result_matrices[0])
        #plt.show()
        heat = 0
        for t in range(1, 10*60):
            for key, room in self.initial_rooms.items():
                nrows, ncols = room.shape
                #room_dt = np.zeros_like(room)
                room_dt = room.copy()
                room_temp = np.mean(room)
                for i in range(1, nrows - 1):
                    for j in range(1, ncols - 1):
                        #print("stara", room[i,j])
                        if 0<self.rooms_with_objects[key][i,j]<1: 
                            #print("check", self.rooms_with_objects[key][i,j]*10*3+10+273, room_temp < (self.rooms_with_objects[key][i,j]*10*3+10+273))
                            if room_temp < (self.rooms_with_objects[key][i,j]*10*3+10+273):
                                laplacian = (room[i+1, j] + room[i-1, j] +
                                            room[i, j+1] + room[i, j-1] -
                                            4 * room[i, j]) / dx**2
                                f = self.rooms_with_objects[key][i,j]*10/10
                                heat = heat + f
                                laplacian = laplacian + f
                                room_dt[i, j] = room[i, j] + D * laplacian * dt
                        elif self.rooms_with_objects[key][i,j] == 1:
                            room_dt[i, j] = self.outside_temp(t)
                        else:
                            laplacian = (room[i+1, j] + room[i-1, j] +
                                        room[i, j+1] + room[i, j-1] -
                                        4 * room[i, j]) / dx**2
                            room_dt[i, j] = room[i, j] + D * laplacian * dt
                self.initial_rooms[key] = room_dt
            self.build_partial_matrices(t)
            self.build_result_matrix(t)
            result_matrices.append(self.result_matrix.copy()-273)
        return result_matrices

    def show(self):
        self.matrix_to_plot()
        cmapmine = ListedColormap(['lightgray','white','black','dodgerblue', 'red'], N=5)
        plt.imshow(self.home,cmap=cmapmine)
        plt.show()

 