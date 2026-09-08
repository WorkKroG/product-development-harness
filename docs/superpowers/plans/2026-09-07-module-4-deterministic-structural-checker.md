# Product Development Workflow — план реализации Module 4: детерминированный структурный checker

> **Для агентной реализации:** ОБЯЗАТЕЛЬНЫЙ SUB-SKILL — `superpowers:subagent-driven-development`
> с проектной топологией Task из `AGENTS.md` и `SPEC.md` §§6–8. Implementation и Change Review
> выполняются разными ограниченными внутренними агентными сессиями под управлением Task coordinator
> Module 4. Не начинать реализацию, пока владелец не примет именно эту версию плана в Task.

**Идентификатор:** `MODULE4-PLAN-v1`. Идентичность review образуют SHA-256 этого файла и точная
база ниже; любое изменение содержимого плана или базы аннулирует `PLAN_PASS`.

**Цель:** добавить детерминированный структурный checker без внешних зависимостей, который выдаёт
C01–C12, отклоняет устаревшие идентичности review и утечки привязок в переносимых файлах и никогда
не выдаёт структурные fixtures за поведенческие или live evidence.

**Архитектура:** один CLI на стандартной библиотеке Python отвечает за проверку входов,
детерминированный выбор файлов, двенадцать независимых функций проверок и стабильный вывод в
text/JSON. Отдельный unittest-набор копирует репозиторий во временные изолированные деревья и
применяет по одной контролируемой мутации. JSON review-state является предоставленным входом:
checker сравнивает идентичности фазы, но не подтверждает live-состояние GitHub, Codex или Git.

**Технологии:** стандартная библиотека Python 3 (`argparse`, `hashlib`, `json`, `pathlib`, `re`,
`unittest`, `subprocess`, `tempfile`, `shutil`), текстовые контракты Markdown/YAML, Git.

**Спецификация:** `SPEC.md` §§6–10 и §12; `AUDIT.md` A07, A11, A13, A14, A18–A21;
`EVALUATION.md` E12, E13, E17–E22, E26–E30, E38–E41; исторический Task 4 из
`docs/superpowers/plans/2026-09-06-first-working-version.md`, приведённый в соответствие с
принятыми 2026-09-07 решениями по названию и координации.

## Общие ограничения

- Точная база: `f008c78980113f67f5bc73c7e93adcf8ad003423`, свежо полученная из `origin/main`
  2026-09-07; `HEAD`, `FETCH_HEAD` и `origin/main` совпадали.
- Активные точка входа и вызов остаются `skills/product-development-workflow/SKILL.md` и
  `$product-development-workflow`; slug репозитория и исторический baseline сохраняют прежние имена.
- Историческое имя `scripts/check_harness.py` заменить на `scripts/check_workflow.py`. Это
  единственная дельта названия; имя продукта повторно не обсуждается.
- Текущая и целевая ступени — `working-prototype`: модуль добавляет воспроизводимое структурное
  evidence, но не runtime enforcement и не доказательство готовности к release.
- Архитектура — принятый владельцем дизайн от 2026-09-07 в `SPEC.md` §§6–8, реализованный в
  Module 3 и интегрированный на точной базе выше.
- Только стандартная библиотека Python. Не устанавливать package, plugin, skill, runtime или scheduler.
- Сохранить `baseline/product-development-cycle/`, `BASELINE.sha256`, `tests/test_skill_contract.py`,
  глобальный skill, исторические планы, `.local-handoff/` и посторонний WIP. Fixtures не являются
  evidence owning system.
- Не входят Task 5, runtime service, telemetry, Hydra, pilot, GitHub mutations, push, PR, merge,
  установка, публикация, редизайн CI или release.
- Обязательное ограничение результата: `Structural checks do not prove behavioral correctness.`
- Planning/PLAN: `gpt-5.6-sol/high`; Implementation: `gpt-5.6-sol/medium`; Change Review:
  `gpt-5.6-sol/high`; FINAL: `gpt-6-astra/high`. Requested assignment, принятое native-назначение
  и независимо подтверждённый runtime-факт записываются отдельно.

