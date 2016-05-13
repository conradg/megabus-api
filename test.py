import megabus

def test():
  #print(megabus.get_journey("Oxford","London","14/05/2016"))
  #print (megabus.all_locations)
  print (megabus.route_search("Oxford", "Paris"))
  count = 0
  for k in megabus.routes.keys():
    count += len(megabus.routes[k])
  print (count)
test()

