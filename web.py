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
    month  = int(split[2])
    info = megabus.get_cheapest_in_month(start, end, month)
    return json.dumps(info)

@app.route('/journey/<path:path>')
def get_journey(path):
    split =  path.split("/")
    start = split[0]
    end   = split[1]
    date  = "/".join(split[2:])
    info = megabus.get_journey(start, end, date)

    return json.dumps(info)





@app.route('/destinations/<starting_location>')
def get_destinations(starting_location):
  result = megabus.get_destinations(starting_location)
  return json.dumps(result)

if __name__ == "__main__":
    app.debug = True
    app.run()

