import setuptools
import sys


REQUIREMENTS = [
    "nose>=1.3,<1.4",
    "slackbot>=0.4,<0.5"
]


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "requirements":
        for req in REQUIREMENTS:
            print(req)
        sys.exit(0)

    setuptools.setup(
        name="countdown-slackbot",
        version="0.0.2",
        author="Sujay Mansingh",
        author_email="sujay.mansingh@gmail.com",
        packages=setuptools.find_packages(),
        scripts=[],
        url="https://github.com/sujaymansingh/countdown-slackbot",
        license="LICENSE.txt",
        description="A slackbot that plays countdown",
        long_description="View the url for more details.",
        install_requires=REQUIREMENTS
    )
