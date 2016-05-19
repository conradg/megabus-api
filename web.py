from flask import Flask, request, render_template
import megabus
import hashlib, time, sys
import json
app = Flask(__name__)

# Return our opening sentence
@app.route('/')
def home():
  return render_template('demo.html')



@app.route('/journey/cheapest/<path:path>')
def get_cheapest_in_month(path):
    split =  path.split("/")
    start = split[0]
    end   = split[1]
    month = split[2]
    try:
      month = int(month)
      info = megabus.get_cheapest_in_month_num(start, end, month)
    except ValueError:
      info = megabus.get_cheapest_in_month_string(start, end, month)
    return json.dumps(info)

@app.route('/journey/<path:path>')
def get_journey(path):
    split =  path.split("/")
    start = split[0]
    end   = split[1]
    date  = "/".join(split[2:])
    info = megabus.get_journey(start, end, date)

    return json.dumps(info)


@app.route('/test/')
def test():
    times = [{"timings": {"arrive": "22:45", "depart": "17:45"}, "days": 0, "date": "8/7/2016", "next_day": 0, "locations": {"arrive": "Leeds", "depart": "Oxford"}, "cost": "1.00", "duration": "5hrs 0mins"}, {"timings": {"arrive": "22:45", "depart": "17:45"}, "days": 0, "date": "22/7/2016", "next_day": 0, "locations": {"arrive": "Leeds", "depart": "Oxford"}, "cost": "1.00", "duration": "5hrs 0mins"}, {"timings": {"arrive": "22:25", "depart": "17:30"}, "days": 0, "date": "26/7/2016", "next_day": 0, "locations": {"arrive": "Leeds", "depart": "Oxford"}, "cost": "1.00", "duration": "4hrs 55mins"}]
    return json.dumps(times)




@app.route('/destinations/<starting_location>')
def get_destinations(starting_location):
  result = megabus.get_destinations(starting_location)
  return json.dumps(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

