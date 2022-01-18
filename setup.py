from distutils.core import setup

setup(
    name="tdw",
    version="1.0",
    packages=[
        "tdw",
        "tdw.graph",
    ],
    package_dir={
        "tdw": "src",
        "tdw.graph": "src/graph",
    },
    requires=["networkx", "Fiona", "matplotlib"],
)