---

## Карта файлов и границы

### Сейчас меняется только план

- Создать `docs/superpowers/plans/2026-09-07-module-4-deterministic-structural-checker.md` — этот
  проверенный план без временных task/agent IDs и путей конкретной машины.

### Один будущий Implementation Work Item

- Создать `scripts/check_workflow.py` — CLI, проверка входов, content revision, C01–C12,
  детерминированный вывод и exit codes.
- Создать `tests/test_check_workflow.py` — контракт CLI, positive/negative cases, ошибки входов,
  фазовые identities и точная изоляция C10/C11.
- Создать `tests/fixtures/review-state/valid-final.json` — синтетический FINAL state с одинаковыми
  reviewed/current identities.
- Создать `tests/fixtures/review-state/valid-change-review.json` — синтетический Change Review
  state с одинаковыми base/head identities.
- Создать `tests/fixtures/invalid/stale-final.json` — отличается от `valid-final.json` только
  `current.main_sha` и падает ровно по C10.
- Создать `tests/fixtures/invalid/incomplete-review-state.json` — неполная фазовая идентичность;
  доказывает обработку неверного входа, а не механический FAIL.
- Создать `tests/fixtures/invalid/leaked-binding.txt` — инертный синтетический leak, добавляемый
  только в копию активного файла; падает ровно по C11.
- Изменить `README.md` — команда, exit codes, граница review-state, JSON и ограничение результата.
- Изменить `docs/PROJECT_STATUS.md` — после реализации заменить stale next-action Module 3 на
  краткий navigation/evidence pointer Module 4, не копируя live Issue/PR/CI state.

Другие пути изменять нельзя. `CHANGELOG.md` — вход C02/C11/C12, но не редактируется. Потребность
в другом активном файле означает изменение плана и новый PLAN review.

## Контракт CLI и данных

```sh
python3 scripts/check_workflow.py \
  --root . \
  --review-state tests/fixtures/review-state/valid-final.json \
  --json
```

`--root PATH` и `--review-state PATH` обязательны. Относительный review-state разрешается от
`--root`. Абсолютный путь принимается, только если после разрешения остаётся внутри root; выход
наружу — неверный вход. `--json` выбирает машинный вывод; без него CLI печатает упорядоченные
checks, итоги, revision и ограничение.

- Exit `0`: все C01–C12 вернули `PASS`.
- Exit `1`: входы пригодны, но хотя бы один check вернул `FAIL`.
- Exit `2`: вызов или вход непригоден — отсутствуют аргументы; root отсутствует/не директория;
  review-state отсутствует, не читается, повреждён или вне root; phase/verdict не поддерживаются;
  типы, ключи или формат identity неверны. Неполные данные не являются C10 FAIL.

JSON success/mechanical failure всегда содержит четыре обязательных поля:

```json
{
  "revision": "sha256:0000000000000000000000000000000000000000000000000000000000000000",
  "passed": ["C01"],
  "failed": ["C02"],
  "checks": [{"id": "C01", "status": "PASS", "evidence": "baseline manifest: 7/7 matched"}]
}
```

Нулевой revision — пример формата. Реальный `revision` — `sha256:` и 64 строчных hex-символа.
Поток начинается с `PDW-STRUCTURAL-REVISION-v1\0`, затем в сортированном POSIX-relative порядке
кодирует объединение C02 manifest, семи жёстко заданных baseline-путей C01 и существующего
опционального `docs/validation.md`. Повреждённый `BASELINE.sha256` не перенаправляет чтение.

```text
8-byte big-endian path length | UTF-8 path | 1-byte kind | 8-byte big-endian byte length | raw bytes
```

Kind: `F` — обычный файл, `M` — отсутствует, `O` — другой filesystem type. Для `M`/`O` длина
нулевая; symlinks не раскрываются. Поэтому missing required file имеет стабильный revision, а
baseline mutation меняет revision и C01. Исключены review-state, `.git`, тесты (кроме checker как
distribution file) и runtime/native state. Revision — identity структурного content, не Git commit
и не live-review attestation; из fixture он не берётся.

