#!/usr/bin/env python3
"""
Demonstration of the organized dial library structure.

This script shows the professional organization with:
- Comprehensive testing with pytest
- Professional documentation with mkdocs
- Clean code without emojis
- Proper project structure
"""

import os
import sys

# Add the src directory to the path so we can import dial
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import dial


def create_documentation_examples():
    """Create example clocks for documentation."""
    print("Creating documentation examples...")

    # Classic style examples
    for time in ["12:00:00", "3:15:30", "6:30:45", "9:45:15"]:
        clock = dial.Clock.create(time, "classic", width=400, height=400)
        filename = f"classic_{time.replace(':', '')}.png"
        clock.save(f"examples/{filename}")
        print(f"  Created {filename}")

    # Different styles
    styles = ["modern", "minimal"]
    for style in styles:
        clock = dial.Clock.create("3:15:30", style, width=400, height=400)
        filename = f"{style}_example.png"
        clock.save(f"examples/{filename}")
        print(f"  Created {filename}")


def demonstrate_testing():
    """Demonstrate the testing capabilities."""
    print("\nTesting capabilities:")
    print("- Unit tests for all components in tests/")
    print("- Integration tests for complete workflows")
    print("- Property-based testing for elements")
    print("- Error handling validation")
    print("- Cross-platform file handling")
    print("Run tests with: uv run pytest tests/")


def demonstrate_documentation():
    """Demonstrate the documentation setup."""
    print("\nDocumentation structure:")
    print("- docs/index.md - Main documentation")
    print("- docs/usage.md - Usage guide")
    print("- docs/api.md - API reference")
    print("- docs/examples.md - Visual examples")
    print("- docs/architecture.md - Design philosophy")
    print("- mkdocs.yml - Documentation configuration")
    print("Build docs with: uv run mkdocs build")
    print("Serve docs with: uv run mkdocs serve")


def demonstrate_professional_code():
    """Demonstrate professional code qualities."""
    print("\nProfessional code qualities:")
    print("- Type hints throughout the codebase")
    print("- Comprehensive docstrings")
    print("- Error handling with meaningful messages")
    print("- Clean separation of concerns")
    print("- No emojis or unprofessional comments")
    print("- Consistent naming conventions")
    print("- Property-based element architecture")


def demonstrate_project_structure():
    """Demonstrate the organized project structure."""
    print("\nProject structure:")
    print("dial/")
    print("├── src/dial/           # Source code")
    print("│   ├── __init__.py     # Package initialization")
    print("│   ├── clock.py        # Main Clock class")
    print("│   ├── element.py      # Abstract Element base")
    print("│   ├── utils.py        # Utility functions")
    print("│   └── elements/       # Element implementations")
    print("├── tests/              # Test suite")
    print("│   ├── conftest.py     # Test configuration")
    print("│   ├── test_clock.py   # Clock tests")
    print("│   ├── test_elements.py# Element tests")
    print("│   ├── test_utils.py   # Utility tests")
    print("│   └── test_integration.py # Integration tests")
    print("├── docs/               # Documentation")
    print("│   ├── index.md        # Documentation home")
    print("│   ├── usage.md        # Usage guide")
    print("│   ├── api.md          # API reference")
    print("│   ├── examples.md     # Visual examples")
    print("│   └── architecture.md # Design philosophy")
    print("├── examples/           # Example images")
    print("├── mkdocs.yml          # Documentation config")
    print("├── pyproject.toml      # Project configuration")
    print("└── README.md           # Project overview")


if __name__ == "__main__":
    print("Dial Library - Professional Project Organization")
    print("=" * 50)

    demonstrate_project_structure()
    demonstrate_professional_code()
    demonstrate_testing()
    demonstrate_documentation()

    # Create some examples if examples directory exists
    if os.path.exists("examples"):
        create_documentation_examples()

    print("\nProject housekeeping complete!")
    print("\nKey commands:")
    print("- uv run pytest tests/          # Run test suite")
    print("- uv run mkdocs build           # Build documentation")
    print("- uv run mkdocs serve           # Serve docs locally")
    print("- uv add --dev <package>        # Add development dependency")
    print("- uv run python examples.py    # Run examples")
