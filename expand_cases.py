from pathlib import Path
import re
from html import escape

root = Path(__file__).parent
index = root / 'index.html'
html = index.read_text()

titles = {
    'fiber-lab': ('Fiber Shredder — Laboratory Scale', 'TEXTILE RECYCLING · MECHANICAL DESIGN'),
    'pipe-robot': ('Pipe Inspection Robot', 'ROBOTICS · INSPECTION'),
    'remote-sensing': ('Remote Sensing Conveyor Screening System', 'MINING · SENSOR INTEGRATION'),
    'espeleorobo': ('EspeleoRobo — Confined-Space Inspection', 'ROBOTICS · FIELD INSPECTION'),
    'espeleorobo-modular': ('Modular EspeleoRobo', 'ROBOTICS · MODULAR DESIGN'),
    'tag-device': ('Drone-Mounted Tag Releasing Device', 'PRODUCT DEVELOPMENT · DRONES'),
    'calibration-rig': ('Sensor Calibration Rig', 'TEST EQUIPMENT · MECHATRONICS'),
    'railway-robot': ('Railway Track Inspection Robot', 'ROBOTICS · RAIL INSPECTION'),
    'aero-design': ('SAE Aero Design Aircraft', 'AEROSPACE · STRUCTURAL DESIGN'),
}

for slug, (title, category) in titles.items():
    pattern = re.compile(r'<section class="modal-panel project-panel" id="' + re.escape(slug) + r'">.*?</section>', re.S)
    match = pattern.search(html)
    if not match:
        raise ValueError(f'Panel not found: {slug}')
    original = match.group()
    img = re.search(r'<img\s+alt="([^"]+)"\s+src="([^"]+)"\s*/>', original)
    if not img:
        raise ValueError(f'Image not found: {slug}')
    sections = []
    for section in re.finditer(r'<div class="text-block">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</div>', original, re.S):
        label, contents = section.groups()
        label = {'Results': 'Result'}.get(label.strip(), label.strip())
        sections.append((label, contents.strip()))
    if [s[0] for s in sections] != ['Problem', 'Objective', 'Result']:
        raise ValueError(f'Unexpected content blocks: {slug}: {[s[0] for s in sections]}')
    media_extra = ''
    video = re.search(r'<div class="video-block">(.*?)</div>\s*</div>\s*</div>\s*</section>', original, re.S)
    if video:
        link = re.search(r'<a\s+class="video-link"\s+href="([^"]+)"[^>]*>', video.group(1))
        if link:
            media_extra = f'<a class="case-video-link" href="{link.group(1)}" target="_blank" rel="noopener noreferrer">▶ Watch Project Video</a>'
    text_sections = ''.join(f'<div class="case-section"><h3>{label}</h3><p>{content}</p></div>' for label, content in sections)
    # No Features copy was supplied for these projects. Keep this field marked for later review.
    text_sections = text_sections.replace('<div class="case-section"><h3>Result</h3>', '<div class="case-section"><h3>Features</h3><p class="case-pending">To be reviewed using existing project documentation.</p></div><div class="case-section"><h3>Result</h3>')
    src = img.group(2)
    alt = img.group(1)
    replacement = f'''<section class="modal-panel project-panel case-modal-panel" id="{slug}">
<div class="case-study">
<div class="case-media">
<button class="case-image-open" data-case-zoom="{escape(src)}" type="button" aria-label="Expand image for {escape(title)}"><img src="{escape(src)}" alt="{escape(alt)}"/></button>
<div class="case-image-caption"><span>Project image</span><span>Click image to enlarge <span aria-hidden="true">↗</span></span></div>
{media_extra}
</div>
<div class="case-information">
<div class="case-heading"><span class="case-eyebrow">{category}</span><h2>{escape(title)}</h2></div>
<div class="case-role"><span aria-hidden="true" class="case-role-icon">◈</span><div><h3>My Role</h3><p>To be confirmed</p></div></div>
{text_sections}
</div>
</div>
</section>'''
    html = html[:match.start()] + replacement + html[match.end():]

index.write_text(html)
css = root / 'assets/css/phase1-case.css'
styles = css.read_text()
styles = styles.replace('#fiber-industrial', '.case-modal-panel')
styles = styles.replace('/* Phase 1: opt-in modernization of one case-study panel only. */', '/* Shared project case-study layout: all ten panels. */')
styles += '\n.case-modal-panel .case-video-link{display:inline-block;margin:4px 3px;color:#27689e;font-size:13px;font-weight:700;text-decoration:none}\n.case-modal-panel .case-video-link:hover{text-decoration:underline}\n'
css.write_text(styles)
print(f'Updated {len(titles)} additional project panels; standardized all ten.')
