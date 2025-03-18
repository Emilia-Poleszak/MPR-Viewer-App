import os
import sys
from PIL import Image
import pydicom
from matplotlib import pyplot as plt
import numpy as np


def get_data(path):
    """
    Loads DICOM files and creates a 3D CT scan form it.

    :param: path: data directory path
    :type path: str

    :return: 3D CT scan
    """
    all_scans = []
    try:
        for i in sorted(os.listdir(path)):
            if i.endswith('.dcm'):
                scan2d = pydicom.dcmread(os.path.join(path, i))
                all_scans.append(scan2d.pixel_array)

        data = np.stack(all_scans, axis=2)
    except ValueError:
        print("Given directory does not contain DICOM files.")
        sys.exit()

    return data


def bresenham_line(x1, y1, x2, y2):
    """
    Bresenham line algorythm implementation.

    Sources: https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm [18.01.2025]

    Creates two arrays of x and y coordinates of a line,
    which starts at (x1, y1), and ends at (x2, y2).

    :param x1: Starting x coordinate.
    :type x1: int
    :param y1: Starting y coordinate.
    :type y1: int
    :param x2: Ending x coordinate.
    :type x2: int
    :param y2: Ending y coordinate.
    :type y2: int

    :return: Array of x coordinates,
             Array of y coordinates.
    """
    x, y = min(x1, x2), y1
    x2 = max(x1, x2)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    p = 2 * dy - dx
    xc = [x]
    yc = [y]

    if dx == 0:
        for i in range(1, (dy + 1)):
            xc.append(x)
            yc.append(y1 + i)
    elif dy == 0:
        for i in range(1, (dx + 1)):
            yc.append(y)
            xc.append(x1 + i)

    for i in range(2, dx + 2):
        if p > 0:
            p = p + 2 * (dy - dx)
            y = y + 1
        else:
            p = p + 2 * dy
            x = x + 1
        xc.append(x)
        yc.append(y)

    return xc, yc


def generate_2d_scan(data):
    """
    Generates 3 2D scans of planes coronal, sagittal and axial.

    :param data: 3D CT scan.
    :type data: ndarray

    :return: Array of 3 2D CT scans,
             table of starting and ending (x,y) coordinates for each plane,
             table of maximal unit of rotation for each plane.
    """
    scan_slices = [data[data.shape[0] // 2, :, :],
                   data[:, data.shape[1] // 2, :],
                   data[:, :, data.shape[2] // 2]]

    xy = [[data.shape[0] // 2, 0, data.shape[0] // 2, data.shape[2] - 1],  # for plane 0
          [data.shape[1] // 2, 0, data.shape[1] // 2, data.shape[2] - 1],  # for plane 1
          [data.shape[2] // 2, 0, data.shape[2] // 2, data.shape[1] - 1]]  # for plane 2

    max_l = [min((data.shape[1] // 2 - 1), (data.shape[2] // 2 - 1)),  # for plane 0
             min((data.shape[0] // 2 - 1), (data.shape[2] // 2 - 1)),  # for plane 1
             min((data.shape[0] // 2 - 1), (data.shape[1] // 2 - 1))]  # for plane 2

    return scan_slices, xy, max_l


def stack_rows(data, x, y, plane):
    """
    Creates a 2D CT scan from a 3D CT scan, using given x, y coordinates.

    :param data: 3D CT scan.
    :type data: ndarray
    :param x: 2D array of x coordinates.
    :type x: list
    :param y: 2D array of y coordinates.
    :type y: list
    :param plane: 0 - coronal, 1 - sagittal, 2 - axial.
    :type plane: int

    :return: 2D CT scan.
    """
    row = []
    if plane == 0:
        for i in range(len(x)):
            if 0 <= x[i] < data.shape[0] and 0 <= y[i] < data.shape[2]:
                row.append(data[x[i], :, y[i]])
        slice_2d = np.stack(row, axis=1)
        return slice_2d

    elif plane == 1:
        for i in range(len(x)):
            if 0 <= x[i] < data.shape[1] and 0 <= y[i] < data.shape[2]:
                row.append(data[:, x[i], y[i]])
        slice_2d = np.stack(row, axis=1)
        return slice_2d

    elif plane == 2:
        for i in range(len(x)):
            if 0 <= x[i] < data.shape[2] and 0 <= y[i] < data.shape[1]:
                row.append(data[:, y[i], x[i]])
        slice_2d = np.stack(row, axis=1)
        return slice_2d


def transmit(data, xy, index, plane):
    """
    Transmits 2D scan slice by given length in given plane.

    :param data: 3D CT scan.
    :type data: ndarray
    :param xy: Table of starting and ending coordinates.
    :type xy: list[list[int]]
    :param index: new position of the plane axis
    :type index: int
    :param plane: 0 - coronal, 1 - sagittal 2 - axial.
    :type plane: int

    :return: Transmitted 2D scan slice,
             table of transformed starting and ending (x,y) coordinates.
    """
    xy[plane][0] = index
    xy[plane][2] = index
    x, y = bresenham_line(xy[plane][0], xy[plane][1], xy[plane][2], xy[plane][3])
    scan2d = stack_rows(data, x, y, plane)

    return scan2d, xy


def rotate(data, xy, l, plane):
    """
    Rotates a 2D scan slice by given angle.

    :param data: 3D CT scan.
    :type data: ndarray
    :param xy: Table of starting and ending (x,y) coordinates.
    :type xy: list[list[int]]
    :param l: Unit of rotation, must be greater or equal to 0.
    :type l: int
    :param plane: 0 - coronal, 1 - sagittal, 2 - axial.
    :type l: int

    :return: Rotated 2D scan slice,
             modified table of (x,y) starting and ending coordinates.
    """
    xy = xy[:]
    xy[plane][0] = xy[plane][0] - l
    xy[plane][2] = xy[plane][2] + l
    if xy[plane][2] - xy[plane][0] == 0:
        x, y = bresenham_line(xy[plane][0], xy[plane][1], xy[plane][2], xy[plane][3])
    else:
        y, x = bresenham_line(xy[plane][1], xy[plane][0], xy[plane][3], xy[plane][2])
    try:
        slice2d = stack_rows(data, x, y, plane)
    except(ValueError, TypeError):
        return

    return slice2d, xy


def show_slice(scan2d):
    """
    Prints one 2D CT scan.

    :param scan2d: 2D CT scan.
    :type scan2d: ndarray
    """
    scan2d_image = Image.fromarray(scan2d)
    plt.imshow(scan2d_image, cmap='gray')
    plt.axis('off')
