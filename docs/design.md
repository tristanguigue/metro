# Models

- `Line`
 - `id`
 - `average_maximum_speed`
 - `rolling_stock`
 - `yearly_traffic`

 - `RollingStock`
    - id
    - `name`
    - `acceleration`
    - `deceleration`
    - `max_speed`

- `Station`
 - `id`
 - `location`
 - `name`
 - `yearly_entries`
 - <`lines`>
 - remove():
    - get time gain when not making stop
     - get traffic between surrounding stops
    - get time lost
     - get closest stations
     - calculate time to walk there

- `Segment`
 - `stationA`
 - `stationB`
 - `traffic_AB`
 - `traffic_BA`
 - `line`

# Data files
- `lines.json`
- `rolling_stock.json`
- `station_yearly_entries.csv`
- <`stops.txt`>
- <`stop_times.txt`>

# Data Population Scripts
- Create stations, lines and segments using `stops.txt` and `stop_times.txt`
- Load entries into segments using `station_yearly_entries.csv`
- Load line traffic into lines using `line_yearly_entries.json`
- Create rolling stock and load rolling stock into lines using `rolling_stock.json`

- Generate traffic data:
    - From line end get traffic for first segment
    - Calculate out and ins for next station based on entries for the rest of the line
    - Repeat until reached other end

# Endpoints:
- `remove_stop()`
 - Calls `station.remove_stop()`

