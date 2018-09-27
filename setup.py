
from setuptools import setup

DEPENDENCIES = [
    "termcolor==1.1.0",
    "ipaddress==1.0.22",
    "ujson==1.35",
    "pyzmq==17.1.2",
    "redis==2.10.6",
    "tornado==5.0.1",
    "pycryptodome==3.6.6",
    "mysql-connector-python==8.0.12",
    "GitPython==2.1.7",
    "tormysql==0.3.7",
    "Sphinx==1.6.3",
    "pyOpenSSL==17.2.0",
    "cffi==1.10.0",
    "cryptography==2.3.1",
    "futures==3.1.1",
    "expiringdict==1.1.4",
    "python-geoip-python3==1.3",
    "python-geoip-geolite2-yplan==2017.608",
    "psutil==5.2.2",
    "lazy==1.3",
    "pympler==0.5",
    "sprockets-influxdb==2.1.0",
    "aioredis==1.1.0",
    "pika==0.12.0",
    "PyMySQL==0.8.0",
    "PyJWT==1.6.1"
]

REPOS = [
    "http://github.com/anthill-utils/PyMySQL/tarball/master#egg=PyMySQL-0.8.0",
    "http://github.com/anthill-utils/pyjwt/tarball/master#egg=PyJWT-1.6.1"
]

setup(
    name='anthill-common',
    version='0.1.0',
    description='Common utils for Anthill platform',
    author='desertkun',
    license='MIT',
    author_email='desertkun@gmail.com',
    url='https://github.com/anthill-platform/anthill-common',
    namespace_packages=["anthill"],
    packages=["anthill.common"],
    zip_safe=False,
    install_requires=DEPENDENCIES,
    dependency_links=REPOS
)