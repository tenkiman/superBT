#!/usr/bin/env python

import struct
import os

def write_2d_list_to_binary(data, filename):
    """
    Converts a 2D Python list to a binary file of IEEE 754 32-bit floats.
    
    Args:
        data (list[list[float]]): 2D list of floats.
        filename (str): Path to output binary file.
    """
    # Validate input type
    if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
        raise TypeError("Input must be a 2D list.")

    # Validate all elements are numbers
    for row in data:
        if not all(isinstance(x, (int, float)) for x in row):
            raise ValueError("All elements must be int or float.")

    try:
        with open(filename, "wb") as f:
            for row in data:
                for value in row:
                    # Pack each value as 32-bit float (little-endian)
                    f.write(struct.pack('<f', float(value)))
        print(f"Binary file '{filename}' written successfully. Size: {os.path.getsize(filename)} bytes")
    except OSError as e:
        print(f"Error writing file: {e}")


def read_binary_to_2d_list(filename, rows, cols):
    """
    Reads a binary file of float32 values into a 2D Python list.
    
    Args:
        filename (str): Path to binary file.
        rows (int): Number of rows in the 2D list.
        cols (int): Number of columns in the 2D list.
    
    Returns:
        list[list[float]]: 2D list of floats.
    """
    try:
        with open(filename, "rb") as f:
            data = []
            for _ in range(rows):
                row = []
                for _ in range(cols):
                    # Read 4 bytes and unpack as float
                    bytes_read = f.read(4)
                    if len(bytes_read) < 4:
                        raise ValueError("Unexpected end of file.")
                    row.append(struct.unpack('<f', bytes_read)[0])
                data.append(row)
        return data
    except OSError as e:
        print(f"Error reading file: {e}")
        return None


# Example usage
if __name__ == "__main__":
    data_2d = [
        [3.14, 2.7, 0.0],
        [-1.0, 1.1, 5.5]
    ]

    file_path = "floats_pure_python.bin"

    # Write binary file
    write_2d_list_to_binary(data_2d, file_path)
    
    # Read back and verify
    loaded_data = read_binary_to_2d_list(file_path, 2, 3)
    print("Loaded 2D list from binary file:")
    print(loaded_data)



