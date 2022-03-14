# Python3 code!

from csv import DictReader, DictWriter
from collections import namedtuple

CSV_File = "/home/samuel/Downloads/Compilation_Table.csv"


PROJECTS = ['1Group16Voices', '16audiomods', 'AvUsage8GroupsAudiomodules',
            'AvUseCase8GroupsNoAudioModules', 'Stresstest2Groups']

DEVICES = ['Desktop PC', 'Q7-i7_5650U-4GB-BVM (2.2 GHz) ',
		   'Q7-Atom_E3950-8GB-Congatec (1.6 GHz)',
		   'Q7-Atom_E3940-4GB-SECO (1.6 GHz)',
		   'Q7-Atom_E3950-8GB-Congatec (2.0 GHz)',
		   'Q7-Pentium_N4200-4GB-AAEON (2.4 GHz) ',
		   'Q7-ARM_RK3399-2GB-Theobroma (1.8/1.41 GHz) [2]']


def _perc_calc(value1, value2):
	"""
	Percentual value1 against value2 (value2 is the base)
	e.g.: if perc = -9% value1 is 9% percentual less than value2
	"""

	diff = value1 - value2
	return (diff / value2) * 100 


def _convert_number_to_string(value):
	if (value >= 0):
		return 'higher'
	elif (value < 0):
		return 'lower'


def get_avr_by_device(device):
	"""
	Read the values of the device and calculates the mean.
	Return a tuple
	"""

	Device_avr = namedtuple('Device', ['mas_max_cpu', 'system_max_cpu',
									   'mas_mean_cpu', 'system_mean_cpu',
									   'audio_level_mean', 'mas_dropouts'])

	sum_mas_max_cpu = 0
	sum_system_max_cpu = 0
	sum_mas_mean_cpu = 0
	sum_system_mean_cpu = 0
	sum_audio_level_mean = 0
	sum_mas_dropouts = 0

	with open(CSV_File, newline='') as csvfile:
		reader = DictReader(csvfile, delimiter=',', quotechar='|')
		filtered_row_counter = 0
		for row in reader:
			if (row['Device'] == device):
				filtered_row_counter += 1
				sum_mas_max_cpu += float(row['MAS_Max_CPU'])
				sum_system_max_cpu += float(row['System_Max_CPU'])
				sum_mas_mean_cpu += float(row['MAS_Mean_CPU'])
				sum_system_mean_cpu += float(row['System_Mean_CPU'])
				sum_audio_level_mean += float(row['Audio_Level_Mean'])
				sum_mas_dropouts += int(row['MAS_Dropouts'])

	dev_arv = Device_avr(sum_mas_max_cpu / filtered_row_counter,
						 sum_system_max_cpu / filtered_row_counter,
						 sum_mas_mean_cpu / filtered_row_counter,
						 sum_system_mean_cpu / filtered_row_counter,
						 sum_audio_level_mean / filtered_row_counter,
						 sum_mas_dropouts / filtered_row_counter)


	return dev_arv


def get_avr_by_dev_and_proj(device, project):
	"""
	Read the values of the device in a project and calculates the mean.
	Return a tuple
	"""

	Device_avr = namedtuple('Device', ['mas_max_cpu', 'system_max_cpu',
									   'mas_mean_cpu', 'system_mean_cpu',
									   'audio_level_mean', 'mas_dropouts'])

	sum_mas_max_cpu = 0
	sum_system_max_cpu = 0
	sum_mas_mean_cpu = 0
	sum_system_mean_cpu = 0
	sum_audio_level_mean = 0
	sum_mas_dropouts = 0

	with open(CSV_File, newline='') as csvfile:
		reader = DictReader(csvfile, delimiter=',', quotechar='|')
		filtered_row_counter = 0
		for row in reader:
			if (row['Device'] == device and row['Project'] == project):
				filtered_row_counter += 1
				sum_mas_max_cpu += float(row['MAS_Max_CPU'])
				sum_system_max_cpu += float(row['System_Max_CPU'])
				sum_mas_mean_cpu += float(row['MAS_Mean_CPU'])
				sum_system_mean_cpu += float(row['System_Mean_CPU'])
				sum_audio_level_mean += float(row['Audio_Level_Mean'])
				sum_mas_dropouts += int(row['MAS_Dropouts'])

	dev_arv = Device_avr(sum_mas_max_cpu / filtered_row_counter,
						 sum_system_max_cpu / filtered_row_counter,
						 sum_mas_mean_cpu / filtered_row_counter,
						 sum_system_mean_cpu / filtered_row_counter,
						 sum_audio_level_mean / filtered_row_counter,
						 sum_mas_dropouts / filtered_row_counter)


	return dev_arv

