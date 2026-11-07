"""Derive outputs from the agent-normalized fictional evidence; no browsing or LLM call."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def build():
    source = json.loads((ROOT / 'demo/input/normalized.json').read_text())
    rows = []
    for item in source['listings']:
        # The agent extracted typed fields from the preserved source quote.
        rent, bills = item['rentMonthly'], item['requiredBillsMonthly']
        minimum = rent + (bills if bills is not None else 0)
        total = minimum if item['allRequiredBillsKnown'] else None
        status = ('Over budget' if minimum > source['search']['budgetMonthly'] else
                  'Fits' if total is not None and item['privateRoom'] else 'Confirm costs/details')
        deposit = item['refundableDeposit']
        rows.append({**item, 'knownMonthlyMinimum': minimum, 'allInMonthly': total,
                     'status': status,
                     'moveInKnownMinimum': minimum + (deposit if deposit is not None else 0),
                     'moveInTotal': None, 'moveInNote': 'One-time fees are unstated; deposit also unknown where null.'})
    rows.sort(key=lambda r: {'Fits': 0, 'Confirm costs/details': 1, 'Over budget': 2}[r['status']])
    result = {'search': source['search'], 'checkedAt': source['checkedAt'], 'listings': rows}
    features = []
    for r in rows:
        if r['coordinates'] is not None:
            lon, lat = r['coordinates']
            features.append({'type': 'Feature', 'id': r['id'], 'geometry': {'type': 'Point', 'coordinates': [lon, lat]},
                             'properties': {'title': f"Fictional {r['title']} room", 'monthlyCost': r['allInMonthly'], 'currency': 'EUR',
                                            'locationPrecision': r['locationPrecision'], 'synthetic': True,
                                            'source': r['source'], 'openStreetMap': f'https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=14/{lat}/{lon}'}})
    geo = {'type': 'FeatureCollection', 'features': features}
    md = ['# Fictional Padova shortlist', '', 'Checked 7 November 2026, 22:24 IST. EUR 600/month all-in budget; private room.', '',
          '| Room / source | Rent | Required bills | Monthly cost | Move-in cash | Status / question |',
          '| --- | --- | --- | --- | --- | --- |']
    for r in rows:
        monthly = f"EUR {r['allInMonthly']} all-in" if r['allInMonthly'] is not None else f"At least EUR {r['knownMonthlyMinimum']}; bills unknown"
        bills = f"EUR {r['requiredBillsMonthly']}" if r['requiredBillsMonthly'] is not None else 'Unknown (null)'
        cash = f"At least EUR {r['moveInKnownMinimum']}; " + ('includes refundable deposit EUR '+str(r['refundableDeposit']) if r['refundableDeposit'] is not None else 'deposit unknown')
        md.append(f"| [{r['title']}]({r['source']}) | EUR {r['rentMonthly']} | {bills} | {monthly} | {cash}; fees unknown | {r['status']}. {r['question']} |")
    md += ['', 'Only Centro has a supported coordinate: approximate neighborhood, not a precise address.',
           'Availability and viewing details still need confirmation. No landlord was contacted.', '',
           '## Preserved evidence', '']
    md += [f"- **{r['id']}**, {r['source']}: {r['evidence']}" for r in rows]
    files = {'shortlist.json': json.dumps(result, indent=2)+'\n', 'shortlist.geojson': json.dumps(geo, indent=2)+'\n', 'shortlist.md': '\n'.join(md)+'\n'}
    return files


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    output = ROOT / 'demo/output'
    for name, content in build().items():
        path = output / name
        if args.check:
            assert path.read_text() == content, f'Stale output: {name}'
        else:
            path.write_text(content)
    result = json.loads(build()['shortlist.json'])['listings']
    assert [r['allInMonthly'] for r in result] == [550, None, 630]
    assert [r['status'] for r in result] == ['Fits', 'Confirm costs/details', 'Over budget']
    assert result[1]['requiredBillsMonthly'] is None and result[1]['refundableDeposit'] is None
    assert result[0]['moveInKnownMinimum'] == 1490 and result[0]['refundableDeposit'] == 940
    geo = json.loads(build()['shortlist.geojson'])
    assert len(geo['features']) == 1 and geo['features'][0]['geometry']['coordinates'] == [11.877, 45.407]
    provenance = json.loads((ROOT / 'demo/provenance.json').read_text())
    for name, digest in provenance['sourceSha256'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, f'Source changed: {name}'
    print('PASS: deterministic outputs, cost/null/deposit invariants, supported pin, source hashes')

if __name__ == '__main__': main()
