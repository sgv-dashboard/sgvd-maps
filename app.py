from flask import Flask, request, render_template
from datetime import datetime
import openrouteservice
from openrouteservice import convert
import folium

app = Flask(__name__)

###############################################################
#                         Web Routes                         #
###############################################################

@app.route('/')
def index():
	return "Dit is een test"

@app.route('/map', methods=['GET'])
def get_map():
	#Key hoort bij mijn account, max 2000 requests per 24h
	client = openrouteservice.Client(key='5b3ce3597851110001cf62484b7bc6e27b5b47fabce3821209f35d73')

	#Test url: http://127.0.0.1:5000/map?latS=51.075824&lonS=5.262364&latE=50.927683&lonE=5.386107
	latitudeStart = float(request.args.get('latS'))
	longitudeStart = float(request.args.get('lonS'))
	latitudeEnd = float(request.args.get('latE'))
	longitudeEnd = float(request.args.get('lonE'))

	coords = ((longitudeStart, latitudeStart),(longitudeEnd, latitudeEnd))
	res = client.directions(coords)
	geometry = client.directions(coords)['routes'][0]['geometry']
	decoded = convert.decode_polyline(geometry)

	#We kunnen ook gewoon de afstand en tijd weergeven, zonder kaartje
	distance = str(round(res['routes'][0]['summary']['distance']/1000,1))
	duration = str(round(res['routes'][0]['summary']['duration']/60,1))

	distance_txt = "<h4> <b>Afstand :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['distance']/1000,1))+" Km </strong>" +"</h4></b>"
	duration_txt = "<h4> <b>Tijd :&nbsp" + "<strong>"+str(round(res['routes'][0]['summary']['duration']/60,1))+" Mins. </strong>" +"</h4></b>"

	m = folium.Map(location=[latitudeStart, longitudeStart],zoom_start=10, control_scale=True,tiles="cartodbpositron")
	folium.GeoJson(decoded).add_child(folium.Popup(distance_txt+duration_txt,max_width=300)).add_to(m)

	folium.Marker(
		location=list(coords[0][::-1]),
		popup="Vertrek",
		icon=folium.Icon(color="green"),
	).add_to(m)

	folium.Marker(
		location=list(coords[1][::-1]),
		popup="Bestemming",
		icon=folium.Icon(color="red"),
	).add_to(m)

	return m.get_root().render()

###############################################################
#                         Api Routes                         #
###############################################################

if __name__=="__main__":
	app.run(debug=True)


