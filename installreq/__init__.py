import os

package_path = os.path.dirname(os.path.abspath(__file__))
requirements_path = os.path.join(package_path, 'requirements.txt')
print(f"The importing file path: {requirements_path}")