При post-parse exit `2` и `--json` вывести те же четыре поля с `revision: null`, пустые массивы и
`error` со стабильными `code`/`message`. Ошибки argparse используют stderr и exit `2`. Evidence
содержит только repository-relative paths, никогда не абсолютные пути машины.

Нормальный результат содержит ровно двенадцать records C01–C12; `passed`/`failed` сохраняют их
порядок; `status` — только `PASS`/`FAIL`. Text output заканчивается обязательным ограничением;
JSON хранит эту фразу в конце `evidence` C12, сохраняя четырёхполевую success-схему.

## Наблюдаемые контракты C01–C12

| ID | Имя | Механическое условие PASS | Негативный тест |
|---|---|---|---|
| C01 | `baseline-hashes` | Строго разобрать `BASELINE.sha256`; ровно семь путей без дубликатов/лишних записей; все файлы есть и hashes совпадают. | Изменить baseline-байт; C01 в `failed`. |
| C02 | `required-active-files` | Все файлы точного manifest ниже — обычные файлы, не symlinks. | Удалить checker из копии; падает ровно C02, revision ненулевой и повторяемый. |
| C03 | `relative-links` | Во всех Markdown-файлах active skill разобрать destinations только inline Markdown links. `http`, `https`, `mailto` и fragment-only destinations игнорируются. У local destination снять query и fragment, затем отклонить absolute path или escape за пределы active skill и потребовать существующий relative file target. | Positive case: существующий local target с query/fragment даёт PASS. Negative case: SKILL route → `references/missing.md`; падает C03. |
| C04 | `metadata` | SKILL: `name: product-development-workflow`, непустой description; YAML: правильный display name, short description и default prompt с `$product-development-workflow`. | Изменить display name; падает C04. |
| C05 | `gate-order` | Level-2 gates ровно `0,1,2,3,3.5,4,5,6,7,8,9,10,11,12,13,14,15,16`, без дубликатов. | Поменять Gate 8/9; падает C05. |
| C06 | `single-light-viability` | Один `## 3.5. Light viability`, нет `## 4.5.`, в SKILL `light Gate 3.5` между `Positioning`/`Journey`; historical Gate 4.5 migration prose допустим. | Удалить `light`; падает C06. |
| C07 | `five-maturity-stages` | Lifecycle: `working-prototype`, `mvp`, `scale-1`, `scale-2`, `mature`; SKILL: `working prototype`, `MVP`, `scale 1`, `scale 2`, `mature operation`. | Удалить label; падает C07. |
| C08 | `required-profile-fields` | В profile есть Process identity, Product, Maturity, Architecture, Load profile, Sources of truth, Runtime, Models, Economics, Applicability и текущие decision-bearing labels. `Unknown` обязателен как default, но не evidence. | Удалить `Transition evidence required`; падает C08. |
| C09 | `required-handoff-fields` | В своих sections присутствуют все точные labels Work package и Review record ниже. | Таблично удалить каждый label, включая `Work Item/module identity`, `Report to identity`, `Phase`; C09 падает. |
| C10 | `review-identity-consistency` | Фазовая schema корректна; все `reviewed == current`. Evidence: `provided input; not live owning-system evidence`. | `stale-final.json` падает ровно C10; PLAN/Change Review/FINAL имеют equal/stale cases. |
| C11 | `forbidden-private-bindings` | Только public allowlist сканируется на user paths, Recipes binding, runtime UUID, credential prefix, client-ID marker; evidence не раскрывает match. | Добавить leak fixture в SKILL-копию; падает ровно C11. |
| C12 | `no-placeholder-markers` | Operational files не содержат line markers `TBD`, `TODO`, `FIXME`, `XXX`, `IMPLEMENT ME`, `FILL IN`; intentional `Unknown`/template fields в assets разрешены. | Добавить `TODO: finish workflow` в reference-копию; падает C12. |

