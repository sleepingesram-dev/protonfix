from parser import parse_log

with open("../samples/apex/apex_failed_launch.log", "r") as f:
    text = f.read()

result = parse_log(text)

print(result)
