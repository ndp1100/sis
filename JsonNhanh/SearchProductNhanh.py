import requests
import json
import JsonNhanh.SearchProductRes

depot_data = {
    '82210' : 'Kho Tổng',
    '98135' : 'Bình Thạnh',
    '98136' : 'Nam Kì',
    '99465' : 'Cần Thơ',
    '99466' : 'Trần Phú'
}

def get_name_depot(depotID : str):
    return depot_data[depotID]

def search_product_info_nhanh():
    url = 'https://open.nhanh.vn/api/product/search'
    myData = {
        'version' : 2.0,
        'appId' : 72301,
        'businessId': 82947,
        'accessToken': 'QX2tulbNG4b0mnpuaxWHSoCFf4Qu5SEzPYs9RSHz2j159XvaIo8BdAhxWYPR4ZlfUGmNr8ulXvA173b9owjmVc18o1qWqesHCpDqk93mKQOjIkmqga4EirF3gA7hFIi5',
        'data' : {"name":"VASE-TP252"}
    }
    x = requests.post(url, data=myData)

    result = JsonNhanh.SearchProductRes.SearchProductResfromdict(json.loads(x.text))
    print(result.data.products.get('37320029').inventory.available)
    depots_data = result.data.products.get('37320029').inventory.depots
    for deID, avai in depots_data.items():
        if avai.available > 0:
            print('Kho ', get_name_depot(deID), ' Con co the ban :', avai.available)
    return x.text

search_product_info_nhanh()




