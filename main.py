"""Installs all the dependencies to run a file (Runs automatically)"""
import argparse
import logging
import sys
import os
import subprocess
import types
import pkg_resources


class InstallRequirements:
    """Main InstallRequirements class"""
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
        parser = argparse.ArgumentParser(
            description='Install requirements of a file.',
            usage='python main.py <file_to_run>'
        )
        parser.add_argument('file_to_run', help='The file you want to run')
        args = parser.parse_args(sys.argv[1:])
        self.file_to_run = args.file_to_run

    def get_pypi_package_name(self, module_name):
        """Get distribution name of the package"""
        if module_name == 'PIL':
            return 'Pillow'
        try:
            distribution = pkg_resources.get_distribution(module_name)
            return distribution.key
        except pkg_resources.DistributionNotFound:
            return None

    def find_modules(self):
        """Find all the modules of the file"""
        try:
            logging.info('Searching for dependencies...')
            modules = []
            with open(self.file_to_run, 'r', encoding='utf-8') as _file:
                lines = _file.readlines()
                for line in lines:
                    if line.startswith('from') or line.startswith('import'):
                        module = line.split()[1]
                        if '.' in module:
                            continue
                        if (module in sys.modules and
                                    isinstance(sys.modules[module], types.ModuleType)):
                            continue
                        if module in sys.stdlib_module_names:
                            continue
                        modules.append(line.split()[1])
                        logging.info('Found module: %s', module)
            return modules
        except FileNotFoundError:
            print('File not found. Try again.')
            return None

    def install_modules(self):
        """Install all modules"""
        try:
            requirements_path = os.path.join(os.path.dirname(self.file_to_run), 'requirements.txt')
            if os.path.isfile(requirements_path):
                subprocess.call([sys.executable, "-m", "pip", "install", '-r', requirements_path])

            modules = self.find_modules()
            for module in modules:
                try:
                    name = self.get_pypi_package_name(module)
                    subprocess.call([sys.executable, '-m', 'pip', 'install', '--upgrade', name])
                except ModuleNotFoundError as error:
                    logging.error('Error while installing module "%s: %s', module, error)
        except FileNotFoundError as error:
            logging.error('Exception while installing dependencies: %s', error)

    def main(self):
        """Main entry point"""
        try:
            self.install_modules()
            os.system('python %s', self.file_to_run)
        except KeyboardInterrupt:
            logging.info('Stopped correctly')
        except Exception as error:
            logging.exception('Exception: %s', error)

if __name__ == '__main__':
    i = InstallRequirements()
    i.main()
