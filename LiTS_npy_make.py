import numpy as np
from multiprocessing import Pool
import SimpleITK as sitk
from batchgenerators.utilities.file_and_folder_operations import *
import torchio as tio
import torch


def unpack_dataset(folder, extension, threads=8, key="data"):
    """
    unpacks all npz files in a folder to npy (whatever you want to have unpacked must be saved unter key)
    :param folder:
    :param threads:
    :param key:
    :return:
    """

    p = Pool(threads)
    nii_files = subfiles(folder, True, None, extension, True) # npz->mha
    print(len(nii_files)) # 5
    p.map(convert_to_npy, zip(nii_files, [key] * len(nii_files)))
    p.close()
    p.join()

def convert_to_npy(args):
    # LiTS dataset rotation
    tmp_lst=['volume-15.nii', 'volume-18.nii', 'volume-28.nii', 'volume-3.nii', 'volume-33.nii', 'volume-37.nii', 'volume-42.nii', 'volume-47.nii', 'volume-5.nii', 'volume-54.nii', 'volume-70.nii', 'volume-73.nii', 'volume-80.nii']
    
    if not isinstance(args, tuple):
        key = "data"
        nii_files = args
    else:
        nii_files, key = args
        
    if (nii_files[-3:] == 'nii'):
        num = 3
        extension = 'nii'
    elif (nii_files[-3:] == 'mhd'):
        num = 3
        extension = 'mhd'
    elif nii_files[-6:] == 'nii.gz':
        num = 3
        extension = 'nii.gz'

    if not isfile(nii_files[:-num] + "npy"):
        
        # resize
        resize = tio.Resize((256,256,-1))
        try:
            #print(nii_files)
            gt_path = nii_files.replace('unetr_pp_Data_plans_v2.1_stage1', 'seg_gt')
            name_OR = gt_path.split('/')[-1]
            #print(name_OR)
            gt_path = gt_path[:-len(name_OR)]
            
            if extension in ['nii', 'nii.gz']:
                name = name_OR.replace('volume', 'segmentation')
            else: # .mhd
                name = name_OR
            
            gt_path = gt_path + name
            #print("gt:", gt_path)

            ####################################
            a = tio.ScalarImage(nii_files)
            #resample = tio.Resample()  # default is 1 mm isotropic
            #resampled = resample(a)

            a = np.array(a)
            a = resize(a) # input: 4D
            a = np.clip(a, -250, 250) # Zhu et al. paper (2024) // HU values / -250, 250
            
            a = (a - np.min(a)) / (np.max(a) - np.min(a)) # normalize - preprocessing
            a = np.transpose(a[0], (2,1,0)) # TODO: 9/24 axial
            #####################################

            #####################################
            gt = tio.ScalarImage(gt_path)
            gt.data = np.where(gt.data >= 1, 1, 0) # Not LiTS, it remove (tumor containing)
            #resample = tio.Resample()  # default is 1 mm isotropic
            #resampled = resample(gt)

            gt = np.array(gt)
            gt = resize(gt) # input: 4D
            if len(np.unique(gt)) != 2: # error check
                print(name_OR)
                raise Exception("No label")
            
            gt = np.transpose(gt[0], (2,1,0)) # TODO: 9/24 axial
            #####################################
            
        except Exception as e:
            print("error file:",name)
            print(e)    

        if name_OR in tmp_lst:
            a = torch.flip(torch.Tensor(a),(2,))
            gt = torch.flip(torch.Tensor(gt),(2,))
            
            a = np.array(a)
            gt = np.array(gt)

        elif num==6: # 3Dircard cases
            a = torch.flip(torch.Tensor(a),(2,))
            gt = torch.flip(torch.Tensor(gt),(2,))
            
            a = np.array(a)
            gt = np.array(gt)
        
        # npy format 생성
        a = a[np.newaxis, ...]
        gt = gt[np.newaxis, ...]
        print(a.shape)
        print(gt.shape)
        if a.shape != gt.shape:
            print(name)
            
        print("saving...")
        final = np.concatenate([a, gt], axis=0) # (2, x, y, x)
        np.save(nii_files[:-num] + "npy", final)


if __name__ == '__main__':

    while True:
        data = input("Dataset names(3Dircadb, LiTS, Sliver):")

        if data in ['3Dircadb', 'LiTS', 'Sliver']:
            if data == 'LiTS':
                extension = '.nii'
            elif data == '3Dircadb':
                extension = '.nii.gz'
            else:
                extension = '.mhd'
            print("Extension:", extension)
            
            folder = './DATASET_Synapse/unetr_pp_raw/unetr_pp_raw_data/Task02_Synapse/Task002_Synapse/unetr_pp_Data_plans_v2.1_stage1/' + data + '/'
            unpack_dataset(folder, extension)
            break

        else:
            print("No dataset")