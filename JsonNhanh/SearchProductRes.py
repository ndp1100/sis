# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = SearchProductResfromdict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any, List, TypeVar, Callable, Type, cast
from datetime import datetime
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_dict(f: Callable[[Any], T], x: Any) -> Dict[str, T]:
    assert isinstance(x, dict)
    return { k: f(v) for (k, v) in x.items() }


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_str(x: Any) -> str:
    # assert isinstance(x, str)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


class ImportTypeLabel(Enum):
    Kýgửi = "Ký gửi"


@dataclass
class Inventory:
    remain: int
    shipping: int
    damaged: int
    holding: int
    warranty: int
    warrantyHolding: int
    available: int
    depots: Dict[str, 'Inventory']

    @staticmethod
    def from_dict(obj: Any) -> 'Inventory':
        assert isinstance(obj, dict)
        remain = from_int(obj.get("remain"))
        shipping = from_int(obj.get("shipping"))
        damaged = from_int(obj.get("damaged"))
        holding = from_int(obj.get("holding"))
        warranty = from_int(obj.get("warranty"))
        warrantyHolding = from_int(obj.get("warrantyHolding"))
        available = from_int(obj.get("available"))
        depots = from_union([lambda x: from_dict(Inventory.from_dict, x), from_none], obj.get("depots"))
        return Inventory(remain, shipping, damaged, holding, warranty, warrantyHolding, available, depots)

    def to_dict(self) -> dict:
        result: dict = {}
        result["remain"] = from_int(self.remain)
        result["shipping"] = from_int(self.shipping)
        result["damaged"] = from_int(self.damaged)
        result["holding"] = from_int(self.holding)
        result["warranty"] = from_int(self.warranty)
        result["warrantyHolding"] = from_int(self.warrantyHolding)
        result["available"] = from_int(self.available)
        result["depots"] = from_union([lambda x: from_dict(lambda x: to_class(Inventory, x), x), from_none], self.depots)
        return result


class Status(Enum):
    New = "New"


class TypeName(Enum):
    Sảnphẩm = "Sản phẩm"


class Unit(Enum):
    BỘ = "BỘ"
    CÁI = "CÁI"
    SET = "SET"


