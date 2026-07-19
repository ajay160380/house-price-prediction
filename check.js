              <div class="score-ring-item">
                <span class="srl">Safety &amp; Infrastructure</span>
                <div class="score-ring"><svg viewBox="0 0 36 36"><circle class="bg-c" cx="18" cy="18" r="15"/><circle class="fg-c safety" id="safetyRing" cx="18" cy="18" r="15"/></svg><span class="sv" id="safetyScore">—</span></div>
              </div>
            </div>
          </div>
          <div class="bento-card">
            <div class="b-title">📍 Location Insight</div>
            <p id="analyticsInsight" style="font-size:13px;line-height:1.6;color:var(--text-dim)">Select a location on the Predictor tab to see AI-powered market analysis here.</p>
          </div>
        </div>
      </section>

      <!-- ===== TAB 3: FINANCIAL HUB ===== -->
      <section id="tab-financial" class="tab-content">
        <div class="bento-grid cols-2">
          <div class="bento-card span-2">
            <div class="b-title">💳 EMI Calculator</div>
            <div class="fin-row">
              <div class="form-group">
                <label>Loan Amount (₹ Lakhs)</label>
                <input type="number" id="emiLoanAmt" value="75" min="1" step="0.5">
              </div>
              <div class="form-group">
                <label>Interest Rate: <strong id="emiRateLabel">8.5%</strong></label>
                <input type="range" id="emiRate" min="1" max="15" value="8.5" step="0.1">
                <div class="range-labels"><span>1%</span><span>15%</span></div>
              </div>
              <div class="form-group">
                <label>Tenure: <strong id="emiTenureLabel">20 Years</strong></label>
                <input type="range" id="emiTenure" min="5" max="30" value="20" step="1">
                <div class="range-labels"><span>5 Yrs</span><span>30 Yrs</span></div>
              </div>
            </div>
            <div>
              <div class="fin-stat"><span>Monthly EMI</span><span class="val accent" id="emiMonthly">₹ 0</span></div>
              <div class="fin-stat"><span>Total Interest Payable</span><span class="val" id="emiTotalInt">₹ 0</span></div>
              <div class="fin-stat"><span>Total Payment</span><span class="val" id="emiTotalPay">₹ 0</span></div>
            </div>
          </div>
          <div class="bento-card span-2">
            <div class="b-title">📈 Rental Yield Estimator</div>
            <div class="fin-row">
              <div class="form-group">
                <label>Property Value (₹ Lakhs)</label>
                <input type="number" id="rentPrice" value="75" min="1" step="0.5">
              </div>
              <div class="form-group">
                <label>Expected Monthly Rent (₹)</label>
                <input type="number" id="rentMonthly" value="25000" min="1000" step="1000">
              </div>
            </div>
            <div>
              <div class="fin-stat"><span>Annual Rent</span><span class="val" id="rentAnnual">₹ 3,00,000</span></div>
              <div class="fin-stat"><span>Gross Rental Yield</span><span class="val accent" id="rentYield">4.00%</span></div>
            </div>
          </div>
        </div>
      </section>

      <!-- ===== TAB 4: CLIENT REPORTS ===== -->
      <section id="tab-reports" class="tab-content">
        <div class="bento-grid cols-2">
          <div class="bento-card span-2" style="text-align:center">
            <div class="b-title">📄 White-Label Property Pitch</div>
            <p style="font-size:13px;color:var(--text-dim);margin-bottom:16px">Generate a professional PDF report with all property insights, AI analysis, forecast data, and EMI breakdown.</p>
            <div class="pdf-preview" id="pdfPreview">
              <h4>🏡 EstateAI Property Report</h4>
              <div class="p-sub">Bengaluru Real Estate Intelligence</div>
              <table>
                <tr><td>Property</td><td id="ppSqft">1,500 sqft · 2 BHK</td></tr>
                <tr><td>Location</td><td id="ppLoc">Whitefield</td></tr>
                <tr><td>Est. Value</td><td class="ph" id="ppPrice">₹ 79.80 Lakhs</td></tr>
                <tr><td>AI Investment Score</td><td id="ppInvest">8/10</td></tr>
                <tr><td>Projected (Year 5)</td><td class="ph" id="ppFuture">₹ 1.07 Cr</td></tr>
              </table>
            </div>
            <div style="margin-top:18px;display:flex;gap:12px;justify-content:center;flex-wrap:wrap">
              <button class="btn-primary" id="pdfGenBtn" style="max-width:320px">📥 Generate &amp; Download PDF</button>
            </div>
          </div>
        </div>
      </section>

      <!-- ===== TAB 5: AMENITIES ===== -->
      <section id="tab-amenities" class="tab-content">
        <div class="bento-grid cols-2">
          <div class="bento-card span-2">
            <div class="b-title">📍 Nearby Places <span style="float:right;font-size:12px;text-transform:none;letter-spacing:0;" id="amenityLocationLabel">Select a location first</span></div>
            <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px" id="amenityFilterBar">
              <button class="btn-secondary amenity-filter active" data-cat="all">All</button>
              <button class="btn-secondary amenity-filter" data-cat="school">🏫 Schools</button>
              <button class="btn-secondary amenity-filter" data-cat="hospital">🏥 Hospitals</button>
              <button class="btn-secondary amenity-filter" data-cat="metro">🚇 Metro</button>
              <button class="btn-secondary amenity-filter" data-cat="park">🌳 Parks</button>
              <button class="btn-secondary amenity-filter" data-cat="restaurant">🍽️ Restaurants</button>
              <button class="btn-secondary amenity-filter" data-cat="mall">🛍️ Malls</button>
              <button class="btn-secondary amenity-filter" data-cat="bus_stop">🚌 Bus Stops</button>
            </div>
            <div class="loading" id="amenityLoading" style="display:none !important"><span class="spinner"></span> Fetching nearby places via OpenStreetMap...</div>
            <div id="amenityResults">
              <p style="color:var(--text-dim);font-size:13px;">Predict a property to discover nearby schools, hospitals, metro stations, parks, restaurants, malls, and bus stops.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- ===== TAB 6: LOCALITY SCORES ===== -->
      <section id="tab-scores" class="tab-content">
        <div class="bento-grid cols-2">
          <div class="bento-card span-full">
            <div class="b-title">📊 Locality Score <span style="float:right;font-size:24px;font-weight:800;background:linear-gradient(135deg,#667eea,#00d4ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;" id="overallScoreDisplay">—</span></div>
            <div id="scoresContent">
              <p style="color:var(--text-dim);font-size:13px;">Predict a property first to see locality scores based on nearby amenities.</p>
            </div>
          </div>
          <div class="bento-card span-full">
            <div class="b-title">📈 Score Breakdown</div>
            <div id="scoreBars">
              <p style="color:var(--text-dim);font-size:13px;">Scores will appear here after prediction.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- ===== TAB 7: AI ANALYSIS ===== -->
      <section id="tab-aianalysis" class="tab-content">
        <div class="bento-grid cols-2">
          <div class="bento-card span-full">
            <div class="b-title">🤖 AI Investment Analysis <span style="float:right;font-size:11px;text-transform:none;letter-spacing:0;" id="analysisLocationLabel"></span></div>
            <div class="loading" id="analysisLoading"><span class="spinner"></span> Generating AI analysis with Groq...</div>
            <div id="analysisContent">
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:18px" id="analysisMetrics">
                <div class="bento-card" style="text-align:center"><div class="b-title">Investment Potential</div><p style="font-size:22px;font-weight:700;color:#e8e8f0;" id="aiInvest">—</p></div>
                <div class="bento-card" style="text-align:center"><div class="b-title">Rental Demand</div><p style="font-size:22px;font-weight:700;color:#e8e8f0;" id="aiRental">—</p></div>
              </div>
              <div id="analysisProsCons" style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:18px">
                <div class="bento-card"><div class="b-title">✅ Pros</div><ul id="aiPros" style="list-style:none;padding:0;font-size:13px;color:var(--text-dim);line-height:1.7"></ul></div>
                <div class="bento-card"><div class="b-title">⚠️ Cons</div><ul id="aiCons" style="list-style:none;padding:0;font-size:13px;color:var(--text-dim);line-height:1.7"></ul></div>
              </div>
              <div class="bento-card"><div class="b-title">📈 Future Growth</div><p id="aiFutureGrowth" style="font-size:13px;line-height:1.6;color:var(--text-dim)">—</p></div>
              <div class="bento-card"><div class="b-title">🎯 Recommendation</div><p id="aiRecommendation" style="font-size:13px;line-height:1.6;color:var(--text-dim)">—</p></div>
            </div>
          </div>
        </div>
      </section>

      <!-- ===== TAB 8: AI CHATBOT ===== -->
      <section id="tab-chatbot" class="tab-content">
        <div class="bento-grid cols-2">
          <div class="bento-card span-full">
            <div class="b-title">💬 AI Property Assistant <span style="float:right;font-size:11px;text-transform:none;letter-spacing:0;color:var(--accent);">Powered by Groq</span></div>
            <div id="chatMessages" style="height:320px;overflow-y:auto;padding:12px;background:rgba(255,255,255,0.02);border-radius:10px;border:1px solid rgba(255,255,255,0.06);margin-bottom:12px;">
              <div class="chat-msg bot">
                <div style="display:flex;gap:10px;margin-bottom:12px;"><div style="width:30px;height:30px;border-radius:8px;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;">🤖</div><div style="background:rgba(255,255,255,0.04);padding:10px 14px;border-radius:10px;font-size:13px;color:var(--text-dim);line-height:1.5;max-width:80%;">Hello! I'm your EstateAI property assistant. Ask me anything about Bengaluru real estate — prices, localities, investment tips, or market trends!</div></div>
              </div>
            </div>
            <div style="display:flex;gap:8px;">
              <input type="text" id="chatInput" placeholder="Ask about Bengaluru real estate..." style="flex:1;padding:10px 14px;border-radius:9px;background:rgba(255,255,255,0.05);border:1.5px solid var(--glass-border);color:var(--text);font-size:13px;outline:none;">
              <button class="btn-primary" id="chatSendBtn" style="width:auto;padding:10px 24px;">Send</button>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</div>

