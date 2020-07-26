import os
import ast

import click
import pandas as pd


def replace_init(result, string):
    if string in result:
        result.remove(string)
        if '__init__' not in result:
            result.append('__init__')

    return result


def get_imports(file_, package_name):
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

    # TODO: auto find assignments in __init__.py
    result = replace_init(result, 'TERM')
    result = replace_init(result, 'KONEKODIR')
    result = replace_init(result, '__version__')
    result = replace_init(result, 'FakeData')
    return result


def get_all_imports(package_path, package_name):
    files = [f for f in os.listdir(package_path)
            if os.path.isfile(f'{package_path}/{f}')]

    return {
        f: get_imports(f'{package_path}/{f}', package_name)
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
    df['Proportion'] = df.Dependents / abs(df.Dependents + df.Dependencies) * 100

    df.sort_values('Proportion', inplace=True, ascending=False)

    print(df.round(0).to_markdown())
    return df


@click.command()
@click.option('-p', '--package-path')
@click.option('-n', '--package-name')
def main(package_path, package_name):
    all_imports = get_all_imports(package_path, package_name)

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
