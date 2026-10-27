.PHONY: html versions clean serve live error-codes check

error-codes:
	python3 scripts/generate_error_codes.py

check:
	python3 scripts/check_bilingual.py

html:
	./scripts/build_docs.sh

versions:
	python3 scripts/build_versioned_site.py

clean:
	rm -rf build public

serve: html
	python3 -m http.server 8000 -d build/html

live: error-codes
	rm -rf build/html build/doctrees
	@if [ -x .venv/bin/sphinx-autobuild ]; then \
		AUTO=.venv/bin/sphinx-autobuild; SPHINX=.venv/bin/sphinx-build; \
	else \
		AUTO=sphinx-autobuild; SPHINX=sphinx-build; \
	fi; \
	"$$AUTO" -c docs/zh_CN -d build/doctrees/zh_CN docs/zh_CN build/html \
		--host 0.0.0.0 --port 8000 \
		--watch docs/en --watch docs/_static --watch theme/agile_docs_theme \
		--watch docs/conf_common.py --watch docs/navigation.py \
		--pre-build "$$SPHINX -b html -W --keep-going -c docs/en -d build/doctrees/en docs/en build/html/en"
