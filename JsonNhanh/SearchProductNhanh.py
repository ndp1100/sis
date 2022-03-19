import requests
import json
import JsonNhanh.Json_ProductNhanh
from flask import Flask, request, render_template
import server

# app = Flask(__name__)

depotName_data = {
    '82210': 'khotong',
    '98135': 'binhthanh',
    '98136': 'namki',
    '99465': 'cantho',
    '99466': 'tranphu'
}


def get_name_depot(depotID: str):
    return depotName_data[depotID]


@server.app.route('/search')
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


# search_product_info_nhanh()


# if __name__ == "__main__":
#     app.run("0.0.0.0")
