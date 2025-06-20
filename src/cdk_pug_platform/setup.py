from setuptools import setup, find_packages

setup(
    name="cdk_pug_platform",
    version="1.0.0",
    author="CESAR MORALES",
    author_email="me@cesarmoralesonya.es",
    description="AWS CDK application for the PUG Platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/morales-corp/cdk-pug-platform",
    packages=find_packages(),
    install_requires=[
        "aws-cdk>=2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
