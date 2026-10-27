# CLAUDE.md

Project rules for every human and agent working in this repository.
These rules are binding and take priority over general style guidance.

## Stack
- Python 3.12+
- Lint and format: `ruff` (`ruff check .`, `ruff format .`)
- Tests: `pytest` (`pytest -q`)
- Configuration lives in `pyproject.toml`. Do not add `setup.py`, `setup.cfg` or separate tool config files.
- Adding a dependency requires saying so explicitly in the task report.

## File layout
- Production code: `src/app/`. One module per responsibility, `snake_case.py`.
- Tests: `tests/`, mirroring `src/app/`. `src/app/orders/pricing.py` → `tests/orders/test_pricing.py`.
- No code at the top level of a module other than imports, constants and definitions.
- Entry points (CLI, scripts) are thin: they parse input, call into `src/app/`, and handle output.

## Naming
- Modules, functions, variables: `snake_case`. Classes: `PascalCase`. Constants: `UPPER_SNAKE_CASE`.
- Functions are verbs (`calculate_total`), classes and variables are nouns (`invoice`, `OrderRepository`).
- Booleans read as questions: `is_valid`, `has_items`.
- No abbreviations (`customer`, not `cust`), no single-letter names except `i`/`j` in short loops,
  no noise words (`data`, `info`, `manager`, `helper`) on their own.
- Test names describe behavior: `test_<unit>_<condition>_<expected_result>`,
  e.g. `test_calculate_total_with_empty_cart_returns_zero`.

## Functions and classes
- A function is at most 20 lines of body and at most 3 parameters.
- No boolean flag parameters; split into two functions instead.
- Full type hints on every public function and method, including the return type.
- No `Any` without a comment explaining why.
- Prefer plain functions and dataclasses. Add a class only when it holds state or
  implements an interface that has more than one implementation.
- Nesting depth at most 2; use guard clauses and early returns.
- No magic numbers or strings; name them as module-level constants.

## Error handling
- Define project exceptions in `src/app/errors.py`, all inheriting from `AppError`.
- Raise specific exceptions with a message that includes the offending value.
- Never return `None` or an error code to signal failure. Never use bare `except:`.
- Catch an exception only to add context, translate it, or handle it for real;
  re-raise with `raise NewError(...) from error`.

## Logging
- Use `logging`, never `print`, in `src/app/`.
- Each module gets its own logger: `logger = logging.getLogger(__name__)`.
- Only entry points configure logging (`logging.basicConfig` or similar); library modules never do.
- Log at system boundaries, on important decisions, and on every caught or raised failure,
  with context (ids, inputs, reason). Use `logger.exception` inside `except` blocks.
- Use lazy formatting: `logger.info("Order %s created", order_id)`, not f-strings.
- Never log secrets, tokens, passwords or personal data.
- Do not log inside small pure helper functions.

## Tests
- Every public function has at least one test for the normal case and one edge case
  (empty input, boundary, invalid input or error path).
- One concept per test. No loops or conditionals inside tests; use `pytest.mark.parametrize`.
- Tests do not touch the network, the real filesystem or the clock; use `tmp_path`,
  fakes or injected dependencies.
- Use `pytest.raises(SpecificError, match=...)` for error paths.

## Git
- Never commit or push directly to `main`. All changes reach `main` through a pull request.
- Branch names: `feat/<short-kebab-description>`, e.g. `feat/order-discounts`.
- Commit messages: `<type>: <short imperative summary>`, lowercase, no trailing period.
  Allowed types: `feat:`, `fix:`, `test:`, `refactor:`.
  Add a body explaining WHY when the change is not trivial.
- One logical change per commit. Stage files by path; never commit `.env`, caches or secrets.
- Never force-push, rewrite published history, or skip hooks (`--no-verify`).
- Pull requests are squash-merged and the branch is deleted after merge.

## Definition of done
`ruff check .`, `ruff format --check .` and `pytest -q` all pass, and the reviewer verdict is
`VERDICT: APPROVED`.
