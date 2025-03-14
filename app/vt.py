import os


from flask import send_from_directory

def get_uploaded_images():
    image_list = []
    rootdir = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) #move up one folder  
    print("Printing current directory:", rootdir)

    for subdir, dirs, files in os.walk(rootdir + '/uploads/'):  #walk through the directory 
        #print("subdir: ", subdir)
        #print("dirs: ", dirs)
        for file in files:
            if file.lower().endswith(('.jpg', '.png', '.jpeg', '.gif')):
                image_list.append(file)    # Print full file path
    print(image_list)



print(get_uploaded_images())

