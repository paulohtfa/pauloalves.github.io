* {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
}

body {
  font-family: "Montserrat", sans-serif;
  background: #0f0f12;
  color: #fff;
  min-height: 100vh;
}

body.modal-open {
  overflow: hidden;
}

.page-shell {
  width: min(1600px, 94vw);
  margin: 0 auto;
  padding: 2rem 0 3rem;
}

/* HERO */
.hero {
  margin-bottom: 2rem;
}

.hero h1 {
  margin: 0;
  font-size: clamp(2.5rem, 6vw, 5rem);
  line-height: 0.98;
  font-weight: 600;
}

.hero h2 {
  margin: 0.35rem 0 0.7rem;
  font-size: clamp(2rem, 4.6vw, 4rem);
  font-weight: 800;
}

.hero p {
  margin: 0;
  font-size: 1rem;
  font-weight: 300;
  text-transform: uppercase;
  letter-spacing: 0.24rem;
}

/* GRID */
.home-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(240px, 1fr));
  gap: 1rem;
}

/* TILE */
.tile {
  border: 1px solid rgba(255,255,255,0.18);
  background: rgba(255,255,255,0.03);
  padding: 1.4rem;
  min-height: 110px;
  cursor: pointer;
  transition: 0.2s;
}

.tile:hover {
  background: rgba(255,255,255,0.08);
}

.tile span {
  font-size: 0.9rem;
  text-transform: uppercase;
}

/* OVERLAY */
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.55);
  display: none;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  z-index: 9999;
}

.overlay.active {
  display: flex;
}

.modal {
  position: relative;
  width: min(1500px, 96vw);
  max-height: 94vh;
}

/* CLOSE BUTTON */
.close-btn {
  position: absolute;
  top: 0.8rem;
  right: 0.8rem;
  z-index: 20;
  background: rgba(0,0,0,0.5);
  color: white;
  padding: 0.5rem;
  cursor: pointer;
}

/* PANELS */
.modal-panel {
  display: none;
}

.modal-panel.active {
  display: block;
}

/* SIMPLE PANELS */
.simple-panel {
  background: #1a1a20;
  padding: 2rem;
  max-height: 94vh;
  overflow: auto;
}

/* 🔥 PROJECT FIX (THIS IS THE IMPORTANT PART) */
.project-layout {
  display: flex;
  align-items: stretch;
  width: 100%;
}

.project-left {
  flex: 1;
  display: flex;
  background: #1c1e26;
}

.project-left img {
  width: 100%;
  height: auto;
  object-fit: contain;
  display: block;
}

/* RIGHT PANEL */
.project-right {
  flex: 1;
  background: #ececec;
  color: #111;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.4rem;
  overflow-y: auto;
}

/* TEXT */
.text-block h3 {
  font-size: 1rem;
  font-weight: 800;
  text-transform: uppercase;
}

.text-block p {
  font-size: 0.95rem;
  line-height: 1.5;
}

/* VIDEO */
.video-link {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  width: 260px;
  margin: auto;
  padding: 10px 18px;
  background: #333;
  color: white;
  text-decoration: none;
  border-radius: 6px;
}

.video-link:hover {
  background: #cc0000;
}

/* RESPONSIVE */
@media (max-width: 900px) {
  .project-layout {
    flex-direction: column;
  }

  .home-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}