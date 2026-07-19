import re

with open('predictor/templates/index.html', 'r') as f:
    content = f.read()

new_css = """
:root {
  --primary: #4f46e5;
  --secondary: #ec4899;
  --accent: #06b6d4;
  --dark: #0f172a;
  --glass: rgba(255, 255, 255, 0.03);
  --glass-border: rgba(255, 255, 255, 0.08);
  --text: #f8fafc;
  --text-dim: #94a3b8;
  --radius: 20px;
  --sidebar-w: 240px;
}

body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background: var(--dark);
  color: var(--text);
  overflow: hidden;
  height: 100vh;
  margin: 0;
  padding: 0;
}

/* Beautiful dynamic mesh background */
.bg {
  position: fixed;
  inset: 0;
  z-index: 0;
  background: 
    radial-gradient(circle at 15% 50%, rgba(79, 70, 229, 0.15), transparent 25%),
    radial-gradient(circle at 85% 30%, rgba(236, 72, 153, 0.15), transparent 25%),
    radial-gradient(circle at 50% 80%, rgba(6, 182, 212, 0.15), transparent 25%);
  background-color: var(--dark);
  animation: bgShift 20s ease-in-out infinite alternate;
}

@keyframes bgShift {
  0% { transform: scale(1); }
  100% { transform: scale(1.1); }
}

.app {
  position: relative;
  z-index: 1;
  display: flex;
  height: 100vh;
  padding: 16px;
  gap: 16px;
}

/* ---- Sidebar (Floating) ---- */
.sidebar {
  width: var(--sidebar-w);
  min-width: var(--sidebar-w);
  height: calc(100vh - 32px);
  background: rgba(15, 23, 42, 0.6);
  backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  display: flex;
  flex-direction: column;
  padding: 0;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  overflow: hidden;
}

.sidebar-logo {
  padding: 28px 24px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid var(--glass-border);
}

.sidebar-logo .icon {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  box-shadow: 0 8px 20px rgba(79, 70, 229, 0.4);
}

.sidebar-logo h2 {
  font-size: 19px;
  font-weight: 800;
  letter-spacing: -0.5px;
  background: linear-gradient(135deg, #fff, var(--text-dim));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.sidebar-logo span {
  font-size: 11px;
  color: var(--text-dim);
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
}

.sidebar-nav {
  flex: 1;
  padding: 20px 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 16px;
  border-radius: 12px;
  color: var(--text-dim);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.nav-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(to bottom, var(--primary), var(--secondary));
  border-radius: 0 4px 4px 0;
  opacity: 0;
  transition: opacity 0.3s;
}

.nav-item svg {
  width: 20px;
  height: 20px;
  transition: transform 0.3s;
}

.nav-item:hover {
  background: var(--glass);
  color: var(--text);
}
.nav-item:hover svg {
  transform: translateX(2px);
}

.nav-item.active {
  background: linear-gradient(90deg, rgba(79, 70, 229, 0.15), transparent);
  color: #fff;
  font-weight: 600;
}

.nav-item.active::before {
  opacity: 1;
}

.nav-item.active svg {
  color: var(--primary);
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid var(--glass-border);
  font-size: 12px;
  color: var(--text-dim);
  text-align: center;
}

/* ---- Main Area ---- */
.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 32px);
  background: rgba(15, 23, 42, 0.4);
  backdrop-filter: blur(12px);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.main-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 32px;
  border-bottom: 1px solid var(--glass-border);
  flex-shrink: 0;
  background: rgba(255,255,255,0.01);
}

.main-header h3 {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.5px;
}
.main-header .sub {
  font-size: 13px;
  color: var(--text-dim);
  margin-top: 4px;
  display: block;
}

.main-header .status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-dim);
  background: var(--glass);
  padding: 6px 12px;
  border-radius: 20px;
  border: 1px solid var(--glass-border);
}
.main-header .status .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 10px #10b981;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
  70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
  100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

.tab-container {
  flex: 1;
  overflow-y: auto;
  padding: 32px;
  position: relative;
}
.tab-container::-webkit-scrollbar { width: 6px; }
.tab-container::-webkit-scrollbar-track { background: transparent; }
.tab-container::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }

/* ---- Tab Content ---- */
.tab-content { display: none; }
.tab-content.active { display: block; animation: slideUpFade 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }

@keyframes slideUpFade {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ---- Bento Grid ---- */
.bento-grid { display: grid; gap: 24px; }
.bento-grid.cols-2 { grid-template-columns: 1fr 1fr; }
.bento-grid.cols-3 { grid-template-columns: 1fr 1fr 1fr; }
.bento-grid .span-2 { grid-column: span 2; }
.bento-grid .span-full { grid-column: 1 / -1; }

.bento-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--glass-border);
  border-radius: calc(var(--radius) - 4px);
  padding: 28px;
  transition: transform 0.3s, box-shadow 0.3s;
  position: relative;
  overflow: hidden;
}

.bento-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
}

.bento-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 20px 40px -10px rgba(0,0,0,0.4);
  background: rgba(255, 255, 255, 0.03);
}

.bento-card .b-title {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--text-dim);
  margin-bottom: 20px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ---- Form elements ---- */
.form-group { margin-bottom: 20px; }
.form-group label { display: block; font-size: 13px; font-weight: 600; color: var(--text); margin-bottom: 10px; }

.slider-wrap { position: relative; padding-top: 32px; }
.slider-value {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  padding: 4px 16px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 700;
  white-space: nowrap;
  box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3);
  transition: left 0.1s;
}

input[type="range"] {
  -webkit-appearance: none;
  width: 100%;
  height: 6px;
  border-radius: 3px;
  outline: none;
  background: rgba(255,255,255,0.05);
}
input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  background: #fff;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 0 10px rgba(0,0,0,0.5);
  border: 4px solid var(--primary);
  transition: transform 0.2s;
}
input[type="range"]::-webkit-slider-thumb:hover { transform: scale(1.2); }
.range-labels { display: flex; justify-content: space-between; font-size: 12px; color: var(--text-dim); margin-top: 8px; font-weight: 500; }

.selector-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
.selector-item { position: relative; cursor: pointer; }
.selector-item input { position: absolute; opacity: 0; pointer-events: none; }
.selector-item .box {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 12px 8px;
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 12px;
  background: rgba(255,255,255,0.02);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.selector-item .box svg { width: 20px; height: 20px; color: var(--text-dim); transition: all 0.3s; }
.selector-item .box .num { font-size: 15px; font-weight: 700; color: var(--text-dim); transition: all 0.3s; }

.selector-item:hover .box {
  background: rgba(255,255,255,0.05);
  border-color: rgba(255,255,255,0.1);
}
.selector-item input:checked + .box {
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.2), rgba(236, 72, 153, 0.2));
  border-color: var(--secondary);
  box-shadow: 0 0 20px rgba(236, 72, 153, 0.15);
}
.selector-item input:checked + .box svg { color: #fff; transform: translateY(-2px); }
.selector-item input:checked + .box .num { color: #fff; }

select, input[type="number"], input[type="text"] {
  width: 100%;
  padding: 12px 16px;
  border-radius: 10px;
  background: rgba(0,0,0,0.2);
  border: 1px solid var(--glass-border);
  color: var(--text);
  font-size: 14px;
  outline: none;
  transition: all 0.3s;
  font-family: inherit;
}
select:focus, input[type="number"]:focus, input[type="text"]:focus {
  border-color: var(--primary);
  background: rgba(0,0,0,0.4);
  box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.1);
}
select option { background: var(--dark); color: var(--text); }

.btn-primary {
  padding: 14px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  width: 100%;
  letter-spacing: 0.5px;
  position: relative;
  overflow: hidden;
}
.btn-primary::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(rgba(255,255,255,0.2), transparent);
  opacity: 0;
  transition: opacity 0.3s;
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(236, 72, 153, 0.4);
}
.btn-primary:hover::after { opacity: 1; }
.btn-primary:active { transform: translateY(0); }

.btn-secondary {
  padding: 10px 20px;
  border-radius: 8px;
  border: 1px solid var(--glass-border);
  background: rgba(255,255,255,0.03);
  color: var(--text);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.btn-secondary:hover {
  background: rgba(255,255,255,0.08);
  border-color: rgba(255,255,255,0.2);
}

.loading { display: none; align-items: center; justify-content: center; gap: 10px; padding: 20px; color: var(--text-dim); font-size: 14px; font-weight: 500;}
.loading.show { display: flex; }
.spinner { width: 20px; height: 20px; border: 3px solid rgba(255,255,255,0.1); border-top-color: var(--accent); border-radius: 50%; animation: spin 0.8s linear infinite; }

/* ---- Predictor Tab ---- */
.predictor-grid { display: grid; grid-template-columns: 420px 1fr; gap: 24px; height: 100%; }
.form-scroll { overflow-y: auto; padding-right: 8px; }

.result-badge {
  margin-top: 20px;
  padding: 24px;
  border-radius: 16px;
  background: linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(236, 72, 153, 0.1));
  border: 1px solid rgba(236, 72, 153, 0.2);
  text-align: center;
  display: none;
  opacity: 0;
}
.result-badge.show { display: block; opacity: 1; animation: popIn 0.5s cubic-bezier(0.16, 1, 0.3, 1); }

@keyframes popIn {
  0% { opacity: 0; transform: scale(0.95); }
  100% { opacity: 1; transform: scale(1); }
}

.result-badge .r-label { font-size: 11px; text-transform: uppercase; letter-spacing: 2px; color: var(--text-dim); margin-bottom: 8px; font-weight: 700;}
.result-badge .r-price {
  font-size: 32px;
  font-weight: 800;
  letter-spacing: -1px;
  background: linear-gradient(135deg, #fff, var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.result-badge .r-sub { font-size: 13px; color: var(--text-dim); margin-top: 6px; }

/* ---- Map ---- */
.map-panel {
  position: relative;
  border-radius: calc(var(--radius) - 4px);
  overflow: hidden;
  border: 1px solid var(--glass-border);
  height: 520px;
  box-shadow: 0 20px 40px -10px rgba(0,0,0,0.3);
}
.map-panel #map { width: 100%; height: 100%; filter: invert(100%) hue-rotate(180deg) brightness(95%) contrast(90%); }

.map-corner { position: absolute; top: 16px; left: 16px; z-index: 1000; padding: 8px 16px; border-radius: 8px; background: rgba(15,23,42,0.8); backdrop-filter: blur(10px); font-size: 13px; font-weight: 600; color: #fff; border: 1px solid rgba(255,255,255,0.1); }
.map-loading { position: absolute; top: 50%; left: 50%; z-index: 1000; transform: translate(-50%, -50%); background: rgba(15,23,42,0.9); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 16px 24px; display: flex; align-items: center; gap: 12px; font-size: 14px; font-weight: 500; color: #fff; transition: opacity 0.3s; }
.map-loading.hidden { opacity: 0; pointer-events: none; }

.insight-glass {
  position: absolute; bottom: 16px; left: 16px; right: 16px; z-index: 1000;
  background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.1); border-radius: 12px;
  padding: 16px 20px; display: none; opacity: 0; transition: all 0.4s;
  transform: translateY(10px);
}
.insight-glass.show { display: block; opacity: 1; transform: translateY(0); }
.insight-glass .i-label { font-size: 10px; text-transform: uppercase; letter-spacing: 1.5px; color: var(--accent); font-weight: 700; margin-bottom: 6px; }
.insight-glass .i-text { font-size: 13px; line-height: 1.6; color: rgba(255,255,255,0.9); }

/* ---- Chart container ---- */
.chart-container { position: relative; height: 300px; width: 100%; margin-top: 10px; }

/* ---- Score rings ---- */
.score-ring-wrap { display: flex; gap: 30px; justify-content: center; margin: 10px 0; }
.score-ring-item { display: flex; flex-direction: column; align-items: center; gap: 8px; }
.score-ring-item .srl { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: var(--text-dim); font-weight: 600;}
.score-ring { width: 70px; height: 70px; position: relative; }
.score-ring svg { width: 100%; height: 100%; transform: rotate(-90deg); filter: drop-shadow(0 0 8px rgba(79, 70, 229, 0.4)); }
.score-ring .bg-c { fill: none; stroke: rgba(255,255,255,0.05); stroke-width: 4; }
.score-ring .fg-c { fill: none; stroke-width: 4; stroke-linecap: round; transition: stroke-dashoffset 1.5s cubic-bezier(0.16, 1, 0.3, 1); }
.score-ring .fg-c.invest { stroke: var(--primary); }
.score-ring .fg-c.safety { stroke: var(--accent); }
.score-ring .sv { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; font-size: 18px; font-weight: 800; color: #fff; }

/* ---- Financial sliders ---- */
.fin-row { display: flex; gap: 20px; margin-bottom: 16px; }
.fin-row > div { flex: 1; }
.fin-stat { display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 14px; font-weight: 500;}
.fin-stat:last-child { border-bottom: none; }
.fin-stat .val { font-weight: 800; color: #fff; }
.fin-stat .val.accent { color: var(--accent); font-size: 18px; }

/* ---- PDF preview ---- */
.pdf-preview { background: #fff; border-radius: 12px; padding: 32px; color: #1e293b; max-width: 540px; margin: 0 auto; font-size: 13px; line-height: 1.6; box-shadow: 0 20px 40px rgba(0,0,0,0.2); }
.pdf-preview h4 { font-size: 20px; color: #0f172a; margin-bottom: 4px; font-weight: 800;}
.pdf-preview .p-sub { color: #64748b; font-size: 12px; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600;}
.pdf-preview table { width: 100%; border-collapse: collapse; margin-bottom: 16px; }
.pdf-preview td { padding: 10px 12px; border-bottom: 1px solid #e2e8f0; font-size: 13px; }
.pdf-preview td:first-child { font-weight: 600; color: #475569; width: 40%; }
.pdf-preview .ph { font-size: 20px; font-weight: 800; color: var(--primary); }

/* ---- Amenities ---- */
.amenity-filter.active { border-color: var(--primary) !important; background: var(--primary) !important; color: #fff !important; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4); }
.amenity-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin-top: 20px; }
.amenity-card { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 20px; display: flex; flex-direction: column; gap: 16px; transition: all 0.3s; }
.amenity-card:hover { transform: translateY(-4px); background: rgba(255,255,255,0.04); border-color: rgba(255,255,255,0.1); box-shadow: 0 10px 25px rgba(0,0,0,0.2);}
.amenity-card-header { display: flex; align-items: center; gap: 12px; font-size: 15px; font-weight: 800; color: #fff; text-transform: uppercase; letter-spacing: 1px; }
.amenity-card-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
.amenity-card-list { display: flex; flex-direction: column; gap: 10px; }
.amenity-card-item { display: flex; justify-content: space-between; align-items: center; font-size: 14px; color: var(--text-dim); }
.amenity-card-item .a-name { font-weight: 500; color: var(--text); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 75%; }
.amenity-card-item .a-dist { font-size: 12px; font-weight: 700; color: rgba(255,255,255,0.5); }

/* ---- Chatbot ---- */
.chat-msg.bot .bot-icon { width: 36px; height: 36px; border-radius: 10px; background: linear-gradient(135deg, var(--primary), var(--secondary)); display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; box-shadow: 0 4px 10px rgba(236, 72, 153, 0.3);}
.chat-msg.user .bubble { display: inline-block; background: linear-gradient(135deg, var(--primary), var(--secondary)); padding: 12px 16px; border-radius: 16px 16px 4px 16px; font-size: 14px; color: #fff; max-width: 75%; text-align: left; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2); }
.chat-msg.bot .bubble { display: inline-block; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); padding: 12px 16px; border-radius: 16px 16px 16px 4px; font-size: 14px; color: var(--text); max-width: 80%; line-height: 1.6; }

/* ---- Animations ---- */
@keyframes spin { to { transform: rotate(360deg); } }

/* Include Google Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
"""

pattern = re.compile(r'<style>.*?</style>', re.DOTALL)
new_content = pattern.sub(f'<style>\n{new_css}\n</style>', content)

with open('predictor/templates/index.html', 'w') as f:
    f.write(new_content)
print("CSS updated successfully")
