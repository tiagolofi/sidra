
import flask
import ocupacao
import rendimentos
import ipca

app = flask.Flask(__name__)

@app.route('/')
def docs():

	return flask.render_template('index.html')

@app.get('/ocupacao')
def ocup():

	table = flask.request.args.get(key = 'table', default = '', type = str)
	
	nid = flask.request.args.get(key = 'nid', default = '', type = str)

	return flask.jsonify(ocupacao.get_data_sidra_ocup(table = table, nid = nid))

@app.get('/rendimento')
def rend():
	
	nid = flask.request.args.get(key = 'nid', default = '', type = str)

	return flask.jsonify(rendimentos.get_data_sidra_renda(nid = nid))

@app.get('/ipca')
def preco():

	return flask.jsonify(ipca.get_data_ipca())

if __name__ == '__main__':

	app.run(debug = True, host='0.0.0.0', port = 8080)
