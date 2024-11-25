

def parse_coordinate(coordinate: list) -> int:
    return coordinate[0] + coordinate[1] / 60 + int(coordinate[2]) / 3600