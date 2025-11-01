import csv
from collections import Counter
from pathlib import Path

csv_path = Path(__file__).resolve().parents[1] / 'data' / 'output' / 'rota_otimizada.csv'
if not csv_path.exists():
    print('CSV not found:', csv_path)
    raise SystemExit(1)

cnt = Counter()
total = 0
with open(csv_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        v = r.get('Velocidade')
        if not v:
            continue
        try:
            vi = int(v)
        except ValueError:
            continue
        cnt[vi] += 1
        total += 1

print(f'Total trechos: {total}')
print('Vel	Count	Pct')
for vel, c in cnt.most_common():
    pct = c / total * 100
    print(f'{vel}\t{c}\t{pct:.1f}%')
