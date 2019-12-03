import os
import re
import sys
from itertools import count

import git
from jinja2 import Template
from pip._internal.req.req_file import preprocess


def git_root():
    root, = os.popen('git rev-parse --show-toplevel')
    return root.strip()


def get_last_changed(fname: str):
    repo = git.Repo(git_root())
    blame = repo.blame('HEAD', os.path.abspath(fname))
    counter = count(1)
    line_dt = {lineno: (commit.authored_datetime, line) for commit, block in blame for line, lineno in zip(block, counter)}

    def key(req_line_no: int):
        return line_dt[req_line_no]

    return key


def get_cogent_lines(reqfile_contents: str):  # TODO - USEME
    """Get cogent requirements lines, suitable for prepending with generic install directive."""
    for lineno, line in preprocess(reqfile_contents, options=None):
        yield lineno, re.sub(r'\s+', ' ', line)


def read_requirements(fname: str):
    with open(fname) as f:
        req_lines = filter(None, f.read().splitlines())  # todo also need to filter out comments etc. but whatever
    return sorted(req_lines, key=get_last_changed(fname))


ADD_REQUIREMENTS_MACRO = """
{%- macro add_requirements(fname) -%}
# Requirements populated from {{fname}}
{% for requirement in read_requirements(fname) -%}
RUN pip install {{ requirement }}
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

