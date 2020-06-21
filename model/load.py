import os,os.path
import git
import pandas as pd
from shutil import copy
import random

# TODO: Add normal X-Ray Images

#Displays git command progress
class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print('update(%s, %s, %s, %s)'%(op_code, cur_count, max_count, message))

# Add Images to exclude here
exclude_images = [

]

#Directories
git_url = "https://github.com/ieee8023/covid-chestxray-dataset.git"
source_dataset_dir = "covid-chestxray-dataset"
source_dataset_dir2 = "Coronahack-Chest-XRay-Dataset"
sorted_dataset_dir = "master-dataset"
working_dir = "../dataset/"
# 
conditions = ["COVID-19", "SARS", "MERS"]

#Creates Dataset parent folder
if not os.path.exists(working_dir+sorted_dataset_dir):
    os.mkdir(working_dir+sorted_dataset_dir)

#Creates folders for conditions
if not os.path.exists(working_dir+sorted_dataset_dir + "/Normal"):
    os.makedirs(working_dir+sorted_dataset_dir + "/Normal")
if not os.path.exists(working_dir+sorted_dataset_dir + "/COVID-19"):
    os.makedirs(working_dir+sorted_dataset_dir + "/COVID-19")
if not os.path.exists(working_dir+sorted_dataset_dir + "/Pneumonia"):
    os.makedirs(working_dir+sorted_dataset_dir + "/Pneumonia")

#Fetch the dataset
if not os.path.exists(working_dir + source_dataset_dir):
    print("\nCloning Dataset from " + git_url)
    # To View Git Clone Pogress
    # git.Repo.clone_from(git_url, working_dir + "\\" + source_dataset_dir, progress=Progress())
    git.Repo.clone_from(git_url, working_dir + "/" + source_dataset_dir)
    print("Finished Cloning")
else:
    print("\nUpdating Dataset from " + git_url)
    git.cmd.Git(working_dir + source_dataset_dir)
    print("Dataset Updated")




print("\nSorting Dataset...")
print("Sorting Dataset 1...")
#Read in data
imgpath = os.path.join(working_dir, source_dataset_dir, "images")
csvpath = os.path.join(working_dir, source_dataset_dir, "metadata.csv")

#Read CSV
csv = pd.read_csv(csvpath)
#Read only PA, AP, and AP Supine Views
csv = csv[csv["view"].isin(["PA", "AP", "AP Supine"])]

#Loads images into dataset folder
for condition in conditions: 
    condition_df = csv[(csv["finding"].str.contains(condition))]
    for img in condition_df["filename"]:
        if not img in exclude_images:
            if condition == 'COVID-19':
                copy(imgpath + "/" + img, working_dir+sorted_dataset_dir + "/" + condition)
            else:
                copy(imgpath + "/" + img, working_dir+sorted_dataset_dir + "/Pneumonia")


                
if os.path.exists(working_dir+ source_dataset_dir2):

    print("Sorting Dataset 2...")
    imgpath = os.path.join(working_dir, source_dataset_dir2, source_dataset_dir2, "train")
    csvpath = os.path.join(working_dir, "Chest_xray_Corona_Metadata.csv")


    csv = pd.read_csv(csvpath)
    csv_train = csv[csv["Dataset_type"].str.contains("TRAIN")]
    csv_train_normal = csv_train[csv_train["Label"].str.contains("Normal")]

    #Normal Images
    for img in csv_train_normal["X_ray_image_name"]:
        copy(imgpath + "/" + img, working_dir+sorted_dataset_dir + "/Normal")

    csv_covid = csv[csv["Label_2_Virus_category"].eq("COVID-19")]

    # COVID-19 Images
    for img in csv_covid["X_ray_image_name"]:
        copy(imgpath + "/" + img, working_dir+sorted_dataset_dir + "/COVID-19")

    csv_viral = csv_train[csv_train["Label_1_Virus_category"].eq("Virus")]
    csv_viral = csv_viral[csv_viral["Label_2_Virus_category"].ne("COVID-19")]

    # Other Viral Pnuemonia Images
    for img in csv_viral["X_ray_image_name"]:
        copy(imgpath + "/" + img, working_dir+sorted_dataset_dir + "/Pneumonia")


    #Randomly Select 200 Images to keep
    dir_to_reduce = ["/Normal/", "/Pneumonia/"]
    num_images = 200
    for folder in range(0, len(dir_to_reduce)):
        allimages = os.listdir(working_dir+sorted_dataset_dir + dir_to_reduce[folder])
        delete_items = random.sample(range(0,len(allimages)), len(allimages)-num_images)
        for img in delete_items:
            os.remove(working_dir+sorted_dataset_dir + dir_to_reduce[folder] +allimages[img])

print("Dataset sorted into ./" + working_dir+sorted_dataset_dir)