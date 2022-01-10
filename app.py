from flask import Flask, request, render_template, Response
from datetime import datetime
import openrouteservice
from openrouteservice import convert
import folium
from flask_cors import CORS
from flask.json import JSONEncoder

app = Flask(__name__)
CORS(app)

VALID_API_KEYS = {'5b3ce3597851110001cf62484b7bc6e27b5b47fabce3821209f35d73'}

###############################################################
#                         Web Routes                         #
###############################################################

@app.route('/')
def index():
	return "Maps API"

@app.route('/documentation')
def documentation():
	return render_template('documentation.html')

###############################################################
#                         Api Routes                         #
###############################################################

@app.route('/map', methods=['GET'])
def get_map():
	if (request.args.get('key') in VALID_API_KEYS):
		client = openrouteservice.Client(key=str(request.args.get('key')))

		latitudeStart = float(request.args.get('latS'))
		longitudeStart = float(request.args.get('lonS'))
		latitudeEnd = float(request.args.get('latE'))
		longitudeEnd = float(request.args.get('lonE'))

		coords = ((longitudeStart, latitudeStart),(longitudeEnd, latitudeEnd))
		res = client.directions(coords)
		geometry = client.directions(coords)['routes'][0]['geometry']
		decoded = convert.decode_polyline(geometry)

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

		data = dict (
			distance = distance,
			duration = duration,
			html_map = m.get_root().render()
		)

		return data
	
	else:
		error = {'error': 'invalid key', 'used-key': str(request.args.get('key'))}
        
		return Response(JSONEncoder().encode(error), status=403, mimetype='application/json')

if __name__=="__main__":
	app.run(debug=True)