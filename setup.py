from setuptools import setup, find_packages

setup(
    name="genetic_scheduler",
    version="1.0.0",
    description="Doctoral-level Genetic Algorithm Framework for Train Scheduling Optimization",
    author="Victor Medina",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "numpy",
        "matplotlib",
        "deap",
        "pandas",
        "seaborn",
        "tqdm",
        "scipy",
        "networkx"  # For graph-based analysis if needed
    ],
    python_requires=">=3.8",
)
