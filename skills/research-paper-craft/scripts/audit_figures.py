#!/usr/bin/env python3
"""Validate local figure provenance contracts without editing, uploading or executing.

Hashes show byte identity, not authenticity. The tool does not inspect pixels,
render figures, recompute statistics, or verify claims/permissions. Relative
source paths are confined to the explicitly supplied project directory.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import sys

KINDS={'graph','overview','photo','screenshot','conceptual'}
ORIGINS={'researcher_original','analysis_output','author_diagram','published_source','synthetic_fixture','generative_ai','unknown'}
LIMIT=64*1024*1024


def audit(manifest: dict, root: Path) -> dict:
    root=Path(root).resolve(); findings=[]
    def add(fid,rule,message,severity='error'):
        findings.append({'figure':fid,'rule':rule,'severity':severity,'message':message})
    if not isinstance(manifest,dict) or manifest.get('schema_version')!=1:
        add(None,'INVALID_SCHEMA','Expected an object with schema_version 1.')
        figures=[]
    else: figures=manifest.get('figures')
    if not isinstance(figures,list) or not figures:
        add(None,'FIGURES_REQUIRED','Provide a nonempty figures list. An empty template is not a passed audit.')
        figures=[]
    ids=set()
    for index,f in enumerate(figures):
        if not isinstance(f,dict):
            add(str(index),'INVALID_FIGURE','Each figure must be an object.'); continue
        fid=f.get('id'); kind=f.get('kind')
        if not isinstance(kind,str): kind=None
        status=f.get('evidence_status')
        if not isinstance(status,str): status=None
        if not isinstance(fid,str) or not fid.strip() or fid in ids:
            add(str(index),'INVALID_FIGURE_ID','A unique nonempty figure id is required.'); fid=f'item-{index}'
        ids.add(fid)
        if kind not in KINDS: add(fid,'INVALID_KIND','Use graph, overview, photo, screenshot or conceptual.')
        for field in ('purpose','caption','evidence_status'):
            if not isinstance(f.get(field),str) or not f[field].strip(): add(fid,'MISSING_FIELD',f'Record {field}.')
        if status not in {'observed','derived','conceptual','synthetic'}:
            add(fid,'INVALID_EVIDENCE_STATUS','Declare the figure evidence role explicitly.')
        if not isinstance(f.get('claim_refs'),list) or not f['claim_refs']:
            add(fid,'CLAIM_REFS_REQUIRED','Link the figure to manuscript claim IDs or method questions.')
        if 'pending_inputs' not in f or not isinstance(f['pending_inputs'],list):
            add(fid,'INPUT_STATUS_REQUIRED','Explicitly record pending_inputs, including an empty list when none are known.')
        elif f['pending_inputs']: add(fid,'PENDING_INPUTS','Ask the researcher for missing originals before production.')
        sources=f.get('sources',[])
        if not isinstance(sources,list): add(fid,'INVALID_SOURCES','sources must be a list.'); sources=[]
        roles=set(); source_ids=set(); checked_paths={}
        for source in sources:
            if not isinstance(source,dict): add(fid,'INVALID_SOURCE','A source entry must be an object.'); continue
            sid=source.get('id'); role=source.get('role'); origin=source.get('origin')
            if not isinstance(sid,str) or not sid or sid in source_ids:
                add(fid,'INVALID_SOURCE_ID','Use unique nonempty source IDs.'); continue
            source_ids.add(sid)
            if isinstance(role,str): roles.add(role)
            else: add(fid,'SOURCE_ROLE_REQUIRED','Record the source role.')
            if not isinstance(origin,str) or origin not in ORIGINS or origin=='unknown':
                add(fid,'SOURCE_ORIGIN_UNVERIFIED','Identify the original and ask the researcher to verify its relationship to the study.')
            if origin=='generative_ai' and (kind in {'photo','screenshot','graph'} or status in {'observed','derived'}):
                add(fid,'GENERATED_EVIDENCE','Generated pixels cannot substitute for observed study evidence or plotted measurements.')
            if origin=='synthetic_fixture' and status in {'observed','derived'}:
                add(fid,'SYNTHETIC_AS_EVIDENCE','Label fixture data as synthetic, never as study observations.')
            rel=source.get('path')
            if not isinstance(rel,str) or not rel.strip(): add(fid,'SOURCE_MISSING','Supply a local original path.'); continue
            try: path=(root/rel).resolve()
            except (OSError,RuntimeError):
                add(fid,'UNSAFE_SOURCE_PATH','Cannot resolve source path safely.'); continue
            if Path(rel).is_absolute() or not path.is_relative_to(root):
                add(fid,'UNSAFE_SOURCE_PATH','Use a relative path inside the project root. No file outside it was read.'); continue
            try:
                if not path.is_file(): raise FileNotFoundError(rel)
                if path.stat().st_size>LIMIT:
                    add(fid,'SOURCE_TOO_LARGE','Above the 64 MiB inspection limit. Verify separately and record evidence.'); continue
                actual=hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError:
                add(fid,'SOURCE_MISSING',f'Cannot read local source {rel}.'); continue
            if source.get('sha256')!=actual: add(fid,'SOURCE_HASH_MISMATCH',f'Recheck the declared source revision for {rel}.')
            checked_paths[sid]=path
        if not sources: add(fid,'SOURCES_REQUIRED','Request original materials; do not invent replacements.')
        review=f.get('review',{})
        if not isinstance(review,dict): review={}
        for field in ('source_verified_by','final_size_checked_by'):
            if not review.get(field): add(fid,'HUMAN_REVIEW_PENDING',f'{field} is not recorded. A name alone is not proof of a check.','review')
        if kind=='graph':
            if not {'plot_data','generation_script'}.issubset(roles):
                add(fid,'GRAPH_SOURCES_REQUIRED','Keep plotted data and its generating script. The tool never runs the script.')
            g=f.get('graph',{})
            if not isinstance(g,dict): g={}
            for field in ('chart_type','aggregation','independent_unit','missing_values','exclusions','transformations'):
                if not isinstance(g.get(field),str) or not g[field].strip(): add(fid,'GRAPH_SPEC_REQUIRED',f'Record graph.{field}.')
            for axis in ('x','y'):
                a=g.get(axis,{})
                if not isinstance(a,dict) or not all(isinstance(a.get(k),str) and a[k].strip() for k in ('label','unit','scale')):
                    add(fid,'AXIS_SPEC_REQUIRED',f'Record {axis} label, unit and scale. Unitless quantities must say dimensionless or category.')
            u=g.get('uncertainty',{})
            if not isinstance(u,dict) or not u.get('type'): add(fid,'UNCERTAINTY_METHOD_REQUIRED','Define uncertainty or explicitly state none with a reason.')
            elif u['type']=='none':
                if not u.get('reason'): add(fid,'UNCERTAINTY_METHOD_REQUIRED','Explain why no interval is shown.')
            elif not all(u.get(k) for k in ('method','unit_of_replication')):
                add(fid,'UNCERTAINTY_METHOD_REQUIRED','Record interval method and independent unit of replication, not a decorative band.')
            if g.get('chart_type')=='bar':
                y=g.get('y',{})
                if isinstance(y,dict) and y.get('baseline')!=0:
                    add(fid,'BAR_BASELINE_REVIEW','Check magnitude encoding and explicitly justify any nonzero baseline.','review')
            columns=g.get('numeric_columns')
            if not isinstance(columns,list) or not columns or not all(isinstance(c,str) and c for c in columns):
                add(fid,'NUMERIC_COLUMNS_REQUIRED','Declare numeric_columns in the plot-data CSV.'); columns=[]
            for source in sources:
                if not isinstance(source,dict) or source.get('role')!='plot_data': continue
                path=checked_paths.get(source.get('id'))
                if path is None: continue
                if path.suffix.lower()!='.csv':
                    add(fid,'PLOT_DATA_NOT_CHECKED','Numeric inspection supports CSV only. Independently inspect other formats.','review'); continue
                try:
                    with path.open(encoding='utf-8-sig',newline='') as stream:
                        rows=csv.DictReader(stream)
                        if not rows.fieldnames or not set(columns).issubset(rows.fieldnames):
                            add(fid,'PLOT_COLUMN_MISSING','Declared numeric columns were not found.'); continue
                        count=0; invalid=False
                        for row in rows:
                            count+=1
                            for col in columns:
                                try: value=float(row[col])
                                except (TypeError,ValueError): invalid=True; break
                                if not math.isfinite(value): invalid=True; break
                            if invalid:
                                add(fid,'NONFINITE_PLOT_VALUE',f'Non-numeric, missing or nonfinite value at CSV data row {count}. Resolve through the declared missing-data policy.'); break
                        if not count: add(fid,'EMPTY_PLOT_DATA','No plotted observations were supplied.')
                except (OSError,UnicodeError,csv.Error): add(fid,'PLOT_DATA_UNREADABLE','CSV inspection failed. Do not mark the data checked.')
        if kind in {'photo','screenshot'}:
            if f.get('evidence_status')!='observed': add(fid,'PHOTO_ROLE_REVIEW','A study photo or screenshot must be an observed asset; label illustration separately.')
            if not f.get('capture_context'): add(fid,'CAPTURE_CONTEXT_REQUIRED','Record study session, setup version and capture context.')
            if not f.get('permissions'): add(fid,'PERMISSION_REQUIRED','Record consent and reuse authorization. This tool cannot verify it.')
            if 'original_image' not in roles: add(fid,'ORIGINAL_IMAGE_REQUIRED','Keep the unmodified researcher-supplied original image.')
        if kind=='overview':
            d=f.get('diagram',{})
            if not isinstance(d,dict): d={}
            nodes=d.get('nodes',[]); edges=d.get('edges',[])
            if not isinstance(nodes,list) or not nodes: add(fid,'DIAGRAM_NODES_REQUIRED','List the actual components.'); nodes=[]
            if not isinstance(edges,list): add(fid,'INVALID_EDGES','edges must be a list.'); edges=[]
            node_ids=set()
            for node in nodes:
                if not isinstance(node,dict): add(fid,'INVALID_NODE','Node must be an object.'); continue
                nid=node.get('id')
                if not isinstance(nid,str) or not nid or nid in node_ids: add(fid,'INVALID_NODE_ID','Node IDs must be unique strings.'); continue
                node_ids.add(nid)
                if not node.get('label') or not isinstance(node.get('status'),str) or node.get('status') not in {'implemented','proposed','external'}:
                    add(fid,'NODE_STATUS_REQUIRED','Label each node and distinguish implemented, proposed and external.')
                if not isinstance(node.get('source_id'),str) or node.get('source_id') not in source_ids or not node.get('locator'):
                    add(fid,'DIAGRAM_SOURCE_REQUIRED','Map each node to a source ID and locator.')
            for edge in edges:
                if not isinstance(edge,dict): add(fid,'INVALID_EDGE','Edge must be an object.'); continue
                if not isinstance(edge.get('from'),str) or not isinstance(edge.get('to'),str) or edge.get('from') not in node_ids or edge.get('to') not in node_ids: add(fid,'DANGLING_EDGE','An arrow endpoint does not exist.')
                if not edge.get('meaning'): add(fid,'EDGE_MEANING_REQUIRED','State whether the arrow means data, control, dependency or another verified relationship.')
                if not isinstance(edge.get('source_id'),str) or edge.get('source_id') not in source_ids or not edge.get('locator'): add(fid,'DIAGRAM_SOURCE_REQUIRED','Map every arrow to evidence, not decoration.')
        if kind=='conceptual':
            if status not in {'conceptual','synthetic'}: add(fid,'CONCEPT_AS_EVIDENCE','Do not present an illustration as an observed result.')
            if not f.get('illustration_approval'): add(fid,'ILLUSTRATION_APPROVAL_REQUIRED','Record explicit researcher approval and the venue policy check.')
    return {'schema_version':1,'findings':findings,'errors':sum(x['severity']=='error' for x in findings),
            'status':'needs_review' if findings else 'no_flags_in_checked_scope',
            'source_authenticity':'not_verified_by_tool','submission_ready':False,
            'not_checked':['pixel_authenticity','source_truth','permissions','statistics_recomputed','rendered_legibility','caption_truth','publication_policy']}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('manifest',type=Path)
    p.add_argument('--root',type=Path,required=True,help='Explicit project root; no paths outside it are read')
    args=p.parse_args(argv)
    try:
        if not args.root.is_dir(): raise ValueError('Project root is not a directory')
        report=audit(json.loads(args.manifest.read_text(encoding='utf-8')),args.root)
    except (ValueError,OSError,UnicodeError) as exc: p.error(str(exc))
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 1 if report['errors'] else 0

if __name__=='__main__': sys.exit(main())
