import os
import argparse
import cv2
import subprocess
from segForeground import SegForeground
from transform import Transform
from poisson import PoissonOut

"""
python demo.py --backgroundVideo backgroundV.mp4 --outPath ./<YourOutPath>
"""

os.chdir(r'/home/zhaoyiwen/SegVideo')


def video2img(v_path,image_save):
    cap=cv2.VideoCapture(v_path)
    frame_count=cap.get(cv2.CAP_PROP_FRAME_COUNT)
    
    for i in range(int(frame_count)-15): #
        _,img=cap.read()
        cv2.imwrite('{}/image{}.jpg'.format(image_save,i),img)


def get_args_parser():
    parser = argparse.ArgumentParser('settings', add_help=False)
    parser.add_argument('--backgroundVideo', default='./images&videos/backgroundV.mp4', type=str,
                        help='path to your source video')
    parser.add_argument('--foregroundVideo', default='./images&videos/thingV.mp4', type=str,
                        help='path to your source video')
    parser.add_argument('--bgPath', default='./testT', type=str,
                        help='output frame dir for bgVideo')
    parser.add_argument('--fgPath', default='./test', type=str,
                        help='output frame dir for fgVideo')
    parser.add_argument('--outPath', default='./outF', type=str,
                        help='output dir for images after poisson confusion')                    

    return parser.parse_args()


if __name__=='__main__':
    args = get_args_parser()

    fgv_path = args.foregroundVideo #source path
    bgv_path = args.backgroundVideo

    fgFramePath = args.fgPath 
    bgFramePath = args.bgPath

    outPath = args.outPath

    fgDir = args.fgPath[2:]+'/'
    bgDir = args.bgPath[2:]+'/'
    outDir = args.outPath[2:]+'/'

    if not os.path.exists(fgFramePath):
        os.makedirs(fgFramePath)
        video2img(fgv_path,fgFramePath)
        print('Foreground frames split!')

    if not os.path.exists(bgFramePath):
        os.makedirs(bgFramePath)
        video2img(bgv_path,bgFramePath)
        print('Background frames split!')

    if not os.path.exists(outPath):
        os.makedirs(outPath)


    SegForeground(fgDir)
    print('Foreground segmented!')

    Transform(fgDir)
    print('Foreground transformed!')

    PoissonOut(bgDir, fgDir, outDir)
    print('Poisson confusion done!')

    


    
    
 
 