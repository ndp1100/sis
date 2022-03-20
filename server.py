import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from flask import Flask, request, render_template
from pathlib import Path
from ProcessExcelFile import GetGiaBanFromMSP
import requests
import JsonNhanh.Json_ProductNhanh
import json
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

app = Flask(__name__)

fe = FeatureExtractor()

# new logic
datas = []


def load_all_data():
    for feature_path in Path("./static/feature").glob("*.npy"):
        maSanPham = feature_path.stem
        giaSanPham, danhMucSanPham = GetGiaBanFromMSP(maSanPham)

        dt_dict = {
            'feature': np.load(feature_path),
            'msp': feature_path.stem,
            'img_path': Path("./static/img") / (feature_path.stem + ".jpg"),
            'danhMucSP': danhMucSanPham,
            'giaSP': giaSanPham
        }
        datas.append(dt_dict)


load_all_data()
print('total data : ', len(datas))

tranh_phu_dieu = {'TRANH-PD-TT', 'TRANH-PD-HH', 'TRANH-PD-RE', 'TRANH-TH'}
tranh_dinh_da = {'TRANH-DD'}
dong_ho = {'DH-AM', 'DH-DG', 'DH-TB', 'DH-HZ', 'DH-HSG', 'DH-ZQ', 'DH-MV', 'DH-ME', 'DH-WE', 'DH-RE', 'DH-LI'}
trang_tri_de_ban = {'TTDEBAN'}
do_gia_dung = {'LYTT', 'XODA', 'HOPKHANGIAY', 'DERUOU', 'BATDIA', 'COCCHEN', 'ONGDUA', 'THAM', 'GATTAN', 'TAMLOTBANAN',
               'THUNGRAC', 'DUAMUONG', 'KHAYMUT', 'CHAILO', 'GIATREOLY', 'KHAYDIATRAICAY', 'SETPHONGTAM', 'BOGIAVI'}
tranh_sat = {'DCKIMLOAI', 'DCCOMPOSITE', 'DCGO'}
kham_trai = {'DGDKT', 'DHKT', 'KTDB', 'KTTT'}
binh_hoa = {'BINHTRANGTRI'}


def get_set_of_madanhmuc(filter: str):
    if filter == 'tranhphudieu':
        return tranh_phu_dieu
    elif filter == 'tranhdinhda':
        return tranh_dinh_da
    elif filter == 'dongho':
        return dong_ho
    elif filter == 'trangtrideban':
        return trang_tri_de_ban
    elif filter == 'dogiadung':
        return do_gia_dung
    elif filter == 'tranhsat':
        return tranh_sat
    elif filter == 'khamtrai':
        return kham_trai
    elif filter == 'binhhoa':
        return binh_hoa
    else:
        return None


def get_data_from_danhmucsp(danhmucsp: str, features: list, img_paths: list, MSP: list, giaSP: list):
    if danhmucsp is not None:
        for dt_dict in datas:
            if dt_dict['danhMucSP'] == danhmucsp:
                features.append(dt_dict['feature'])
                img_paths.append(dt_dict['img_path'])
                MSP.append(dt_dict['msp'])
                giaSP.append(dt_dict['giaSP'])
    else:  # get data in list danh muc san pham
        for dt_dict in datas: # get all data
            features.append(dt_dict['feature'])
            img_paths.append(dt_dict['img_path'])
            MSP.append(dt_dict['msp'])
            giaSP.append(dt_dict['giaSP'])


def get_list_feature_data_from_danh_muc_sp(filter_madanhmuc: str):
    features = []
    img_paths = []
    MSP = []
    giaSP = []

    if filter_madanhmuc is not None:
        set_of_madanhmuc = get_set_of_madanhmuc(filter_madanhmuc)
        for m in set_of_madanhmuc:
            get_data_from_danhmucsp(m, features, img_paths, MSP, giaSP)
    else:
        get_data_from_danhmucsp(None, features, img_paths, MSP, giaSP)
    return features, img_paths, MSP, giaSP


