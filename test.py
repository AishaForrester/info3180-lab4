import os

rootdir = os.getcwd()  #Get current working directory like: C:\Users\aisha\OneDrive\Desktop\info3180-lab4
print("Printing current directory:", rootdir)


for subdir, dirs, files in os.walk(rootdir + '/uploads/'):  #walk through the directory 
    #print("subdir: ", subdir)
    #print("dirs: ", dirs)
    for file in files:
        print(os.path.join(subdir, file))  # Print full file path