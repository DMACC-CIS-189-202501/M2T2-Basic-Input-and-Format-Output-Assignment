import pytest
import ast
import importlib
from unittest.mock import patch


def get_ast_tree(filename):
    with open(filename, 'r') as file:
        code = file.read()
    return ast.parse(code)

def has_docstring(tree):
    return ast.get_docstring(tree) is not None

def has_constant(tree, constant_name):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == constant_name:
                    return True
    return False

def has_variable(tree, variable_name):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == variable_name:
                    return True
    return False


def get_variable_type(tree, variable_name):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == variable_name:
                    return type(node.value)
    return None


def test_docstring():
    tree = get_ast_tree('assignment.py')
    assert has_docstring(tree), "Docstring is missing."

def test_constant():
    tree = get_ast_tree('assignment.py')
    assert has_constant(tree, 'NUM_SCORES'), "NUM_SCORES constant is missing."

def test_first_name():
    tree = get_ast_tree('assignment.py')
    assert has_variable(tree, 'first_name'), "first_name variable is missing."

def test_last_name():
    tree = get_ast_tree('assignment.py')
    assert has_variable(tree, 'last_name'), "last_name variable is missing."

def test_age():
    tree = get_ast_tree('assignment.py')
    assert has_variable(tree, 'age'), "age variable is missing."

def test_total():
    tree = get_ast_tree('assignment.py')
    assert has_variable(tree, 'total'), "total variable is missing."

def test_avg_score():
    tree = get_ast_tree('assignment.py')
    assert has_variable(tree, 'avg_score'), "avg_score variable is missing."


def test_final_print():
    with patch('builtins.input', side_effect=["John", "Smith", 26, 98, 99, 96]):
        with patch('builtins.print') as mock_print:
            import assignment
            expected_output = "Smith, John age: 26 average grade: 97.67"
            try:
                mock_print.assert_called_with(expected_output)
            except AssertionError as e:
                actual_output = mock_print.call_args[0][0] if mock_print.call_args else "No output"
                raise AssertionError(
                    f'Tested using inputs: ["John", "Smith", 26, 98, 99, 96]\n'
                    f"Expected print output: '{expected_output}'\n"
                    f"Actual print output: '{actual_output}'\n"
                    "DMACC Student: Please check the formatting and calculation of the average grade; as well as spaces"
                ) from e

def test_final_print_even():
    with patch('builtins.input', side_effect=["Even", "Stevens", 27, 90, 90, 90]):
        with patch('builtins.print') as mock_print:
            import assignment
            importlib.reload(assignment) #Note to grader: This helps it re-execute
            expected_output = "Stevens, Even age: 27 average grade: 90.00"
            try:
                mock_print.assert_called_with(expected_output)
            except AssertionError as e:
                actual_output = mock_print.call_args[0][0] if mock_print.call_args else "No output"
                raise AssertionError(
                    f'Tested using inputs: ["Even", "Stevens", 27, 90, 90, 90]\n'
                    f"Expected print output: '{expected_output}'\n"
                    f"Actual print output: '{actual_output}'\n"
                    "DMACC Student: Please check the formatting and calculation of the average grade; as well as spaces"
                ) from e


if __name__ == "__main__":
    pytest.main()