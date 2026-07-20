import re

with open('predictor/templates/index.html', 'r') as f:
    html = f.read()

# 1. Insert the HTML for tab-compare
compare_html = """
      <!-- ===== TAB: COMPARE LOCALITIES ===== -->
      <section id="tab-compare" class="tab-content">
        <div class="bento-grid cols-2">
          
          <!-- Selectors -->
          <div class="bento-card span-2" style="display:flex; gap:20px;">
            <div class="form-group" style="flex:1;">
              <label style="color:#c9a96e;">Location A (Gold)</label>
              <select id="compareLocA" class="loc-dropdown"><option value="">Select first neighborhood...</option></select>
            </div>
            <div class="form-group" style="flex:1;">
              <label style="color:#3498db;">Location B (Blue)</label>
              <select id="compareLocB" class="loc-dropdown"><option value="">Select second neighborhood...</option></select>
            </div>
          </div>

          <!-- Financial Duel -->
          <div class="bento-card">
            <div class="b-title">Price & ROI Duel</div>
            <div style="margin-top:20px; display:flex; flex-direction:column; gap:24px;">
                <div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                        <span id="cA_Price" style="color:#c9a96e; font-weight:bold;">₹ -- L</span>
                        <span style="font-size:12px; color:var(--text-secondary);">Avg Price</span>
                        <span id="cB_Price" style="color:#3498db; font-weight:bold;">₹ -- L</span>
                    </div>
                    <div style="width:100%; height:8px; background:#222; border-radius:4px; display:flex;">
                        <div id="cA_PriceBar" style="height:100%; background:#c9a96e; width:50%; border-radius:4px 0 0 4px; box-shadow:0 0 10px #c9a96e66;"></div>
                        <div id="cB_PriceBar" style="height:100%; background:#3498db; width:50%; border-radius:0 4px 4px 0; box-shadow:0 0 10px #3498db66;"></div>
                    </div>
                </div>
                <div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                        <span id="cA_Yield" style="color:#c9a96e; font-weight:bold;">-- %</span>
                        <span style="font-size:12px; color:var(--text-secondary);">Rental Yield</span>
                        <span id="cB_Yield" style="color:#3498db; font-weight:bold;">-- %</span>
                    </div>
                    <div style="width:100%; height:8px; background:#222; border-radius:4px; display:flex;">
                        <div id="cA_YieldBar" style="height:100%; background:#c9a96e; width:50%; border-radius:4px 0 0 4px; box-shadow:0 0 10px #c9a96e66;"></div>
                        <div id="cB_YieldBar" style="height:100%; background:#3498db; width:50%; border-radius:0 4px 4px 0; box-shadow:0 0 10px #3498db66;"></div>
                    </div>
                </div>
                <div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                        <span id="cA_Invest" style="color:#c9a96e; font-weight:bold;">-- / 10</span>
                        <span style="font-size:12px; color:var(--text-secondary);">Investment Score</span>
                        <span id="cB_Invest" style="color:#3498db; font-weight:bold;">-- / 10</span>
                    </div>
                    <div style="width:100%; height:8px; background:#222; border-radius:4px; display:flex;">
                        <div id="cA_InvestBar" style="height:100%; background:#c9a96e; width:50%; border-radius:4px 0 0 4px; box-shadow:0 0 10px #c9a96e66;"></div>
                        <div id="cB_InvestBar" style="height:100%; background:#3498db; width:50%; border-radius:0 4px 4px 0; box-shadow:0 0 10px #3498db66;"></div>
                    </div>
                </div>
            </div>
          </div>

          <!-- Radar Chart Compare -->
          <div class="bento-card">
            <div class="b-title">Livability Battle</div>
            <div class="chart-container" style="height: 250px; position:relative;">
                <canvas id="compareRadarChart"></canvas>
            </div>
          </div>

          <!-- Trend Line Chart -->
          <div class="bento-card span-2">
            <div class="b-title">5-Year Price Trajectory Comparison (₹ Lakhs)</div>
            <div class="chart-container" style="height: 300px;">
                <canvas id="compareTrendChart"></canvas>
            </div>
          </div>

        </div>
      </section>

      <!-- ===== TAB 4: CLIENT REPORTS ===== -->
"""

html = html.replace('<!-- ===== TAB 4: CLIENT REPORTS ===== -->', compare_html)

with open('predictor/templates/index.html', 'w') as f:
    f.write(html)