def device_cmp(device1, device2):
	"""
	Device1 and Device2 should be namedtuple returned from get_avr_by_device
	Based on: https://www.skillsyouneed.com/num/percent-change.html
	Return absolute and % diff
	"""

	ABS_diff = namedtuple('abs_diff', ['mas_max_cpu', 'system_max_cpu',
									  'mas_mean_cpu', 'system_mean_cpu',
									  'audio_level_mean', 'mas_dropouts'])

	PERC_diff = namedtuple('abs_diff', ['mas_max_cpu', 'system_max_cpu',
									  'mas_mean_cpu', 'system_mean_cpu',
									  'audio_level_mean', 'mas_dropouts'])


	# feeding absolute difference (device 1 - device 2)
	abs_diff = ABS_diff(device1.mas_max_cpu - device2.mas_max_cpu,
						device1.system_max_cpu - device2.system_max_cpu,
						device1.mas_mean_cpu - device2.mas_mean_cpu,
						device1.system_mean_cpu - device2.system_mean_cpu,
						device1.audio_level_mean - device2.audio_level_mean,
						device1.mas_dropouts - device2.mas_dropouts)


	# feeding percentual difference (device 1 - device 2)
	perc_diff = PERC_diff(_perc_calc(device1.mas_max_cpu, device2.mas_max_cpu),
						  _perc_calc(device1.system_max_cpu, device2.system_max_cpu),
						  _perc_calc(device1.mas_mean_cpu, device2.mas_mean_cpu),
						  _perc_calc(device1.system_mean_cpu, device2.system_mean_cpu),
						  _perc_calc(device1.audio_level_mean, device2.audio_level_mean),
						  _perc_calc(device1.mas_dropouts, device2.mas_dropouts))


	return abs_diff, perc_diff


#### TESTS ####
def write_avr_all():
	
	with open("avr_all.csv", 'w', newline='') as csvfile:
		fieldnames = ['Project', 'Device', 'MAS_Max_CPU', 'System_Max_CPU',
					  'MAS_Mean_CPU', 'System_Mean_CPU', 'Audio_Level_Mean',
					  'MAS_Dropouts']
		writer = DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()

		for proj in PROJECTS:
			for dev in DEVICES:
				tmp = get_avr_by_dev_and_proj(dev, proj)

				writer.writerow({'Project': proj, 'Device': dev,
								 'MAS_Max_CPU': tmp.mas_max_cpu,
								 'System_Max_CPU': tmp.system_max_cpu,
								 'MAS_Mean_CPU': tmp.mas_mean_cpu,
								 'System_Mean_CPU': tmp.system_mean_cpu,
								 'Audio_Level_Mean': tmp.audio_level_mean,
								 'MAS_Dropouts': tmp.mas_dropouts})



def write_avr_by_device():
	with open("avr_by_device.csv", 'w', newline='') as csvfile:
		fieldnames = ['Device', 'MAS_Max_CPU', 'System_Max_CPU',
					  'MAS_Mean_CPU', 'System_Mean_CPU', 'Audio_Level_Mean',
					  'MAS_Dropouts']
		writer = DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		
		for device in DEVICES:
			tmp = get_avr_by_device(device)
			writer.writerow({'Device': device,
							 'MAS_Max_CPU': tmp.mas_max_cpu,
							 'System_Max_CPU': tmp.system_max_cpu,
							 'MAS_Mean_CPU': tmp.mas_mean_cpu,
							 'System_Mean_CPU': tmp.system_mean_cpu,
							 'Audio_Level_Mean': tmp.audio_level_mean,
							 'MAS_Dropouts': tmp.mas_dropouts})


def print_cmp_msg(device1, device2):
	abs_diff, perc_diff = device_cmp(get_avr_by_device(device1),
									 get_avr_by_device(device2))
	

	print("Comparing '{}' against '{}'".format(device1, device2))
	print("The 'MAS Max CPU' usage for '{}' is {:.2f}% {} than for '{}'".format(device1,
		             			abs(perc_diff.mas_max_cpu),
		                        _convert_number_to_string(perc_diff.mas_max_cpu),
		                        device2))

	print("The 'System Max CPU' usage for '{}' is {:.2f}% {} than for '{}'".format(device1,
		             			abs(perc_diff.system_max_cpu),
		                        _convert_number_to_string(perc_diff.system_max_cpu),
		                        device2))


	print("The 'MAS Mean CPU' usage for '{}' is {:.2f}% '{}' than for '{}'".format(device1,
		             			abs(perc_diff.mas_mean_cpu),
		                        _convert_number_to_string(perc_diff.mas_mean_cpu),
		                        device2))

	print("The 'System Mean CPU' usage for '{}' is {:.2f}% {} than for '{}'".format(device1,
		             			abs(perc_diff.system_mean_cpu),
		                        _convert_number_to_string(perc_diff.system_mean_cpu),
		                        device2))

	print("The 'Audio Level Mean' for '{}' is {:.2f}% {} than for '{}'".format(device1,
		             			abs(perc_diff.audio_level_mean),
		                        _convert_number_to_string(perc_diff.audio_level_mean),
		                        device2))

	print("The 'MAS Dropouts' for '{}' is {:.2f}% {} than for '{}'".format(device1,
		             			abs(perc_diff.mas_dropouts),
		                        _convert_number_to_string(perc_diff.mas_dropouts),
		                        device2))

	print("INFO: lower is better\n")



write_avr_all()
write_avr_by_device()
print_cmp_msg('Q7-Pentium_N4200-4GB-AAEON (2.4 GHz) ', 'Q7-Atom_E3950-8GB-Congatec (1.6 GHz)')
print_cmp_msg('Q7-Atom_E3950-8GB-Congatec (2.0 GHz)', 'Q7-Atom_E3950-8GB-Congatec (1.6 GHz)')
print_cmp_msg('Q7-Atom_E3950-8GB-Congatec (1.6 GHz)', 'Q7-Atom_E3940-4GB-SECO (1.6 GHz)')