Точный manifest C02:

```text
scripts/check_workflow.py
BASELINE.sha256
README.md
CHANGELOG.md
docs/PROJECT_STATUS.md
skills/product-development-workflow/SKILL.md
skills/product-development-workflow/agents/openai.yaml
skills/product-development-workflow/assets/AGENTS.template.md
skills/product-development-workflow/assets/PROJECT_STATUS.template.md
skills/product-development-workflow/assets/project-profile.template.md
skills/product-development-workflow/assets/role-prompts.md
skills/product-development-workflow/assets/work-item-and-review-templates.md
skills/product-development-workflow/references/agentic-development.md
skills/product-development-workflow/references/codex-runtime.md
skills/product-development-workflow/references/dependencies.md
skills/product-development-workflow/references/financial-model.md
skills/product-development-workflow/references/lifecycle.md
skills/product-development-workflow/references/quality-gates.md
```

C11 сканирует ровно:

```text
skills/product-development-workflow/**/*.md
skills/product-development-workflow/**/*.yaml
README.md
CHANGELOG.md
docs/PROJECT_STATUS.md
docs/validation.md (only when present)
```

C11 не сканирует `baseline/`, `.local-handoff/`, `tests/`, `SPEC.md`, `AUDIT.md`, `EVALUATION.md`,
`HANDOFF.md`, `SOURCES.md`, `VERIFICATION.md` или plans. Literal `.local-handoff/` разрешён в
public safety prose: C11 ищет private bindings, а не запрет публикации каталога.

C12 сканирует `SKILL.md`, `agents/openai.yaml`, active `references/`, `README.md`, `CHANGELOG.md`,
`docs/PROJECT_STATUS.md`, опциональный `docs/validation.md`; `assets/` исключены, потому что
literal `Unknown` и angle-bracket values являются требуемыми placeholders templates.

Точные section-local labels C09:

```text
Work package / handoff:
Work Item/module identity; Outcome/why; Scope/non-goals; Binding sources; Dependencies;
Maturity identity; Architecture identity; Process identity; Plan identity; Exact base;
Exact head; Allowed paths; Permissions/data/recovery; Acceptance criteria; Checks; Role;
Executor kind; Native ID; Parent identity; Report to identity; Constraints;
Current state/findings; Next action.

Review record:
Phase; Independent reviewer kind; Independent reviewer Native ID;
Reviewed plan hash or base/head/main; Binding sources; Checks; Findings; Verdict;
Invalidation condition.
```

## Схема review-state

Git SHA — ровно 40 lowercase hex, plan hash — 64. Допустимы только формы:

```json
{"phase":"PLAN","verdict":"PLAN_PASS","reviewed":{"plan_hash":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","base_sha":"1111111111111111111111111111111111111111"},"current":{"plan_hash":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","base_sha":"1111111111111111111111111111111111111111"}}
```

```json
{"phase":"CHANGE_REVIEW","verdict":"PASS","reviewed":{"base_sha":"1111111111111111111111111111111111111111","head_sha":"2222222222222222222222222222222222222222"},"current":{"base_sha":"1111111111111111111111111111111111111111","head_sha":"2222222222222222222222222222222222222222"}}
```

```json
{"phase":"FINAL","verdict":"FINAL_PASS","reviewed":{"main_sha":"1111111111111111111111111111111111111111"},"current":{"main_sha":"1111111111111111111111111111111111111111"}}
```

Лишние/отсутствующие keys или ошибки schema/type/format/verdict дают exit `2`; корректная форма
с разными identities — C10 failure и exit `1`. Fixtures используют явно синтетические hex и
помечаются в README как offline inputs. C10 доказывает внутреннюю согласованность provided data,
но не их происхождение из GitHub/Codex/Git, от reviewer или назначенной модели.

---

### Task 1: реализовать и документировать единый Work Item Module 4

**Файлы:**

