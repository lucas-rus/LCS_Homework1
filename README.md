# Logic Formula Parser

A Python tool for parsing and validating logical formulas using propositional logic operators. This parser helps determine if a given formula is well-formed and shows the step-by-step analysis of the formula's structure.

## Features

- Validates logical formulas
- Provides step-by-step analysis
- Supports multiple logical operators
- Handles nested expressions
- Shows substitution steps

## Prerequisites

- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

## Installation

1. Clone this repository or download the `logic_parser.py` file:
```bash
git clone https://your-repository-url.git
# or
curl -O your-raw-file-url/logic_parser.py
```

2. Place the file in your desired working directory.

## Supported Logical Operators

The parser supports the following logical operators:

- `⇔` : Equivalence (can be copied from a text editor)
- `⇒` : Implication (can be copied from a text editor)
- `∨` : Disjunction (OR)
- `∧` : Conjunction (AND)
- `¬` : Negation (NOT)

## Usage

### Basic Usage

1. Create a Python script or use an interactive Python shell
2. Import and create an instance of the LogicParser:

```python
from logic_parser import LogicParser

parser = LogicParser()
```

3. Solve a single formula:

```python
formula = "(P ∧ Q)"
result = parser.solve_formula(formula)
print(result)
```

### Adding Multiple Formulas

To analyze multiple formulas, you can create a list of formulas and iterate through them:

```python
formulas = [
    "(P ∧ Q)",
    "(P ⇒ Q)",
    "(¬P ∨ Q)"
]

for i, formula in enumerate(formulas, 1):
    print(f"\nProblem {i}: {formula}")
    print(parser.solve_formula(formula))
    print("-" * 75)
```

### Formula Writing Guidelines

When writing formulas, follow these rules:

1. Enclose binary operations in parentheses: `(P ∧ Q)`
2. Spaces between symbols are optional
3. Atomic propositions should be single letters (A-Z), optionally followed by numbers
4. Negations should be properly enclosed: `(¬P)` or `(¬(P ∧ Q))`

Valid examples:
```python
formulas = [
    "(P ∧ Q)",                    # Simple conjunction
    "((P ⇒ Q) ∨ R)",             # Nested operations
    "(¬(P ∧ Q))",                # Negation of conjunction
    "(P1 ⇔ (Q2 ∧ R3))",         # Using numbered propositions
    "(((P ⇒ Q) ∨ S) ⇔ T)"       # Complex nested formula
]
```

Invalid examples:
```python
formulas = [
    "P ∧ Q",       # Missing outer parentheses
    "(P)",         # Single proposition in parentheses
    "¬P",          # Negation without parentheses
    "((P ∧ Q)",    # Unbalanced parentheses
]
```

## Input Methods for Special Operators

Since logical operators are special characters, here are different ways to input them:

1. Copy and paste from this README
2. Use a text editor with symbol support
3. Create variables with the symbols and use string formatting:
```python
operators = {
    'equiv': '⇔',
    'implies': '⇒',
    'or': '∨',
    'and': '∧',
    'not': '¬'
}

formula = f"({operators['not']}P {operators['and']} Q)"
```

## Common Issues and Solutions

1. **Parentheses Errors**
   - Ensure each opening parenthesis has a matching closing one
   - Every binary operation should be enclosed in parentheses

2. **Operator Formatting**
   - Make sure to use the correct Unicode characters for operators
   - Don't use ASCII alternatives (like '->' for implication)

3. **Atomic Propositions**
   - Use only single letters (A-Z) optionally followed by numbers
   - Don't use lowercase letters or special characters

## Output Interpretation

The parser output includes:
1. Initial formula analysis
2. Identification of atomic propositions
3. Step-by-step substitutions
4. Final validation result
5. Reverse substitution steps

Example output:
```
Analyzing formula: (P ∧ Q)

P - atomic => P belongs to P(v)
Q - atomic => Q belongs to P(v)

Begin substitutions:
Current formula: (P ∧ Q)
Found principal operation (P ∧ Q)
P, Q belong to P(v) => (P∧Q) belongs to P(v)
not. (P∧Q) := X1 => X1 belongs to P(v)

Final result: X1
Reverse substitution:
X1 = (P∧Q)

Therefore, this is a well-formed formula.
```

## Contributing

Feel free to submit issues and enhancement requests!

