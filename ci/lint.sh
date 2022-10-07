set -euo pipefail

exit_code=0

function error() {
  log E "$@"
  exit_code=1
}

function info() {
  log I "$@"
}

function log() {
  local level=$1
  shift
  echo "[$(date +%H:%M:%S)][$level] $@" >&2
}

required_tags=(
  author
  minBotVersion
  version
)

for rule_file in rules/*.yml; do

  info "Linting rules file ${rule_file}"

  info "+++ Checking with YAMLlint..."
  yamllint -c ci/yamllint.yml ${rule_file}

  info "+++ Checking required tags..."
  for tag in "${required_tags[@]}"; do
    grep -Eq "^# @${tag} .+$" ${rule_file} || error "Missing required tag: ${tag}"
  done

  info "+++ Checking subscription URL..."
  exp_url="${RULE_BASE}${rule_file}"
  sub_url="$(yq -r '.subscribe_from' ${rule_file})"
  [[ $sub_url == $exp_url ]] || error "Wrong subscription URL: expected ${exp_url}"
done

exit $exit_code
