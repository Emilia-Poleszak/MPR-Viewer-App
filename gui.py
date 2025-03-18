from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button
import mpr


class MprViewerApp:
    """
    A class for visualizing 3D Medical Image reconstructions using MPR (Multi-Planar Reconstruction) techniques.
    Provides a graphical user interface (GUI) to view and manipulate scans in different planes (axial, coronal, and sagittal).

    :param __rawdata: The raw 3D medical image data used for visualization.
    :type __rawdata: ndarray
    :param __scans: The reconstructed 2D slices for each plane.
    :type __scans: list[ndarray]
    :param max_l: The maximum allowed rotation angles for each plane.
    :type max_l: list[int]
    :param xy: Coordinates defining intersections and projections for the planes.
    :type xy: list[list[int]]
    :param colors: Colors used to distinguish the axes of different planes.
    :type colors: list[str]
    :param __mainFigure: The main figure for the GUI.
    :type __mainFigure: matplotlib.figure.Figure
    :param __sfigs: Sub-figures for individual planes and controls.
    :type __sfigs: list[matplotlib.figure.SubFigure]
    """

    def __init__(self, directory: str):
        """
        Initializes the viewer with a directory containing CT data.
        It sets up the main figure, subfigures, and interactive sliders for manipulating 3D MPR viewports.

        :param directory: path to the dicom files with CT data
        :type directory: str
        """
        self.__rawdata = mpr.get_data(directory)
        self.__scans, self.xy, self.max_l = mpr.generate_2d_scan(self.__rawdata)
        self.previous_l = [0, 0, 0]
        self.choice = 0
        self.colors = ['r', 'y', 'g']
        self.__mainFigure = plt.figure("3D MPR Reconstruction Viewer", dpi=100)
        self.__mainFigure.patch.set_color('black')
        self.__mainFigure.subfigures(2, 2)
        self.__sfigs = self.__mainFigure.subfigs

        for i in range(3):
            self.update_scan(i)
            self.__sfigs[i].patch.set_width(0.98)
            self.__sfigs[i].patch.set_height(0.98)
            self.__sfigs[i].patch.set_linewidth(1)
            self.__sfigs[i].patch.set_edgecolor(self.colors[i])
            self.__sfigs[i].canvas.mpl_connect('scroll_event', self.onscroll)
            self.__sfigs[i].canvas.mpl_connect('button_press_event', self.onclick)
        self.__sfigs[0].set_linewidth(3)

        self.__sfigs[3].add_subplot(4, 1, 2)
        self.__transmit_slider = Slider(ax=self.__sfigs[3].axes[0], label="Projection number", valmin=0,
                                        valmax=self.__rawdata.shape[0] - 1,
                                        valinit=self.xy[self.choice][0], track_color='gray', valstep=1)
        self.__transmit_slider.on_changed(self.move_section)
        self.__transmit_slider.label.set_position((1, 0))
        self.__transmit_slider.label.set_color('gray')

        self.__sfigs[3].add_subplot(4, 1, 3)
        self.__rotate_slider = Slider(ax=self.__sfigs[3].axes[1], label="Rotation angle",
                                      valmin=-1 * self.max_l[0], valmax=self.max_l[0],
                                      valinit=0, track_color='gray')
        self.__rotate_slider.on_changed(self.rotate_section)
        self.__rotate_slider.label.set_position((1, 0))
        self.__rotate_slider.label.set_color('gray')

        self.__sfigs[3].add_subplot(5 , 3, 15)
        self.__reset_button = Button(self.__sfigs[3].axes[2], label="Reset", color='gray')
        self.__reset_button.on_clicked(self.reset)

        plt.show()

    def update_scan(self, plane: int):
        """
        Redraws a viewport and its axes for the given plane.

        :param plane: number of the plane for which a scan is redrawn (0 - coronal, 1 - sagittal, 2 - axial)
        :type plane: int

        :raises Exception: Wrong plane number input
        """
        if plane < 0 or plane >= 3: raise Exception("Wrong plane choice")
        self.__sfigs[plane].clear()
        self.__sfigs[plane].subplots()
        mpr.show_slice(self.__scans[plane])
        self.update_lines(plane=plane)
        self.__mainFigure.canvas.draw_idle()
        self.__mainFigure.canvas.flush_events()

    def update_lines(self, plane: int):
        """
        Redraws axes overlaid on a scan image of the given plane that shows orientation of other planes' intersections
        
        :param plane: number of the plane for which lines are redrawn (0 - coronal, 1 - sagittal, 2 - axial)
        :type plane: int

        :raises Exception: Wrong plane number input
        """
        if plane < 0 or plane >= 3: raise Exception("Wrong plane choice")
        if plane == 0:
            x = 2
            y = 1
        elif plane == 1:
            x = 2
            y = 0
        elif plane == 2:
            x = 1
            y = 0

        vertical = plt.axline(xy1=(self.xy[x][0], self.xy[x][1]),
                              xy2=(self.xy[x][2], self.xy[x][3]))
        horizontal = plt.axline(xy1=(self.xy[y][1], self.xy[y][0]),
                                xy2=(self.xy[y][3], self.xy[y][2]))
        vertical.set_color(self.colors[x])
        horizontal.set_color(self.colors[y])

    def move_section(self, index: int):
        """
        Updates the current section being viewed based on the transmit slider's value.

        :param index: transmit slider's value describing plane axis position
        :type index: int
        """
        try:
            self.__scans[self.choice], self.xy = mpr.transmit(self.__rawdata, self.xy, index, self.choice)
        except(ValueError, TypeError):
            return
        for i in range(3):
            self.update_scan(i)

    def rotate_section(self, l):
        """
        Rotates the axes of the chosen plane by the given angle using the rotate slider.

        :param l: unit of rotation defined by the rotate slider
        """
        temp = int(l)
        l = int(l) - self.previous_l[self.choice]
        self.previous_l[self.choice] = temp
        try:
            if self.choice == 0:
                self.__scans[1], self.xy = mpr.rotate(self.__rawdata, self.xy, l, 1)
                self.__scans[2], self.xy = mpr.rotate(self.__rawdata, self.xy, (-1 * l), 2)
            elif self.choice == 1:
                self.__scans[0], self.xy = mpr.rotate(self.__rawdata, self.xy, l, 0)
                self.__scans[2], self.xy = mpr.rotate(self.__rawdata, self.xy, (-1 * l), 2)
            elif self.choice == 2:
                self.__scans[0], self.xy = mpr.rotate(self.__rawdata, self.xy, l, 0)
                self.__scans[1], self.xy = mpr.rotate(self.__rawdata, self.xy, (-1 * l), 1)
        except (ValueError, TypeError):
            return

        for i in range(3):
            self.update_scan(i)

    def reset(self, event):
        """
        Resets chosen plane and its parameters to their initial state.
        """
        self.__transmit_slider.set_val(self.__rawdata.shape[self.choice]//2)
        self.__rotate_slider.set_val(0)
        for i in range(3):
            self.update_scan(i)

    def onscroll(self, event):
        """
        Handles scroll events to navigate through sections of the chosen plane.

        :param event: scroll event connected to subfigures
        """
        try:
            if event.button == 'up' and self.xy[self.choice][0] > 0:
                self.__scans[self.choice], self.xy = mpr.transmit(self.__rawdata, self.xy, -1, self.choice)
            if event.button == 'down' and self.xy[self.choice][0] < self.__rawdata.shape[self.choice] - 1:
                self.__scans[self.choice], self.xy = mpr.transmit(self.__rawdata, self.xy, 1, self.choice)

            self.__transmit_slider.set_val(self.xy[self.choice][0])
            for i in range(3):
                self.update_scan(i)
        except:
            print("onscroll error")

    def onclick(self, event):
        """
        Handles mouse click events to select the active plane for modifications.

        :param event: click event connected to subfigures
        """
        if event.inaxes in self.__sfigs[3].axes:
            return
        for i in range(3):
            if self.__sfigs[i].axes[0] == event.inaxes:
                self.choice = i
                self.__sfigs[i].patch.set_linewidth(3)

                self.__transmit_slider.valmax = self.__rawdata.shape[i] - 1
                self.__transmit_slider.set_val(self.xy[i][0])

                self.__rotate_slider.valmin = -1 * self.max_l[i]
                self.__rotate_slider.valmax = self.max_l[i]
                self.previous_l = [0, 0, 0]
                self.__rotate_slider.set_val(0)
            else:
                self.__sfigs[i].patch.set_linewidth(1)
        self.__mainFigure.canvas.draw_idle()
        self.__mainFigure.canvas.flush_events()
