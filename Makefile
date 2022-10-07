OUTDIR :=_site
export RULE_BASE := https://github.com/Luzifer/twitch-bot-rules/raw/main/

default:

rules_lint:
	bash ci/lint.sh

index: .venv
	rm -rf $(OUTDIR)
	mkdir $(OUTDIR)
	./.venv/bin/python ci/indexer.py \
		$(OUTDIR)/index.html \
		rules

.venv:
	python -m venv .venv
	./.venv/bin/pip install -r ci/requirements.yml
