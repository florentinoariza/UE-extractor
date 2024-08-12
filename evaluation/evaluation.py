import pyntcloud
import numpy as np
import os
# import open3d as o3d

def read_dir(path):
    files= os.listdir(path)
    files_sorted = sorted(files)
    return files_sorted

root_path = "/home/florentino/saecce/evaluation/"
# algorithm_path
# patchworkpp
# algorithm_dir_path = root_path + "patchworkpp_downsampled/"
# optimised
algorithm_dir_path = root_path + "optimised_downsampled/"
algorithm_files = read_dir(algorithm_dir_path)

# algorithm_files = ['50.pcd', '100.pcd', '150.pcd', '200.pcd', '250.pcd']
# print(algorithm_files)

groundtruth_dir_path = root_path + "groundtruth/"
groundtruth_files = read_dir(groundtruth_dir_path)
print(groundtruth_files)
if len(groundtruth_files)!=len(algorithm_files):
    print("groundtruth file number not equals algorithm file number, please check it!")

algorithm_pointcloud_set = []
for file in algorithm_files:
    # print(algorithm_dir_path+file)
    pcd = pyntcloud.PyntCloud.from_file(algorithm_dir_path+file)
    pcd_array = np.asarray(pcd.points)
    print("len(pcd_array):",len(pcd_array))
    algorithm_pointcloud_set.append(pcd_array)

groundtruth_pointcloud_set = []
for file in groundtruth_files:
    f = open(groundtruth_dir_path+file)
    line = f.readline()
    data_list = []
    while line:
        num = list(map(float,line.split()))
        data_list.append(num)
        line = f.readline()
    f.close()
    data_array = np.array(data_list)
    print("len(data_array):",len(data_array))
    groundtruth_pointcloud_set.append(data_array)

TP_set = []
FP_set = []
FN_set = []
TN_set = []
precision_set = []
recall_set = []
f1_score_set = []
for i in range(len(algorithm_pointcloud_set)):
    algorithm_data = algorithm_pointcloud_set[i]
    groundtruth_data = groundtruth_pointcloud_set[i]
    TP = 0
    FP = 0
    FN = 0
    TN = 0

    for j in range(len(algorithm_data)):
        if algorithm_data[j][3]==10 and groundtruth_data[j][4]==0:
            TP += 1
        elif algorithm_data[j][3]==10 and groundtruth_data[j][4]==1:
            FP += 1
        elif algorithm_data[j][3]==20 and groundtruth_data[j][4]==0:
            FN += 1
        elif algorithm_data[j][3]==20 and groundtruth_data[j][4]==1:
            TN += 1
        else:
            print("invalid input!")
            print("algorithm_data[j][3]: ", algorithm_data[j][3])
            print("groundtruth_data[j][4]: ", groundtruth_data[j][4])
    
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1_score = 2*TP / (2*TP + FP + FN)
    
    # precision = 0
    # recall = 0
    # f1_score = 0

    precision_set.append(precision)
    recall_set.append(recall)
    f1_score_set.append(f1_score)
    TP_set.append(TP)
    FP_set.append(FP)
    FN_set.append(FN)
    TN_set.append(TN)

    # print("TP: ", TP)
    # print("FP: ", FP)
    # print("FN: ", FN)
    # print("TN: ", TN)
    # print("precision: ", precision)
    # print("recall: ", recall)
    # print("f1_score: ", f1_score)


n = len(TP_set)
print("frame number: ", n)
print("TP_set: ", TP_set)
print("FP_set: ", FP_set)
print("FN_set: ", FN_set)
print("TN_set: ", TN_set) 
print("precision_set: ", FP_set)
print("recall_set: ", recall_set)
print("f1_score_set: ", f1_score_set) 
average_precision = sum(precision_set)/n
average_recall = sum(recall_set)/n
average_f1_score = sum(f1_score_set)/n
print("average_precision: ", average_precision) 
print("average_recall: ", average_recall) 
print("average_f1_score: ", average_f1_score) 