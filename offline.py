from PIL import Image
from feature_extractor import FeatureExtractor
from pathlib import Path
import numpy as np
from ProcessExcelFile import DownloadImgFromExcelFile

from glob import glob
import csv
import urllib
import os
import pathlib
path = pathlib.Path().absolute()
print(path)

def CreateFeatureExtractor(fe, ImgpathFolder, featurePathFolder):
    for img_path in sorted(Path("./static/",ImgpathFolder).glob("*.jpg")):
        print(img_path)  # e.g., ./static/img/xxx.jpg
        try:
            feature = fe.extract(img=Image.open(img_path))
            feature_path = Path("./static/", featurePathFolder) / (img_path.stem + ".npy")  # e.g., ./static/feature/xxx.npy
            np.save(feature_path, feature)
        except Exception:
            pass

if __name__ == '__main__':
    fe = FeatureExtractor()

    CreateFeatureExtractor(fe, 'img', 'feature')

    # for img_path in sorted(Path("./static/img").glob("*.jpg")):
    #     print(img_path)  # e.g., ./static/img/xxx.jpg
    #     try:
    #         feature = fe.extract(img=Image.open(img_path))
    #         feature_path = Path("./static/feature") / (img_path.stem + ".npy")  # e.g., ./static/feature/xxx.npy
    #         np.save(feature_path, feature)
    #     except Exception:
    #         pass


