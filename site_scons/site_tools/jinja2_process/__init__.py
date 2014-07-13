""" Tool to generate files from jinja2 templates """

import codecs
from SCons.Action import Action

def exists(env):
	try:
		import jinja2
		return True
	except ImportError:
		return False

def process(source, dest, context):
	from jinja2 import Environment, Template, FileSystemLoader
	environment = Environment(loader=FileSystemLoader("."))
	template = environment.get_template(source)
	with codecs.open(dest, "w", "utf-8") as f:
		for token in template.generate(context):
			f.write(token)

def generate(env):
	env.SetDefault(jinja2_context={})
	action = Action(
		lambda target, source, env: process(source[0].path, target[0].path, env['jinja2_context']),
		"Generating $TARGET from template ${SOURCE}.")
	env['BUILDERS']['jinja2Process'] = env.Builder(action=action,
		src_sufix=".j2",
	sufix="")

