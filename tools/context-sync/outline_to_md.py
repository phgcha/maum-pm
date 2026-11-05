"""Outline MCP `list_documents` 결과(ProseMirror JSON)를 마크다운 파일과 색인으로 변환한다.

사용법:
    python3 tools/context-sync/outline_to_md.py <출력 디렉토리> <결과 파일> [<결과 파일> ...]

- 결과 파일: `mcp__outline__list_documents` 호출 결과가 커서 자동 저장된 JSON 파일
- 출력: 문서마다 `<urlId>.md`, 전체 목록 `_index.tsv` (작성일, 수정일, 글자 수, 파일, 상위 경로, 제목, URL, 작성자)
- 출력 디렉토리는 리포지토리 밖에 둔다. Outline 본문은 사내 비공개 자료다.
"""
import json, sys, os, re

def inline(nodes):
    out = []
    for n in nodes or []:
        t = n.get('type')
        if t == 'text':
            s = n.get('text', '')
            for m in n.get('marks', []) or []:
                if m.get('type') == 'link':
                    href = (m.get('attrs') or {}).get('href', '')
                    if href and href != s:
                        s = f'[{s}]({href})'
            out.append(s)
        elif t in ('hard_break', 'br'):
            out.append('\n')
        elif t == 'mention':
            a = n.get('attrs') or {}
            out.append('@' + str(a.get('label') or a.get('modelId') or ''))
        elif t == 'image':
            out.append('[image]')
        elif t == 'attachment':
            a = n.get('attrs') or {}
            out.append(f"[attachment: {a.get('title','')}]")
        else:
            out.append(inline(n.get('content')))
    return ''.join(out)

def block(n, depth=0):
    t = n.get('type'); c = n.get('content') or []; a = n.get('attrs') or {}
    pad = '  ' * depth
    if t == 'heading':
        return '#' * int(a.get('level', 1)) + ' ' + inline(c) + '\n'
    if t == 'paragraph':
        s = inline(c)
        return (pad + s + '\n') if s.strip() else ''
    if t in ('bullet_list', 'ordered_list', 'checkbox_list'):
        out = []
        for i, li in enumerate(c):
            mark = f'{i+1}.' if t == 'ordered_list' else '-'
            if t == 'checkbox_list':
                mark = '- [x]' if (li.get('attrs') or {}).get('checked') else '- [ ]'
            parts = [block(x, depth + 1) for x in (li.get('content') or [])]
            body = ''.join(parts).strip('\n')
            first, *rest = body.split('\n') if body else ['']
            out.append(pad + mark + ' ' + first.strip() + '\n' + ''.join(r + '\n' for r in rest))
        return ''.join(out)
    if t in ('code_block', 'code_fence'):
        return '```\n' + inline(c) + '\n```\n'
    if t == 'table':
        rows = []
        for r in c:
            cells = [' '.join(block(x).strip().replace('\n', ' / ') for x in (cell.get('content') or [])) for cell in (r.get('content') or [])]
            rows.append('| ' + ' | '.join(cells) + ' |')
        return '\n'.join(rows) + '\n'
    if t == 'image':
        return pad + '[image]\n'
    if t == 'attachment':
        return pad + f"[attachment: {a.get('title','')}]\n"
    if t == 'hr':
        return '---\n'
    if c:
        return ''.join(block(x, depth) for x in c)
    return ''

docs = {}
for f in sys.argv[2:]:
    for b in json.load(open(f)):
        try:
            d = json.loads(b['text'])
        except Exception:
            continue
        if isinstance(d, dict) and d.get('id'):
            docs[d['id']] = d
outdir = sys.argv[1]
os.makedirs(outdir, exist_ok=True)
def path_of(d):
    parts = []; cur = d; seen = set()
    while cur and cur.get('parentDocumentId') and cur['parentDocumentId'] in docs and cur['id'] not in seen:
        seen.add(cur['id']); cur = docs[cur['parentDocumentId']]; parts.append(cur.get('title') or '')
    return ' / '.join(reversed(parts))
index = []
for d in docs.values():
    body = block(d.get('data') or {})
    body = re.sub(r'\n{3,}', '\n\n', body)
    fn = d['urlId'] + '.md'
    url = d.get('url', '') if d.get('url', '').startswith('http') else 'https://wiki.worvgrip.com' + d.get('url', '')
    hdr = f"# {d.get('title')}\n\n- url: {url}\n- path: {path_of(d)}\n- created: {d.get('createdAt','')[:10]} by {(d.get('createdBy') or {}).get('name','')}\n- updated: {d.get('updatedAt','')[:10]} by {(d.get('updatedBy') or {}).get('name','')}\n\n"
    open(os.path.join(outdir, fn), 'w').write(hdr + body)
    index.append((d.get('createdAt','')[:10], d.get('updatedAt','')[:10], len(body), fn, path_of(d), d.get('title') or '', url, (d.get('createdBy') or {}).get('name',''), 'archived' if d.get('archivedAt') else ''))
index.sort()
with open(os.path.join(outdir, '_index.tsv'), 'w') as w:
    w.write('created\tupdated\tchars\tfile\tparent_path\ttitle\turl\tauthor\tflag\n')
    for r in index:
        w.write('\t'.join(str(x).replace('\t', ' ') for x in r) + '\n')
print('docs', len(docs), 'chars', sum(r[2] for r in index))
