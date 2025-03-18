import sys
import gui

if __name__ == "__main__":
    try:
        gui.MprViewerApp(sys.argv[1])
    except(IndexError, FileNotFoundError):
        print("No directory found.")
