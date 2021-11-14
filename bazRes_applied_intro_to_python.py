import os
from PIL import Image

def find_files_in_a_folder_by_file_extension(my_folder, my_extension):
    """This function takes a folder, and checks that folder for any files with a file extension
    that matches the one supplied.

    This function is not recursive - it will not look in subfolders

    It returns a list of matching full file paths"""
    # this is an empty string. We will add any matching file paths to it later on
    matching_files = []

    # this command returns a list of all the things in a folder
    files_in_folder = os.listdir(my_folder)

    # File extensions can be lower or upper case so we need to make sure we're using case meaningfully. 
    #The uppercase string ".TXT" will not match with the lowercase ".txt"
    # In this case, we are going to lower case BOTH terms - the found extension, and the supplied
    my_extension = my_extension.lower()

    # we use a for loop to iterate over all the things in the list  
    for my_file in files_in_folder:
        # this command splits the filename from the file extension
        # we could do it manually by splitting the my_file string on the "."
        # e.g filename, ext = my_file.split(".") but this might cause 
        # problems when we encounter filenames with multiple "." characters, like "my_archive.warc.gz"  
        filename, ext = os.path.splitext(my_file)

        # Lowercaseing the extracted extension
        ext = ext.lower()
       

        # The "os.path.splitext" command includes the "." in the extension. We need to make sure we have a similar pattern 
        # with our supplied extension. We can use a logical test to check if the string starts with ".", and correct if needed
        if not my_extension.startswith("."):
            my_extension = "."+my_extension

        # we use a logic test, "if", to see if we have a match:
        if ext == my_extension:
            print (f"Extension Match: {my_file}") 
            # if we do find a match, we will add the full file path to the list of matching files.  
            # first we make the fill file path
            matching_file_path = os.path.join(my_folder, my_file)
            # then we add (append) to the matching files list
            matching_files.append(matching_file_path)

    # When we've checked all the files we return the list of matching files to the main flow
    return matching_files
 
def find_files_in_a_folder_by_list_of_file_extension(my_folder, my_extensions):
    """ this is the same basic process as find_files_in_a_folder_by_file_extension, except it takes a list of input extensions"""
    matching_files = []
    files_in_folder = os.listdir(my_folder)

    # Lowercasing the list of extensions. 
    # This is easily achieved using a powerful and useful technique called "list comprehension" 
    my_extensions = [x.lower() for x in my_extensions]

    # Adding the preceding "." to all items in the list of extensions:
    for i, my_extension in enumerate(my_extensions):
        if not my_extension.startswith("."):
            my_extension = "." + my_extension
            my_extensions[i] = my_extension

    # We can  make things tidier, and remove any duplicates using a set()
    my_extensions = set(my_extensions)

    for my_file in files_in_folder:
        filename, ext = os.path.splitext(my_file)
        ext = ext.lower()
        if ext in my_extensions:
            matching_file_path = os.path.join(my_folder, my_file)
            matching_files.append(matching_file_path)

    return matching_files

def recursively_find_files_in_a_folder_by_list_of_file_extensions(my_folder, my_extensions):
    """Based on the previous flat file version, takes a folder and a list on extensions,
    and returns all files with matching extension"""
    matching_files = []

    # Using the os.walk() function to explore and search subfolders
    files_in_folder = []
    for root, sub, files in os.walk(my_folder):
        for f in files:
            files_in_folder.append(os.path.join(root, f))

    my_extensions = [x.lower() for x in my_extensions]
    for i, my_extension in enumerate(my_extensions):
        if not my_extension.startswith("."):
            my_extension = "." + my_extension
            my_extensions[i] = my_extension

    for my_file in files_in_folder:
        filename, ext = os.path.splitext(my_file)
        ext = ext.lower()
        if ext in my_extensions:
            matching_file_path = os.path.join(my_folder, my_file)
            matching_files.append(matching_file_path)

    return matching_files

#####

def get_image_from_file(filepath):
    """takes a file path for an image, and returns the image as a PIL object"""
    return Image.open(filepath)

def save_image_to_file(my_image, my_filepath):
    """Takes a PIL image object and a filepath saves it"""
    if "rgb" not in my_image.info:
        my_path, my_ext = my_filepath.rsplit(".", 1)
        my_filepath = my_path + ".png"
    my_image.save(my_filepath)

def resize_image_by_percent(my_image, percent):
    width, height = my_image.size
    new_width = int((width / 100) * percent)   
    new_height = int((height / 100) * percent)   
    return my_image.resize((new_width, new_height), Image.ANTIALIAS)

