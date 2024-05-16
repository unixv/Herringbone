import glob

with open("dataset.csv", "w") as dataset:
	for logfile in glob.glob("./*/*.log"):
		logtype = logfile.split("/")[1]
		data = open(logfile, "r").read().split("\n")
		for line in data:
			dataset.write(logtype +","+ line +",")
