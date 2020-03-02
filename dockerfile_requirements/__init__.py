import os
import sys
import datetime

import git
from jinja2 import Template


def git_root():
    root, = os.popen('git rev-parse --show-toplevel')
    return root.strip()


def get_last_changed(fname):
    repo = git.Repo(git_root())
    blame = repo.blame('HEAD', os.path.abspath(fname))
    line_dt = {line: commit.authored_datetime for commit, block in blame for line in block}
    def key(reqline):
        last_modified = line_dt.get(reqline, datetime.datetime.now(datetime.timezone.utc))
        return last_modified, reqline
    return key


def read_requirements(fname):
    with open(fname) as f:
        req_lines = filter(None, f.read().splitlines())  # todo also need to filter out comments etc. but whatever
    return sorted(req_lines, key=get_last_changed(fname))


ADD_REQUIREMENTS_MACRO = """
{%- macro add_requirements(fname, args="") -%}
# Requirements populated from {{fname}}
{% for requirement in read_requirements(fname) -%}
RUN pip install {{ args }} "{{ requirement }}" 
{% endfor -%}
{%- endmacro -%}
"""


def main(dockerfile_fname=None):
    if dockerfile_fname is None:
        dockerfile_fname = sys.argv[1]
    with open(dockerfile_fname, 'r') as f:
        template = Template('\n'.join((ADD_REQUIREMENTS_MACRO, f.read())))
    print(template.render(read_requirements=read_requirements))


if __name__ == '__main__':
    main(sys.argv[1])

