
import requests
import pandas
import links

def trim_to_month(value):

	ano = value[-4:]

	trim = int(value[0])

	if trim == 4:

		return '01/' + str(trim * 3) + '/' + ano

	else:

		return '01/0' + str(trim * 3) + '/' + ano

def get_data_sidra_ocup(table: str, nid: str):
	
	if nid in '4114 4115 9360'.split() and table != '6483':

		return {'Aviso': 'ID da Tabela Inválido'}

	elif nid in '4116 4117 9368'.split() and table != '6484':

		return {'Aviso': 'ID da Tabela Inválido'}

	elif nid not in '4114 4115 9360 4116 4117 9368'.split() or table not in '6483 6484'.split():

		return {'Aviso': 'ID da Variável ou Tabela Inválidos'}

	if table == '6483':
		
		data = requests.get(links.url_6483).json()
	
	elif table == '6484':

		data = requests.get(links.url_6484).json()

	keys = data[0].values()
	
	data.pop(0)
	
	df = pandas.DataFrame(data)
	
	df.columns = keys

	df['Data'] = df['Trimestre'].apply(trim_to_month)

	df['Valor'] = df['Valor'].replace('...', 0).astype(float)

	return df[df['Variável (Código)'] == nid].to_dict('records')