- Создать: `scripts/check_workflow.py`
- Создать: `tests/test_check_workflow.py`
- Создать: `tests/fixtures/review-state/valid-final.json`
- Создать: `tests/fixtures/review-state/valid-change-review.json`
- Создать: `tests/fixtures/invalid/stale-final.json`
- Создать: `tests/fixtures/invalid/incomplete-review-state.json`
- Создать: `tests/fixtures/invalid/leaked-binding.txt`
- Изменить: `README.md`
- Изменить: `docs/PROJECT_STATUS.md`
- Сохранить и запускать: `tests/test_skill_contract.py`, `BASELINE.sha256`

**Интерфейсы:** получает `Path root`, `Path review_state` и текущие active-file contracts;
производит `main(argv: Sequence[str] | None = None) -> int`, C01–C12, четырёхполевой JSON,
content revision и exits 0/1/2; не использует network, GitHub/Codex APIs, task IDs, `.git`,
private handoff, behavioral fixtures или scheduler state.

- [ ] **Шаг 1: загрузить `skill-creator`, test-driven-development и инструкции репозитория**

  Implementation session читает `AGENTS.md`, exact plan, active SKILL и delivery/runtime
  references/templates; записывает base, plan hash, requested/accepted model facts, allowed paths
  и sole-writer status. Это не разрешает installation или GitHub action.

- [ ] **Шаг 2: добавить синтетические review-state и leak fixtures**

  Использовать только inert fixed examples. `stale-final.json` меняет только `current.main_sha`.
  `leaked-binding.txt` читается тестами и не входит в production allowlist C11:

  ```text
  Synthetic private binding: /Users/example/Develop/Projects/recipes-v1
  Synthetic repository binding: WorkKroG/recipes-v1
  Synthetic task identity: 11111111-2222-3333-4444-555555555555
  Synthetic credential prefix: ghp_AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
  Synthetic provisional identity: client-new-thread:synthetic-only
  ```

- [ ] **Шаг 3: написать падающие unit tests ядра/revision/C02**

  Импортировать script напрямую. Проверить root, contained review-state path, framed revision,
  JSON/text renderers и `check_c02(root)`: missing checker → C02 FAIL со стабильным revision;
  baseline mutation меняет revision; review-state не меняет; evidence не содержит absolute root.

  ```python
  def load_checker_module():
      spec = importlib.util.spec_from_file_location("check_workflow", SCRIPT)
      module = importlib.util.module_from_spec(spec)
      spec.loader.exec_module(module)
      return module
  ```

- [ ] **Шаг 4: запустить тесты ядра и подтвердить RED**

  ```sh
  python3 -B -m unittest tests.test_check_workflow.WorkflowCheckerCoreTest -v
  ```

  Ожидается FAIL из-за отсутствия script/functions; fixture/dependency failure не считается RED.

- [ ] **Шаг 5: реализовать core types, input helpers, framed revision, renderers и C02**

  Реализовать точный manifest C02 и pure helpers. Не создавать fake results последующих checks
  и пока не собирать registry/CLI.

  ```python
  @dataclass(frozen=True)
  class Check:
      id: str
      status: str
      evidence: str

  CHECK_IDS = tuple(f"C{number:02d}" for number in range(1, 13))

  class InputError(ValueError):
      def __init__(self, code: str, message: str):
          super().__init__(message)
          self.code = code
  ```

  Реализовать `compute_revision(root: Path) -> str` и `check_c02(root: Path) -> Check` по
  полному framed algorithm и C02 contract выше.

- [ ] **Шаг 6: запустить тесты ядра и подтвердить GREEN**

  ```sh
  python3 -B -m unittest tests.test_check_workflow.WorkflowCheckerCoreTest -v
  ```

  Ожидается PASS для containment, renderers, revision и C02; unimplemented checks не считаются PASS.

