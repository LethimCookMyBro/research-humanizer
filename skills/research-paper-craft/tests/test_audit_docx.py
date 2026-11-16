"""Synthetic OOXML tests only. No native Word rendering is performed."""
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/audit_docx.py'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
TYPES = '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>'

def paragraph(text='Ordinary prose.', props='', runs=None):
    return f'<w:p><w:pPr>{props}</w:pPr>' + (runs if runs is not None else f'<w:r><w:t>{text}</w:t></w:r>') + '</w:p>'

class AuditDocxTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SCRIPT.exists(), 'Missing read-only DOCX preflight')
        spec = importlib.util.spec_from_file_location('audit_docx', SCRIPT)
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'synthetic.docx'

    def fixture(self, body=None, extras=None):
        with ZipFile(self.path, 'w') as archive:
            archive.writestr('[Content_Types].xml', TYPES)
            archive.writestr('word/document.xml', f'<w:document xmlns:w="{W}" xmlns:m="{M}"><w:body>{body or paragraph()}</w:body></w:document>')
            for name, text in (extras or {}).items():
                archive.writestr(name, text)
        return self.path

    def inspect(self, body=None, extras=None):
        return self.mod.audit_docx(self.fixture(body, extras))

    def codes(self, report):
        return {f['code'] for f in report['findings']}

    def test_no_findings_is_not_native_word_approval(self):
        report = self.inspect()
        self.assertEqual(report['status'], 'manual_review_required')
        for key in ('native_word_verified', 'pagination_verified', 'rendering_verified', 'scientific_semantics_verified'):
            self.assertFalse(report[key])
        self.assertTrue(report['read_only'])

    def test_source_is_byte_identical_after_audit(self):
        self.fixture(paragraph('Many  spaces.'))
        before = self.path.read_bytes()
        self.mod.audit_docx(self.path)
        self.assertEqual(before, self.path.read_bytes())
        self.assertEqual(len(list(self.path.parent.iterdir())), 1)

    def test_spaces_split_across_runs(self):
        runs = '<w:r><w:t xml:space="preserve">A </w:t></w:r><w:r><w:t xml:space="preserve"> B</w:t></w:r>'
        self.assertIn('REPEATED_SPACES', self.codes(self.inspect(paragraph(runs=runs))))

    def test_justified_soft_break(self):
        body = paragraph(props='<w:jc w:val="both"/>', runs='<w:r><w:t>Text</w:t><w:br/><w:t>Next</w:t></w:r>')
        self.assertIn('JUSTIFIED_SOFT_BREAK', self.codes(self.inspect(body)))

    def test_manual_break_without_explicit_justification_remains_candidate(self):
        self.assertIn('MANUAL_LINE_BREAK', self.codes(self.inspect(paragraph(runs='<w:r><w:br/></w:r>'))))

    def test_distributed_alignment(self):
        self.assertIn('DISTRIBUTED_ALIGNMENT', self.codes(self.inspect(paragraph(props='<w:jc w:val="thaiDistribute"/>'))))

    def test_tracking_and_scaling(self):
        runs = '<w:r><w:rPr><w:spacing w:val="25"/><w:w w:val="85"/></w:rPr><w:t>Text</w:t></w:r>'
        codes = self.codes(self.inspect(paragraph(runs=runs)))
        self.assertTrue({'CHARACTER_SPACING','TEXT_SCALE'}.issubset(codes))

    def test_normal_tracking_and_scaling_not_flagged(self):
        runs = '<w:r><w:rPr><w:spacing w:val="0"/><w:w w:val="100"/></w:rPr><w:t>Text</w:t></w:r>'
        self.assertFalse({'CHARACTER_SPACING','TEXT_SCALE'} & self.codes(self.inspect(paragraph(runs=runs))))

    def test_exact_line_height(self):
        body = paragraph(props='<w:spacing w:line="200" w:lineRule="exact"/>', runs='<m:oMath><m:r><m:t>x</m:t></m:r></m:oMath>')
        self.assertIn('FIXED_LINE_HEIGHT', self.codes(self.inspect(body)))

    def test_style_definition_is_explicitly_not_resolved_style(self):
        styles = f'<w:styles xmlns:w="{W}"><w:style w:styleId="Wide"><w:rPr><w:spacing w:val="40"/></w:rPr></w:style></w:styles>'
        report = self.inspect(extras={'word/styles.xml': styles})
        self.assertIn('CHARACTER_SPACING', self.codes(report))
        self.assertFalse(report['effective_styles_resolved'])
        self.assertIn('word/styles.xml', {f['part'] for f in report['findings']})

    def test_suspicious_glyphs_are_review_candidates_not_replaced(self):
        report = self.inspect(paragraph('¿ □ �'))
        self.assertIn('GLYPH_REVIEW', self.codes(report))
        self.assertTrue(all(f['severity']=='review' for f in report['findings']))

    def test_thai_and_nonbreaking_spaces_not_rewritten(self):
        path = self.fixture(paragraph('ภาษาไทย\u00a010\u202fmm'))
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        report = self.mod.audit_docx(path)
        self.assertEqual(digest, report['source_sha256'])
        self.assertNotIn('REPEATED_SPACES', self.codes(report))

    def test_exact_row_height_and_cannot_split(self):
        body = '<w:tbl><w:tr><w:trPr><w:trHeight w:val="180" w:hRule="exact"/><w:cantSplit/></w:trPr><w:tc>' + paragraph() + '</w:tc></w:tr></w:tbl>'
        codes = self.codes(self.inspect(body))
        self.assertTrue({'EXACT_ROW_HEIGHT','UNSPLITTABLE_ROW'}.issubset(codes))

    def test_false_boolean_is_not_enabled(self):
        body = paragraph(props='<w:keepNext w:val="0"/>')
        self.assertNotIn('KEEP_WITH_NEXT', self.codes(self.inspect(body)))

    def test_blank_paragraph_chain_but_not_one_required_paragraph(self):
        self.assertNotIn('BLANK_PARAGRAPH_CHAIN', self.codes(self.inspect('<w:p/>'+paragraph())))
        self.assertIn('BLANK_PARAGRAPH_CHAIN', self.codes(self.inspect('<w:p/><w:p/>'+paragraph())))

    def test_stale_field_error(self):
        self.assertIn('FIELD_ERROR_TEXT', self.codes(self.inspect(paragraph('Error! Reference source not found.'))))

    def test_equations_counted_not_certified(self):
        body = paragraph(runs='<m:oMath><m:r><m:t>x</m:t></m:r></m:oMath>')
        report = self.inspect(body)
        self.assertEqual(report['inventory']['equations'], 1)
        self.assertFalse(report['scientific_semantics_verified'])

    def test_headers_and_footers_are_scanned(self):
        hdr = f'<w:hdr xmlns:w="{W}">{paragraph("Header  text")}</w:hdr>'
        report = self.inspect(extras={'word/header1.xml':hdr})
        self.assertIn('word/header1.xml', {f['part'] for f in report['findings']})

    def test_part_hashes_available_for_comparison(self):
        report = self.inspect()
        self.assertIn('word/document.xml', report['part_sha256'])

    def test_wrong_file_type_rejected(self):
        path = Path(self.temp.name)/'paper.pdf'
        path.write_bytes(b'%PDF')
        with self.assertRaises(ValueError):
            self.mod.audit_docx(path)

    def test_bad_zip_rejected(self):
        self.path.write_bytes(b'not a zip')
        with self.assertRaises(ValueError):
            self.mod.audit_docx(self.path)

    def test_missing_document_rejected(self):
        with ZipFile(self.path,'w') as archive:
            archive.writestr('[Content_Types].xml', TYPES)
        with self.assertRaises(ValueError):
            self.mod.audit_docx(self.path)

    def test_malformed_xml_not_silently_skipped(self):
        self.fixture(extras={'word/styles.xml':'<broken>'})
        with self.assertRaises(ValueError):
            self.mod.audit_docx(self.path)

    def test_doctype_rejected(self):
        self.fixture(extras={'word/styles.xml':'<!DOCTYPE x [<!ENTITY a "x">]><x>&a;</x>'})
        with self.assertRaises(ValueError):
            self.mod.audit_docx(self.path)

    def test_unsupported_namespace_not_clean_report(self):
        with ZipFile(self.path, 'w') as archive:
            archive.writestr('[Content_Types].xml', TYPES)
            archive.writestr('word/document.xml', '<document/>')
        with self.assertRaises(ValueError):
            self.mod.audit_docx(self.path)

    def test_no_manuscript_excerpts_leak_into_report(self):
        report = self.inspect(paragraph('PRIVATE_STUDY_NAME  confidential'))
        self.assertNotIn('PRIVATE_STUDY_NAME', json.dumps(report))

    def test_cli_json_and_findings_exit(self):
        self.fixture(paragraph('Two  spaces.'))
        run = subprocess.run([sys.executable,'-B',str(SCRIPT),str(self.path),'--json','--fail-on-findings'],capture_output=True,text=True)
        self.assertEqual(run.returncode,1,run.stderr)
        self.assertEqual(json.loads(run.stdout)['status'],'manual_review_required')

if __name__ == '__main__':
    unittest.main()
