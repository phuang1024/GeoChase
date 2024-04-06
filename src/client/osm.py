import xml.etree.ElementTree as ET
from dataclasses import dataclass


@dataclass
class Node:
    id: int
    lat: float
    lon: float


@dataclass
class Way:
    id: int
    nodes: list[Node]
    tags: dict[str, str]


@dataclass
class OSM:
    nodes: dict[int, Node]
    ways: list[Way]

    # lat and lon bounds
    top: float
    left: float
    bottom: float
    right: float

    scaling_factor: float = 1


def parse_osm_file(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return parse_osm(root)


def parse_osm(root):
    nodes = {}
    ways = []

    top = float("inf")
    left = float("inf")
    bottom = float("-inf")
    right = float("-inf")

    for child in root:
        if child.tag == "node":
            id = int(child.attrib["id"])
            lat = float(child.attrib["lat"])
            lon = float(child.attrib["lon"])
            nodes[id] = Node(
                id=id,
                lat=lat,
                lon=lon,
            )

            top = min(top, lat)
            left = min(left, lon)
            bottom = max(bottom, lat)
            right = max(right, lon)

        elif child.tag == "way":
            way = Way(
                id=int(child.attrib["id"]),
                nodes=[],
                tags={},
            )
            for subchild in child:
                if subchild.tag == "nd":
                    way.nodes.append(nodes[int(subchild.attrib["ref"])])
                elif subchild.tag == "tag":
                    way.tags[subchild.attrib["k"]] = subchild.attrib["v"]
            ways.append(way)

    # TODO explain this
    scaling = 1 / np.cos(np.radians(top))

    return OSM(
        nodes=nodes,
        ways=ways,
        top=top,
        left=left,
        bottom=bottom,
        right=right,
        scaling_factor=scaling,
    )
