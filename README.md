# GeoChase

Play tag using the local geography.

![](https://github.com/phuang1024/GeoChase/blob/master/examples/sample1.jpg)

## Gameplay

There are three types of players:

- Robbers need to collect Targets --- randomly placed points on the map.
- Cops need to catch Robbers.
- Helicopters can see all players on the map.
  They do not directly catch Robbers,
  but can provide information to Cops.

Communication between like player types is encouraged.

## Usage

`python src/server/main.py` once to start the server.

`python src/client/main.py` as many times as needed.

### Hotkeys:

- `WASD` or arrow keys to move.
- `v` to toggle window view mode.
- `i` to toggle info style.
- `b` to toggle drawing buildings (slow).
- `p` to toggle draw all paths and roads.
- `c` to toggle show collision surface.
