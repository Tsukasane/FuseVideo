# FuseVideo
fuse videos in a natural way using image segmentation and Poisson confusion

<div align="center">

<h2>Fused Opening → "Thing on Ice" </h2>

[Video Demo](https://www.bilibili.com/video/BV1wh4y1J7z5/?share_source=copy_web&vd_source=7839947b95a2165c825a92ecb6bdc544)

<image src="images&videos/opening.png" width="720px" />

</div>

---


## Introduction

Hi there! This is the code base of my final project for the Image-Processing Class. I use image segmentation and Poisson confusion to mix two videos, making the synthesized video looks as natural as possible. Videos can be seen as integrations of frames, so I performed the transform based on images.

Hopefully, this README file can serve as the hand-in report for the class, since I really don't want to write another one with the same meaning.

This idea comes from a practical need. I want to make an opening for my skating video, where two performers cosplay Wednesday and Enid, two characters of the Netflix series *Wednesday*. Fans of this series know that Wednesday has a faithful servant, the Thing, a human hand-like creature that can think independently. I want to bring Thing to the opening of my video.

In the beginning, I naively believed that only using Poisson confusion would be fine, as the demo in the [original paper](https://www.cs.jhu.edu/~misha/Fall07/Papers/Perez03.pdf) shows even though the backgrounds of the two images are slightly different, this method can still generate natural results. However, the source video for Thing is very noisy with a messy background. If I brutally Poisson confuse them, the brightness and balance of the output image will become wired. That's the time when image segmentation comes to my mind. Empowered by the recently released large model, SAM, Thing can be separated from the original frame in a scraped quality since the model cannot handle low resolution and blur that well.

In addition, the performance of using Poisson confusion plus image segmentation is also better than barely using segmentation. Because Poisson confusion calculates the gradient of images, it fuses the two inputs more naturally, making the output less like a sticker on the background.

## Installation

This is a simple tutorial for using the code.

Create a virtual environment using conda
```
conda create -n fusevideo python=3.8
```

Notice that Python version should be >=3.8

cd into the root directory of this project
```
pip install -r requirements.txt
```
Then download the checkpoint file for the SAM following [this tutorial](https://github.com/facebookresearch/segment-anything#getting-started).

Change the os directory in ``demo.py`` line 13 according to your own setting.

Run the code by using the following command in terminal
```
python demo.py --backgroundVideo backgroundV.mp4 \ 
--foregroundVideo thingV.mp4 \ 
--bgPath  ./<Your/Path> \
--fgPath  ./<Your/Path> \
--outPath ./<Your/Path>
```

This will generate valid output frames in one folder. Then use ``img2video.py`` to integrate the frames into a video. Change the file path in line 4 to the same as you set in --outPath ./<Your/Path> in ``demo.py``
```
python img2video.py
```
This will output a video with default name outV.mp4

## References
Part of the codes are borrowed from the following sources

[Scaling the image and filling the blank with white](https://blog.csdn.net/qq_52787609/article/details/125517221?spm=1001.2014.3001.5501)

[Segment anything -- GitHub repo & Colab notebook](https://github.com/facebookresearch/segment-anything)

[RGB --> RGBA](https://blog.csdn.net/qq_36321330/article/details/116808301)


Other references

[Export environment settings](https://blog.csdn.net/qq_41667743/article/details/128273061)


Thanks for their great work and kindness!
