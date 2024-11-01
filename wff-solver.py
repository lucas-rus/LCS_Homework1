class LogicParser:
    def __init__(self):
        # Dictionary of logical operators we'll work with
        self.operators = {
            '⇔': 'equivalence',
            '⇒': 'implication',
            '∨': 'disjunction',
            '∧': 'conjunction',
            '¬': 'negation'
        }
        # Counter for creating new substitution variables (X1, X2, etc.)
        self.atomic_counter = 0
        # List to store each step of the solution
        self.steps = []
        # Dictionary to remember what each substitution represents
        self.substitutions = {}
        # List to store steps in reverse order for showing our work
        self.reverse_steps = []

    def is_atomic(self, formula):
        # Checks if something is a basic formula (like P or P1)
        if not formula:
            return False
        if len(formula) == 1:
            return formula.isalpha()
        return (formula[0].isalpha() and formula[1:].isdigit())

    def check_parentheses(self, formula):
        # Makes sure parentheses are balanced (every open has a close)
        count = 0
        for char in formula:
            if char == '(':
                count += 1
            elif char == ')':
                count -= 1
            if count < 0:  # Found a close before an open
                return False
        return count == 0  # Should be zero if balanced

    def find_subformula_end(self, formula, start):
        # Given a starting parenthesis, finds its matching closing one
        count = 1
        for i in range(start + 1, len(formula)):
            if formula[i] == '(':
                count += 1
            elif formula[i] == ')':
                count -= 1
                if count == 0:  # Found the matching close
                    return i
        return -1

    def is_valid_negation(self, formula):
        # Checks if a negation is properly formed (like (¬P) or (¬(P∧Q)))
        if formula.startswith('(') and formula.endswith(')'):
            inner = formula[1:-1]
            if inner.startswith('¬'):
                after_neg = inner[1:]
                if self.is_atomic(after_neg):  # Can negate atomic formula
                    return True
                if after_neg.startswith('('):  # Can negate compound formula
                    inner_of_neg = after_neg[1:-1] if after_neg.endswith(')') else after_neg
                    if self.is_atomic(inner_of_neg):  # But not atomic in parentheses
                        return False
                    return True
                return False
        return True

    def is_basic_compound(self, formula):
        # Checks if we have a simple formula with two parts and one operator
        # Like (P∧Q) or (X1∨R), but not ((P∧Q)∨R)
        if not (formula.startswith('(') and formula.endswith(')')):
            return False

        inner = formula[1:-1]
        if inner.startswith('¬'):  # Handle negations separately
            after_neg = inner[1:]
            return self.is_atomic(after_neg) or after_neg in self.substitutions

        parts = []
        paren_count = 0
        current = ''
        operator = None

        # Split the formula into parts around the operator
        for char in inner:
            if char == '(':
                paren_count += 1
                current += char
            elif char == ')':
                paren_count -= 1
                current += char
            elif char in self.operators and paren_count == 0:
                if operator is None:
                    operator = char
                    if current:
                        parts.append(current)
                    current = ''
                else:
                    return False  # Found multiple operators at same level
            else:
                current += char

        if current:
            parts.append(current)

        # Must have exactly two parts and one operator between them
        if len(parts) != 2 or operator is None:
            return False

        # Both parts must be atomic formulas or previous substitutions
        return all(self.is_atomic(p) or p in self.substitutions for p in parts)

    def find_first_basic_compound(self, formula):
        # Finds the first simple compound formula at the deepest level
        # Ex: in ((P∧Q)∨R), it would find (P∧Q) first
        max_level = 0
        compound_start = -1
        compound_end = -1
        current_level = 0

        for i, char in enumerate(formula):
            if char == '(':
                current_level += 1
                if current_level >= max_level:
                    potential_end = self.find_subformula_end(formula, i)
                    if potential_end != -1:
                        potential_compound = formula[i:potential_end + 1]
                        if self.is_basic_compound(potential_compound):
                            max_level = current_level
                            compound_start = i
                            compound_end = potential_end + 1
            elif char == ')':
                current_level -= 1

        if compound_start != -1 and compound_end != -1:
            return compound_start, compound_end, formula[compound_start:compound_end]
        return None, None, None

    def extract_components(self, formula):
        # Takes a formula apart into its operator and operands
        # Ex: (P∧Q) becomes '∧', 'P', 'Q'
        inner = formula[1:-1]

        if self.is_atomic(inner):
            return None, None, None

        if inner.startswith('¬'):
            if not self.is_valid_negation(formula):
                return None, None, None
            return '¬', None, inner[1:]

        paren_count = 0
        for i, char in enumerate(inner):
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            elif paren_count == 0 and char in self.operators:
                return char, inner[:i], inner[i + 1:]

        return None, None, None

    def generate_new_atomic(self):
        # Creates new substitution variables X1, X2, etc.
        self.atomic_counter += 1
        return f"X{self.atomic_counter}"

    def solve_formula(self, original_formula):
        # Main method that solves the formula step by step
        formula = original_formula.replace(" ", "")
        self.steps = []
        self.reverse_steps = []
        self.atomic_counter = 0
        self.substitutions = {}
        self.steps.append(f"Analyzing formula: {formula}\n")

        atomic_vars = set()
        current_formula = formula

        # Check if it's already just an atomic formula
        if self.is_atomic(current_formula):
            self.steps.append(f"{current_formula} - atomic => {current_formula} belongs to P(v)")
            self.steps.append(f"\nTherefore, this is a well-formed formula.")
            return "\n".join(self.steps)

        # Check if it's just an atomic formula in parentheses (invalid)
        if formula.startswith('(') and formula.endswith(')'):
            inner = formula[1:-1]
            if self.is_atomic(inner):
                self.steps.append(f"Error: Atomic formula {inner} should not be surrounded by parentheses")
                self.steps.append("\nNot a valid formula in P(v)")
                return "\n".join(self.steps)

        # First identify all atomic formulas in the expression
        i = 0
        while i < len(formula):
            if i < len(formula) and formula[i].isalpha():
                j = i + 1
                while j < len(formula) and formula[j].isdigit():
                    j += 1
                potential_atomic = formula[i:j]
                if self.is_atomic(potential_atomic) and potential_atomic not in atomic_vars:
                    atomic_vars.add(potential_atomic)
                    self.steps.append(f"{potential_atomic} - atomic => {potential_atomic} belongs to P(v)")
                i = j
            else:
                i += 1

        self.steps.append("\nBegin substitutions:")

        # Main processing loop
        while True:
            if self.is_atomic(current_formula):
                break

            self.steps.append(f"\nCurrent formula: {current_formula}")

            # Find next compound formula to process
            start, end, compound = self.find_first_basic_compound(current_formula)
            if compound is None:
                self.steps.append("Error: No valid basic compound formula found")
                self.steps.append("\nNot a valid formula in P(v)")
                return "\n".join(self.steps)

            self.steps.append(f"Found principal operation {compound}")

            # Extract the parts of the compound formula
            op, left, right = self.extract_components(compound)

            if op is None:
                self.steps.append(f"Error: Invalid formula format in {compound}")
                self.steps.append("\nNot a valid formula in P(v)")
                return "\n".join(self.steps)

            # Create new substitution variable
            new_atomic = self.generate_new_atomic()

            # Handle negation differently from binary operations
            if op == '¬':
                right_str = right if self.is_atomic(right) else self.substitutions.get(right, right)
                self.steps.append(f"{right_str} belongs to P(v) => ({op}{right_str}) belongs to P(v)")
                self.steps.append(f"not. ({op}{right_str}) := {new_atomic} => {new_atomic} belongs to P(v)")
                self.reverse_steps.insert(0, f"{new_atomic} = ({op}{right_str})")
            else:
                left_str = left if self.is_atomic(left) else self.substitutions.get(left, left)
                right_str = right if self.is_atomic(right) else self.substitutions.get(right, right)
                self.steps.append(f"{left_str}, {right_str} belong to P(v) => ({left_str}{op}{right_str}) belongs to P(v)")
                self.steps.append(f"not. ({left_str}{op}{right_str}) := {new_atomic} => {new_atomic} belongs to P(v)")
                self.reverse_steps.insert(0, f"{new_atomic} = ({left_str}{op}{right_str})")

            # Store the substitution and update the formula
            self.substitutions[compound] = new_atomic
            current_formula = current_formula[:start] + new_atomic + current_formula[end:]

        # Show final results
        if self.is_atomic(current_formula):
            self.steps.append(f"\nFinal result: {current_formula}")
            self.steps.append("\nReverse substitution:")
            for step in self.reverse_steps:
                self.steps.append(step)
            self.steps.append(f"\nSince {current_formula} belongs to P(v) and following the substitutions backwards,")
            self.steps.append(f"we can conclude that {original_formula} belongs to P(v)")
            self.steps.append("Therefore, this is a well-formed formula.")
        else:
            self.steps.append("\nNot a valid formula in P(v)")

        return "\n".join(self.steps)

parser = LogicParser()

formulas = ["(((P ⇒ Q) ∨ S) ⇔ T)", "((P ⇒ (Q ∧ (S ⇒ T))))", "(¬(B(¬Q)) ∧ R)", "(P ∧ ((¬Q) ∧ (¬(¬(Q ⇔ (¬R))))))", "((P ∨ Q) ⇒ ¬(P ∨ Q)) ∧ (P ∨ (¬(¬Q)))"]

c = 1
for formula in formulas:
    print(f"\nProblem {c}: {formula}")
    c += 1
    print(parser.solve_formula(formula))
    print("-" * 75)