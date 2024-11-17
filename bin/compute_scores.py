#!/usr/bin/env python3
import sys
from PIL import Image
import numpy as np
from scipy.spatial.distance import cdist

def read_image(image_filename):
    """Read PNG image and convert to RGB numpy array."""
    try:
        with Image.open(image_filename) as img:
            # Convert to RGB mode if not already
            img = img.convert('RGB')
            # Convert to numpy array
            return np.array(img)
    except Exception as e:
        print(f"Failed to open image: {e}", file=sys.stderr)
        return None

def compute_column_scores(image_array):
    """Compute pairwise column similarity scores using scipy's cdist."""
    height, width, _ = image_array.shape
    
    # Reshape columns into 2D array where each row represents a column's RGB values
    columns = image_array.reshape(height, width, 3).transpose(1, 0, 2)
    columns = columns.reshape(width, -1)  # Flatten each column's RGB values
    
    # Compute pairwise Manhattan distances between all columns
    distances = cdist(columns, columns, metric='cityblock')
    
    # We only need the upper triangle
    distances = np.triu(distances, k=1)
    
    return distances

def write_tsplib(scores, image_filename):
    """Write the scores in TSPLIB format."""
    width = scores.shape[0]
    
    print(f"NAME : column similarity for {image_filename}")
    print("TYPE : TSP")
    print(f"DIMENSION : {width + 1}")
    print("EDGE_WEIGHT_TYPE : EXPLICIT")
    print("EDGE_WEIGHT_FORMAT : UPPER_ROW")
    print("NODE_COORD_TYPE : NO_COORDS")
    print("DISPLAY_DATA_TYPE : NO_DISPLAY")
    print()
    print("EDGE_WEIGHT_SECTION :")
    
    # Print first row of zeros
    print(" ".join("0" for _ in range(width)))
    
    # Print upper triangular matrix
    for i in range(width):
        row = [str(int(scores[i, j])) for j in range(i + 1, width)]
        if row:  # Only print if there are elements in the row
            print(" ".join(row))

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} input.png", file=sys.stderr)
        sys.exit(1)
        
    image_filename = sys.argv[1]
    
    # Read image
    image_array = read_image(image_filename)
    if image_array is None:
        print(f"{sys.argv[0]}: Failed to read image", file=sys.stderr)
        sys.exit(1)
    
    # Compute scores
    scores = compute_column_scores(image_array)
    
    # Write output in TSPLIB format
    write_tsplib(scores, image_filename)

if __name__ == "__main__":
    main()
