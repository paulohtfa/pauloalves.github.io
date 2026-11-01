"""Apply the reviewed concise project narratives without changing layouts or images."""
from pathlib import Path
from html import escape
import re

index = Path(__file__).with_name('index.html')
source = index.read_text()

# Role descriptions and sections as approved during the portfolio review.
cases = {
 'fiber-lab': {
  'role': 'Sole engineer responsible for the complete mechanical development of the laboratory-scale textile shredding machine. Independently managed CAD design, component manufacturing, assembly, experimental testing, and iterative mechanical improvements, reporting key developments to my research advisor.',
  'problem': 'Conventional textile shredding systems provide limited control over fiber separation, often producing excessive fabric fragmentation and inconsistent fiber quality. A flexible experimental platform was needed to investigate and optimize mechanical recycling processes.',
  'solution': 'Developed a modular shredding system featuring custom carding-wire drums, adjustable rotational speed, inter-drum spacing, and processing time. Integrated pressurized-air systems for material transport between drums and pneumatic actuation of the discharge door, enabling controlled experimentation and mechanical optimization.',
  'result': 'The reconfigurable platform enabled systematic testing across different textiles and operating conditions. Mechanical improvements enhanced material flow, promoted shear-dominant fiber separation, and increased fiber recovery while reducing unwanted fabric fragments.'
 },
 'fiber-industrial': {
  'role': 'Sole engineer responsible for the mechanical redesign and industrial scale-up of the textile shredding machine. Led CAD development, component design, manufacturing documentation, and DFM/DFA implementation. Currently overseeing component fabrication and assembly.',
  'problem': 'The laboratory-scale machine had limited processing capacity and required significant redesign to support industrial throughput, manufacturability, structural reliability, and future scalability.',
  'solution': 'Developed a scalable parametric CAD architecture and a multi-component shredding drum designed for cost-effective manufacturing. Applied GD&T and DFM/DFA principles to critical interfaces and created an Excel-based sizing tool to automatically adjust machine dimensions and support future configurations.',
  'result': 'Completed the mechanical design and manufacturing documentation for an industrial-scale textile shredding system. The estimated manufacturing cost is more than 75% lower than the selling price of a comparable commercial machine. The parametric architecture enables rapid design scaling and reconfiguration, while manufacturing and assembly remain in progress.'
 },
 'pipe-robot': {
  'role': 'Co-developed the complete mechanical design alongside another mechanical engineering intern. Contributed to CAD modeling, component design, locomotion mechanisms, and system integration, with engineering decisions reviewed by the supervising engineer.',
  'problem': 'Mining pipelines require inspection in confined, wet, and debris-filled environments. Conventional methods are costly, hazardous, and difficult to adapt to varying pipe diameters and operating conditions.',
  'solution': 'Developed a modular robotic platform featuring interchangeable wheel and tracked locomotion systems for different pipe configurations. Integrated a sealed mechanical enclosure, protective interfaces, and thermal management to prevent water and dust ingress while protecting internal electronic components.',
  'result': 'Successfully manufactured and tested the robot, demonstrating its modular locomotion capabilities and adaptability to different pipe configurations. The complete robotic system achieved IP67 certification, validating protection against dust ingress and temporary water immersion. The technology also resulted in a granted patent.'
 },
 'remote-sensing': {
  'role': 'Solely responsible for the mechanical development of a LiDAR-based conveyor screening system. Independently designed the structural components, protective enclosure, and sensor mounting mechanisms. Managed mechanical design decisions and supervised component fabrication and assembly.',
  'problem': 'Conveyor screening inspections exposed workers to hazardous operating areas. Dust, moisture, and continuous vibration created challenges for reliable sensor positioning, environmental protection, and thermal management.',
  'solution': 'Developed a robust mechanical system featuring an IP67-sealed enclosure, adjustable LiDAR mounting mechanisms, and vibration-resistant structural supports. Integrated a Peltier-based active cooling system with passive heat-dissipation fins on the hot side to manage internal temperatures while maintaining environmental sealing.',
  'result': 'Successfully manufactured, installed, and field-tested the system on an operating conveyor. The enclosure was tested and validated to IP67 standards, while the integrated cooling and adjustable mounting architecture supported reliable sensor operation in harsh mining conditions. The technology also resulted in a granted patent.'
 },
 'espeleorobo': {
  'role': 'Collaborated with a mechanical engineer and another engineering intern on mechanical design and continuous improvement. Responsible for transmission development, chassis modifications, CAD modeling, manufacturing drawings, preventive maintenance, and mechanical improvements. Participated in laboratory maintenance and field testing.',
  'problem': 'Inspection robots operating in caves and confined industrial environments face uneven terrain, debris, moisture, and limited accessibility. These conditions increase mechanical wear, complicate maintenance, and demand robust environmental protection.',
  'solution': 'Developed transmission and chassis improvements to enhance mechanical reliability and serviceability. Redesigned access points to simplify internal component replacement and preventive maintenance. Implemented sealing solutions to ensure IP67 compliance while maintaining accessibility to critical mechanical and electronic components.',
  'result': 'Improved robot maintainability, component accessibility, and mechanical robustness through iterative redesign. Supported successful IP67 certification and participated in laboratory and field testing to evaluate the robot’s performance in demanding operating conditions.'
 },
 'espeleorobo-modular': {
  'role': 'Independently conceived and developed a redesigned mechanical architecture for the EspeleoRobo. Responsible for the complete mechanical design, CAD modeling, component development, and engineering decisions. Presented the proposed redesign to senior engineers for evaluation.',
  'problem': 'The existing robot’s integrated mechanical architecture complicated maintenance and component replacement, requiring extensive disassembly. Limited internal accessibility also increased servicing time and restricted system reconfiguration.',
  'solution': 'Designed independent motor and transmission modules for each wheel, enabling rapid replacement without major disassembly. Developed a simplified chassis with upper and lower access doors, dedicated lifting structures, and mounting interfaces for external equipment and sensors.',
  'result': 'Completed and presented a modular mechanical redesign intended to simplify assembly, improve component accessibility, and reduce maintenance complexity. The proposal was submitted for technical evaluation but had not been implemented when my internship ended.'
 },
 'tag-device': {
  'role': 'Independently developed the complete mechanical system, from concept to functional prototype, in less than one week. Responsible for CAD design, fabrication, assembly, and iterative improvements. Collaborated with other engineers during field testing and delivered the final operational device.',
  'problem': 'RFID tags placed before blasting frequently suffered damage, while manual placement after detonation exposed workers to unstable mining areas. A safer deployment method was required.',
  'solution': 'Designed a drone-mounted mechanism capable of carrying and selectively releasing up to ten RFID tags. Integrated a servo-actuated release mechanism, snap-fit mounting interface, and balanced component arrangement to minimize interference with drone stability.',
  'result': 'Successfully manufactured, field-tested, and delivered a fully functional deployment system within one week. The device enabled remote tag placement without requiring workers to enter hazardous areas. The innovation resulted in a granted patent, with my name listed as an inventor.'
 },
 'calibration-rig': {
  'role': 'Independently designed, fabricated, and assembled the complete mechanical testing platform. Collaborated with a controls engineer on electronics and software integration to enable automated testing procedures. Personally conducted experimental testing and validation.',
  'problem': 'Commercial sensor testing equipment can be expensive and difficult to customize for experimental research. A flexible, low-cost platform was needed to characterize force and strain sensors under controlled loading conditions.',
  'solution': 'Developed a modular electromechanical testing platform featuring a rigid mechanical structure, interchangeable fixtures, a precision linear actuator, and integrated load and position sensing. Combined mechanical hardware with control software to enable both force-controlled and displacement-controlled testing procedures.',
  'result': 'Successfully manufactured, assembled, and validated a functional testing platform. Conducted experimental sensor characterization, including drift, hysteresis, and repeatability measurements, providing a customizable solution for research and sensor development.'
 },
 'railway-robot': {
  'role': 'Solely responsible for the complete mechanical design of the railway inspection robot. Developed CAD models, mechanical assemblies, manufacturing drawings, and a Bill of Materials (BOM). Independently made key engineering decisions and incorporated feedback from technical reviews.',
  'problem': 'Railway inspection in high-risk mining areas presents significant safety challenges due to restricted human access. A remotely operated platform was needed to enable track inspection without exposing personnel to hazardous conditions.',
  'solution': 'Designed a modular inspection robot featuring motorized propulsion with standardized railway wheels. The structure incorporated 30 × 30 mm aluminum extrusions, machined metal components, and 3D-printed parts. Integrated adjustable camera and lighting mounts to support comprehensive rail inspection and future sensor expansion.',
  'result': 'Completed the mechanical design, assembly architecture, and manufacturing documentation. The project remained at the design stage because communication restrictions within the intended operating area prevented implementation and field testing.'
 },
 'aero-design': {
  'role': 'Responsible for the complete mechanical design of the aircraft fuselage. Participated in manufacturing, developed detailed assembly instructions, and led the assembly of the entire aircraft. Collaborated on engineering decisions and participated in structural and flight testing.',
  'problem': 'SAE Aero Design competition requirements demanded a lightweight aircraft capable of maximizing payload capacity while maintaining structural integrity, flight stability, and manufacturability under strict design constraints.',
  'solution': 'Designed a lightweight fuselage using balsa wood, MDF, carbon fiber, carbon tubes, and composite materials. Applied CAD modeling, structural design principles, and weight-distribution considerations to optimize strength-to-weight performance. Developed assembly documentation and coordinated the integration of aircraft components.',
  'result': 'Successfully manufactured, assembled, and flight-tested the complete aircraft. The design demonstrated reliable flight performance and contributed to the team’s advancement to the SAE Aero Design First Division.'
 }
}

