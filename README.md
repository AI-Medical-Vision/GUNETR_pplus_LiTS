# G-UNETR++: Whole liver segmentation
---
![model](./images/model.png)  
  
**🔥G-UNETR++: A gradient-enhanced network for accurate and robust liver segmentation from CT images**   
Paper: [G-UNETR++](#)
  
---
# Requirements
Our code is based on [UNETR++](https://github.com/Amshaker/unetr_plus_plus) code.  
But, we modified the code for easy implementation.
Our GPU is `RTX 3090 GPU`.  
  
## Environment
1. Create and activate conda environment  
```bash
conda create --name gunetr_pp python=3.9
conda activate gunetr_pp
```
  
2. Install pytorch
```bash
# cuda 11.3
conda install pytorch==1.12.0 torchvision==0.13.0 torchaudio==0.12.0 cudatoolkit=11.3 -c pytorch
```
It is important that check your `cuda version`.  
Please, see the [pytorch document](https://pytorch.org/get-started/previous-versions/#v1120).  
  
3. Install other dependencies
```
pip install -r requirements.txt
```
  
---
# Dataset
In paper, we teseted `LiTS`, `3Dircadb`, and `Sliver07`.  
  
## Dataset format
```
GUNETR_pplus_LiTS
├── DATASET_Synapse                  
│   ├── unetr_pp_raw
│       ├── unetr_pp_raw_data           
│           ├── Task02_Synapse           
│               ├── Task002_Synapse         
│                   ├── seg_gt
│                       ├── 3Dircadb
│                       ├── LiTS
│                           ├── segmentation-3.nii
│                           ├── segmentation-5.nii
│                           ├── ...
│                           └── segmentation-127.nii
│                       ├── Sliver07
│                   ├── unetr_pp_Data_plans_v2.1_stage1
│                       ├── 3Dircadb
│                       ├── LiTS
│                           ├── volume-3.nii
│                           ├── volume-5.nii
│                           ├── ...
│                           └── volume-127.nii
│                       ├── Sliver07
│                   └── unetr_pp_Plansv2.1_plans_3D.pkl
```
LiTS dataset: [131 cases](https://github.com/Auggen21/LITS-Challenge?tab=readme-ov-file).  
3Dircadb link: [20 cases](https://www.ircad.fr/research/data-sets/liver-segmentation-3d-ircadb-01/).  
Sliver07 link: [20 cases](https://sliver07.grand-challenge.org/).
> Our LiTS-testset number is `3, 5, 15, 18, 28, 33, 37, 42, 47, 54, 62, 70, 73, 80, 90, 100, 105, 110, 121, and 127`.  
  
## Model Checkpoint
```
GUNETR_pplus_LiTS
├── output_synapse                 
│   ├── 3d_fullres
│       ├── Task002_Synapse                   
│           ├── unetr_pp_trainer_synapse__unetr_pp_Plansv2.1        
│               ├── fold_4
│                   ├── validation_raw
│                   ├── model_best.model
│                   └── model_best.model.pkl
```
Best-model-chekcpoint: [link](https://drive.google.com/drive/folders/11H3IcizvI180RIrgDSNW7VlFGXL39H7k?usp=drive_link).  
  
---
# Implementation
1. Make npy files
```bash
$> python LiTS_npy_make.py
```
You select the options, `LiTS`, `3Dircadb`, and `Sliver`.  
  
2. Evaluation script
```bash
$> cd ./evaluation_scripts
$> sh run_evaluation_synapse.sh
```
You select the options, `LiTS`, `3Dircadb`, and `Sliver`.  
  
3. Calculation metrics
Please see our [jupyter notebook](https://github.com/AI-Medical-Vision/GUNETR_pplus_LiTS/blob/main/LiTS_metric.ipynb).  
We implemented all of metric classes.  
> You can control post-processing option through `flag_post = True`.
  
---
# Result
## LiTS
| Model | DSC | Jaccard | VOE | RAVD | ASSD | RMSD | MSSD |  
| --- | --- | --- | --- | --- | --- | --- | --- |  
| Guo et al. | 0.9430 | --- | --- | --- | 2.30 | 4.70 | 34.70 | 
| Song et al. | 0.9680 | --- | 0.0700 | 0.0150 | --- | --- | --- | 
| Lei et al.  | 0.9630 | --- | 0.0688 | 0.0146 | 1.37 | 77.60 | --- | 
| Chen et al. | 0.9650 | --- | 0.0670 | 0.0090 | 1.22 | 28.09 | --- | 
| Zhu et al. | 0.9688 | 0.9422 | 0.0578 | **0.0039** | 1.09 | --- | 16.08 | 
| Chen et al. | 0.9727 | --- | 0.0531 | 1.0800 | 1.31 | 3.05 | --- | 
| **Ours (G-UNTER++)** | **0.9737** | **0.9490** | **0.0511** | 0.0201 | **0.64** | **1.17** | **12.75** | 
  
---
# References
[UNETR++](https://arxiv.org/abs/2212.04497)  
  
---
# Citation
```bibtex
@ARTICLE{
  title={G-UNETR++: A gradient-enhanced network for accurate and robust liver segmentation from CT images}, 
  author={Seungyoo Lee, Kyujin Han, Hangyeul Shin, Harin Park, Xiaopeng Yang, Jae Do Yang, Hee Chul Yu, Heecheon You},
  journal={}, 
  year={2024},
  doi={}}
```
