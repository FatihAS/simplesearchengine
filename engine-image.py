from clarifai.rest import ClarifaiApp
app = ClarifaiApp(api_key='aaf468ee68224c069416a4ac1aef4b74')

filename = "static/img/bmw/5.png"
response = app.inputs.search_by_image(filename=filename)
for x in range(0,len(response)):
    print(response[x].url)