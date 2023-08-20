from setuptools import setup, find_packages

setup(
    name='commafixer',
    version='0.1.0',
    description='Fixing commas using Deep Learning.',
    author='Karol Lasocki',
    author_email='karolasocki@gmail.com',
    url='https://huggingface.co/spaces/klasocki/comma-fixer',
    packages=find_packages(include=['commafixer', 'commafixer.*']),
    install_requires=[
        "fastapi == 0.101.1",
        "uvicorn == 0.23.2",
        "torch == 2.0.1",
        "transformers == 4.31.0",
        # for the tokenizer of the baseline model
        "protobuf == 4.24.0",
        "sentencepiece == 0.1.99",

    ],
    extras_require={
        'training': [
            'datasets==2.14.4',
            'notebook'
        ],
        'test': [
            'pytest',
            'httpx'
        ]
    },
)
