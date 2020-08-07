import os
import ast
from pathlib import Path

import click
import pandas as pd


def get_assignments_from_init(path):
    with open(path, 'r') as f:
        return get_assignments(f.read())


def get_assignments(source):
    parsed = ast.parse(source)
    assigments = [x for x in parsed.body
                  if type(x) is ast.Assign
                  if x.col_offset == 0]

    return [a.targets[0].id
            for a in assigments]


def replace_init(result, string):
    if string in result:
        result.remove(string)
        if '__init__' not in result:
            result.append('__init__')

    return result


def get_imports(file_, package_name, assigments):
    with open(file_, 'r') as f:
        source = f.read()

    parsed = ast.parse(source)
    # ast.Import excluded as its not local
    imports = [x for x in parsed.body
               if type(x) is ast.ImportFrom]

    result = [
        name.name
        for item in imports
        for name in item.names
        if item.module == package_name
    ]

    for a in assigments:
        result = replace_init(result, a)

    return result


def get_all_imports(package_path, package_name, assigments):
    files = [f for f in os.listdir(package_path)
            if os.path.isfile(f'{package_path}/{f}')]

    return {
        f: get_imports(f'{package_path}/{f}', package_name, assigments)
        for f in files
    }


def number_of_dependents(file_, all_imports):
    return len([item
        for module, imports in all_imports.items()
            if module != file_
                for item in imports
                    if file_.replace('.py', '') in item
    ])


def generate_df(dependents, dependencies):
    df = pd.DataFrame.from_dict(dependents, orient='index', columns=['Dependents'])
    df['Dependencies'] = dependencies.values()
    df['Score'] = df.Dependents - df.Dependencies
    df['Proportion'] = df.Dependents / (df.Dependents + df.Dependencies) * 100

    df.sort_values('Proportion', inplace=True, ascending=False)

    print(df.round(0).to_markdown())
    return df


@click.command()
@click.option('-p', '--package-path', type=Path)
@click.option('-n', '--package-name')
@click.option('-i', '--init_file', default='__init__.py')
def main(package_path, package_name, init_file):
    if init_file:
        assigments = get_assignments_from_init(package_path / init_file)
    else:
        assigments = []

    all_imports = get_all_imports(package_path, package_name, assigments)

    dependencies = {
        module: len(imports)
        for module, imports in all_imports.items()
    }

    dependents = {
        module: number_of_dependents(module, all_imports)
        for module in all_imports.keys()
    }

    generate_df(dependents, dependencies)


if __name__ == '__main__':
    main()