for slug, sections in cases.items():
    panel_re = re.compile(r'(<section class="modal-panel project-panel case-modal-panel" id="' + re.escape(slug) + r'">)(.*?)(</section>)', re.S)
    found = panel_re.search(source)
    if not found:
        raise RuntimeError(f'Missing panel: {slug}')
    body = found.group(2)
    role_re = re.compile(r'(<p class="case-role-description">).*?(</p>)', re.S)
    body, count = role_re.subn(lambda m: m.group(1) + escape(sections['role']) + m.group(2), body)
    if count != 1:
        raise RuntimeError(f'Missing role description: {slug}')
    first_section = body.find('<div class="case-section"><h3>Problem</h3>')
    if first_section < 0:
        raise RuntimeError(f'Missing problem section: {slug}')
    replacement = ''.join(
        f'<div class="case-section"><h3>{label}</h3><p>{escape(sections[key])}</p></div>\n'
        for label, key in [('Problem', 'problem'), ('Solution', 'solution'), ('Result', 'result')]
    )
    body = body[:first_section] + replacement + '</div></div>\n'
    source = source[:found.start()] + found.group(1) + body + found.group(3) + source[found.end():]

index.write_text(source)
print(f'Updated {len(cases)} panels. Word counts:', {slug: sum(len(v.split()) for v in data.values()) for slug, data in cases.items()})
