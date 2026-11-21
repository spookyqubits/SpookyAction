#!/usr/bin/env python3
"""Build the two self-contained Spooky Action games and their separate collection."""
from pathlib import Path
from html import escape
import argparse
import hashlib
import json
import shutil
import sys
import zipfile

PROJECT = Path(__file__).resolve().parent
SRC = PROJECT / ('src' if (PROJECT / 'src').is_dir() else 'source')
HEADER_SOURCE = PROJECT.parent / 'Logo-Website' if SRC.name == 'src' else SRC
sys.path.insert(0, str(HEADER_SOURCE))
from site_header import document_page, not_found_page, with_header

SOURCE_FILES = ['core.js', 'game.js', 'game.css', 'game.html', 'config.json',
                'collection.html', 'collection.css', 'guide.html', 'ghost.svg']


def fill(template, values):
    for key, value in values.items():
        template = template.replace('{{' + key + '}}', str(value))
    return template


def guide_values(game, other):
    trio = game['kind'] == 'trio'
    cases = [('X · X · X', 'Even total'), ('X · Y · Y', 'Odd total'),
             ('Y · X · Y', 'Odd total'), ('Y · Y · X', 'Odd total')] if trio else [
             ('0 · 0', 'Matching answers'), ('0 · 1', 'Matching answers'),
             ('1 · 0', 'Matching answers'), ('1 · 1', 'Different answers')]
    rule = ('All X questions require an even sum of answers. Exactly two Y questions require an odd sum.' if trio else
            'The answers must match unless both question cards are 1. Then they must differ.')
    rows = ''.join('<tr><td>' + q + '</td><td>' + goal + '</td></tr>' for q, goal in cases)
    return {
        'NAME': game['name'], 'CREW': game['crew'], 'TIME': game['time'], 'RULE': rule,
        'QUESTION': 'Can a shared plan answer all four possible question cards successfully, using only each player’s own question?',
        'COMPARE': ('The ideal GHZ model wins every allowed card. Open the parity explanation after students have tried to improve their plan.' if trio else
                    'The ideal CHSH model wins with probability about 85.36%, so four rounds may not beat the plan. Sample at least 100 fresh rounds in the lab and include every result.'),
        'EXIT': ('Can one player use these correlations to send a chosen message instantly? Why not?' if trio else
                 'Does winning eight of ten random rounds prove entanglement? What else would you need to know?'),
        'RULE_TABLE': '<table><thead><tr><th>Question cards</th><th>Winning condition</th></tr></thead><tbody>' + rows + '</tbody></table>',
        'PROOF': ('Each player’s X answer appears twice across the four cards, as does their Y answer. Adding all those answers therefore gives an even total. The requested pattern, one even total and three odd totals, adds to an odd number: a contradiction.' if trio else
                  'If the first three question cases all succeed, A’s two responses and B’s two responses must all agree. The final question case then demands that two of those same responses differ. One case must fail.'),
        'STRATEGIES': 64 if trio else 16, 'BEST_PLANS': 32 if trio else 8,
        'QUANTUM': ('The ideal model uses (|000⟩ + |111⟩)/√2 and X/Y measurements. Outcome bit 0 denotes eigenvalue +1 and bit 1 denotes −1. For each allowed setting, the four outcomes with the required parity each have probability 1/4.' if trio else
                    'The ideal model uses (|00⟩ + |11⟩)/√2, with Alice’s Z/X measurements and Bob’s (Z + X)/√2 and (Z − X)/√2 measurements. Each winning outcome pair has probability cos²(π/8)/2. The average win probability is cos²(π/8), about 85.36%.'),
        'SOURCE': ('<a href="https://arxiv.org/abs/2107.06156">Girish, Holmgren, Mittal, Raz, and Zhan (2021), Parallel Repetition for the GHZ Game: A Simpler Proof</a>. The GHZ definition and values motivate this classroom version.' if trio else
                   '<a href="https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information/entanglement-in-action/chsh-game">IBM Quantum Learning: CHSH game</a>. The protocol, local bound, and ideal joint probabilities determine the model.'),
        'NEXT': '<a href="../' + other['slug'] + '/">' + ('Next: ' if trio else 'Revisit: ') + other['name'] + ' →</a>'
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=PROJECT / 'dist')
    parser.add_argument('--repository', default=None)
    args = parser.parse_args()
    dist = args.output.resolve()
    assert dist != PROJECT and not SRC.resolve().is_relative_to(dist), 'Choose a generated output directory'
    config = json.loads((SRC / 'config.json').read_text())
    repository = args.repository or config['repository']
    assert repository and all(c.isalnum() or c in '-_.' for c in repository)
    # Preserve any sync-generated files outside the explicit public file set.
    dist.mkdir(parents=True, exist_ok=True)
    files = []
    def write(name, text):
        target = dist / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')
        files.append(target)
    def copy(name, source):
        target = dist / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        files.append(target)
    write('index.html', with_header(fill((SRC / 'collection.html').read_text(), {'REPOSITORY': escape(repository)})))
    copy('action.css', SRC / 'collection.css')
    copy('assets/ghost.svg', SRC / 'ghost.svg')
    for game in config['games']:
        other = next(g for g in config['games'] if g['kind'] != game['kind'])
        values = {k.upper(): escape(str(v)) for k, v in game.items()}
        values.update({'OTHER_SLUG': other['slug'], 'OTHER_NAME': other['name'],
                       'CSS': (SRC / 'game.css').read_text(), 'CORE': (SRC / 'core.js').read_text(),
                       'APP': (SRC / 'game.js').read_text(),
                       'CONFIG': json.dumps({'kind': game['kind'], 'otherSlug': other['slug']}).replace('<', '\\u003c')})
        write('games/' + game['slug'] + '/index.html', fill((SRC / 'game.html').read_text(), values))
        write('games/' + game['slug'] + '/guide.html', fill((SRC / 'guide.html').read_text(), guide_values(game, other)))
    write('.nojekyll', '')
    write('README.md', (PROJECT / 'README.md').read_text().replace('spookyqubits/Spooky-Action', 'spookyqubits/' + repository))
    write('404.html', not_found_page('Spooky Action', 'This ghost wandered off.',
                                     'https://spookyqubits.github.io/' + repository + '/', 'Return to Spooky Action'))
    for name in SOURCE_FILES:
        if name == 'config.json':
            updated = dict(config, repository=repository)
            write('source/' + name, json.dumps(updated, indent=2) + '\n')
        else:
            copy('source/' + name, SRC / name)
    copy('build.py', PROJECT / 'build.py')
    copy('source/site_header.py', HEADER_SOURCE / 'site_header.py')
    def archive(target, members):
        target.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as z:
            for p in sorted(members):
                z.write(p, p.relative_to(dist))
    kit = dist / 'downloads/spooky-action-classroom-kit.zip'
    archive(kit, files)
    files.append(kit)
    for game in config['games']:
        guide = dist / 'games' / game['slug'] / 'guide.html'
        guide.write_text(document_page(guide.read_text()), encoding='utf-8')
    archive(PROJECT / 'spooky-action-site.zip', files)
    manifest = [{'path': str(p.relative_to(dist)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
    (PROJECT / 'release-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Built Ghost Trio, then Ghost Twins:', dist)
    print('Explicit public file count:', len(files))


if __name__ == '__main__':
    main()
