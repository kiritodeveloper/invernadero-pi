from setuptools import find_packages, setup

setup(
    name='piinvernalio',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask','sqlite3','apscheduler',
    ],
)

