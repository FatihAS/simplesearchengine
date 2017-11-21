#!flask/bin/python
from flask import Flask, render_template, request, abort, send_from_directory, redirect
from engine import search
import requests

app = Flask(__name__, static_url_path='/static')

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('static/img/', path)

@app.route('/webdata/<path:path>')
def send_webdata(path):
    return send_from_directory('static/webdata/', path)

@app.route('/',)
def index():
    pageName = "index"
    return render_template('%s.html' % pageName)

@app.route('/search', methods=['GET'])
def searchResult():
    pageName = "result"
    data = request.args.get("search")
    page = request.args.get("p")
    
    try:
        page = int(page)
    except:
        page = 1

    if data is not None :
        r = requests.get("https://agri.gravicodev.id/map_data/route.json")
        r = r.json()
        result = search(data)

        jumlahPage = int(len(result)/10)
        if len(result) % 10 != 0:
            jumlahPage += 1

        if page > jumlahPage:
            page = 1
        
        if page*10 > len(result):
            result = result[(page-1)*10:]
        else:
            result = result[(page-1)*10:page*10]

        passParam = {}
        passParam['result'] = result
        passParam['route'] = r
        passParam['query'] = data
        passParam['totalPage'] = jumlahPage
        passParam['currentPage'] = page
        return render_template('%s.html' % pageName, variable = passParam)
    else:
        return redirect("/", code=302)


if __name__ == '__main__':
    app.run(debug=True)