- [ ] **Шаг 7: написать падающие direct tests C01, C03–C09 и C12**

  Копировать repo без `.git`, `.local-handoff`, bytecode/caches. Вызывать pure checks отдельно.
  Применить все table mutations. Для C03 добавить inline link на существующий local file с
  query/fragment и подтвердить PASS, затем отдельно заменить target на отсутствующий и подтвердить
  FAIL. Для C09 удалить по одному каждый точный label. Untouched input даёт PASS той же функции;
  mutation — её ID и FAIL.

  ```python
  def assert_check(self, check, expected_id, expected_status):
      self.assertEqual(expected_id, check.id)
      self.assertEqual(expected_status, check.status)
  ```

- [ ] **Шаг 8: запустить C01/C03–C09/C12 и подтвердить RED**

  ```sh
  python3 -B -m unittest tests.test_check_workflow.WorkflowStructuralChecksTest -v
  ```

  Ожидается FAIL из-за отсутствия конкретных functions; C02 не входит в пакет.

- [ ] **Шаг 9: минимально реализовать C01, C03–C09 и C12**

  Следовать точным contracts; без generic Markdown/YAML engine. C06 разрешает historical 4.5;
  C08/C09 парсят named sections; C12 исключает required template values.

- [ ] **Шаг 10: повторить тесты и подтвердить GREEN**

  ```sh
  python3 -B -m unittest tests.test_check_workflow.WorkflowStructuralChecksTest -v
  ```

- [ ] **Шаг 11: написать падающие direct schema/identity tests C10**

  Вызывать `parse_review_state(root, path)` и `check_c10(state, relative_source)`; покрыть equal/
  stale PLAN, Change Review, FINAL; invalid/extra keys → stable `InputError`; evidence redacted.

- [ ] **Шаг 12: запустить C10 tests и подтвердить RED**

  ```sh
  python3 -B -m unittest tests.test_check_workflow.WorkflowReviewIdentityTest -v
  ```

- [ ] **Шаг 13: реализовать phase-aware C10**

  Проверять exact forms/verdict/types/lengths до сравнения полных maps. Не вызывать Git/GitHub/Codex.

- [ ] **Шаг 14: повторить C10 tests и подтвердить GREEN**

  ```sh
  python3 -B -m unittest tests.test_check_workflow.WorkflowReviewIdentityTest -v
  ```

- [ ] **Шаг 15: написать падающие direct allowlist/rule/redaction tests C11**

  Вызывать `check_c11(root)`; отдельно проверить все пять rules, redaction и ignored paths.

- [ ] **Шаг 16: запустить C11 tests и подтвердить RED**

  ```sh
  python3 -B -m unittest tests.test_check_workflow.WorkflowPrivateBindingTest -v
  ```

- [ ] **Шаг 17: реализовать bounded C11 scan**

  Только объявленный allowlist; named regex rules; без symlinks, broad walk, private reads и echo match.

- [ ] **Шаг 18: повторить C11 tests и подтвердить GREEN**

  ```sh
  python3 -B -m unittest tests.test_check_workflow.WorkflowPrivateBindingTest -v
  ```

- [ ] **Шаг 19: написать падающие full CLI integration tests**

  После pure checks добавить subprocess helper. Проверить exact JSON/text, order, exits,
  determinism, redaction, revision invariance, limitation; stale-final → ровно C10;
  aggregate leak → ровно C11; post-parse errors → empty core + stable error.

  ```python
  def run_checker(root: Path, review_state: str | None, *, json_output: bool = True):
      command = [sys.executable, str(SCRIPT), "--root", str(root)]
      if review_state is not None:
          command += ["--review-state", review_state]
      if json_output:
          command.append("--json")
      return subprocess.run(command, text=True, capture_output=True, check=False)
  ```

- [ ] **Шаг 20: запустить CLI tests и подтвердить RED**

  ```sh
  python3 -B -m unittest tests.test_check_workflow.WorkflowCheckerCliTest -v
  ```

  Ожидается FAIL, потому что `main()` ещё не собрал parsing, registry и outputs.