@dataclass
class Product:
    idNhanh: int
    privateId: None
    parentId: int
    brandId: None
    brandName: str
    typeId: int
    typeName: TypeName
    avgCost: int
    importType: int
    importTypeLabel: ImportTypeLabel
    merchantCategoryId: None
    merchantProductId: None
    categoryId: int
    code: str
    barcode: str
    name: str
    otherName: None
    importPrice: int
    oldPrice: None
    price: int
    wholesalePrice: int
    thumbnail: str
    image: str
    status: Status
    showHot: int
    showNew: int
    showHome: int
    order: str
    previewLink: str
    shippingWeight: int
    width: None
    length: None
    height: None
    vat: None
    createdDateTime: datetime
    inventory: Inventory
    warrantyAddress: None
    warrantyPhone: None
    warranty: None
    countryName: str
    unit: Unit
    advantages: None
    description: str
    content: None
    highlights: Optional[List[Any]] = None
    images: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Product':
        assert isinstance(obj, dict)
        idNhanh = int(from_str(obj.get("idNhanh")))
        privateId = from_none(obj.get("privateId"))
        parentId = int(from_str(obj.get("parentId")))
        brandId = from_none(obj.get("brandId"))
        brandName = from_str(obj.get("brandName"))
        typeId = int(from_str(obj.get("typeId")))
        typeName = TypeName(obj.get("typeName"))
        avgCost = from_union([from_none, lambda x: int(from_str(x))], obj.get("avgCost"))
        importType = int(from_str(obj.get("importType")))
        importTypeLabel = ImportTypeLabel(obj.get("importTypeLabel"))
        merchantCategoryId = from_none(obj.get("merchantCategoryId"))
        merchantProductId = from_none(obj.get("merchantProductId"))
        categoryId = int(from_str(obj.get("categoryId")))
        code = from_str(obj.get("code"))
        barcode = from_str(obj.get("barcode"))
        name = from_str(obj.get("name"))
        otherName = from_none(obj.get("otherName"))
        importPrice = from_union([from_none, lambda x: int(from_str(x))], obj.get("importPrice"))
        oldPrice = from_none(obj.get("oldPrice"))
        price = int(from_str(obj.get("price")))
        wholesalePrice = int(from_str(obj.get("wholesalePrice")))
        thumbnail = from_str(obj.get("thumbnail"))
        image = from_str(obj.get("image"))
        status = Status(obj.get("status"))
        showHot = from_int(obj.get("showHot"))
        showNew = from_int(obj.get("showNew"))
        showHome = from_int(obj.get("showHome"))
        order = from_str(obj.get("order"))
        previewLink = from_str(obj.get("previewLink"))
        shippingWeight = from_union([from_none, lambda x: int(from_str(x))], obj.get("shippingWeight"))
        width = from_none(obj.get("width"))
        length = from_none(obj.get("length"))
        height = from_none(obj.get("height"))
        vat = from_none(obj.get("vat"))
        createdDateTime = from_datetime(obj.get("createdDateTime"))
        inventory = Inventory.from_dict(obj.get("inventory"))
        warrantyAddress = from_none(obj.get("warrantyAddress"))
        warrantyPhone = from_none(obj.get("warrantyPhone"))
        warranty = from_none(obj.get("warranty"))
        countryName = from_str(obj.get("countryName"))
        unit = Unit(obj.get("unit"))
        advantages = from_none(obj.get("advantages"))
        description = from_str(obj.get("description"))
        content = from_none(obj.get("content"))
        highlights = from_union([lambda x: from_list(lambda x: x, x), from_none], obj.get("highlights"))
        images = from_union([lambda x: from_list(from_str, x), from_none], obj.get("images"))
        return Product(idNhanh, privateId, parentId, brandId, brandName, typeId, typeName, avgCost, importType, importTypeLabel, merchantCategoryId, merchantProductId, categoryId, code, barcode, name, otherName, importPrice, oldPrice, price, wholesalePrice, thumbnail, image, status, showHot, showNew, showHome, order, previewLink, shippingWeight, width, length, height, vat, createdDateTime, inventory, warrantyAddress, warrantyPhone, warranty, countryName, unit, advantages, description, content, highlights, images)

    def to_dict(self) -> dict:
        result: dict = {}
        result["idNhanh"] = from_str(str(self.idNhanh))
        result["privateId"] = from_none(self.privateId)
        result["parentId"] = from_str(str(self.parentId))
        result["brandId"] = from_none(self.brandId)
        result["brandName"] = from_str(self.brandName)
        result["typeId"] = from_str(str(self.typeId))
        result["typeName"] = to_enum(TypeName, self.typeName)
        result["avgCost"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.avgCost)
        result["importType"] = from_str(str(self.importType))
        result["importTypeLabel"] = to_enum(ImportTypeLabel, self.importTypeLabel)
        result["merchantCategoryId"] = from_none(self.merchantCategoryId)
        result["merchantProductId"] = from_none(self.merchantProductId)
        result["categoryId"] = from_str(str(self.categoryId))
        result["code"] = from_str(self.code)
        result["barcode"] = from_str(self.barcode)
        result["name"] = from_str(self.name)
        result["otherName"] = from_none(self.otherName)
        result["importPrice"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.importPrice)
        result["oldPrice"] = from_none(self.oldPrice)
        result["price"] = from_str(str(self.price))
        result["wholesalePrice"] = from_str(str(self.wholesalePrice))
        result["thumbnail"] = from_str(self.thumbnail)
        result["image"] = from_str(self.image)
        result["status"] = to_enum(Status, self.status)
        result["showHot"] = from_int(self.showHot)
        result["showNew"] = from_int(self.showNew)
        result["showHome"] = from_int(self.showHome)
        result["order"] = from_str(self.order)
        result["previewLink"] = from_str(self.previewLink)
        result["shippingWeight"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.shippingWeight)
        result["width"] = from_none(self.width)
        result["length"] = from_none(self.length)
        result["height"] = from_none(self.height)
        result["vat"] = from_none(self.vat)
        result["createdDateTime"] = self.createdDateTime.isoformat()
        result["inventory"] = to_class(Inventory, self.inventory)
        result["warrantyAddress"] = from_none(self.warrantyAddress)
        result["warrantyPhone"] = from_none(self.warrantyPhone)
        result["warranty"] = from_none(self.warranty)
        result["countryName"] = from_str(self.countryName)
        result["unit"] = to_enum(Unit, self.unit)
        result["advantages"] = from_none(self.advantages)
        result["description"] = from_str(self.description)
        result["content"] = from_none(self.content)
        result["highlights"] = from_union([lambda x: from_list(lambda x: x, x), from_none], self.highlights)
        result["images"] = from_union([lambda x: from_list(from_str, x), from_none], self.images)
        return result


@dataclass
class Data:
    currentPage: int
    totalPages: int
    products: Dict[str, Product]

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        assert isinstance(obj, dict)
        currentPage = from_int(obj.get("currentPage"))
        totalPages = from_int(obj.get("totalPages"))
        products = from_dict(Product.from_dict, obj.get("products"))
        return Data(currentPage, totalPages, products)

    def to_dict(self) -> dict:
        result: dict = {}
        result["currentPage"] = from_int(self.currentPage)
        result["totalPages"] = from_int(self.totalPages)
        result["products"] = from_dict(lambda x: to_class(Product, x), self.products)
        return result


@dataclass
class SearchProductRes:
    code: int
    data: Data

    @staticmethod
    def from_dict(obj: Any) -> 'SearchProductRes':
        assert isinstance(obj, dict)
        code = from_int(obj.get("code"))
        data = Data.from_dict(obj.get("data"))
        return SearchProductRes(code, data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = from_int(self.code)
        result["data"] = to_class(Data, self.data)
        return result


def SearchProductResfromdict(s: Any) -> SearchProductRes:
    return SearchProductRes.from_dict(s)


def SearchProductRestodict(x: SearchProductRes) -> Any:
    return to_class(SearchProductRes, x)
