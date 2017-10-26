import pickle
import argparse
import dateutil.parser

import matplotlib.pyplot as plt

import database_tools as db

if __name__ == "__main__": #if this is the main file, parse the command args
	parser = argparse.ArgumentParser(description="Tool that can read historical data from the db or from a file and visualize it as a graph.")
	parser.add_argument('data', type=str, help='The data to visualize. Can be a filepath to a pickled (single!) dataset or a key in the db.')
	parser.add_argument('--type', type=str, default='file', choices=['key', 'file'], help='What type of data to load and visualize- key from the database or a file.')
	parser.add_argument('--index', type=int, default=0, help='If loading a file, provide the index of the property in the data matrix to be visualized.')
	parser.add_argument('--start', type=str, default=None, help='The start date. YYYY-MM-DD-HH')
	parser.add_argument('--end', type=str, default=None, help='The end date. YYYY-MM-DD-HH')

	args, _ = parser.parse_known_args()

	start = dateutil.parser.parse(args.start) if args.start is not None else None
	end = dateutil.parser.parse(args.end) if args.end is not None else None

	if args.type=='file':
		with open(args.data, 'rb') as f:
			data = pickle.load(f)
			values = data['dataset'][:, 0, args.index]
			dates = data['dates']

			print(values, dates)
	elif args.type=='key':
		data = db.loadData(db.getChunkstore(), args.data, start, end, True)
		values = data[args.data].values
		dates = data['date'].values

	plt.plot(dates, values)
	plt.xlabel = 'Timeline'
	plt.ylabel = 'Value of '+args.data
	plt.show()
	