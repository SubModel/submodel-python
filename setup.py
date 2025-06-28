"""
submodel-python | setup.py
Called to setup the submodel-python package.
"""

from setuptools import find_packages, setup

# README.md > long_description
with open("README.md", encoding="utf-8") as long_description_file:
    long_description = long_description_file.read()

# requirements.txt > requirements
with open("requirements.txt", encoding="UTF-8") as requirements_file:
    install_requires = requirements_file.read().splitlines()

extras_require = {
    "test": [
        "asynctest",
        "faker",
        "nest_asyncio",
        "pytest",
        "pytest-cov",
        "pytest-timeout",
        "pytest-asyncio",
    ]
}

if __name__ == "__main__":

    setup(
        name="submodel",
        use_scm_version=True,
        setup_requires=["setuptools>=45", "setuptools_scm", "wheel"],
        install_requires=install_requires,
        extras_require=extras_require,
        packages=find_packages(),
        python_requires=">=3.8",
        description="Python library for Submodel API and serverless worker SDK.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Submodel",
        author_email="product@submodel.ai",
        url="https://submodel.ai",
        project_urls={
            "Documentation": "https://submodel.gitbook.io/",
            "Source": "https://github.com/submodel/submodel-python",
            "Bug Tracker": "https://github.com/submodel/submodel-python/issues",
            "Changelog": "https://github.com/submodel/submodel-python/blob/main/CHANGELOG.md",
        },
        classifiers=[
            "Environment :: Web Environment",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        ],
        include_package_data=True,
        entry_points={"console_scripts": ["submodel = submodel.cli.entry:submodel_cli"]},
        keywords=[
            "submodel",
            "ai",
            "gpu",
            "serverless",
            "SDK",
            "API",
            "python",
            "library",
        ],
        license="MIT",
    )
