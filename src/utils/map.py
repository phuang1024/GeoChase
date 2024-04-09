__all__ = (
    "VALID_ROAD_TYPES",
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
class Way:
    nodes: np.ndarray
    """Shape (n, 2). Coords of the nodes in the way."""
    left_top: np.ndarray
    """Shape (2). Top-left corner of the bounding box."""
    right_bottom: np.ndarray
    """Shape (2). Bottom-right corner of the bounding box."""
    tags: dict[str, str]


@dataclass
class OSM:
    #nodes: dict[int, Node]
    ways: list[Way]

    com: np.ndarray
    """Center of mass (coords) of the map."""
    stretch_factor: float = 1
    """secant(avg_lat)"""

    # lat and lon bounds
    """
    top: float
    left: float
    bottom: float
    right: float
    """

    def get_rand_road(self) -> Way:
        while True:
            way = random.choice(self.ways)
            if way.tags.get("highway", None) in VALID_ROAD_TYPES:
                break
        return way

    def get_rand_road_pos(self) -> tuple[Way, np.ndarray]:
        way = self.get_rand_road()
        node = random.choice(way.nodes)
        return way, node

    def get_rand_pos(self) -> np.ndarray:
        return self.get_rand_road_pos()[1]


def parse_osm_file(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return parse_osm(root)


def parse_osm(root):
    node_locs = {}
    ways = []
    com = np.zeros(2)
    com_n = 0

    for child in root:
        if child.tag == "node":
            id = int(child.attrib["id"])
            lat = float(child.attrib["lat"])
            lon = float(child.attrib["lon"])
            loc = np.array([lon, lat])
            node_locs[id] = loc

        elif child.tag == "way":
            way_locs = []
            tags = {}
            for subchild in child:
                if subchild.tag == "nd":
                    way_locs.append(node_locs[int(subchild.attrib["ref"])])
                elif subchild.tag == "tag":
                    tags[subchild.attrib["k"]] = subchild.attrib["v"]
            way_locs = np.array(way_locs)

            if "highway" in tags or "addr:street" in tags:
                ways.append(Way(
                    nodes=way_locs,
                    left_top=np.min(way_locs, axis=0),
                    right_bottom=np.max(way_locs, axis=0),
                    tags=tags,
                ))
                com += np.sum(way_locs, axis=0)
                com_n += way_locs.shape[0]

    com /= com_n
    # TODO explain this
    stretch = 1 / np.cos(np.radians(com[1]))

    return OSM(
        ways=ways,
        com=com,
        stretch_factor=stretch,
    )
