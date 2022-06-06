import os
import subprocess
import re
import pprint
import json
def parse_result(raw_result):
    tests = []
    current_test = None
    current_it = None
    total_time = 0
    for line in raw_result.splitlines():
        print(line)
        if "<DESCRIBE::>" in line:
            if current_test:
                current_test["total_time"] = total_time
                total_time = 0
                tests.append(current_test)
            current_test = {}
            current_test["name"] = line.split("<DESCRIBE::>")[1]
            current_test["it"] = []
        elif "<IT::>" in line:
            if current_it:
                current_test["it"].append(current_it)
            current_it = {}
            current_it["name"] = line.split("<IT::>")[1]
        elif "<PASSED::>" in line:
            current_it["err"] = None
            current_it["passed"] = True
        elif "<FAILED::>" in line:
            current_it["err"] = line.split("<FAILED::>")[1].replace('<:LF:>', '\n')
            current_it["passed"] = False
        elif "<COMPLETEDIN::>" in line:
            if current_it:
                current_it["time"] = float(line.split("<COMPLETEDIN::>")[1]) if line.split("<COMPLETEDIN::>")[1] else -1
                current_test["it"].append(current_it)
                if (current_it["time"] > 0):
                    total_time += current_it["time"]
                current_it = None
    if current_it:
        current_test["it"].append(current_it)
    if current_test:
        tests.append(current_test)
    return {
        "tests": tests,
        "test_count": sum(1 for test in tests for it in test["it"]),
        "passed": sum(1 for test in tests for it in test["it"] if it["passed"]),
        "failed": sum(1 for test in tests for it in test["it"] if not it["passed"])
    }

class Runner:
    def __init__(self, language, image, code, test_script):
        self.command = None
        self.image = image
        self.code = code
        self.test_script = test_script
        self.language = language

    def format_output(self, output):
        return {"stdout": output.stdout.decode('utf-8'), "stderr": output.stderr.decode('utf-8').replace("/home/codewarrior/fixture.c /home/codewarrior/solution.c -o /home/codewarrior/solution ./frameworks/c/criterion.c -I./frameworks/c -lcriterion -lm/home/codewarrior/", "")}

    def search(self, str, needle):
        try:
            return str.index(needle)
        except ValueError:
            return -1

    def run(self):
        self.command = ["docker", "run", "--rm", self.image, "run", "-l", self.language, "-c", self.code, "-t", "cw", "-f", self.test_script, "-d"]
        output = subprocess.run(self.command, capture_output=True)
        std_out = output.stdout.decode('utf-8')
        std_err = output.stderr.decode('utf-8')
        if std_err and not std_out:
            std_err = std_err.replace("/home/codewarrior/fixture.c /home/codewarrior/solution.c -o /home/codewarrior/solution ./frameworks/c/criterion.c -I./frameworks/c -lcriterion -lm/home/codewarrior/", "")
            return {"stdout": std_out, "stderr": std_err, "error": True}
        else:
            if self.search(std_out, '<ERROR::>') > -1:
                std_out = std_out.replace('<:LF:>', '\\n')
                return {"stdout": std_out, "stderr": std_err, "error": True}
            else:
                new_arr = parse_result(std_out)
                new_arr["stderr"] = std_err.split("[----]")[0]
                new_arr["error"] = False
                pprint.pprint(new_arr)
                return new_arr
