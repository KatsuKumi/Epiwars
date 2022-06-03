import os
import subprocess


class Runner:
    def __init__(self, language, image, code, test_script):
        self.command = None
        self.image = image
        self.code = code
        self.test_script = test_script
        self.language = test_script

    def format_output(self, output):
        return output.decode('utf-8')

    def run(self):
        print("Running {}".format(self.image))
        print("Command: {}".format(self.command))
        # Example : docker run --rm codewars/systems-runner run -l c -c "var a = 1;" -t cw -f "Test.assertEquals(a, 1)"
        self.command = "docker run -it --rm {} run -l {} -c \"{}\" -t cw -f \"{}\""\
            .format(self.image, self.language, self.code, self.test_script)
        output = subprocess.check_output(self.command, shell=True)
        return self.format_output(output)
