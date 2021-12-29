import os
import pathlib
import shutil
import yaml
from tools.apispec.plugin import ApiDocsGenerator

from aiohttp.web import Application

from src.service.routes import setup_routes


if __name__ == '__main__':
    project_root = pathlib.Path('..') / '..'
    config = yaml.safe_load((project_root / 'src' / 'config.yml').read_text())

    application_version = config['service']['version']
    spec_path: pathlib.Path = project_root / 'public' / 'docs' / f'v{application_version}'

    #if os.path.exists(spec_path):
    #    raise FileExistsError('Данная версия АПИ уже существует')

    app = Application()
    app['static_dir'] = 'app/static'
    setup_routes(app)

    service_name = config['service']['name']
    OPENAPI_SPEC = f"""
        openapi: 3.0.2
        info:
          description: {service_name} service API
          title: {service_name} service API

          version: {application_version}
        servers:
        - url: http://localhost:{config['service']['port']}/
          description: The local API server
        """

    docs_generator = ApiDocsGenerator(app, openapi_base=OPENAPI_SPEC)

    yaml_spec = docs_generator.generate()
    spec_path.mkdir(parents=True, exist_ok=True)
    with (spec_path / 'api_config.yaml').open('w', encoding='utf-8') as api_file:
        api_file.write(yaml_spec)
    shutil.copyfile(
        project_root / 'tools' / 'apispec' / 'api_view.html', spec_path / 'api_view.html',
    )
