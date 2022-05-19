import altair as alt
import csv
import pandas as pd

from vega_datasets import data

data_file = 'national_revenue.csv'
state_file = 'state_map.csv'
pop_file = 'nst-est2019-alldata.csv'

by_state = {}
by_year = {}

state_map = {}
id_map = {}

display_years = list(range(2000,2019))
year = 2017

df_rev = {}
df_pop = {}

def go(): 
	parse_data()
	#check_year_data()
	parse_state_map()
	add_pop_data()
	calc_percents()
	build_display_df()
	#plot_revenue()
	plot_rev_pop_diff()

def parse_data(): 
	global by_state
	global by_year

	with open(data_file, 'r') as csvfile: 
		csvreader = csv.reader(csvfile)
		headers = next(csvreader)

		for row in csvreader: 
			state = row[0].strip()
			year = row[2].strip()
			revenue = row[5].strip()

			if year == '' or state == '' or revenue == '': 
				continue

			year = int(year)
			revenue = int(revenue)

			if state not in by_state:
				by_state[state] = {}
			
			if year not in by_state[state]: 
				by_state[state][year] = 0

			if year not in by_year: 
				by_year[year] = 0

			if revenue != '':
				by_state[state][year] += revenue
				by_year[year] += revenue

def parse_state_map(): 
	global state_map
	global id_map

	with open(state_file, 'r') as csvfile: 
		csvreader = csv.reader(csvfile)
		headers = next(csvreader)

		for row in csvreader: 
			postal = row[1].strip()
			map_id = int(row[2].strip())

			state_map[postal] = map_id

	id_map = {v: k for k, v in state_map.items()}

def build_display_df():
	global df_rev

	display_dict = {}

	index = 0
	for state in by_state: 
		for year in by_state[state]: 
			display_dict[index] = {
				'state': state, 
				'year': str(year),
				'revenue': by_state[state][year],
				'id': state_map[state]
			}
			index += 1

	df_rev = pd.DataFrame.from_dict(display_dict, orient='index').reset_index()

def check_year_data(): 
	years = list(by_year.keys())
	years.sort()
	for year in by_year: 
		states = count_year(year)
		print('%s - %d' % (year, states))

def count_year(year):
	count = 0
	for state in by_state: 
		if year in by_state[state]: 
			count += 1

	return count

def plot_revenue():
	global df_rev 

	states = alt.topo_feature(data.us_10m.url, 'states')

	df_rev = df_rev.pivot(index='id', columns='year', values='revenue').reset_index()

	df_rev['state'] = df_rev['id'].apply(lambda s: id_map[s]['name'])

	columns = [str(year) for year in display_years]
	slider = alt.binding_range(min=2000, max=2018, step=1)
	select_year = alt.selection_single(name='revenue', fields=['year'],
                                   bind=slider, init={'year': 2017})

	chart = alt.Chart(states).mark_geoshape(
	    stroke='black',
	    strokeWidth=0.2
	).project(
	    type='albersUsa'
	).transform_lookup(
	    lookup='id',
	    from_=alt.LookupData(df_rev, 'id', columns + ['state'])
	).transform_fold(
	    columns, as_=['year', 'revenue']
	).transform_calculate(
	    year='parseInt(datum.year)',
	    revenue='isValid(datum.revenue) ? datum.revenue : -1'  
	).encode(
	    color = alt.condition(
	        'datum.revenue > 0',
	        alt.Color('revenue:Q', scale=alt.Scale(scheme='blues')),
	        alt.value('#ffffff')
	    ),
	    tooltip=['year:O', 'state:O', 'revenue:Q']
	).add_selection(
	    select_year
	).properties(
	    width=700,
	    height=400,
	    title={
	        'text': 'Forfeiture Revenue by State',
    	}
	).transform_filter(
	    select_year
	)

	chart.show()

def add_pop_data(): 
	with open(pop_file, 'r') as csvfile: 
		csvreader = csv.reader(csvfile)
		headers = next(csvreader)

		for row in csvreader: 
			map_id = int(row[3].strip())
			pop = int(row[5].strip())	
			name = row[4].strip()

			if map_id in id_map: 
				id_map[map_id] = {
					'population' : pop, 
					'postal': id_map[map_id],
					'name': name
				}

def calc_percents(): 
	global df_pop 

	total_revenue = by_year[year]
	total_pop = 308745538

	for state_id in id_map:
		state = id_map[state_id]['postal']
		
		if state not in by_state or year not in by_state[state]: 
			id_map[state_id]['revenue'] = -1
			continue
		
		if year in by_state[state]:
			revenue = by_state[state][year]
			rev_perc = revenue / (total_revenue * 1.0)
			pop_perc = id_map[state_id]['population'] / (total_pop * 1.0)

			id_map[state_id]['revenue'] = revenue
			id_map[state_id]['revenue%'] = rev_perc
			id_map[state_id]['population%'] = pop_perc
			id_map[state_id]['percent_diff'] = (rev_perc - pop_perc)

	df_pop = pd.DataFrame.from_dict(id_map, orient='index').reset_index()

def plot_rev_pop_diff(): 
	states = alt.topo_feature(data.us_10m.url, 'states')

	click = alt.selection_multi(fields=['name'])

	pop_map = alt.Chart(states).mark_geoshape(
	    stroke='black',
	    strokeWidth=0.2
	).project(
	    type='albersUsa'
	).transform_lookup(
	    lookup='id',
	    from_=alt.LookupData(df_pop, 'index', ['name','revenue', 'revenue%','population', 'population%', 'percent_diff'])
	).encode(
	    color = alt.condition(
	    	'datum.percent_diff === null',
	        alt.value('#f1f2f3'),
	        alt.Color('percent_diff:Q', scale=alt.Scale(scheme='blueorange'), legend=alt.Legend(format=".0%"), title='% Difference')
	    ),
	    opacity=alt.condition(click, alt.value(1), alt.value(0.2)),
	    tooltip=['name:O', alt.Tooltip('population:Q',format=',.0f'), alt.Tooltip('population%:Q', format='.2%'), alt.Tooltip('revenue:Q',format='$,.0f'), alt.Tooltip('revenue%:Q', format='.2%'), alt.Tooltip('percent_diff:Q', format='.2%')]
	).properties(
	    width=700,
	    height=500,
	    title={
	        'text': '2017 Forfeiture Revenue vs. Population by State',
	        'subtitle': ['Population is based on 2010 US Census']
    	}
	).add_selection(click)

	pop_chart = alt.Chart(df_pop).mark_bar().encode(
		alt.X('percent_diff:Q', axis=alt.Axis(format='%'), title='% Difference'),
		alt.Y('name:N', title='State', sort=alt.EncodingSortField(field='percent_diff', order='descending')),
		color=alt.Color('percent_diff:Q', scale=alt.Scale(scheme='blueorange'), legend=alt.Legend(format=".0%")),
		opacity=alt.condition(click, alt.value(1), alt.value(0.2)),
		tooltip=['name:O', alt.Tooltip('population:Q',format=',.0f'), alt.Tooltip('population%:Q', format='.2%'), alt.Tooltip('revenue:Q',format='$,.0f'), alt.Tooltip('revenue%:Q', format='.2%'), alt.Tooltip('percent_diff:Q', format='.2%')]
	).properties(
		height=500,
		width=200
	).add_selection(click)

	together = alt.hconcat(pop_chart, pop_map)
	#together.show()
	together.save('rev_pop_diff.html')