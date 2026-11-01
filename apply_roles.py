"""Apply user-approved Position and My Role text to the ten project panels."""
from pathlib import Path
from html import escape
import re

root = Path(__file__).parent
index = root / 'index.html'
source = index.read_text()

# Position is the academic/employment affiliation. My Role is project-specific.
roles = {
 'fiber-lab': (
  'Graduate Research Assistant', 'Mechanical Design & Development',
  'Sole engineer responsible for the complete mechanical development of the laboratory-scale textile shredding machine, from initial concept to prototyping and validation. Independently led CAD modeling, component design, manufacturing, assembly, testing, and iterative design improvements. Managed mechanical design decisions autonomously, reporting project progress and key developments to my research advisor.'),
 'fiber-industrial': (
  'Mechanical Design Engineer', 'Lead Mechanical Design Engineer',
  'Sole engineer responsible for the mechanical design and industrial scale-up of the textile shredding machine. Led parametric CAD development, component and assembly design, manufacturing drawings, BOM preparation, and DFM/DFA implementation. Developed an automated sizing tool and currently oversee component manufacturing and assembly to ensure design compliance.'),
 'pipe-robot': (
  'Mechanical Engineering Intern', 'Co-Designer',
  'Collaborated with another mechanical engineering intern on the complete mechanical design and development of a modular pipe inspection robot. Contributed to CAD modeling, mechanical component design, locomotion systems, and system integration. Shared responsibility for engineering decisions and design development, reporting technical progress and proposed solutions to the supervising engineer.'),
 'remote-sensing': (
  'Mechanical Engineering Intern', 'Sole Mechanical Designer',
  'Independently led the complete mechanical design of a LiDAR-based conveyor screening system, including structural supports, sensor mounting, protective enclosures, and mechanical integration. Took full responsibility for mechanical design decisions, CAD development, and component design. Also oversaw fabrication and assembly to ensure proper implementation of the design.'),
 'espeleorobo': (
  'Mechanical Engineering Intern', 'Mechanical Design & Development',
  'Collaborated with a mechanical engineer and another engineering intern on the development and continuous improvement of a confined-space inspection robot. Responsible for mechanical component design, CAD modeling, manufacturing drawings, preventive maintenance, and the implementation of mechanical improvements to enhance reliability, performance, and serviceability.'),
 'espeleorobo-modular': (
  'Mechanical Engineering Intern', 'Independent Mechanical Design',
  'Independently conceived and developed a redesigned modular architecture for the EspeleoRobo, including self-contained motor and transmission modules, a simplified chassis, quick-replacement mechanisms, and improved component accessibility. Responsible for the complete mechanical design, CAD modeling, and development of solutions to improve maintainability and system integration. Presented the proposed redesign to senior engineering management for evaluation and potential implementation.'),
 'tag-device': (
  'Mechanical Engineering Intern', 'Independent Product Development',
  'Independently designed and developed a drone-mounted RFID tag deployment mechanism, from initial concept to a fully functional system in less than one week. Led mechanical design, CAD modeling, prototyping, and iterative improvements. Collaborated with other engineers during field testing, implemented design refinements based on test results, and successfully delivered a fully operational solution.'),
 'calibration-rig': (
  'Graduate Research Assistant', 'Mechanical Design & Controls Integration',
  'Independently designed, fabricated, and assembled the complete mechanical system of a modular sensor testing platform. Collaborated with a controls engineer on electronics and control software integration to enable standardized testing procedures. Personally conducted all experimental testing and validation, evaluating system performance and ensuring reliable, repeatable measurements.'),
 'railway-robot': (
  'Mechanical Engineering Intern', 'Independent Mechanical Design & Development',
  'Solely responsible for the complete mechanical design of a modular railway inspection robot, including the structural frame, camera and lighting mounts, and mechanical component integration. Independently developed CAD models, component designs, and assembly solutions, making key engineering decisions throughout the project. Presented the design for technical review and incorporated feedback into the final proposal.'),
 'aero-design': (
  'Undergraduate Student — SAE Aero Design Team Member', 'Fuselage Mechanical Designer & Aircraft Assembly Lead',
  'Responsible for the complete mechanical design of the aircraft fuselage, including CAD modeling, structural development, and manufacturing considerations. Participated in component fabrication and led the assembly of the entire aircraft, coordinating team activities and developing comprehensive assembly instructions. Contributed to aircraft testing and validation, collaborating with team members on engineering decisions and design improvements.'),
}

for slug, (position, role, details) in roles.items():
    pattern = re.compile(r'(<section class="modal-panel project-panel case-modal-panel" id="' + re.escape(slug) + r'">.*?<div class="case-heading">.*?</div>)(.*?)(<div class="case-section"><h3>Problem</h3>)', re.S)
    match = pattern.search(source)
    if not match or '<div class="case-role">' not in match.group(2):
        raise ValueError(f'Cannot find a unique editable role field in {slug}')
    block = (
        '<div class="case-position"><h3>Position</h3><p>' + escape(position) + '</p></div>\n'
        '<div class="case-role"><span aria-hidden="true" class="case-role-icon">◈</span>'
        '<div><h3>My Role</h3><p class="case-role-title">' + escape(role) + '</p>'
        '<p class="case-role-description">' + escape(details) + '</p></div></div>\n'
    )
    source = source[:match.start()] + match.group(1) + '\n' + block + match.group(3) + source[match.end():]

index.write_text(source)
css = root / 'assets/css/phase1-case.css'
styles = css.read_text()
styles += '''
/* Position identifies formal status; My Role describes individual technical contributions. */
.case-modal-panel .case-position{margin-bottom:8px;padding:0 1px}
.case-modal-panel .case-position h3{font-size:11px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:#6a7e95;margin:0 0 2px}
.case-modal-panel .case-position p{font-size:13px;font-weight:600;line-height:1.35;color:#244460;margin:0}
.case-modal-panel .case-role{align-items:flex-start}
.case-modal-panel .case-role .case-role-title{font-size:13px;line-height:1.35;font-style:normal;font-weight:700;color:#244460;margin:0 0 4px}
.case-modal-panel .case-role .case-role-description{font-size:13px;line-height:1.43;font-style:normal;color:#40556b;margin:0}
'''
css.write_text(styles)
print('Updated Position and My Role in', len(roles), 'project panels.')
