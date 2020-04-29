import click
import yaml
import functools
import os


class Helper:

    RESUME_FILE = f'{os.path.join(os.path.dirname(__file__), "resume.yaml")}'
    PRINT_WIDTH = 2

    @staticmethod
    def load_resume():
        with open(Helper.RESUME_FILE, 'r') as file:
            data = file.read()
        return yaml.safe_load(data) if data else {}

    @staticmethod
    def deps_command(dep_map: dict):

        class DepsCommand(click.Command):
            def invoke(self, ctx):
                for dependency, dependents_tuple in dep_map.items():
                    if ctx.params[dependency] is None and ctx.params[dependents_tuple[0]] in dependents_tuple[1]:
                        raise click.ClickException(f'--{dependents_tuple[0]} option with value in [{",".join(dependents_tuple[1])}] requires --{dependency} to be set')
                super(DepsCommand, self).invoke(ctx)

        return DepsCommand

    @staticmethod
    def dict_exclude(data, *attrs):
        if isinstance(data, dict):
           return {k: v for k, v in data.items() if k not in attrs}
        elif isinstance(data, (list, tuple)):
            for x in data:
                return [Helper.dict_exclude(x, *attrs) for x in data]
        return data

    def __init__(self):
        self.resume = self.load_resume()

    def get_resource(self, *resource_seq, data=None, exclude=None):

        resources = list(filter(lambda x: x is not None, resource_seq))

        data = functools.reduce(
            lambda x, y: x.get(y),
            resources,
            data or self.resume
        )

        data =  Helper.dict_exclude(data, *(exclude or []))

        return {resources[-1]: data} if len(resources) else data

    def print_resource(self, data: dict, depth=0, prefix=''):

        def get_indent():
            indent = ' '*Helper.PRINT_WIDTH*depth
            if depth and prefix:
                indent = indent[:len(indent)-2] + f'{prefix} '
            return indent

        if isinstance(data, dict):
            for k, v in data.items():
                print(f'{get_indent()}{f"{k}: ":<{Helper.PRINT_WIDTH}}', end='')
                if isinstance(v, (tuple, list, dict)):
                    print()
                    self.print_resource(v, depth + 1)
                else:
                    print(f'{v}')
                prefix = ''

        elif isinstance(data, (tuple, list)):
            for x in data:
                self.print_resource(x, depth + 1, prefix='-')
        else:
            print(f'{get_indent()}{data:<{Helper.PRINT_WIDTH}}')


helper = Helper()


@click.group()
def mbnatafgi():
    pass


@mbnatafgi.group(help='Show info about me; the whole purpose of this CLI!')
def get():
    pass


@get.command(name='all', help='Show all info about me in one shot; in case you\'re in a hurry! ')
def _all():
    helper.print_resource(helper.get_resource())


@get.command(help='Show info about my contact; in case you want to contact me!')
@click.option('-r', '--resource', type=click.Choice(['name', 'alias', 'title', 'nationality', 'languages', 'address']))
def contact(resource):
    helper.print_resource(helper.get_resource('contact', resource))


@get.command(help='Show info about my skills; in case you\'re a tech enthusiast!')
@click.option('-r', '--resource', type=click.Choice(['languages', 'frameworks', 'databases', 'vcs', 'devops']))
def skills(resource):
    helper.print_resource(helper.get_resource('skills', resource))


@get.command(help='Show info about my education; in case you value the intellect!',
             cls=Helper.deps_command({'eid': ('resource', ['affiliation','location','start_date','end_date','degree',
                                                     'cumulative_avg','major_avg','awards','publications','coursework',
                                                     'projects', 'projects.name', 'projects.link', 'projects.stack']),
                                      'pid': ('resource', ['projects.name', 'projects.link', 'projects.stack'])}))
@click.option('-r', '--resource', type=click.Choice(['affiliation','location','start_date','end_date','degree',
                                                     'cumulative_avg','major_avg','awards','publications','coursework',
                                                     'projects', 'projects.name', 'projects.link', 'projects.stack']))
@click.option('-i', '--eid')
@click.option('-p', '--pid')
def education(resource, eid, pid):

    exclude, data = [], helper.resume

    if eid:
        data['education'] = next(filter(lambda x: x['id'] == eid, data['education']), {})

    if pid:
        data['education']['projects'] = next(filter(lambda x: x['id'] == pid, data['education']['projects']), {})
        resource = resource.split('.')
        data = helper.get_resource(*resource, data=data['education'])
    else:
        if resource is None:
            exclude += ['projects', 'coursework']
        data = helper.get_resource('education', resource, data=data, exclude=exclude)
#

    helper.print_resource(data)


@get.command(help='Show info about my experience; the typical thing!',
             cls=Helper.deps_command({'eid': ('resource', ['affiliation','location','start_date','end_date','position',
                                                     'employment', 'tasks','tasks.name','tasks.type',
                                                     'tasks.link', 'tasks.stack', 'tasks.accomplishments']),
                                      'tid': ('resource', ['tasks.name','tasks.type','tasks.link', 'tasks.stack',
                                                           'tasks.accomplishments'])}))
@click.option('-r', '--resource', type=click.Choice(['affiliation','location','start_date','end_date','position',
                                                     'employment', 'tasks','tasks.name','tasks.type',
                                                     'tasks.link', 'tasks.stack', 'tasks.accomplishments']))
@click.option('-i', '--eid')
@click.option('-t', '--tid')
def experience(resource, eid, tid):

    exclude, data = [], helper.resume

    if eid:
        data['experience'] = next(filter(lambda x: x['id'] == eid, data['experience']), {})

    if tid:
        data['experience']['tasks'] = next(filter(lambda x: x['id'] == tid, data['experience']['tasks']), {})
        resource = resource.split('.')
        exclude += ['accomplishments']
        data = helper.get_resource(*resource, data=data['experience'], exclude=exclude)
    else:
        if resource is None:
            exclude.append('tasks')
        exclude.append('accomplishments')
        data = helper.get_resource('experience', resource, data=data, exclude=exclude)#

    helper.print_resource(data)


if __name__ == '__main__':
    mbnatafgi()
