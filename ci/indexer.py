import jinja2
import os
import re
import sys
import yaml

FIELD_REGEX = r"^# @([^ ]+)\s+(.*)$"


def get_doc_field(content, field, default=None):
    matches = re.finditer(FIELD_REGEX, content, re.MULTILINE)

    fields = {}

    for matchNum, match in enumerate(matches, start=1):
        fields[match.groups()[0]] = match.groups()[1]

    return fields[field] if field in fields else default


def get_rules_index(rules_dir):
    rules = []

    for file in os.listdir(rules_dir):
        fullpath = '/'.join([rules_dir, file])
        with open(fullpath, 'r') as rulefile:
            content = rulefile.read()

            rule = yaml.load(content, Loader=yaml.SafeLoader)

            rules.append({
                "actions": [x["type"] for x in rule["actions"]],
                "author": get_doc_field(content, "author"),
                "min_bot_ver": get_doc_field(content, "minBotVersion", "v3.x"),
                "description": rule["description"],
                "file": fullpath,
                "shortened_id": rule["uuid"].split('-')[0],
                "version": get_doc_field(content, "version", "v0"),
            })

    return sorted(rules, key=lambda x: x["description"])


def main(args):
    outfile = args[1]
    rules_dir = args[2]

    rules = get_rules_index(rules_dir)

    render_index(outfile, rules)

    return 0


def render_index(outfile, rules):
    with open('index.tpl.html', 'r') as template_source:
        env = jinja2.Environment()
        tpl = env.from_string(template_source.read())

        with open(outfile, 'w') as output:
            output.write(tpl.render(
                rule_base=os.environ['RULE_BASE'] if 'RULE_BASE' in os.environ else '/',
                rules=rules,
            ))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
