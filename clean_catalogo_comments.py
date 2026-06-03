import io
import os
import re
import tokenize
from pathlib import Path

root = Path('catalogo')
html_comment = re.compile(r'<!--.*?-->', re.S)

for path in root.rglob('*.py'):
    text = path.read_text(encoding='utf-8')
    try:
        tokens = tokenize.generate_tokens(io.StringIO(text).readline)
    except Exception as e:
        print(f'ERROR tokenizing {path}: {e}')
        continue
    out = []
    prev_end = (1, 0)
    for tok_type, tok_str, start, end, line in tokens:
        if tok_type == tokenize.COMMENT:
            continue
        if tok_type == tokenize.NL:
            out.append(tok_str)
            prev_end = end
            continue
        if start > prev_end:
            row, col = prev_end
            if start[0] == row:
                out.append(' ' * (start[1] - prev_end[1]))
            else:
                out.append('\n' * (start[0] - row))
                out.append(' ' * start[1])
        out.append(tok_str)
        prev_end = end
    new_text = ''.join(out)
    path.write_text(new_text, encoding='utf-8')

for path in root.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    new_text = re.sub(html_comment, '', text)
    path.write_text(new_text, encoding='utf-8')

print('Limpieza completada')
