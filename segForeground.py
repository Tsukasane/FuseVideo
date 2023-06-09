from segment_anything import SamPredictor, sam_model_registry
import numpy as np
import torch
import matplotlib.pyplot as plt
import cv2
import imageio
import skimage.io as io
import os
from PIL import Image


def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)
    
def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)   
    
def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))    

def SegForeground(base_path):
    #base_path = 'test/'
    images = os.listdir(base_path)
    sam_checkpoint = "checkpoint/sam_vit_h_4b8939.pth"
    model_type = "vit_h"

    print('Checkpoint loaded!')
    # the prompt input is a hyperparameter
    input_point = np.array([[230, 270]])
    input_label = np.array([1])


    # change cuda:<number> according to the number of GPU(s) you use
    device = torch.device('cuda:1') if torch.cuda.is_available() else torch.device('cpu')

    sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
    sam.to(device=device)

    predictor = SamPredictor(sam)

    print('Predictor ready!')

    for i_path in images:
        filename = base_path+i_path
        # print(type(filename))
        # break

        image = cv2.imread(filename)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        predictor.set_image(image)

        masks, scores, logits = predictor.predict(
            point_coords=input_point,
            point_labels=input_label,
            multimask_output=True,
        )

        mask = masks[-1]
        # for i, (mask, score) in enumerate(zip(masks, scores)):
        #     print(f"Mask {i+1}, Score: {score:.3f}")

        h, w = mask.shape[-2:]
        b_channel, g_channel, r_channel = cv2.split(image)
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255 #creating a dummy alpha channel image.
        img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
        mask_image = mask.reshape(h, w, 1) * img_BGRA

        #plt.gca().imshow(mask_image)

        plt.imsave(filename,mask_image)