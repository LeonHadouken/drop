import xml.etree.ElementTree as ET
from .models import Type

def parse_types_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    for type_element in root.findall('type'):
        data = {
            "name": type_element.get("name"),
            "nominal": int(type_element.find("nominal").text) if type_element.find("nominal") is not None else None,
            "lifetime": int(type_element.find("lifetime").text) if type_element.find("lifetime") is not None else None,
            "restock": int(type_element.find("restock").text) if type_element.find("restock") is not None else None,
            "min": int(type_element.find("min").text) if type_element.find("min") is not None else None,
            "quantmin": int(type_element.find("quantmin").text) if type_element.find("quantmin") is not None else None,
            "quantmax": int(type_element.find("quantmax").text) if type_element.find("quantmax") is not None else None,
            "cost": int(type_element.find("cost").text) if type_element.find("cost") is not None else None,
            "category": type_element.find("category").get("name") if type_element.find("category") is not None else None,
            "tier": type_element.find("value").get("user") if type_element.find("value") is not None else None,
            "tags": [tag.get("name") for tag in type_element.findall("tag")]
        }
        Type.objects.update_or_create(name=data["name"], defaults=data)