<!-- Hidden PDF Template -->
<div id="pdfTemplate" style="display:none">
  <div style="font-family:'Segoe UI',Arial,sans-serif;padding:28px;color:#1a1a2e;background:#fff">
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px">
      <div style="width:36px;height:36px;border-radius:8px;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;color:#fff;font-size:18px">🏡</div>
      <div><h1 style="font-size:20px;margin:0;color:#1a1a2e">EstateAI Property Report</h1><div style="font-size:12px;color:#666">Bengaluru Real Estate Intelligence</div></div>
    </div>
    <div style="font-size:15px;font-weight:700;color:#667eea;margin:18px 0 8px;padding-bottom:3px;border-bottom:2px solid #667eea">Property Overview</div>
    <table style="width:100%;border-collapse:collapse;margin-bottom:12px;font-size:13px">
      <tr><td style="padding:6px 10px;border-bottom:1px solid #e0e0e0;font-weight:600;color:#333;width:40%">Area</td><td style="padding:6px 10px;border-bottom:1px solid #e0e0e0" id="pdfSqft"></td></tr>
      <tr><td style="padding:6px 10px;border-bottom:1px solid #e0e0e0;font-weight:600;color:#333">Configuration</td><td style="padding:6px 10px;border-bottom:1px solid #e0e0e0" id="pdfConfig"></td></tr>
      <tr><td style="padding:6px 10px;border-bottom:1px solid #e0e0e0;font-weight:600;color:#333">Location</td><td style="padding:6px 10px;border-bottom:1px solid #e0e0e0" id="pdfLocation"></td></tr>
      <tr><td style="padding:6px 10px;border-bottom:1px solid #e0e0e0;font-weight:600;color:#333">Estimated Value</td><td style="padding:6px 10px;border-bottom:1px solid #e0e0e0;font-size:18px;font-weight:800;color:#667eea" id="pdfPrice"></td></tr>
      <tr><td style="padding:6px 10px;font-weight:600;color:#333">Price Range</td><td style="padding:6px 10px" id="pdfRange"></td></tr>
    </table>
    <div style="font-size:15px;font-weight:700;color:#667eea;margin:18px 0 8px;padding-bottom:3px;border-bottom:2px solid #667eea">AI Market Intelligence</div>
    <p style="font-size:13px;line-height:1.6;color:#333;margin-bottom:8px" id="pdfInsight"></p>
    <table style="width:100%;border-collapse:collapse;margin-bottom:12px;font-size:13px">
      <tr><td style="padding:6px 10px;border-bottom:1px solid #e0e0e0;font-weight:600;color:#333">Investment Score</td><td style="padding:6px 10px;border-bottom:1px solid #e0e0e0" id="pdfInvest"></td></tr>
      <tr><td style="padding:6px 10px;font-weight:600;color:#333">Safety Score</td><td style="padding:6px 10px" id="pdfSafety"></td></tr>
    </table>
    <div style="font-size:15px;font-weight:700;color:#667eea;margin:18px 0 8px;padding-bottom:3px;border-bottom:2px solid #667eea">5-Year Forecast &amp; EMI</div>
    <table style="width:100%;border-collapse:collapse;margin-bottom:12px;font-size:13px">
      <tr><td style="padding:6px 10px;border-bottom:1px solid #e0e0e0;font-weight:600;color:#333">Projected Value (Year 5)</td><td style="padding:6px 10px;border-bottom:1px solid #e0e0e0;font-size:18px;font-weight:800;color:#667eea" id="pdfFuture"></td></tr>
      <tr><td style="padding:6px 10px;border-bottom:1px solid #e0e0e0;font-weight:600;color:#333">Monthly EMI</td><td style="padding:6px 10px;border-bottom:1px solid #e0e0e0" id="pdfEMI"></td></tr>
      <tr><td style="padding:6px 10px;font-weight:600;color:#333">Total Payment</td><td style="padding:6px 10px" id="pdfTotalPay"></td></tr>
    </table>
    <div style="font-size:10px;color:#999;text-align:center;margin-top:16px;padding-top:10px;border-top:1px solid #e0e0e0">Generated by EstateAI — Powered by Groq AI + Scikit-Learn | Bengaluru, India</div>
  </div>
