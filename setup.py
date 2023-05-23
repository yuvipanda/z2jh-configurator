from setuptools import setup, find_packages

setup(
    name="z2jh-configurator",
    version="1.0",
    packages=find_packages(),
    license="3-BSD",
    author="yuvipanda",
    author_email="yuvipanda@gmail.com",
    install_requires=[
        "jupyterhub",
        "django",
        "social-auth-core",
        "social-auth-app-django",
    ],
    include_package_data=True,
)
