# WARNING !!! BEFORE RUNNING DELETE ALL COMMENTS
# -*- coding: utf-8 -*-
"""Object detection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jIjbyThGL-nu0F7jWMtrz5Bu5B9sfyK1
"""

# Commented out IPython magic to ensure Python compatibility.
!git clone https://github.com/oballinger/yolov5_RS 
# %cd yolov5_RS # placed the repository
# %pip install -qr requirements.txt
# %pip install -q roboflow # the package to load dataset from Roboflow

from roboflow import Roboflow #importing Roboflow package
rf = Roboflow(api_key="6bjY3TS4iBLl0LS6fL70") #identify personal Roboflow key to download dataset
project = rf.workspace('object-detection-sga8x').project("hard-hat-sample-fn9iq") # to address dataset information
dataset = project.version("1").download("yolov5") #downloading the dataset

!python train.py --data {dataset.location}/data.yaml --batch 32 --cache

from IPython.display import Image

# results.png file path then display results
results_path = "runs/train/exp/results.png"
display(Image(filename=results_path))

#Display F1-confidence curve
results_path = "runs/train/exp/F1_curve.png"
display(Image(filename=results_path))

#Display recall-confidence curve
results_path = "runs/train/exp/R_curve.png"
display(Image(filename=results_path))

# Display precision-recall curve
results_path = "runs/train/exp/PR_curve.png"
display(Image(filename=results_path))

from IPython.display import Image

# results.png dosyasının yolunu belirt
results_path = "runs/train/exp/labels.jpg"
display(Image(filename=results_path))

#Display confusion matrix
results_path = "runs/train/exp/confusion_matrix.png"
display(Image(filename=results_path))

from IPython.display import Image

# results.png dosyasının yolunu belirt
results_path = "runs/train/exp/labels_correlogram.jpg"
display(Image(filename=results_path))

import os
from IPython.display import Image, display

# Sonuçların kaydedildiği dizini tanımla
results_path = "runs/train/exp"

# Dizin içindeki tüm dosyaları listele ve sadece görüntü dosyalarını seç
result_images = [f for f in os.listdir(results_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Görselleri sırayla göster
for img_name in result_images:
    img_path = os.path.join(results_path, img_name)
    display(Image(filename=img_path))

import yaml


opt_path = "runs/train/exp/opt.yaml"  # opt.yaml file path

# reading opt.yaml file
with open(opt_path, 'r') as file:
    opt_data = yaml.safe_load(file)

# Display content of the file
print(yaml.dump(opt_data, sort_keys=False, indent=4))

