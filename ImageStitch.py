'''
Image stitching script for use on 'Spores in Space' project (Prof. Elena Ivanova and ResearchSat).

Images to be stitched must be stored in a directory named 'images' (case sensitive) and labelled
in the format 'row_col' (for example the image from row 1, column 3 is labelled 1_3.jpg).

@author: Sasha Brooke

'''

from PIL import Image
import os
import time
from functools import wraps

def current_time():
    """
    Gets current time.

    @return: Current time, formatted hour:minute:second
    @rtype message: str

    """
    t = time.localtime()
    return time.strftime("%H:%M:%S", t)

def log(message):
    """
    Displays log information to the user (including time-stamps).

    @param message: The log message to be displayed to the user - can be a variable value or progress message.
    @type message: str

    """
    print(f"{current_time()} [ LOG: {message} ]")

def timer(func):
    @wraps(func)
    def wrapper():
        start_time = time.perf_counter()
        func()
        end_time = time.perf_counter()
        total_time = end_time - start_time
        log(f"Grid stitch ({func.__name__}) success ({total_time:.4f} seconds)")
    return wrapper

@timer
def main():
    log("Performing grid stitch")

    # set the size of each image
    img_size = 300

    # set the directory where the images are stored
    img_dir = './source_images'

    # get the list of image filenames
    img_files = os.listdir(img_dir)

    # determine the number of rows and columns based on the image filenames
    max_row = max([int(filename.split('_')[0].strip('.jpg')) for filename in img_files])
    max_col = max([int(filename.split('_')[1].strip('.jpg')) for filename in img_files])
    rows, cols = max_row, max_col
    log(f"num_files={str(rows*cols)}")
    log(f"rows={str(rows)} cols={str(cols)}")

    # create a new image to hold the collage
    collage = Image.new('RGB', (cols*img_size, rows*img_size))

    # iterate over each image and paste it into the collage
    for img_filename in img_files:
        # extract the row and column information from the filename
        row, col = [int(img_filename.split('_')[0]), int(img_filename.split('_')[1].strip('.jpg')) ]
        
        # open the image file
        img_path = os.path.join(img_dir, img_filename)
        img = Image.open(img_path)
        
        # resize the image to fit in the grid
        img = img.resize((img_size, img_size))
        
        # calculate the position of the image in the collage
        x = (col-1)*img_size
        y = (row-1)*img_size
        
        # paste the image into the collage
        collage.paste(img, (x, y))

    # save the collage as a new image
    output_dir = "stitched_images"
    file_name = os.path.join(output_dir, "Grid_stitch_{time}.png".format(time = current_time().replace(':', '-')))
    collage.save(file_name)

if __name__ == "__main__":
    main()