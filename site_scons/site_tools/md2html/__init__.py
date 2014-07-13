""" Tool to generate simple html files from markdown """

import codecs
from cStringIO import StringIO
from SCons.Action import Action


def exists(env):
	try:
		import markdown
		import jinja2
		return True
	except ImportError:
		return False

def md2html(source, dest, templateName, context):
	import markdown
	from jinja2 import Environment, FileSystemLoader
	md = markdown.Markdown(extensions=['meta'], output='html5')
	buffer = StringIO()
	md.convertFile(input=source, output=buffer)
	content = buffer.getvalue()
	buffer.close()
	jinjaEnvironment = Environment(loader=FileSystemLoader("."))
	template = jinjaEnvironment.get_template(templateName)
	newContext = dict(content_html=content, content_meta=md.Meta, **context)
	html = template.render(**newContext)
	with codecs.open(dest, "w", "utf-8") as f:
		f.write(html)



def generate(env):
	action = Action(
		lambda target, source, env: md2html(source[0].path, target[0].path, env['md2html_template'], {}),
		"Converting markdown $SOURCE to HTML")
	env['BUILDERS']['md2html'] = env.Builder(action=action, src_suffix=".md", suffix=".html")

