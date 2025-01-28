# Model Dyfuzji Ciepła w Mieszkaniu

Projekt symulacji ogrzewania mieszkania pozwala na modelowanie i wizualizację rozprzestrzeniania się ciepła w pomieszczeniach.

[raport](https://github.com/ppodgors/HomeHeatingModel/blob/main/raport.ipynb)
## Wprowadzenie

Model opiera się na równaniu reakcji-dyfuzji i uwzględnia różne warunki brzegowe dla okien, drzwi i ścian. 
Schemat mieszkania i rozkład wszystkich obiektów - `Home diagram.png`.

## Funkcje

- Symulacja interaktywna pozwalająca na wybór czasu ogrzewania i poziomów grzejników.
- Wizualizacja procesu ogrzewania poprzez heatmapy.
- Modelowanie wpływu okien, drzwi i ścian na dystrybucję ciepła.

## Uruchomienie

Aby uruchomić symulację należy uruchomić `main`. Alternatywnie, można użyć aplikacji interaktywnej w serwisie streamlit.io ([link](https://homeheatingmodel-fvftdvvvwvqn3m6fn4nvoy.streamlit.app/)) do zasymulowania ogrzewania, wybierając poziom grzejnika oraz czas trwania symulacji.

## Technologie

- Python 3.8
- NumPy
- Matplotlib