def make_thumbnail(my_thumbnail_image, size):
    """This uses the inbuilt PIL thumbnail function. Its an "in place" function, 
    which means it the resize happens on the given image, not on a newly created image"""
    my_thumbnail_image.thumbnail([size, size], Image.ANTIALIAS)
    return my_thumbnail_image

def make_storage_loctation(root, project_name):
    """takes a root folder, and project name, and creates a new folder on the filestore. Returns the folder path"""
    new_folder = os.path.join(root, project_name)
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    return new_folder

def process_a_set_of_files():
    files_directory = {}
    for my_image_filepath in matching_files:
        ### using a Try/Except block to filter out files that aren't really image files as far as python can tell 
        try:
            my_image = get_image_from_file(my_image_filepath)
        except Exception as e:
            my_image = None
            if str(e).startswith("cannot identify image file"):
                print (f"Skipping - Probably not an image file - {my_image_filepath}")
            else:
                print ("Couldn't process file:", e)

        ### Logical test that only proceeds if we have a valid image, if not, it checks the next file.
        if my_image:

            ### resize image to n% of original dimensions. 
            percent = 75
            my_resized_image = resize_image_by_percent(my_image, percent)

            ### make thumnail of size n pixels on the largest edge
            size = 128
            my_thumbnail_image = make_thumbnail(my_image.copy(), size)


            #### save stuff
            filename, ext = os.path.basename(my_image_filepath).rsplit(".", 1)

            ### deals with resized images
            resized_filename = filename+"_resized."+ext
            resized_filepath = os.path.join(destination, resized_filename) 
            if not os.path.exists(resized_filepath):
                save_image_to_file(my_resized_image, resized_filepath)
            else:
                print (f"File already exists - {resized_filepath}")
                ### uncomment the below line if you want to enable overwrite
                #  save_image_to_file(my_resized_image, resized_filepath)
            if "resized" not in files_directory: 
                files_directory["resized"] = []
            files_directory["resized"].append(resized_filepath)


            ### deals with thumbnails
            thumbnail_filename = filename+"_thumbnail."+ext
            thumbnail_filepath = os.path.join(destination, thumbnail_filename)
            if not os.path.exists(thumbnail_filepath):
                save_image_to_file(my_thumbnail_image, thumbnail_filepath)
            else:
                print (f"File already exists - {thumbnail_filepath}")
                ### uncomment the below line if you want to enable overwrite
                # save_image_to_file(my_thumbnail_image, thumbnail_filepath)
            if "thumbnail" not in files_directory: 
                files_directory["thumbnail"] = []
            files_directory["thumbnail"].append(thumbnail_filepath)

    return files_directory

#####

def make_html(files_directory, html_destination, html_filename, project_name):
    html = """<!DOCTYPE html>
    <html lang="en"
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>##### Gallery</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <style>
    img {
      border: 1px solid #ddd;
      border-radius: 4px;
      padding: 5px;
      width: 150px;
    }

    img:hover {
      box-shadow: 0 0 2px 1px rgba(0, 140, 186, 0.5);
    }
    </style>
    <body>
        
        <h2>Thumbnail Image</h2>
        <p>Click on the image to enlarge it.</p>"""

    footer = """</body>
    </html>"""
    html = html.replace("#####", project_name)
    for i, item in enumerate (files_directory['resized']):
        html += f"""<a target="_blank" href="{item}">
          <img src="{files_directory['thumbnail'][i]}" alt="Forest">
        </a>"""

    html += footer

    try:
        from bs4 import BeautifulSoup
        html = BeautifulSoup(html, 'html.parser').prettify()
    except:
        print ("BeautifulSoup not installed. resulting HTML might be a little rough...")
        

    with open(os.path.join(html_destination, html_filename), "w") as outfile:
        outfile.write(html) 

#### 


### Step one - generate a list of files found in a folder based on a fixed criteria 

my_source_folder = r"\\wlgprdfile12\home$\Wellington\GattusoJ\HomeData\Desktop\baz_rez_test_folder"
my_extensions = ["jpg", ".JPG", ".tiff", ".TIF", "png"]
# my_extension = "jpg"

# matching_files = find_files_in_a_folder_by_file_extension(my_folder, my_extension)
# matching_files = find_files_in_a_folder_by_list_of_file_extension(my_source_folder, my_extensions)
matching_files = recursively_find_files_in_a_folder_by_list_of_file_extensions(my_source_folder, my_extensions)

### Step two
my_destination_folder = r"\\wlgprdfile12\home$\Wellington\GattusoJ\HomeData\Desktop\baz_res_products"
my_project_label = "testing"
destination  = make_storage_loctation(my_destination_folder, my_project_label)

files_directory = process_a_set_of_files()

make_html(files_directory, destination, "index.html", my_project_label )