# get_list_feature_data_from_danh_muc_sp('TRANH-DD')
# print(MSP)


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

        # Save query image
        img = Image.open(file.stream)  # PIL image
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + file.filename

        # rotate img if necessary
        if auto_rotate:
            if request.form.get('checkbox') is None:
                img = img.rotate(-90)

        img.save(uploaded_img_path)

        # prepare data : feature, msp, img_path
        danhmucsanphamfilter = request.form.get('danhmucsanpham')
        features, img_paths, MSP, giaSP = get_list_feature_data_from_danh_muc_sp(danhmucsanphamfilter)

        # Run search
        query = fe.extract(img)
        dists = np.linalg.norm(features - query, axis=1)  # L2 distances to features
        ids = np.argsort(dists)[:24]  # Top 24 results
        scores = [(dists[id], img_paths[id], MSP[id], giaSP[id]) for id in ids]

        # refine data to easy show in html
        rangeLoop = int(len(scores) / 3)
        result = []
        i = 0
        x = 0
        while i < rangeLoop:
            s = [scores[x], scores[x + 1], scores[x + 2]]
            result.append(s)
            x = x + 3
            i = i + 1

        return render_template('index.html',
                               query_path=uploaded_img_path,
                               scores=result)
    else:
        return render_template('index.html')


accessCode = None
@app.route('/nhanhvn', methods=['GET', 'POST'])
def get_nhanh_accessCode():
    # res = requests.get('https://nhanh.vn/oauth?appId=72301&returnLink=http://103.153.74.38/nhanhvn')
    # f = open("accessCode_Nhanh.txt", "w")
    # f.write(res.text)
    # f.close()
    args = request.args
    accessCode = args.get('accessCode')
    if accessCode is not None:
        f = open("accessCode_Nhanh.txt", "w")
        f.write(accessCode)
        f.close()
        return accessCode
    else:
        return render_template('getaccesscode.html')

@app.route('/searchnhanh', methods=['GET', 'POST'])
def search_product_info_nhanh():
    url = 'https://open.nhanh.vn/api/product/search'
    myData = {
        'version' : 2.0,
        'appId' : 72301,
        'businessId': 82947,
        'accessToken': 'QX2tulbNG4b0mnpuaxWHSoCFf4Qu5SEzPYs9RSHz2j159XvaIo8BdAhxWYPR4ZlfUGmNr8ulXvA173b9owjmVc18o1qWqesHCpDqk93mKQOjIkmqga4EirF3gA7hFIi5',
        'data' : '{"page":1}'
    }
    x = requests.post(url, data=myData)
    # print(x.text)
    result = json.loads(x.text)
    print(result)
    # result = JsonNhanh.SearchProductRes.search_product_res_from_dict(x.text)
    # print(result.data.products.get('37320029'))
    return x.text

depotName_data = {
    '82210': 'khotong',
    '98135': 'binhthanh',
    '98136': 'namki',
    '99465': 'cantho',
    '99466': 'tranphu'
}


def get_name_depot(depotID: str):
    return depotName_data[depotID]


@app.route('/search')
def productinfor():
    args = request.args
    masanpham = args.get('msp')
    dataValue = '{\"name\":\"' + masanpham + '\"}'
    url = 'https://open.nhanh.vn/api/product/search'
    myData = {
        'version': 2.0,
        'appId': 72301,
        'businessId': 82947,
        'accessToken': 'QX2tulbNG4b0mnpuaxWHSoCFf4Qu5SEzPYs9RSHz2j159XvaIo8BdAhxWYPR4ZlfUGmNr8ulXvA173b9owjmVc18o1qWqesHCpDqk93mKQOjIkmqga4EirF3gA7hFIi5',
        'data': dataValue
    }
    x = requests.post(url, data=myData)

    result = JsonNhanh.Json_ProductNhanh.SearchProductResfromdict(json.loads(x.text))
    product = None
    for productID, value in result.data.products.items():
        product = value
        depots_data = product.inventory.depots
        depot = {}
        for x,y in depotName_data.items():
            depot.update({y:0})

        for deID, avai in depots_data.items():
            depot.update({get_name_depot(deID): avai.available})
            # if avai.available > 0:
            #     print('Kho ', get_name_depot(deID), ' Con co the ban :', avai.available)

    return render_template('productinfor.html',
                           masanpham=product.code,
                           giasanpham="{:,.0f} VND".format(product.price),
                           mieutasanpham=product.description,
                           depot=depot,
                           imgs=product.image)


sentry_sdk.init(
    dsn="https://972fab6ef46c4002908f7be605cafb6d@o1172500.ingest.sentry.io/6267466",
    integrations=[FlaskIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0
)

@app.route('/debug-sentry')
def trigger_error():
    division_by_zero = 1 / 0

if __name__ == "__main__":
    app.run("0.0.0.0")
