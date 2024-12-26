# Contributing to EG4 Monitor Integration

First off, thank you for considering contributing to the EG4 Monitor Integration! It's people like you that make this integration better for everyone.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check [existing issues](https://github.com/ZoarTech/EG4_HA_Inverter/issues) as you might find that you don't need to create one. When you create a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps to reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include logs from Home Assistant
* Include screenshots if relevant

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* A clear and descriptive title
* A detailed description of the proposed feature
* Explain why this enhancement would be useful
* List any similar features in other integrations
* Include mockups or examples if applicable

### Pull Requests

* Fill in the required template
* Follow the Python style guide (flake8, black)
* Include appropriate tests
* Update documentation for any new features
* End files with a newline
* Follow the commit message guidelines

## Development Process

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Write or update tests
5. Update documentation
6. Submit a pull request

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/your-username/EG4_HA_Inverter.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_dev.txt
```

### Running Tests

```bash
pytest
```

### Code Style

We use:
* [black](https://github.com/psf/black) for code formatting
* [flake8](https://flake8.pycqa.org/) for style guide enforcement
* [isort](https://pycqa.github.io/isort/) for import sorting

Run code style checks:
```bash
black .
flake8 .
isort .
```

## Documentation

* Update README.md if needed
* Update documentation in /docs
* Include docstrings for new functions
* Update configuration examples if needed

## Community

* Be welcoming and inclusive
* Respect different viewpoints and experiences
* Accept constructive criticism
* Focus on what's best for the community
* Show empathy towards other community members

## Questions?

Feel free to create an issue tagged as 'question' if you need help or clarification.
