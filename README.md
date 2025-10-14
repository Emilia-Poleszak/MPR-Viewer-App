# ISMED Projekt 2 "MPR Viewer App"

Projekt wykonany w trakcie kursu Informatyczne Systemy Medyczne (ISMED) w czasie studiów na kierunku
Inżynieria Biomedyczna na Politechnice Warszawskiej, Wydziale Elektroniki i Technik Informacyjnych.

## Autorzy

- Emilia Poleszak (https://github.com/Emilia-Poleszak)
- Anna Czarkowska (https://github.com/czarkosia)

## Uruchomienie programu

### Wymagania

Zainstalowany Python3.

### Instalowanie bibliotek

Lista wymaganych zewnętrznych bibliotek znajduje się w pliku `requirements.txt`,
który znajduje się w katalogu głównym repozytorium. Aby je zainstalować, należy
wpisać poniższe polecenie do terminala:

```
pip install -r requirements.txt
```

### Uruchomienie programu

Program można uruchomić poprzez wpisanie poniższego polecenia do terminala:

```
python3 main.py <directory_path>
```

Gdzie <directory_path> to ścieżka bezwzględna do folderu z danymi wpisana bez cudzysłowu.

Program działa na zbiorze danych w formacie DICOM.

## Obsługa programu

Aby wyświetlić rekonstrukcję MPR należy uruchomić program, podając jako argument ścieżkę
do folderu z danymi w formacie DICOM. Aby wybrać skan do zmiany położenia lub zmiany
nachylenia kąta obrotu należy najechać na ten skan myszką, a następnie nacisnąć
lewy przycisk myszy. W celu zmiany kąta nachylenia osi danego skanu należy skorzystać
z dolnego suwaka. W celu zmiany położenia osi należy skorzystać z górnego suwaka
lub scrolla. Możliwe jest naprzemienne korzystanie z suwaków. Aby wrócić do ustawień 
początkowych danego skanu, należy nacisnąć przycisk reset.

## Działanie programu

Program pobiera dane z plików w formacie DICOM, a następnie tworzy z nich skan 3D.
Po uruchomieniu programu domyślnie wyświetla przekroje wyrównane do osi
coronal (górny lewy skan), sagittal (górny prawy skan) i axial (dolny skan) oraz wybiera
górny lewy skan do edycji. Do wyznaczenia obróconej lub przeniesionej płaszczyzny program
korzysta z algorytmu Bresenham'a.

## Zbiór danych

- https://www.ire.pw.edu.pl/~trubel/ismed/files/data/dicom_cranium_ct.zip

- https://www.dicomlibrary.com/?manage=1b9baeb16d2aeba13bed71045df1bc65
