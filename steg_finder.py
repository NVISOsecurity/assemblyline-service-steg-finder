import shutil, subprocess, csv, json

from assemblyline_v4_service.common.base import ServiceBase
from assemblyline_v4_service.common.result import Result, ResultSection, BODY_FORMAT


class StegFinder(ServiceBase):
	def __init__(self, config=None):
		super(StegFinder, self).__init__(config)

	def start(self):
		self.log.debug("Steg Finder service started")

	def stop(self):
		self.log.debug("Steg Finder service ended")

	def read_csv(self, csv_path):
		my_dict = {}

		with open(csv_path, "r") as f:
			next(f)
			file_data = csv.DictReader(f)

			for row in file_data:
				my_dict = row

		return my_dict

	def beautify_dict(self, my_dict):
		try:
			my_dict.pop("File name")
		except KeyError:
			pass

		for key in my_dict:
			try:
				if int(float(my_dict[key])) != float(my_dict[key]):
					my_dict[key] = "{0:.2f %}".format(float(my_dict[key]) * 100)
				if my_dict[key] == "NaN" or my_dict[key] == "null":
					my_dict[key] = "0.00 %"
			except ValueError:
				pass

		return my_dict

	def execute(self, request):
		result = Result()

		file_path = request.file_path
		file_type = request.file_type

		shutil.copyfile(file_path, self.working_directory + "/analyzed")

		p1 = subprocess.Popen("java -jar /var/lib/assemblyline/StegExpose/StegExpose.jar " + self.working_directory + " standard default " + self.working_directory + "/report.csv", shell=True)
		p1.wait()

		lsb_steg_results = self.read_csv(self.working_directory + "/report.csv")
		lsb_steg_results = self.beautify_dict(lsb_steg_results)

		kv_section = ResultSection("Result of the LSB steganalysis", body_format=BODY_FORMAT.KEY_VALUE, body=json.dumps(lsb_steg_results))
		result.add_section(kv_section)

		request.result = result