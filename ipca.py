import requests
import pandas
import links

def text_to_month(value):

	m = {
		'jan': '01',
		'fev': '02',
		'mar': '03',
		'abr': '04',
		'mai': '05',
		'jun': '06',
		'jul': '07',
		'ago': '08',
		'set': '09',
		'out': '10',
		'nov': '11',
		'dez': '12'
	}

	ano = value[-4:]

	month = value[0:3]

	return '01/' + m.get(month) + '/' + ano

def get_data_ipca():
			
	data = requests.get(links.url_7061).json()
	
	keys = data[0].values()
	
	data.pop(0)
	
	df = pandas.DataFrame(data)
	
	df.columns = keys

	df['Data'] = df['Mês'].apply(text_to_month)

	df['Valor'] = df['Valor'].astype(float)

	df = df.pivot_table(
		index = ['Mês', 'Data'], 
		columns = ['Variável', 'Geral, grupo, subgrupo, item e subitem'], 
		values = 'Valor',
		aggfunc = 'first'
	).reset_index()

	df.columns = [
		'Mês', 'Data', 
		'Peso (Alimentação)', 'Peso (Habitação)', 'Peso (Transportes)', 'Peso (Geral)',
		'Variação % (Alimentação)', 'Variação % (Habitação)', 'Variação % (Transportes)', 'Variação % (Geral)'
	]

	for i in 'Alimentação Habitação Transportes'.split():

		df['Impacto (' + i + ')'] = (df['Variação % (' + i + ')']/100) * (df['Peso (' + i + ')']/100)

		df['Contribuição % (' + i + ')'] = (df['Impacto (' + i + ')']/(df['Variação % (Geral)']/100))*100

	return df.to_dict('records')
