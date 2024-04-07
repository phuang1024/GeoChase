__all__ = (
    "VALID_ROAD_TYPES",
    "Node",
    "Way",
    "OSM",
    "parse_osm_file",
)

import random
import xml.etree.ElementTree as ET
from dataclasses import dataclass

import numpy as np

VALID_ROAD_TYPES = (
    "motorway",
    "trunk",
    "primary",
    "secondary",
    "tertiary",
    "residential",
    "unclassified",
)


@dataclass
class Node:
    id: int
    lat: float
    lon: float
    tags: dict[str, str]


@dataclass
class Way:
    id: int
    nodes: list[Node]
    tags: dict[str, str]

    # lat and lon bounds
    top: float = float("inf")
    left: float = float("inf")
    bottom: float = float("-inf")
    right: float = float("-inf")


@dataclass
class OSM:
    nodes: dict[int, Node]
    ways: list[Way]

    # lat and lon bounds
    top: float
    left: float
    bottom: float
    right: float

    # 1 / cos(latitude)
    stretch_factor: float = 1

    def get_com(self):
        lat = 0
        lon = 0
        for node in self.nodes.values():
            lat += node.lat
            lon += node.lon
        lat /= len(self.nodes)
        lon /= len(self.nodes)
        return lon, lat

    def get_rand_road(self):
        while True:
            way = random.choice(self.ways)
            if way.tags.get("highway", None) in VALID_ROAD_TYPES:
                break
        return way

    def get_rand_road_pos(self):
        way = self.get_rand_road()
        node = random.choice(way.nodes)
        return way, (node.lon, node.lat)

    def get_rand_pos(self):
        return self.get_rand_road_pos()[1]


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

            tags = {}
            for subchild in child:
                if subchild.tag == "tag":
                    tags[subchild.attrib["k"]] = subchild.attrib["v"]

            nodes[id] = Node(
                id=id,
                lat=lat,
                lon=lon,
                tags=tags
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

            way.top = min(node.lat for node in way.nodes)
            way.left = min(node.lon for node in way.nodes)
            way.bottom = max(node.lat for node in way.nodes)
            way.right = max(node.lon for node in way.nodes)

            if "highway" in way.tags or "addr:street" in way.tags:
                ways.append(way)

    # TODO explain this
    stretch = 1 / np.cos(np.radians(top))

    return OSM(
        nodes=nodes,
        ways=ways,
        top=top,
        left=left,
        bottom=bottom,
        right=right,
        stretch_factor=stretch,
    )
