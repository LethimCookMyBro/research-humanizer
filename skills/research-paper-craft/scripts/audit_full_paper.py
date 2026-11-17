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


# These are support declarations, not execution states or automatic truth judgments.
SUPPORT_STATES = ('Verified', 'Partially Supported', 'Unverified', 'Proposed',
                  'Contradicted', 'Not Applicable')
REASONING_CRITERIA = ('gap', 'originality', 'impact', 'alignment', 'finding',
                      'limitation', 'metric', 'revision', 'feedback')
FEEDBACK_CLASSES = ('Universal Research Principle', 'Domain-Specific Principle',
                    'Project-Specific Correction', 'Unverified Recommendation')


def audit_reasoning_review(review: Any, owner: Any, add: Any) -> None:
    """Check optional declarations and references; never read or certify evidence.

    Existing schema-1 records without this extension retain their exact behavior.
    Locators are opaque references to existing records, not a parallel evidence store.
    """
    root = 'reasoning_review'
    if not isinstance(review, dict):
        add('REASONING_STRUCTURE', root, 'Expected an optional object, not a null or scalar.')
        return
    if type(review.get('schema_version')) is not int or review['schema_version'] != 1:
        add('REASONING_SCHEMA', root, 'Expected reasoning_review schema_version integer 1.')
        return
    phase = review.get('phase')
    required = {'planning': ('gap', 'originality', 'alignment'),
                'evidence': ('alignment', 'finding'),
                'review': ('gap', 'originality', 'impact', 'alignment', 'finding', 'limitation')}
    if not isinstance(phase, str) or phase not in required:
        add('REASONING_PHASE', root + '.phase', 'Use planning, evidence or review.')
        phase = 'review'
    if review.get('workflow_owner') != owner:
        add('REASONING_WORKFLOW_OWNER', root, 'Reuse the parent workflow owner and its checkpoints.')
    rq_refs = review.get('rq_refs')
    if not strings(rq_refs):
        add('REASONING_RQ_COVERAGE', root + '.rq_refs', 'Reference the actual questions in the paper map.')
        rq_refs = []
    elif len(rq_refs) != len(set(rq_refs)):
        add('REASONING_RQ_COVERAGE', root + '.rq_refs', 'Question references must be unique.')
    refs = review.get('record_refs')
    if not isinstance(refs, dict) or not nonempty(refs.get('qa_report')):
        add('REASONING_RECORD_REFS', root + '.record_refs', 'Locate the existing QA report. Do not duplicate evidence.')
    assessments = review.get('assessments')
    if not isinstance(assessments, list):
        add('REASONING_STRUCTURE', root + '.assessments', 'Expected a list of scoped review declarations.')
        return
    seen_ids: set[str] = set()
    seen_criteria: set[str] = set()
    aligned: set[str] = set()
    for index, item in enumerate(assessments):
        path = f'{root}.assessments[{index}]'
        if not isinstance(item, dict):
            add('REASONING_STRUCTURE', path, 'Expected an assessment object.')
            continue
        key = item.get('id')
        if not nonempty(key) or key in seen_ids:
            add('REASONING_ID', path, 'Assessment IDs must be nonempty and unique.')
        else:
            seen_ids.add(key)
        kind = item.get('criterion')
        if not isinstance(kind, str) or kind not in REASONING_CRITERIA:
            add('REASONING_CRITERION', path, 'Unrecognized research review criterion.')
            continue
        seen_criteria.add(kind)
        status = item.get('status')
        if status not in SUPPORT_STATES:
            add('REASONING_STATUS', path, 'Use one of the six documented support states.')
        for field in ('record_ref', 'scope', 'rationale'):
            if not nonempty(item.get(field)):
                add('REASONING_CONTEXT', path + '.' + field, 'Locate and justify the assessment within its stated scope.')
        asserted = item.get('asserted_as_fact', False)
        if type(asserted) is not bool:
            add('REASONING_STRUCTURE', path + '.asserted_as_fact', 'Use a boolean, not a truthy string.')
        if status == 'Verified' and (not strings(item.get('evidence_refs')) or not nonempty(item.get('review_locator'))):
            add('REASONING_VERIFICATION', path, 'Verified needs evidence references and an actual review record. Presence is not truth verification.')
        if asserted is True and status in ('Unverified', 'Proposed', 'Contradicted', 'Not Applicable'):
            add('REASONING_UNSUPPORTED_ASSERTION', path, 'Do not present this support state as an established finding.')
        if asserted is True and status == 'Partially Supported' and not nonempty(item.get('qualification_ref')):
            add('REASONING_UNSUPPORTED_ASSERTION', path, 'Locate the qualification that limits the partially supported claim.')
        if status == 'Not Applicable':
            if kind == 'gap' and item.get('gap_closed') is True:
                add('REASONING_GAP_CLOSURE', path, 'Not Applicable cannot be used to declare an evidence gap closed.')
            continue

        if kind == 'gap':
            if not strings(item.get('prior_work_refs')) or not strings(item.get('closest_work_refs')):
                add('REASONING_GAP_BASIS', path, 'Locate prior knowledge and closest work. Search absence is not proof of absence.')
            if any(not nonempty(item.get(f)) for f in ('known', 'unknown', 'importance', 'study_fit')):
                add('REASONING_GAP_BASIS', path, 'State known, unknown, importance and fit separately from the proposed solution.')
            if item.get('absence_claim') is True and item.get('search_only') is not False:
                add('REASONING_ABSENCE', path, 'A search that found nothing does not establish universal novelty.')
            closed = item.get('gap_closed', False)
            if type(closed) is not bool:
                add('REASONING_STRUCTURE', path + '.gap_closed', 'Use a boolean; do not infer closure from a complete draft.')
            if closed is True and (status != 'Verified' or not strings(item.get('closure_evidence_refs'))
                                   or any(not nonempty(item.get(f)) for f in ('closure_scope', 'remaining_uncertainty'))):
                add('REASONING_GAP_CLOSURE', path, 'Gap existence and closure differ. Locate sufficient closure evidence, its scope and remaining uncertainty.')
        elif kind == 'originality':
            if (not strings(item.get('prior_work_refs')) or not nonempty(item.get('contribution_type'))
                    or not nonempty(item.get('knowledge_gain'))):
                add('REASONING_ORIGINALITY', path, 'Compare prior work and explain the knowledge gain, including valid replication or negative evidence.')
            if item.get('novelty_basis') == 'tool_or_context_change' and not nonempty(item.get('change_rationale_ref')):
                add('REASONING_ORIGINALITY', path, 'A tool or context change needs a reason why it tests or adds knowledge.')
        elif kind == 'impact':
            if item.get('impact_type') not in ('Scientific Impact', 'Methodological Impact', 'Practical Impact'):
                add('REASONING_IMPACT_TYPE', path, 'Classify the impact domain; use separate rows for distinct claims.')
            basis, reported = item.get('impact_basis'), item.get('reported_impact')
            if basis not in ('Expected Impact', 'Demonstrated Impact') or reported not in ('Expected Impact', 'Demonstrated Impact'):
                add('REASONING_IMPACT_TYPE', path, 'Separate expected from demonstrated impact.')
            if basis == 'Expected Impact' and reported == 'Demonstrated Impact':
                add('REASONING_IMPACT_INFLATION', path, 'An expected benefit cannot be reported as demonstrated.')
            if reported == 'Demonstrated Impact' and not strings(item.get('observed_support_refs')):
                add('REASONING_IMPACT_EVIDENCE', path, 'Locate evidence of the claimed impact, not just task completion.')
            if any(not nonempty(item.get(f)) for f in ('beneficiaries', 'application_limits')):
                add('REASONING_CONTEXT', path, 'Identify intended users of the finding and application limits.')
        elif kind == 'alignment':
            rq = item.get('rq_ref')
            if nonempty(rq) and rq in rq_refs:
                aligned.add(rq)
            else:
                add('REASONING_ALIGNMENT', path, 'Link to a declared research question.')
            if (item.get('suitable') is not True or not strings(item.get('data_or_argument_refs'))
                    or any(not nonempty(item.get(f)) for f in ('method_ref', 'analysis_ref'))):
                add('REASONING_ALIGNMENT', path, 'Locate suitable method, data or theoretical argument, and analysis for this question.')
        elif kind == 'finding':
            if item.get('finding_type') not in ('Observed Results', 'Derived Results', 'Interpretation', 'Hypothesis', 'Unsupported Claim'):
                add('REASONING_FINDING_TYPE', path, 'Separate observation, derivation, interpretation, hypothesis and unsupported claim.')
            if not strings(item.get('result_refs')):
                add('REASONING_RESULT_LINK', path, 'Locate the results or argument supporting this finding, or leave support unresolved.')
            if status == 'Verified' and item.get('consistency') in ('partial', 'unverified'):
                add('REASONING_RESULT_CONFLICT', path, 'Verified support conflicts with a partial or unverified result-to-finding comparison.')
            if item.get('consistency') == 'contradicted':
                add('REASONING_RESULT_CONFLICT', path, 'The finding conflicts with the declared results. Preserve the conflict for researcher review.')
            elif item.get('consistency') not in ('consistent', 'partial', 'unverified'):
                add('REASONING_RESULT_LINK', path, 'Declare consistency, partial support or unverified comparison.')
            if item.get('finding_type') == 'Derived Results' and not nonempty(item.get('derivation_ref')):
                add('REASONING_DERIVATION', path, 'Locate the actual calculation or derivation.')
            if item.get('relation') == 'causal' and (item.get('association_only') is True or not nonempty(item.get('causal_basis_ref'))):
                add('REASONING_CAUSAL', path, 'Locate a defensible causal design/identification argument. Association alone is insufficient.')
            if item.get('finding_type') in ('Hypothesis', 'Unsupported Claim') and (asserted is True or status == 'Verified'):
                add('REASONING_UNSUPPORTED_ASSERTION', path, 'A hypothesis or unsupported claim is not an established result.')
        elif kind == 'limitation':
            if (any(not nonempty(item.get(f)) for f in ('original_answer', 'matters_answer', 'knowledge_answer'))
                    or not strings(item.get('limitation_refs'))):
                add('REASONING_CONTRIBUTION_REVIEW', path, 'Locate answers about originality, importance and new knowledge, with the limits of those answers.')
        elif kind == 'metric':
            if any(not nonempty(item.get(f)) for f in ('definition_ref', 'measurement_ref', 'selection_rationale', 'limitations')):
                add('REASONING_METRIC', path, 'Reference the existing metric plan for definition, measurement, rationale and limitations.')
        elif kind == 'revision':
            if type(item.get('scientific_change')) is not bool:
                add('REASONING_STRUCTURE', path, 'Declare whether the revision changes scientific content.')
            elif item['scientific_change'] and not nonempty(item.get('approval_ref')):
                add('REASONING_APPROVAL', path, 'A scientific change requires a researcher approval record, not a prose edit.')
        elif kind == 'feedback':
            if item.get('classification') not in FEEDBACK_CLASSES:
                add('REASONING_FEEDBACK_CLASS', path, 'Classify the feedback before applying it outside its source project.')
            promote = item.get('promote_to_general', False)
            if type(promote) is not bool:
                add('REASONING_STRUCTURE', path, 'Use a boolean for general-principle promotion.')
            if promote is True and (status != 'Verified' or item.get('classification') != 'Universal Research Principle'
                    or item.get('validation_basis') not in ('independent_sources', 'methodological_argument')
                    or any(not nonempty(item.get(f)) for f in ('validation_ref', 'exceptions', 'approval_ref'))):
                add('REASONING_FEEDBACK_PROMOTION', path, 'A single expert opinion is not universal. Require scoped validation, exceptions and approval before versioned promotion.')
    missing = [kind for kind in required[phase] if kind not in seen_criteria]
    if missing:
        add('REASONING_COVERAGE', root, 'Missing scoped assessments: ' + ', '.join(missing) + '.')
    for rq in rq_refs:
        if rq not in aligned:
            add('REASONING_RQ_COVERAGE', root, 'No alignment assessment for ' + rq + '.')


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
    if 'reasoning_review' in data:
        audit_reasoning_review(data['reasoning_review'], workflow, add)
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
