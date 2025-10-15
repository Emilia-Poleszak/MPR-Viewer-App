# ISMED Projekt 2 "MPR Viewer App"

[English version below]

## [PL]

Aplikacja wyświetla 3 pojedńcze, ortogonalne slice'y skanu 3D. Możliwe jest obracanie i przesuwanie wyświetlanych slice'ów.
Obsługiwane są wyłącznie pliki formatu DICOM.

Projekt wykonany w trakcie kursu Informatyczne Systemy Medyczne (ISMED) w czasie studiów na kierunku
Inżynieria Biomedyczna na Politechnice Warszawskiej, Wydziale Elektroniki i Technik Informacyjnych.

### Autorzy

- Emilia Poleszak (https://github.com/Emilia-Poleszak)
- Anna Czarkowska (https://github.com/czarkosia)

### Wymagania

Zainstalowany Python3.

Lista wymaganych zewnętrznych bibliotek znajduje się w pliku `requirements.txt`,
który znajduje się w katalogu głównym repozytorium. Aby je zainstalować, należy
wpisać poniższe polecenie do terminala:

```
pip install -r requirements.txt
```

### Obsługa programu

Program można uruchomić poprzez wpisanie poniższego polecenia do terminala:

```
python3 main.py <directory_path>
```
Gdzie directory_path - ścieżka do folderu ze skanami DICOM. 

Aby wyświetlić rekonstrukcję MPR należy uruchomić program, podając jako argument ścieżkę
do folderu z danymi w formacie DICOM. Aby wybrać skan do zmiany położenia lub zmiany
nachylenia kąta obrotu należy najechać na ten skan myszką, a następnie nacisnąć
lewy przycisk myszy. W celu zmiany kąta nachylenia osi danego skanu należy skorzystać
z dolnego suwaka. W celu zmiany położenia osi należy skorzystać z górnego suwaka
lub scrolla. Możliwe jest naprzemienne korzystanie z suwaków. Aby wrócić do ustawień 
początkowych danego skanu, należy nacisnąć przycisk reset.

### Działanie programu

Program pobiera dane z plików w formacie DICOM, a następnie tworzy z nich skan 3D.
Po uruchomieniu programu domyślnie wyświetla przekroje wyrównane do osi
coronal (górny lewy skan), sagittal (górny prawy skan) i axial (dolny skan) oraz wybiera
górny lewy skan do edycji. Do wyznaczenia obróconej lub przeniesionej płaszczyzny program
korzysta z algorytmu Bresenham'a.

### Moje zadania

Backend aplikacji:
- Wyłuskanie ortogonalnych slice'ów z całego skanu 3D
- Implementacja algorytmu Bresenhama
- Rotacja i transmisja płaszczyzn przekrojów

## [ENG]

The application displays three individual, orthogonal slices of the 3D scan. The displayed slices can be rotated and moved. 
Only DICOM files are supported.

This project was completed during the Information Systems in Medicine course ("Informatyczne Systemy Medyczne" - ISMED) 
during Biomedical Engineering studies at the Warsaw University of Technology, Faculty of Electronics and Information Technology.

### Authors

- Emilia Poleszak (https://github.com/Emilia-Poleszak)
- Anna Czarkowska (https://github.com/czarkosia)
  
### Requirements

Python3.

The list of required external libraries is located in the `requirements.txt` file,
located in the repository's root directory. To install use:

```
pip install -r requirements.txt
```

### User manual

To run use:

```
python3 main.py <directory_path>
```
Add directory path of DICOM scans as directory_path.

To display an MPR reconstruction, run the program, specifying the path to the folder containing the DICOM data as an argument. 
To select a scan for repositioning or changing the rotation angle, hover over the scan and then press the left mouse button. 
To change the axis tilt angle of a given scan, use the lower slider. To change the axis position, use the upper slider or scroll wheel. 
You can alternate between the sliders. To return to the initial settings for a given scan, press the reset button.

### How it works

The program retrieves data from DICOM files and then creates a 3D scan from them.
When the program is launched, it displays cross-sections aligned to the coronal (upper left scan), 
sagittal (upper right scan), and axial (lower scan) axes by default, and selects the upper left scan for editing.
The program uses the Bresenham algorithm to determine the rotated or translated plane.

### My responsibilites

Backend:
- Extracting orthogonal slices form 3D scan
- Implementing Bresenham line algorithm
- Rotation and transmission of planes
