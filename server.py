import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from flask import Flask, request, render_template
from pathlib import Path
from ProcessExcelFile import GetGiaBanFromMSP
import requests

app = Flask(__name__)

# Read image features
fe = FeatureExtractor()
features = []
img_paths = []
MSP = []
for feature_path in Path("./static/feature").glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path("./static/img") / (feature_path.stem + ".jpg"))
    MSP.append(feature_path.stem)
features = np.array(features)

# # new logic
# datas = []
# def load_all_data():
#     for feature_path in Path("./static/feature").glob("*.npy"):
#         dt_dict = {
#             'feature' : np.load(feature_path),
#             'msp' : feature_path.stem,
#             'img_path' : Path("./static/img") / (feature_path.stem + ".jpg")
#         }
#         datas.append(dt_dict)
#
# load_all_data()
# print('total data : ', len(datas))

# def get_list_feature_data_from_danh_muc_sp(danhmucsp):
#     features = []
#     img_paths = []
#     MSP = []
#     for dt_dict in datas:
#         if dt_dict['msp'] == danhmucsp:
#             features.append(dt_dict['feature'])
#             img_paths.append(dt_dict['img_path'])
#             MSP.append(dt_dict['msp']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['query_img_album']
        auto_rotate = False

        if str.isspace(file.filename) or len(file.filename) <= 0:
            file = request.files['query_img_camera']
            auto_rotate = True

        if file is None:
            return render_template('index.html')

        print("Checkbox", request.form.get('checkbox'))

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename

        print('before : img width', img.width, 'img height', img.height)

        # rotate img if necessary
        if auto_rotate:
            if request.form.get('checkbox') is None:
                img = img.rotate(-90)

        print('after : img width', img.width, 'img height', img.height)

        img.save(uploaded_img_path)

        # Run search
        query = fe.extract(img)
        dists = np.linalg.norm(features - query, axis=1)  # L2 distances to features
        ids = np.argsort(dists)[:30]  # Top 30 results        
        scores = [(dists[id], img_paths[id], MSP[id], GetGiaBanFromMSP(MSP[id])) for id in ids]

        # print(scores[1])

        return render_template('index.html',
                               query_path=uploaded_img_path,
                               scores=scores)
    else:
        return render_template('index.html')

# accessCode = None
@app.route('/nhanhvn')
def get_nhanh_accessCode():
    res = requests.get('https://nhanh.vn/oauth?appId=72301&returnLink=http://103.153.74.38/nhanhvn')
    f = open("accessCode_Nhanh.txt", "w")
    f.write(res.text)
    f.close()
    # args = request.args
    # accessCode = args.get('accessCode')
    # if accessCode is not None:
    #     f = open("accessCode_Nhanh.txt", "w")
    #     f.write(accessCode)
    #     f.close()
    #     return accessCode
    # else:
        return render_template('getaccesscode.html')

if __name__ == "__main__":
    app.run("0.0.0.0")