- [ ] **Шаг 21: реализовать финальную композицию CLI**

  Реализовать `main(argv: Sequence[str] | None = None) -> int`, C01–C12 в точном порядке,
  revision до checks, review-state до C10 и exits 0/1/2. Никаких временных stubs.

- [ ] **Шаг 22: повторить CLI tests и подтвердить GREEN**

  ```sh
  python3 -B -m unittest tests.test_check_workflow.WorkflowCheckerCliTest -v
  ```

- [ ] **Шаг 23: обновить README и навигацию**

  Описать command, JSON, IDs, exits, review-state, revision и limitation. PROJECT_STATUS содержит
  только Module 3 base, Module 4 evidence pointer/limitation и next gate; никаких Task 5/pilot/
  install/release/live GitHub claims.

- [ ] **Шаг 24: выполнить focused и full verification**

  ```sh
  python3 -B -m unittest tests.test_check_workflow -v
  python3 -B -m unittest discover -s tests -v
  python3 scripts/check_workflow.py --root . --review-state tests/fixtures/review-state/valid-final.json --json
  shasum -a 256 -c BASELINE.sha256
  git diff --check
  git status --short
  git rev-parse HEAD
  ```

  Ожидается: tests PASS; checker exit `0`; `passed` = C01–C12; `failed` пуст; baseline 7/7.
  Это структурное evidence, не выполнение E01–E41.

- [ ] **Шаг 25: создать один local candidate commit**

  Changed paths — ровно девять Work Item paths выше плюс принятый plan, если не был committed.

  ```sh
  git commit -m "test: add deterministic workflow checks"
  ```

  Никаких push, PR, merge, install или release.

- [ ] **Шаг 26: выполнить независимый Change Review точного candidate**

  Fresh read-only agent получает sources, plan/hash, base/head, full diff, paths, checks/fixtures,
  но не Implementation conversation. Новый commit аннулирует PASS; corrections остаются в Work Item.

- [ ] **Шаг 27: остановиться на границе integration**

  `READY_FOR_INTEGRATION` требует current Change Review PASS и authorized ready PR. Merge ручной.
  После merges отдельный FINAL проверяет exact current main; drift аннулирует FINAL_PASS. Module 4
  не DONE только потому, что checker или plan прошёл.

## Критерии приёмки и риски

1. C01–C12 PASS на exact candidate, stable order, useful relative evidence.
2. Каждый check имеет positive и meaningful negative test структуры/мутации, не только фразы.
3. Stale FINAL падает ровно C10; injected active-path binding — ровно C11.
4. Missing/incomplete review-state → exit `2`; valid stale identity → exit `1`.
5. C10 покрывает PLAN, Change Review, FINAL.
6. C11 использует только public allowlist и synthetic leak fixture.
7. C12 сохраняет intentional `Unknown` и angle-bracket values templates.
8. `revision` детерминирован и не копируется из review-state.
9. Существующие 26 tests и baseline 7/7 остаются зелёными и неизменными.
10. README/status не заявляют live state, behavior, installation, release readiness или Task 5.

Риски и меры:

- **Ложная уверенность:** limitation в обоих output modes/docs; behavior/pilot остаются позже.
- **Хрупкий text matching:** exact headings, section-local labels, front matter, links, JSON; без engine.
- **Fixture принят за live:** review-state вне revision, provided-input label, synthetic identities.
- **False positives/secret echo:** exact allowlist, named rules, exclusions, только rule + relative path.
- **Scope creep:** один Work Item; без Task 5, scheduler, telemetry, pilot, install или CI redesign.

## Review плана и следующее разрешение

PLAN проверяет весь файл по SHA-256 на базе `f008c78980113f67f5bc73c7e93adcf8ad003423`
и binding sources. Изменение plan/base аннулирует `PLAN_PASS`. После PASS Task coordinator
представляет identity-bound package владельцу. Принятие разрешает только Implementation одного
Work Item и local candidate/checks; не разрешает GitHub mutation, push, PR, merge, install,
pilot, publication или release.

**Structural checks do not prove behavioral correctness.**
