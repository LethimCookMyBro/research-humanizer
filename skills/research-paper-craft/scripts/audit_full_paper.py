#!/usr/bin/env python3
"""Read-only consistency audit of declared full-paper records, not research validation.

No network calls, source execution, file mutation, rendering, or submission approval.
The supplied records are assertions; this tool does not prove they are truthful.
"""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import sys
from typing import Any
from urllib.parse import urlsplit

CHECKS = ('numbers', 'citations', 'meaning', 'style', 'visuals', 'equations', 'anonymity', 'word_layout')
MAX_BYTES = 2 * 1024 * 1024


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def url(value: Any) -> bool:
    if not nonempty(value):
        return False
    try:
        parsed = urlsplit(value)
        return parsed.scheme in ('https', 'http') and bool(parsed.hostname) and not parsed.username
    except ValueError:
        return False


def strings(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(nonempty(x) for x in value)


def audit_record(data: Any) -> dict[str, Any]:
    """Return structural findings without upgrading a manuscript's release status."""
    findings: list[dict[str, str]] = []

    def add(code: str, path: str, message: str) -> None:
        findings.append({'code': code, 'path': path, 'message': message})

    def obj(value: Any, path: str) -> dict:
        if not isinstance(value, dict):
            add('STRUCTURE', path, 'Expected an object. The record is incomplete.')
            return {}
        return value

    def rows(value: Any, path: str) -> list:
        if not isinstance(value, list):
            add('STRUCTURE', path, 'Expected a list. The record is incomplete.')
            return []
        return value

    def done() -> dict[str, Any]:
        return {
            'record_status': 'needs_review' if findings else 'consistent',
            'findings': findings,
            'scientific_verification': 'not_performed_by_this_tool',
            'submission_approved': False,
            'scope': 'Declared record consistency only. No source retrieval, tool execution, semantic verification or rendered-layout inspection.',
        }

    if not isinstance(data, dict) or type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        add('SCHEMA', '$', 'Expected schema_version integer 1 in an object.')
        result = done(); result['record_status'] = 'incomplete'; return result
    if data.get('mode') != 'full-paper':
        add('MODE', 'mode', 'This auditor expects a full-paper record, not a revision-only job.')
    workflow = data.get('workflow')
    if workflow not in ('ars', 'standalone'):
        add('WORKFLOW', 'workflow', 'Select ars or explicitly declared standalone.')
    if workflow == 'ars':
        deps = obj(data.get('dependencies'), 'dependencies')
        ars = obj(deps.get('ars'), 'dependencies.ars')
        if ars.get('loaded') is not True or not nonempty(ars.get('entry')):
            add('ARS_UNAVAILABLE', 'dependencies.ars', 'Record actual ARS resource loading. Do not simulate ARS.')
        if not nonempty(ars.get('version')):
            add('ARS_VERSION', 'dependencies.ars.version', 'Record the installed dependency version.')
        if ars.get('confirmations_preserved') is not True:
            add('ARS_CONFIRMATIONS', 'dependencies.ars', 'Do not bypass or fabricate ARS checkpoints.')
    study = obj(data.get('study'), 'study')
    if not nonempty(study.get('question')) or not nonempty(study.get('source_version')):
        add('STUDY_PENDING', 'study', 'Record the actual question and authoritative source version.')
    lit = obj(data.get('literature'), 'literature')
    if lit.get('status') != 'searched':
        add('SEARCH_PENDING', 'literature.status', 'Search is not recorded as performed. Keep the limitation visible.')
    if not strings(lit.get('queries')):
        add('SEARCH_LOG', 'literature.queries', 'Record actual queries, not a claim of broad coverage.')
    try:
        date.fromisoformat(lit.get('searched_on', ''))
    except (ValueError, TypeError):
        add('SEARCH_DATE', 'literature.searched_on', 'Provide a valid ISO date for the actual search.')
    venue = obj(lit.get('venue'), 'literature.venue')
    if not url(venue.get('url')) or not nonempty(venue.get('requirements_locator')):
        add('VENUE_PENDING', 'literature.venue', 'Locate the official target requirements. A sample paper is not the authority.')
    sources: dict[str, dict] = {}
    for i, value in enumerate(rows(lit.get('sources'), 'literature.sources')):
        p = f'literature.sources[{i}]'; item = obj(value, p); key = item.get('id')
        if not nonempty(key):
            add('SOURCE_ID', p, 'A nonempty source id is required.'); continue
        if key in sources:
            add('SOURCE_DUPLICATE', p, 'Duplicate source id.'); continue
        sources[key] = item
        if not url(item.get('url')) or not nonempty(item.get('title')):
            add('SOURCE_IDENTITY', p, 'Record a title and canonical web source.')
        if item.get('access') not in ('full_text', 'abstract_only', 'metadata_only', 'unavailable'):
            add('SOURCE_ACCESS', p, 'Record the actual access level.')
        if not strings(item.get('locators')):
            add('SOURCE_LOCATOR', p, 'Record source-specific locations or the access limitation.')
    if not sources:
        add('SOURCES_PENDING', 'literature.sources', 'No consulted sources are recorded.')
    metric_ids: set[str] = set()
    for i, value in enumerate(rows(data.get('metrics'), 'metrics')):
        p = f'metrics[{i}]'; metric = obj(value, p); key = metric.get('id')
        if not nonempty(key) or key in metric_ids:
            add('METRIC_ID', p, 'Metric ids must be nonempty and unique.')
        else:
            metric_ids.add(key)
        decision = metric.get('decision')
        if decision not in ('selected', 'adapted', 'proposed', 'rejected', 'not_applicable'):
            add('METRIC_DECISION', p, 'Record the metric decision explicitly.')
        if decision in ('rejected', 'not_applicable'):
            if not nonempty(metric.get('reason')):
                add('METRIC_REASON', p, 'Record why this metric is not used.')
            continue
        if not strings(metric.get('source_ids')):
            add('METRIC_SOURCE_UNKNOWN', p, 'Provide source ids for the metric definition.')
        else:
            for sid in metric['source_ids']:
                if sid not in sources:
                    add('METRIC_SOURCE_UNKNOWN', p, f'Unregistered source {sid}.')
                elif sources[sid].get('access') != 'full_text':
                    add('METRIC_SOURCE_ACCESS', p, 'Detailed metric decisions require inspected methods, not metadata or an abstract alone.')
        if not nonempty(metric.get('definition')) or not nonempty(metric.get('independent_unit')):
            add('METRIC_DEFINITION', p, 'Define the metric and independent analysis unit.')
        if decision in ('selected', 'adapted'):
            if not strings(metric.get('raw_fields')) or not nonempty(metric.get('code_locator')):
                add('METRIC_DATA', p, 'Map selected metrics to actual inputs and implementation.')
            if not nonempty(metric.get('approval')):
                add('METRIC_APPROVAL', p, 'Record the researcher decision before changing analysis.')
        status = metric.get('result_status')
        if status not in ('not_measured', 'computed', 'reported'):
            add('RESULT_STATUS', p, 'Distinguish not measured from computed or reported.')
        if status in ('computed', 'reported') and not nonempty(metric.get('validation_locator')):
            add('RESULT_UNVERIFIED', p, 'A reported quantity needs a raw-result reconciliation record.')
    sections = rows(data.get('sections'), 'sections')
    if not sections:
        add('SECTIONS_PENDING', 'sections', 'An empty section list does not represent a full manuscript.')
    for i, value in enumerate(sections):
        p = f'sections[{i}]'; section = obj(value, p)
        if not nonempty(section.get('name')) or section.get('status') not in ('drafted', 'not_applicable'):
            add('SECTION_PENDING', p, 'Record drafted content or an explained non-applicable section.')
        elif section['status'] == 'drafted' and not nonempty(section.get('evidence_locator')):
            add('SECTION_EVIDENCE', p, 'Locate the drafted section and its evidence.')
        elif section['status'] == 'not_applicable' and not nonempty(section.get('reason')):
            add('SECTION_REASON', p, 'Explain why the section is not applicable.')
    if type(data.get('docx_requested')) is not bool:
        add('FORMAT_PENDING', 'docx_requested', 'Declare whether Word output is requested.')
    checks = obj(data.get('checks'), 'checks')
    for name in CHECKS:
        check = obj(checks.get(name), f'checks.{name}')
        if check.get('status') == 'passed':
            if not nonempty(check.get('evidence_locator')):
                add('CHECK_EVIDENCE', f'checks.{name}', 'Passed checks need a real evidence location.')
        elif check.get('status') == 'not_applicable':
            if not nonempty(check.get('reason')):
                add('CHECK_REASON', f'checks.{name}', 'Not applicable needs an explanation.')
        else:
            add('CHECK_PENDING', f'checks.{name}', 'Failed or unperformed checks remain open.')
        if name == 'word_layout' and data.get('docx_requested') is True and check.get('status') != 'passed':
            add('WORD_PENDING', 'checks.word_layout', 'DOCX delivery still requires native Word inspection of the saved artifact.')
    return done()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    parser.add_argument('--json', action='store_true', dest='json_output')
    args = parser.parse_args()
    try:
        with args.record.open('rb') as stream:
            raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise ValueError('Record exceeds 2 MiB.')
        def invalid_constant(value: str) -> None:
            raise ValueError(f'Nonstandard JSON constant {value}.')
        result = audit_record(json.loads(raw.decode('utf-8'), parse_constant=invalid_constant))
    except (OSError, ValueError, UnicodeError) as error:
        result = {'record_status':'incomplete','findings':[{'code':'INPUT_ERROR','path':'$','message':str(error)}],
                  'scientific_verification':'not_performed_by_this_tool','submission_approved':False}
    if args.json_output:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print('Record consistency: ' + result['record_status'])
        for item in result['findings']:
            print(f"{item['code']} [{item['path']}] {item['message']}")
        print('No scientific verification or submission approval is provided by this tool.')
    return 2 if result['record_status'] == 'incomplete' else int(bool(result['findings']))


if __name__ == '__main__':
    sys.exit(main())