</div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
(function() {
  // ===== TAB SYSTEM =====
  const tabTitles = {
    predictor: ['Predictor Engine', 'Real-time ML property valuation'],
    analytics: ['Market Analytics', 'Deep data & AI-powered insights'],
    financial: ['Financial Hub', 'EMI & rental yield calculators'],
    reports: ['Client Reports', 'White-label PDF report generation'],
    amenities: ['Nearby Places', 'Schools, hospitals, metro & more'],
    scores: ['Locality Scores', 'Education, healthcare, transport, lifestyle'],
    aianalysis: ['AI Investment Analysis', 'Groq-powered pro & con analysis'],
    chatbot: ['AI Property Assistant', 'Ask anything about Bengaluru real estate'],
  };
  const tabTitleEl = document.getElementById('tabTitle');
  const tabSubEl = document.getElementById('tabSub');
  let currentTab = 'predictor';

  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', function() {
      const tab = this.dataset.tab;
      if (tab === currentTab) return;
      document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
      this.classList.add('active');
      document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
      const target = document.getElementById('tab-' + tab);
      target.classList.add('active');
      const info = tabTitles[tab] || ['Dashboard', ''];
      tabTitleEl.textContent = info[0];
      tabSubEl.textContent = info[1];
      currentTab = tab;

      // Handle chart resize when switching to analytics
      if (tab === 'analytics' && trendChartInstance) {
        setTimeout(() => trendChartInstance.resize(), 150);
      }
      // Handle map resize when switching to predictor
      if (tab === 'predictor' && window.mapInstance) {
        setTimeout(() => window.mapInstance.invalidateSize(), 200);
      }
    });
  });

  // ===== DOM REFS =====
  const form = document.getElementById('predictForm');
  const sqftSlider = document.getElementById('sqftSlider');
  const sliderValue = document.getElementById('sliderValue');
  const locationSelect = document.getElementById('location');
  const loading = document.getElementById('loading');
  const resultBadge = document.getElementById('resultBadge');
  const priceRange = document.getElementById('priceRange');
  const basePrice = document.getElementById('basePrice');
  const insightGlass = document.getElementById('insightGlass');
  const insightText = document.getElementById('insightText');
  const mInvest = document.getElementById('mInvest');
  const mSafety = document.getElementById('mSafety');
  const investScore = document.getElementById('investScore');
  const safetyScore = document.getElementById('safetyScore');
  const investRing = document.getElementById('investRing');
  const safetyRing = document.getElementById('safetyRing');
  const analyticsInsight = document.getElementById('analyticsInsight');
  let currentInvestScore = '—';
  let currentSafetyScore = '—';

  // ===== INDIAN CURRENCY FORMATTER =====
  function formatIndianCurrency(valueInLakhs) {
    const val = Number(valueInLakhs);
    if (val < 100) return '₹ ' + val.toFixed(2) + ' Lakhs';
    return '₹ ' + (val / 100).toFixed(2) + ' Cr';
  }
  function fmtShort(v) {
    const val = Number(v);
    if (val < 100) return '₹ ' + val.toFixed(2) + ' L';
    return '₹ ' + (val / 100).toFixed(2) + ' Cr';
  }

  // ===== SLIDER =====
  function updateSlider(val) {
    const pct = ((val - 300) / (5000 - 300)) * 100;
    sliderValue.textContent = Number(val).toLocaleString('en-IN') + ' sqft';
    sliderValue.style.left = 'calc(' + pct + '% - ' + (pct * 0.18) + 'px)';
    sqftSlider.style.background = 'linear-gradient(to right, #667eea ' + pct + '%, rgba(255,255,255,0.1) ' + pct + '%)';
  }
  sqftSlider.addEventListener('input', function() { updateSlider(this.value); });
  updateSlider(sqftSlider.value);

  // ===== CUSTOM RADIO =====
  document.querySelectorAll('.selector-item input[type="radio"]').forEach(r => {
    r.addEventListener('change', function() {
      this.closest('.selector-grid').querySelectorAll('input[type="radio"]').forEach(s => s.checked = (s === this));
    });
  });

  const locationCoords = {
    "Jayanagar":[12.9299,77.5883],"Malleshwaram":[12.9975,77.5699],"Basavangudi":[12.9417,77.5705],
    "Rajaji Nagar":[12.9900,77.5528],"Vijayanagar":[12.9719,77.5331],"Sadashiva Nagar":[12.9960,77.5800],
    "Ulsoor":[12.9823,77.6200],"Domlur":[12.9610,77.6387],"HAL Airport":[12.9500,77.6680],
    "Murugeshpalya":[12.9593,77.6570],"Old Airport Road":[12.9550,77.6600],"CV Raman Nagar":[12.9814,77.6600],
    "Hoodi":[12.9959,77.7162],"Brookefield":[12.9694,77.7107],"Kundalahalli":[12.9631,77.7125],
    "KR Puram":[12.9988,77.7012],"Mahadevpura":[12.9865,77.6966],"Banaswadi":[12.9898,77.6403],
    "RT Nagar":[13.0200,77.5950],"Sanjay Nagar":[13.0200,77.6070],"Jakkur":[13.0750,77.6050],
    "Yelahanka New Town":[13.1000,77.5900],"Thanisandra":[13.0550,77.6300],"Nagavara":[13.0450,77.6150],
    "Kannamangala":[12.9800,77.7300],"Hoskote":[13.0700,77.7980],"Sarjapur":[12.8600,77.6850],
    "Attibele":[12.8300,77.7700],"Anekal":[12.7100,77.6950],"Jigani":[12.7800,77.6400],
    "Bommasandra":[12.8200,77.6600],"Chandapura":[12.8000,77.6900],"Begur":[12.8700,77.6200],
    "Gottigere":[12.8700,77.5800],"Uttarahalli":[12.9000,77.5400],"Kengeri":[12.9100,77.4800],
    "Nagarbhavi":[12.9600,77.5100],"Laggere":[12.9900,77.5300],"Peenya":[13.0300,77.5200],
    "Yeshwanthpur":[13.0200,77.5450],"Mathikere":[13.0100,77.5650],"Vidyaranyapura":[13.0800,77.5800],
    "Dasarahalli":[13.0600,77.5400],"Magadi Road":[12.9700,77.5500],"Mysore Road":[12.9400,77.5200],
    "Kanakpura Road":[12.8800,77.5600],"Bannerghatta Road":[12.8800,77.5950],"Hulimavu":[12.8800,77.6100],
    "Arekere":[12.8900,77.6000],"Bommanahalli":[12.9000,77.6200],"HSR Layout Sector 2":[12.9120,77.6390],
    "HSR Layout Sector 7":[12.9080,77.6430],"Haralur Road":[12.9000,77.6500],"Hosa Road":[12.8950,77.6680],
    "Electronic City Phase II":[12.8350,77.6600],"Electronics City Phase 1":[12.8450,77.6600],
    "EPIP Zone":[12.9400,77.6900],"ITPL":[12.9600,77.7100],"Bannerghatta":[12.8000,77.5800],
    "AECS Layout":[12.9550,77.7200],"Singasandra":[12.8850,77.6250],"Kadugodi":[12.9900,77.7500],
    "Kaggadasapura":[12.9700,77.6850],"Amruthahalli":[13.0600,77.6100],"Kodigehalli":[13.0500,77.6200]
  };
  const BLR_CENTER = [12.9716, 77.5946];

  async function loadLocations() {
    try {
      const res = await fetch('/get_location_names');
      const data = await res.json();
      data.locations.forEach(loc => {
        const opt = document.createElement('option');
        opt.value = loc; opt.textContent = loc;
        locationSelect.appendChild(opt);
      });
    } catch(e) { console.error('Locations fetch failed:', e); }
  }

  // ===== MAP =====
  const mapFrame = document.getElementById('map');
  const mapLoading = document.getElementById('mapLoading');

  let currentAmenities = null;
  let currentAmenityFilter = 'all';

  function updateMapLegend(amenities) {
    const legend = document.getElementById('mapLegend');
    if (!legend) return;
    const rows = legend.querySelectorAll('.ml-row[data-cat]');
    let hasData = false;
    rows.forEach(r => {
      const cat = r.getAttribute('data-cat');
      if (amenities && amenities[cat] && amenities[cat].length > 0) {
        r.classList.add('active');
        hasData = true;
      } else {
        r.classList.remove('active');
      }
    });
    const propRow = legend.querySelector('.ml-row:not([data-cat])');
    if(propRow) propRow.classList.add('active');
    
    if (hasData) {
      legend.classList.add('active');
    } else {
      legend.classList.remove('active');
    }
  }

  async function geocodeAndUpdateMap(location) {
    mapLoading.classList.remove('hidden');
    
    // Update Google Maps iframe
    const q = encodeURIComponent(location + ', Bengaluru, Karnataka, India');
    mapFrame.src = 'https://maps.google.com/maps?q=' + q + '&t=m&z=14&output=embed';
    
    document.getElementById('mapLabel').textContent = '📍 ' + location;
    updateMapLegend(null);
    
    try {
      const fd = new FormData();
      fd.append('location', location);
      const r = await fetch('/get_nearby_amenities', { method: 'POST', body: fd });
      const d = await r.json();
      if (d.amenities && d.total > 0) {
        currentAmenities = d.amenities;
        updateMapLegend(d.amenities);
      }
    } catch(e) { console.warn('Map amenities fetch failed:', e); }

    mapLoading.classList.add('hidden');
  }

  // ===== SCORE RING HELPER =====
  function setScoreRing(ringEl, valEl, score) {
    const circ = 2 * Math.PI * 15;
    const off = circ - (score / 10) * circ;
    ringEl.style.strokeDasharray = circ;
    ringEl.style.strokeDashoffset = circ;
    valEl.textContent = score;
    requestAnimationFrame(() => { ringEl.style.strokeDashoffset = off; });
  }

  // ===== AI INSIGHTS =====
  async function fetchInsight(location) {
    if (!location) return;
    try {
      const fd = new FormData(); fd.append('location', location);
      const res = await fetch('/get_location_insights', { method:'POST', body:fd });
      const data = await res.json();
      const txt = data.insight_text || 'No insight available.';
      const inv = data.investment_score || 7;
      const saf = data.safety_score || 7;
      currentInvestScore = inv;
      currentSafetyScore = saf;
      insightText.textContent = txt;
      mInvest.textContent = inv; mSafety.textContent = saf;
      setScoreRing(investRing, investScore, inv);
      setScoreRing(safetyRing, safetyScore, saf);
      analyticsInsight.textContent = txt;
      insightGlass.classList.add('show');
      document.getElementById('ppInvest').textContent = inv + '/10';
    } catch(e) {
      insightText.textContent = 'Unable to fetch AI insight.';
      insightGlass.classList.add('show');
    }
  }

  locationSelect.addEventListener('change', function() {
    const loc = this.value;
    insightGlass.classList.remove('show');
    if (!loc) return;
    geocodeAndUpdateMap(loc);
    fetchInsight(loc);
  });

  // ===== CHART =====
  let trendChartInstance = null;

  function buildForecast(base) {
    const labels = ['Now', 'Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'];
    const rates = [0, 0.06, 0.055, 0.065, 0.06, 0.07];
    const vals = [base];
    for (let i = 1; i <= 5; i++) {
      const j = (Math.random() - 0.5) * 0.02;
      vals.push(+(vals[i-1] * (1 + rates[i] + j)).toFixed(2));
    }
    vals[0] = base;
    return { labels, values: vals };
  }

  function renderChart(basePriceLakhs) {
    const canvas = document.getElementById('trendChart');
    if (!canvas) return null;
    const ctx = canvas.getContext('2d');
    if (trendChartInstance) trendChartInstance.destroy();
    const { labels, values } = buildForecast(basePriceLakhs);
    const grad = ctx.createLinearGradient(0, 0, 0, 240);
    grad.addColorStop(0, 'rgba(102,126,234,0.2)');
    grad.addColorStop(1, 'rgba(102,126,234,0)');
    trendChartInstance = new Chart(ctx, {
      type:'line',
      data:{ labels, datasets:[{ data:values, borderColor:'#667eea', backgroundColor:grad, borderWidth:2.5, fill:true, tension:0.35, pointBackgroundColor:'#00d4ff', pointBorderColor:'#0a0a12', pointBorderWidth:2, pointRadius:4, pointHoverRadius:6 }] },
      options:{
        responsive:true, maintainAspectRatio:false,
        plugins:{ legend:{ display:false }, tooltip:{ enabled:true, backgroundColor:'#1a1a2e', titleColor:'#e8e8f0', bodyColor:'#999aaf', borderColor:'rgba(255,255,255,0.1)', borderWidth:1, callbacks:{ label:function(ctx){ var v=ctx.parsed.y; return v>=100?'₹ '+(v/100).toFixed(2)+' Cr':'₹ '+v.toFixed(2)+' L'; } } } },
        scales:{ x:{ grid:{ color:'rgba(255,255,255,0.03)' }, ticks:{ color:'#999aaf', font:{ size:10 } } }, y:{ grid:{ color:'rgba(255,255,255,0.03)' }, ticks:{ color:'#999aaf', font:{ size:10 }, callback:function(v){ return v>=100?'₹'+(v/100).toFixed(1)+'Cr':'₹'+v.toFixed(1)+'L'; } } } }
      }
    });
    return { labels, values };
  }

  // ===== PREDICT =====
  let lastPredictionData = null;

  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    resultBadge.classList.remove('show');
    loading.classList.add('show');

    const formData = new FormData(form);
    formData.set('sqft', sqftSlider.value);

    try {
      const res = await fetch('/predict_home_price', { method:'POST', body:formData });
      const data = await res.json();
      loading.classList.remove('show');

      if (data.estimated_price !== undefined) {
        const low = data.estimated_price_low;
        const high = data.estimated_price_high;
        const base = data.estimated_price;
        priceRange.textContent = fmtShort(low) + ' — ' + fmtShort(high);
        basePrice.textContent = formatIndianCurrency(base);
        resultBadge.classList.add('show');

        lastPredictionData = {
          sqft: sqftSlider.value, bhk: document.querySelector('input[name="bhk"]:checked').value,
          bath: document.querySelector('input[name="bath"]:checked').value,
          location: locationSelect.value, price: data.estimated_price,
          priceLow: data.estimated_price_low, priceHigh: data.estimated_price_high,
        };

        // Update financial hub with predicted price
        document.getElementById('emiLoanAmt').value = data.estimated_price;
        document.getElementById('rentPrice').value = data.estimated_price;
        recalcEMI();
        recalcRent();

        // Update chart
        const chartResult = renderChart(data.estimated_price);
        if (chartResult) lastPredictionData.forecast = chartResult;

        // Update PDF preview
        if (currentInvestScore === '—' && locationSelect.value) {
          await fetchInsight(locationSelect.value);
        }
        updatePDFPreview(data);
      } else {
        priceRange.textContent = data.error || 'Prediction failed';
        resultBadge.classList.add('show');
      }
    } catch(err) {
      loading.classList.remove('show');
      priceRange.textContent = 'Network error.';
      resultBadge.classList.add('show');
    }
  });

  // ===== PDF PREVIEW =====
  function updatePDFPreview(data) {
    const loc = locationSelect.value || 'Whitefield';
    const sqft = sqftSlider.value;
    const bhk = document.querySelector('input[name="bhk"]:checked').value;
    const bath = document.querySelector('input[name="bath"]:checked').value;
    document.getElementById('ppSqft').textContent = Number(sqft).toLocaleString('en-IN') + ' sqft · ' + bhk + ' BHK';
    document.getElementById('ppLoc').textContent = loc;
    document.getElementById('ppPrice').textContent = formatIndianCurrency(data.estimated_price);
    document.getElementById('ppInvest').textContent = (currentInvestScore || '7') + '/10';
    const fv = data.estimated_price * Math.pow(1.06, 5);
    document.getElementById('ppFuture').textContent = formatIndianCurrency(fv);
  }

  // ===== FINANCIAL HUB: EMI (real-time) =====
  const emiLoanEl = document.getElementById('emiLoanAmt');
  const emiRateEl = document.getElementById('emiRate');
  const emiTenureEl = document.getElementById('emiTenure');
  const emiRateLabel = document.getElementById('emiRateLabel');
  const emiTenureLabel = document.getElementById('emiTenureLabel');

  function recalcEMI() {
    const P = parseFloat(emiLoanEl.value) * 100000;
    const r = parseFloat(emiRateEl.value) / 12 / 100;
    const n = parseInt(emiTenureEl.value) * 12;
    if (!P || !r || !n) return;
    const emi = P * r * Math.pow(1+r, n) / (Math.pow(1+r, n) - 1);
    const tp = emi * n;
    document.getElementById('emiMonthly').textContent = '₹ ' + Math.round(emi).toLocaleString('en-IN') + '/mo';
    document.getElementById('emiTotalInt').textContent = '₹ ' + Math.round(tp - P).toLocaleString('en-IN');
    document.getElementById('emiTotalPay').textContent = '₹ ' + Math.round(tp).toLocaleString('en-IN');
  }

  emiRateEl.addEventListener('input', function() {
    emiRateLabel.textContent = parseFloat(this.value).toFixed(1) + '%';
    recalcEMI();
  });
  emiTenureEl.addEventListener('input', function() {
    emiTenureLabel.textContent = this.value + ' Years';
    recalcEMI();
  });
  emiLoanEl.addEventListener('input', recalcEMI);

  // ===== FINANCIAL HUB: Rental Yield (real-time) =====
  const rentPriceEl = document.getElementById('rentPrice');
  const rentMonthlyEl = document.getElementById('rentMonthly');

  function recalcRent() {
    const p = parseFloat(rentPriceEl.value) * 100000;
    const m = parseFloat(rentMonthlyEl.value);
    if (!p || !m) return;
    const annual = m * 12;
    const yieldPct = (annual / p) * 100;
    document.getElementById('rentAnnual').textContent = '₹ ' + annual.toLocaleString('en-IN');
    document.getElementById('rentYield').textContent = yieldPct.toFixed(2) + '%';
  }

  rentPriceEl.addEventListener('input', recalcRent);
  rentMonthlyEl.addEventListener('input', recalcRent);

  // Initial calc
  recalcEMI();
  recalcRent();

  // ===== PDF GENERATION =====
  document.getElementById('pdfGenBtn').addEventListener('click', async function() {
    if (!lastPredictionData) {
      alert('Please run a prediction first on the Predictor tab.');
      return;
    }
    const d = lastPredictionData;
    const P = d.price * 100000;
    const r = 8.5 / 12 / 100;
    const n = 20 * 12;
    const emi = Math.round(P * r * Math.pow(1+r, n) / (Math.pow(1+r, n) - 1));
    const fv = d.forecast ? d.forecast.values[5] : +(d.price * Math.pow(1.06, 5)).toFixed(2);

    document.getElementById('pdfSqft').textContent = Number(d.sqft).toLocaleString('en-IN') + ' sqft';
    document.getElementById('pdfConfig').textContent = d.bhk + ' BHK, ' + d.bath + ' Bath';
    document.getElementById('pdfLocation').textContent = d.location;
    document.getElementById('pdfPrice').textContent = formatIndianCurrency(d.price);
    document.getElementById('pdfRange').textContent = fmtShort(d.priceLow) + ' — ' + fmtShort(d.priceHigh);
    document.getElementById('pdfInsight').textContent = insightText.textContent || 'AI insight available upon location selection.';
    document.getElementById('pdfInvest').textContent = (currentInvestScore || '7') + '/10';
    document.getElementById('pdfSafety').textContent = (currentSafetyScore || '7') + '/10';
    document.getElementById('pdfFuture').textContent = formatIndianCurrency(fv);
    document.getElementById('pdfEMI').textContent = '₹ ' + emi.toLocaleString('en-IN') + '/mo';
    document.getElementById('pdfTotalPay').textContent = '₹ ' + (emi * 12 * 20).toLocaleString('en-IN');

    this.disabled = true;
    this.textContent = '⏳ Generating...';
    try {
      await html2pdf().set({
        margin: [0.4, 0.4, 0.4, 0.4],
        filename: 'EstateAI_Report_' + d.location.replace(/\s+/g,'_') + '.pdf',
        image: { type:'jpeg', quality:0.95 },
        html2canvas: { scale: 2, useCORS: true, backgroundColor:'#ffffff' },
        jsPDF: { unit:'in', format:'a4', orientation:'portrait' }
      }).from(document.getElementById('pdfTemplate')).save();
    } catch(err) { console.error('PDF:', err); }
    this.disabled = false;
    this.innerHTML = '📥 Generate &amp; Download PDF';
  });

  // ===== AMENITY ICONS =====
  const amenityIcons = { school:'🏫', hospital:'🏥', metro:'🚇', park:'🌳', restaurant:'🍽️', mall:'🛍️', bus_stop:'🚌' };
  const amenityLabels = { school:'School', hospital:'Hospital', metro:'Metro', park:'Park', restaurant:'Restaurant', mall:'Mall', bus_stop:'Bus Stop' };
  let currentAmenities = null;
  let currentAmenityFilter = 'all';

  // ===== AMENITIES =====
  async function fetchAmenities(location, lat, lon) {
    const results = document.getElementById('amenityResults');
    const label = document.getElementById('amenityLocationLabel');
    results.innerHTML = '<p style="color:var(--text-dim);font-size:13px;">Loading nearby places...</p>';
    label.textContent = '📍 ' + location;
    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 90000);
      const fd = new FormData();
      fd.append('location', location);
      const res = await fetch('/get_nearby_amenities', { method:'POST', body:fd, signal:controller.signal });
      clearTimeout(timeout);
      const data = await res.json();
      if (data.error) {
        results.innerHTML = '<p style="color:var(--danger);font-size:13px;">⚠️ ' + data.error + '</p>';
        return;
      }
      if (data.amenities && data.total > 0) {
        currentAmenities = data.amenities;
        renderAmenities('all');
      } else {
        const note = data.note ? ': ' + data.note : ' for this location.';
        results.innerHTML = '<p style="color:var(--text-dim);font-size:13px;">No amenities found' + note + '</p>';
      }
    } catch(e) {
      if (e.name === 'AbortError') {
        results.innerHTML = '<p style="color:var(--danger);font-size:13px;">⚠️ Request timed out. The server took too long to respond.</p>';
      } else {
        results.innerHTML = '<p style="color:var(--danger);font-size:13px;">⚠️ Network error: ' + e.message + '</p>';
      }
    }
  }

  const AMENITY_BG = { school: 'rgba(52,152,219,0.15)', hospital: 'rgba(231,76,60,0.15)', metro: 'rgba(155,89,182,0.15)', park: 'rgba(46,204,113,0.15)', restaurant: 'rgba(230,126,34,0.15)', mall: 'rgba(241,196,15,0.15)', bus_stop: 'rgba(149,165,166,0.15)' };

  function renderAmenities(category) {
    const results = document.getElementById('amenityResults');
    currentAmenityFilter = category || 'all';
    let html = '<div class="amenity-grid">';
    let total = 0;
    const cats = currentAmenityFilter === 'all'
      ? Object.keys(currentAmenities)
      : [currentAmenityFilter];
    cats.forEach(cat => {
      const items = currentAmenities[cat] || [];
      if (items.length === 0) return;
      total += items.length;
      const bg = AMENITY_BG[cat] || 'rgba(255,255,255,0.1)';
      html += '<div class="amenity-card"><div class="amenity-card-header"><div class="amenity-card-icon" style="background:'+bg+'">' + (amenityIcons[cat]||'📍') + '</div>' + (amenityLabels[cat]||cat) + ' (' + items.length + ')</div><div class="amenity-card-list">';
      items.forEach(item => {
        const distStr = item.distance_km < 1 ? (item.distance_km*1000).toFixed(0)+'m' : item.distance_km.toFixed(2)+'km';
        html += '<div class="amenity-card-item"><span class="a-name" title="'+item.name+'">' + item.name + '</span><span class="a-dist">' + distStr + '</span></div>';
      });
      html += '</div></div>';
    });
    html += '</div>';
    if (total === 0) {
      html = '<p style="color:var(--text-dim);font-size:13px;padding:20px 0;">No ' + (currentAmenityFilter === 'all' ? '' : amenityLabels[currentAmenityFilter]) + ' amenities found nearby.</p>';
    }
    results.innerHTML = html;
  }

  document.querySelectorAll('.amenity-filter').forEach(btn => {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.amenity-filter').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      if (currentAmenities) renderAmenities(this.dataset.cat);
    });
  });

  // ===== LOCALITY SCORES =====
  function renderScores(scores) {
    const container = document.getElementById('scoreBars');
    const overallEl = document.getElementById('overallScoreDisplay');
    const content = document.getElementById('scoresContent');

    if (!scores) {
      container.innerHTML = '<p style="color:var(--text-dim);font-size:13px;">No score data available.</p>';
      return;
    }

    overallEl.textContent = scores.overall + '/10';

    const scoreItems = [
      { key:'education', label:'Education', color:'#667eea' },
      { key:'healthcare', label:'Healthcare', color:'#28a745' },
      { key:'transport', label:'Transport', color:'#00d4ff' },
      { key:'lifestyle', label:'Lifestyle', color:'#ff6b6b' },
    ];

    let barsHtml = '';
    scoreItems.forEach(si => {
      const val = scores[si.key] || 0;
      const pct = (val / 10) * 100;
      barsHtml += '<div class="score-bar-wrap"><div class="score-bar-label"><span class="sbl">' + si.label + '</span><span class="sbv">' + val.toFixed(1) + '/10</span></div><div class="score-bar"><div class="score-bar-fill" style="width:' + pct + '%;background:linear-gradient(90deg,' + si.color + ',' + si.color + '88);"></div></div></div>';
    });
    container.innerHTML = barsHtml;

    content.innerHTML = '<div style="text-align:center;padding:8px 0;"><span style="font-size:48px;font-weight:800;background:linear-gradient(135deg,#667eea,#00d4ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">' + scores.overall.toFixed(1) + '</span><span style="color:#999aaf;font-size:18px;">/10</span><br><span style="color:#999aaf;font-size:13px;text-transform:uppercase;letter-spacing:1.5px;">Overall Locality Score</span></div>';
  }

  // ===== AI ANALYSIS =====
  async function fetchAIAnalysis(location, price) {
    const loading = document.getElementById('analysisLoading');
    const label = document.getElementById('analysisLocationLabel');
    loading.classList.add('show');
    label.textContent = '📍 ' + location;
    try {
      const fd = new FormData();
      fd.append('location', location);
      fd.append('price', price || '');
      fd.append('amenities', JSON.stringify(currentAmenities || {}));
      const res = await fetch('/get_ai_analysis', { method:'POST', body:fd });
      const data = await res.json();
      loading.classList.remove('show');
      if (data.pros) {
        document.getElementById('aiInvest').textContent = data.investment_potential || '—';
        document.getElementById('aiRental').textContent = data.rental_demand || '—';
        document.getElementById('aiFutureGrowth').textContent = data.future_growth || '—';
        document.getElementById('aiRecommendation').textContent = data.recommendation || '—';
        const prosEl = document.getElementById('aiPros');
        const consEl = document.getElementById('aiCons');
        prosEl.innerHTML = data.pros.map(p => '<li style="margin-bottom:6px;">✅ ' + p + '</li>').join('');
        consEl.innerHTML = data.cons.map(c => '<li style="margin-bottom:6px;">⚠️ ' + c + '</li>').join('');
        if (data.breakdown_scores) renderScores(data.breakdown_scores);
      }
    } catch(e) {
      loading.classList.remove('show');
    }
  }

  // ===== CHATBOT =====
  const chatInput = document.getElementById('chatInput');
  const chatSendBtn = document.getElementById('chatSendBtn');
  const chatMessages = document.getElementById('chatMessages');
  let chatContext = {};

  function addChatMessage(text, isUser) {
    const div = document.createElement('div');
    if (isUser) {
      div.className = 'chat-msg user';
      div.innerHTML = '<div class="bubble">' + text.replace(/\n/g,'<br>') + '</div>';
    } else {
      div.className = 'chat-msg bot';
      div.innerHTML = '<div style="display:flex;gap:10px;"><div class="bot-icon">🤖</div><div class="bubble">' + text.replace(/\n/g,'<br>') + '</div></div>';
    }
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  async function sendChatMessage() {
    const msg = chatInput.value.trim();
    if (!msg) return;
    addChatMessage(msg, true);
    chatInput.value = '';
    chatInput.disabled = true;
    chatSendBtn.disabled = true;

    if (lastPredictionData) {
      chatContext = {
        location: lastPredictionData.location,
        price: lastPredictionData.price,
        scores: currentAmenities ? null : null,
      };
    }

    try {
      const fd = new FormData();
      fd.append('message', msg);
      fd.append('context', JSON.stringify(chatContext));
      const res = await fetch('/chatbot', { method:'POST', body:fd });
      const data = await res.json();
      addChatMessage(data.reply || "I couldn't process that. Please try again.", false);
    } catch(e) {
      addChatMessage("I'm having trouble connecting. Please check your network and try again.", false);
    }
    chatInput.disabled = false;
    chatSendBtn.disabled = false;
    chatInput.focus();
  }

  chatSendBtn.addEventListener('click', sendChatMessage);
  chatInput.addEventListener('keydown', function(e) { if (e.key === 'Enter') sendChatMessage(); });

  // ===== HOOK INTO LOCATION CHANGE =====
  locationSelect.addEventListener('change', function() {
    const loc = this.value;
    if (loc) {
      fetchAmenities(loc, null, null);
      fetchAIAnalysis(loc, lastPredictionData ? lastPredictionData.price : '');
    }
  });

  // ===== HOOK INTO PREDICTION =====
  form.addEventListener('submit', function() {
    setTimeout(() => {
      const loc = locationSelect.value;
      if (loc && lastPredictionData) {
        fetchAmenities(loc, null, null);
        fetchAIAnalysis(loc, lastPredictionData.price);
      }
    }, 1500);
  });

  // ===== INIT =====
  loadLocations();
})();
</script>
</body>
</html>
