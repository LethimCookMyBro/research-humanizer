"""Adversarial JSON and file-boundary regressions on synthetic manifests."""
from pathlib import Path
import importlib.util
import tempfile
import unittest
S=Path(__file__).resolve().parents[1]/'scripts/audit_figures.py'
s=importlib.util.spec_from_file_location('figure_edges',S); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
class FigureEdgeCases(unittest.TestCase):
    def test_arbitrary_json_types_report_errors(self):
        with tempfile.TemporaryDirectory() as d:
            for f in ({'kind':[]}, {'kind':{}}, {'id':[]},
                      {'kind':'graph','evidence_status':[]},
                      {'kind':'photo','sources':[{'id':[], 'role':[]}]}):
                with self.subTest(f=f):
                    self.assertGreater(m.audit({'schema_version':1,'figures':[f]},Path(d))['errors'],0)
    def test_origin_objects_report_errors(self):
        with tempfile.TemporaryDirectory() as d:
            f={'id':'x','kind':'photo','sources':[{'id':'s','origin':{},'path':'missing','role':'original_image'}]}
            self.assertGreater(m.audit({'schema_version':1,'figures':[f]},Path(d))['errors'],0)
    def test_diagram_unhashable_ids_report_errors(self):
        with tempfile.TemporaryDirectory() as d:
            f={'kind':'overview','diagram':{'nodes':[{'id':'a','source_id':[]}], 'edges':[{'from':[],'to':{},'source_id':[]}]}}
            self.assertGreater(m.audit({'schema_version':1,'figures':[f]},Path(d))['errors'],0)
    def test_symlink_escape_not_read(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'project'; root.mkdir(); outside=Path(d)/'secret'; outside.write_text('private')
            (root/'link').symlink_to(outside)
            f={'id':'x','kind':'photo','sources':[{'id':'s','path':'link','role':'original_image','origin':'researcher_original'}]}
            result=m.audit({'schema_version':1,'figures':[f]},root)
            self.assertIn('UNSAFE_SOURCE_PATH',{x['rule'] for x in result['findings']})
if __name__=='__main__': unittest.main()
