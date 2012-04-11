'''
	Some utility functions to help algorithm runs, etc.
'''
import os
import string
import random
import logging

from Stemweb.algorithms.models import Algorithm
from forms import field_types
from Stemweb import settings
from Stemweb.files.models import InputFile

from django.template.defaultfilters import slugify

def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
	''' Semiunique ID generator -- copypaste code.

		Source:	http://stackoverflow.com/questions/2257441/python-random-string-generation-with-upper-case-letters-and-digits

		size:	length of the random string. Default 8.
		chars:	set of chars from which the string is created

		Returns random string.
	'''
	return ''.join(random.choice(chars) for x in range(size))


def build_run_folder(user, input_file_id, algorithm_name):  
	''' Builds unique path for run's result folder.

		runfile:	 Absolute path to file to use as input_file for a run.
		run_id:		 ID of the R_runs db-table's entry

		Returns path to run's storage folder if it has been succesfully created. 
		Otherwise returns -1
	'''
	uppath = os.path.join('users')
	uppath = os.path.join(uppath, user.username)
	uppath = os.path.join(uppath, 'runs')
	uppath = os.path.join(uppath, slugify(algorithm_name))    # Refactor with actual script's name
	uppath = os.path.join(uppath, '%s' % input_file_id)
	uppath = os.path.join(uppath, id_generator())
	return uppath


def build_args(form = None, algorithm_id = None, request = None):
	''' Generate dynamic running args from given form.
		
		Returns dictionary with running arguments. If form has id of InputFile 
		model instance which is not owned by request.user returns None.
	'''
	run_args = {}
	for key in form.cleaned_data.keys():
		if type(form.fields[key]) == type(field_types['input_file']):
			'''
				Some how the input files get "corrupted" in cleaned data and 
				show the text that was visible to user, not the id it should.
				
				TODO: fix this!
			'''
			input_file = InputFile.objects.get(id = form.data[key])	
			if input_file.user != request.user:
				logger = logging.getLogger('stemweb.algorithm_run')
				logger.warning("Could not build args for AlgorithmRun because request.user %s was not InputFile.user %s" % (request.user, input_file.user))
				return None
			run_args[key] = input_file.path
			run_args['%s_id' % (key)] = input_file.id
			run_args['file_id'] = input_file.id	# TODO: Hack, use upper line.
			input_file.save() # Save it to change last_access
		else:
			run_args[key] = form.cleaned_data[key]
	
	''' Build run folder based on input file's id and algorithm's name. '''		
	run_folder = build_run_folder(request.user, run_args['file_id'], Algorithm.objects.get(pk = algorithm_id).name)
	abs_folder = os.path.join(settings.MEDIA_ROOT, run_folder) 
	try: os.makedirs(abs_folder)
	except: print "noononnono"
	run_args['url_base'] = run_folder	# TODO: Hack, fix this
	run_args['outfolder']  = abs_folder
	return run_args
			