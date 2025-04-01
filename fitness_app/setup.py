from setuptools import setup, find_packages
 
setup(
    name='fitness_app',
    version='0.1',
    packages=find_packages(include=['aws_services']),
    install_requires=[
        'boto3',  # Add other dependencies if needed
    ],
)
