import sys
sys.path.insert(0, 'reportlab.zip')
sys.path.insert(0, '.')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import traceback
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.runtime import DeadlineExceededError

import substratestack

from StringIO import StringIO
from fakefile import FakeFile

# overrive open in substratestack
substratestack.open = FakeFile


# load sample substrate definition
sample_path = os.path.join(os.path.dirname(__file__), 'sample.py')

template_values = {
    'script': open(sample_path).read(),
    'ss_version': substratestack.__version__
}

tmpl_path = os.path.join(os.path.dirname(__file__), 'index.html')
index_html = template.render(tmpl_path, template_values, debug=True)


class MainPage(webapp.RequestHandler):
    def get(self):
        try:
            self.response.out.write(index_html)
        except DeadlineExceededError:
            self.response.clear()
            self.response.set_status(500)
            self.response.out.write("This operation could not be completed in time...")
        except:
            self.response.out.write(traceback.format_exc())


class RunScript(webapp.RequestHandler):
    def post(self):
        script = self.request.get('script')
        download = self.request.get('download')

        # submitting the script through form/POST has \r\n line endings, causing
        # trouble
        script = script.replace('\r\n', '\n')

        FakeFile.clear()
        # stolen from google-app-engine-samples/shell
        try:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            try:
                if download:
                    output = StringIO()
                else:
                    output = self.response.out
                sys.stdout = output
                sys.stderr = output
                exec script
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr
            null = StringIO()
        except DeadlineExceededError:
            self.response.clear()
            self.response.set_status(500)
            self.response.out.write("This operation could not be completed in time...")
        except:
            self.response.out.write(traceback.format_exc())
            return
        if download:
            self.response.clear()
            self.response.headers['Content-Type'] = 'application/zip'
            self.response.headers['Content-Disposition'] = 'attachment;filename="sstack.zip"'
            self.response.out.write(FakeFile.zip().getvalue())       


def main():
    application = webapp.WSGIApplication([('/', MainPage), ('/run', RunScript)], debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

