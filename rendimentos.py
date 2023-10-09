
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

def get_data_sidra_renda(nid):
			
	if nid not in '5933 5935 5941 5943'.split():

		return {'Aviso': 'ID da Variável Inválido'}

	data = requests.get(links.url_5436).json()
	
	keys = data[0].values()
	
	data.pop(0)
	
	df = pandas.DataFrame(data)
	
	df.columns = keys
	
	df['Data'] = df['Trimestre'].apply(trim_to_month)

	df['Valor'] = df['Valor'].astype(float)

	return df[df['Variável (Código)'] == nid].to_dict('records')