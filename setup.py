import setuptools

setuptools.setup(
    name="FuPlot",
    version="0.1",
    description="Framework for creating animatable data visualizations from tabular data for DaVinci Resolve Fusion.",
    url="https://github.com/brunocbreis/FuPlot",
    author="Bruno Reis",
    install_requires=[
        "pysion @ git+https://github.com/brunocbreis/pysion#egg=pysion",
        "pandas",
        "pyperclip",
    ],
    author_email="brunocbreis@gmail.com",
    packages=setuptools.find_packages(),
    zip_safe=False,
)
