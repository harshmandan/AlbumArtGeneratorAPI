import flask, json, requests
from flask import request, jsonify, send_file
import improcess
from PIL import Image
from io import BytesIO

app = flask.Flask(__name__)
app.config["DEBUG"] = True

apikey = "your_key_here"
searchurl = "http://api.musixmatch.com/ws/1.1/track.search?apikey="
lyricurl = "http://api.musixmatch.com/ws/1.1/track.lyrics.get?apikey="
getimageurl= "https://source.unsplash.com/600x600/?nature,water,abstract,minimal,clean,camping,morning,night,smoke,old"
trackidurl = "http://api.musixmatch.com/ws/1.1/track.get?apikey="+ apikey + "&track_id="

@app.route('/', methods=['GET'])
def home():
	return "<h1>Album Art Generator</h1><p>This site lets you generate beautiful album art for your favorite tracks</p>"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/gettrack/', methods=['GET'])
def api_search():
	if 'artist' in request.args:
		artist = request.args.get('artist')
	if 'track' in request.args:
		track = request.args.get('track')
	else:
		return "Error: Please specify both fields: Artist name & Track name"

	req_url = searchurl+apikey+"&q_artist="+artist+"&q_track="+track
	song_dict = json.loads(requests.get(req_url).text)
	if (len(song_dict['message']['body']['track_list']) > 0):
		response_dict={};
		tracks = []
		for song in song_dict['message']['body']['track_list']:
			print (song['track']['track_id'])
			tracks.append({"artist" : song['track']['artist_name'],
							"album_name" : song['track']['album_name'],
							"track_name" : song['track']['track_name'],
							"id" : song['track']['track_id']})
		response_dict["tracks"] = tracks
		#print (json.dumps(response_dict,indent=2))

	return (json.dumps(response_dict,indent=2))

@app.route('/api/getalbumart/', methods=['GET'])
def api_getart():
	if 'id' in request.args:
		trackid = request.args.get('id')
	else:
		return ("Error: No ID specified! Obtain Id from /api/gettrack/ first!")
	req_url = lyricurl+apikey+"&track_id="+trackid
	lyric_dict = json.loads(requests.get(req_url).text)
	#print(lyric_dict['message']['header']['status_code'])
	if ('404' == str(lyric_dict['message']['header']['status_code'])):
		return ("Error: No track associated with that ID")
	lyric_body = lyric_dict['message']['body']['lyrics']['lyrics_body']
	lst = lyric_body.split('\n')
	#lyric_sentences = lst[:len(lst)-3] Removes copyright line, not neccessary!
	print(lst)
	finalitem = improcess.prepare_image(lst)
	print(finalitem)
	url_trackid = trackidurl+trackid
	info_dict = json.loads(requests.get(url_trackid).text)
	artistname = info_dict['message']['body']['track']['artist_name']
	trackname = info_dict['message']['body']['track']['track_name']
	response = requests.get(getimageurl)
	img = Image.open(BytesIO(response.content))
	filename = improcess.generate_img(img, finalitem, artistname, trackname)
	return send_file(filename, mimetype='image/jpg')

app.run()