import subprocess
import os
from PytestResult import PytestResult

# Pytest class utilisé pour run les Pytest
class Pytest:
    # Initialisation
    def __init__(self):
        self.results = [] # liste qui va stocker les Pytest runs
        
    # Run les Pytests tests
    def run(self, test_file):
        # The command to run the Pytest tests
        command = ['pytest', test_file]
        
        # Run the Pytest tests and capture its output
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Store the result of the Pytest run in the results list
        return PytestResult(test_file, result.returncode == 0, result.stderr, result.stdout)
        
    # Run a quick self check test of Pytest
    def selfcheck(self):
        test_file = 'test_hello_world.py' # The test file name
        
        # Write a simple test to the test file
        with open(test_file, 'w') as f:
            f.write("def test_hello_world():\n    assert True")
        
        # Run the test file with Pytest
        result = self.run(test_file)
        
        # Remove the test file
        os.remove(test_file)
        return result
    
    
