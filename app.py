import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from house import House
from room import Room
from window import Window
from heater import Heater
from door import Door
import time
rooms = {"I": Room(0, 50, 0, 39, (lambda x: 283 + np.random.random(x.shape))), "II": Room(0, 34, 40, 100,(lambda x: 285 + np.random.random(x.shape))),
            "III": Room(35, 60, 40, 100,(lambda x: 286 + np.random.random(x.shape))),"IV": Room(61, 100, 40, 80,(lambda x: 287 + np.random.random(x.shape))),
            "V": Room(61, 100, 81, 100,(lambda x: 282 + np.random.random(x.shape)))}
windows = [Window(False, 75, 15, 0, "II"), Window(False, 50, 15, 0,"II"), Window(False, 10, 20, 0,"I"), 
            Window(True, 10, 15, 100,"II"), Window(True, 40, 15, 100,"III"), Window(True, 70, 20, 100,"V"),
            Window(False, 50, 20, 100,"IV"), Window(True, 15, 20, 0,"I")]
walls = {"I": [False, False, False, True], "II": [False, True, True, False], "III": [True, True, True, False], "IV":[True, False, False, True], "V": [True, False, True, False]} 

doors = [Door(True, 15, 10, 39,"I"),Door(True, 15, 10, 40,"II"), Door(False, 65, 10, 34,"II"),Door(False, 65, 10, 35,"III"), Door(False, 65, 10, 60,"III"),Door(False, 65, 10, 61,"IV"), 
            Door(False, 85,10,60,"III"),Door(False, 85,10,61,"V")]

def create_house_with_heater_levels(heater_levels):
    heaters = [Heater(False, 65, 10, 2,"II",heater_levels["II"]), Heater(False, 15, 10, 2, "I",heater_levels["I"]), Heater(False, 45, 15, 58,"III",heater_levels["III"],exterior=False),
            Heater(False, 55, 10, 98, "IV",heater_levels["IV"]), Heater(False, 85, 10, 98, "V",heater_levels["V"]), Heater(True, 20, 10, 98, "II",heater_levels["II"]), 
            Heater(True, 75, 10, 42, "IV",heater_levels["IV"]), Heater(True, 20, 10, 2, "I",heater_levels["I"])]

    params = {
        "rooms": rooms, 
        "windows": windows, 
        "heaters": heaters, 
        "doors": doors, 
        "walls": walls }

    return House(params)

def display_heatmap(frame_data):
    fig, ax = plt.subplots()
    heatmap = ax.imshow(frame_data, cmap='coolwarm', interpolation='nearest')
    plt.colorbar(heatmap)
    plt.close(fig)
    return fig, heatmap

def main():
    st.title("Symulacja rozkładu ciepła w domu")
    heater_levels = {}
    for room in rooms.keys():
        level = st.slider(f"Poziom mocy grzejnika dla pokoju {room}", 1, 5, 3)
        heater_levels[room] = level
    how_long = st.slider("Czas trwania symulacji (h)",1,24,10)
    placeholder = st.empty()

    if st.button('Start symulacji'):
        home = create_house_with_heater_levels(heater_levels)
        x, heat = home.solution(0.1, how_long)
        
        fig, heatmap = display_heatmap(x[0])
        placeholder.pyplot(fig)

        for frame in range(1, len(x), 10):
            current_time = round(frame / 60, 2)
            updated_state = x[frame]
            heatmap.set_data(updated_state)
            heatmap.axes.set_title(f"Czas symulacji: {current_time} h")
            placeholder.pyplot(fig)
            time.sleep(0.001)

if __name__ == "__main__":
    main()
