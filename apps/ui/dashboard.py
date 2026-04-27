import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="MSME Credit Risk Portal",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Hide Streamlit elements to make the custom UI look native
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
        iframe {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }
    </style>
""", unsafe_allow_html=True)

# The HTML content from the premium UI
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MSME Credit Risk Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
    :root {
      --color-background-primary: #ffffff;
      --color-background-secondary: #f8fafc;
      --color-border-primary: #e2e8f0;
      --color-border-secondary: #cbd5e1;
      --color-border-tertiary: #f1f5f9;
      --color-text-primary: #0f172a;
      --color-text-secondary: #475569;
      --color-text-tertiary: #94a3b8;
      --color-accent-primary: #1e40af;
      --color-accent-secondary: #3b82f6;
      --color-accent-light: #eff6ff;
      --color-success: #10b981;
      --color-warning: #f59e0b;
      --color-danger: #ef4444;
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --border-radius-sm: 4px;
      --border-radius-md: 8px;
      --border-radius-lg: 12px;
      --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
      --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: var(--font-sans); background: var(--color-background-secondary); color: var(--color-text-primary); -webkit-font-smoothing: antialiased; overflow-x: hidden; }

    .sidebar {
      position: fixed; left: 0; top: 0; height: 100vh; width: 240px;
      background: var(--color-background-primary);
      border-right: 1px solid var(--color-border-tertiary);
      display: flex; flex-direction: column; padding: 24px 0; z-index: 100;
      transition: all 0.3s ease;
    }

    .logo {
      padding: 0 24px 24px;
      border-bottom: 1px solid var(--color-border-tertiary);
      margin-bottom: 16px;
    }
    .logo-mark { display: flex; align-items: center; gap: 12px; }
    .logo-icon {
      width: 36px; height: 36px; border-radius: 10px;
      background: linear-gradient(135deg, var(--color-accent-primary), var(--color-accent-secondary));
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 4px 12px rgba(30, 64, 175, 0.2);
    }
    .logo-icon svg { width: 20px; height: 20px; stroke: white; }
    .logo-text { font-size: 16px; font-weight: 700; color: var(--color-text-primary); letter-spacing: -0.02em; }
    .logo-sub { font-size: 11px; color: var(--color-text-tertiary); font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }

    .nav-section { padding: 0 12px; margin-bottom: 8px; }
    .nav-label { font-size: 11px; color: var(--color-text-tertiary); padding: 12px 12px 8px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
    .nav-item {
      display: flex; align-items: center; gap: 10px;
      padding: 10px 12px; border-radius: var(--border-radius-md);
      cursor: pointer; font-size: 14px; color: var(--color-text-secondary);
      transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .nav-item:hover { background: var(--color-background-secondary); color: var(--color-accent-primary); }
    .nav-item.active { background: var(--color-accent-light); color: var(--color-accent-primary); font-weight: 600; }
    .nav-item svg { width: 18px; height: 18px; stroke-width: 2; fill: none; stroke: currentColor; }
    .nav-badge {
      margin-left: auto; font-size: 11px; font-weight: 600;
      background: var(--color-danger); color: #fff; border-radius: 12px;
      padding: 2px 8px; min-width: 20px; text-align: center;
    }

    .sidebar-footer { margin-top: auto; padding: 16px 12px 0; border-top: 1px solid var(--color-border-tertiary); }
    .user-row {
      display: flex; align-items: center; gap: 12px;
      padding: 12px; border-radius: var(--border-radius-md);
      cursor: pointer; transition: background 0.2s;
    }
    .user-row:hover { background: var(--color-background-secondary); }
    .avatar {
      width: 36px; height: 36px; border-radius: 50%;
      background: var(--color-accent-light); color: var(--color-accent-primary);
      display: flex; align-items: center; justify-content: center;
      font-size: 14px; font-weight: 600;
    }
    .user-info { flex: 1; min-width: 0; }
    .user-name { font-size: 14px; font-weight: 600; color: var(--color-text-primary); }
    .user-role { font-size: 11px; color: var(--color-text-tertiary); }

    .main { margin-left: 240px; min-height: 100vh; transition: margin 0.3s; }

    .topbar {
      height: 64px; border-bottom: 1px solid var(--color-border-tertiary);
      background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(12px);
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 32px; position: sticky; top: 0; z-index: 90;
    }
    .page-title { font-size: 18px; font-weight: 700; color: var(--color-text-primary); letter-spacing: -0.01em; }
    .page-sub { font-size: 12px; color: var(--color-text-tertiary); }
    .topbar-right { display: flex; align-items: center; gap: 16px; }
    .topbar-btn {
      display: flex; align-items: center; gap: 8px;
      padding: 8px 16px; border-radius: var(--border-radius-md);
      border: 1px solid var(--color-border-primary);
      background: white; cursor: pointer;
      font-size: 13px; font-weight: 500; color: var(--color-text-secondary);
      transition: all 0.2s;
    }
    .topbar-btn:hover { border-color: var(--color-border-secondary); background: var(--color-background-secondary); }
    .run-btn { background: var(--color-accent-primary); color: #fff; border: none; box-shadow: 0 4px 12px rgba(30, 64, 175, 0.2); }
    .run-btn:hover { background: #1e3a8a; transform: translateY(-1px); }

    .status-dot {
      width: 8px; height: 8px; border-radius: 50%; background: var(--color-success);
      box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
      margin-right: 8px;
    }

    .content { padding: 32px; max-width: 1400px; margin: 0 auto; }

    .metrics-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 32px; }
    .metric-card {
      background: white; border-radius: var(--border-radius-lg);
      padding: 24px; border: 1px solid var(--color-border-tertiary);
      box-shadow: var(--shadow-sm); transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); }
    .metric-label { font-size: 12px; color: var(--color-text-tertiary); margin-bottom: 8px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
    .metric-value { font-size: 28px; font-weight: 700; color: var(--color-text-primary); }
    .metric-delta { font-size: 12px; margin-top: 8px; display: flex; align-items: center; gap: 4px; font-weight: 500; }
    .delta-up { color: var(--color-success); }
    .delta-down { color: var(--color-danger); }

    .charts-row { display: grid; grid-template-columns: 1.8fr 1fr; gap: 20px; margin-bottom: 32px; }
    .panel {
      background: white; border: 1px solid var(--color-border-tertiary);
      border-radius: var(--border-radius-lg); padding: 24px; box-shadow: var(--shadow-sm);
    }
    .panel-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; }
    .panel-title { font-size: 16px; font-weight: 700; color: var(--color-text-primary); }
    .tab-pill {
      font-size: 12px; padding: 6px 12px; border-radius: 100px; cursor: pointer;
      border: 1px solid var(--color-border-tertiary); color: var(--color-text-secondary); background: white;
      transition: all 0.2s; font-weight: 500;
    }
    .tab-pill.sel { background: var(--color-accent-primary); color: white; border-color: var(--color-accent-primary); }

    .donut-wrap { position: relative; display: flex; align-items: center; justify-content: center; }
    .donut-center { position: absolute; text-align: center; }
    .donut-num { font-size: 24px; font-weight: 700; color: var(--color-text-primary); }
    .donut-sub { font-size: 12px; color: var(--color-text-tertiary); font-weight: 500; }

    .risk-badge {
      padding: 4px 10px; border-radius: 100px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.02em;
    }
    .risk-low { background: #dcfce7; color: #166534; }
    .risk-med { background: #fef3c7; color: #92400e; }
    .risk-high { background: #fee2e2; color: #991b1b; }
    .risk-crit { background: #fecaca; color: #7f1d1d; }

    /* Modal Styles */
    .modal-overlay {
      position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(15, 23, 42, 0.4); backdrop-filter: blur(4px);
      display: none; align-items: center; justify-content: center; z-index: 1000;
      opacity: 0; transition: opacity 0.3s ease;
    }
    .modal-content {
      background: white; width: 600px; max-width: 95%; border-radius: var(--border-radius-lg);
      box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1); transform: scale(0.95); transition: transform 0.3s ease;
    }
    .modal-header { padding: 24px; border-bottom: 1px solid var(--color-border-tertiary); display: flex; justify-content: space-between; align-items: center; }
    .modal-body { padding: 24px; max-height: 70vh; overflow-y: auto; }
    .modal-footer { padding: 24px; border-top: 1px solid var(--color-border-tertiary); display: flex; justify-content: flex-end; gap: 12px; }

    .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    .form-group { margin-bottom: 16px; }
    .form-group.full { grid-column: span 2; }
    label { display: block; font-size: 13px; font-weight: 600; color: var(--color-text-secondary); margin-bottom: 6px; }
    input, select, textarea {
      width: 100%; padding: 10px 12px; border: 1px solid var(--color-border-primary);
      border-radius: var(--border-radius-md); font-size: 14px; outline: none; transition: border-color 0.2s;
    }
    input:focus { border-color: var(--color-accent-primary); box-shadow: 0 0 0 3px rgba(30, 64, 175, 0.1); }

    .btn { padding: 10px 20px; border-radius: var(--border-radius-md); cursor: pointer; font-weight: 600; font-size: 14px; transition: all 0.2s; border: none; }
    .btn-primary { background: var(--color-accent-primary); color: white; }
    .btn-secondary { background: var(--color-background-secondary); color: var(--color-text-secondary); border: 1px solid var(--color-border-primary); }

    .notification {
      position: fixed; bottom: 24px; right: 24px; padding: 16px 24px;
      background: white; border-radius: var(--border-radius-md); box-shadow: var(--shadow-md);
      border-left: 4px solid var(--color-accent-primary); z-index: 2000;
      display: flex; align-items: center; gap: 12px; transform: translateX(120%); transition: transform 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    .notification.show { transform: translateX(0); }
    
    .table-wrap { overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    thead th {
      padding: 12px 16px; text-align: left;
      color: var(--color-text-tertiary); font-weight: 600; font-size: 11px;
      text-transform: uppercase; letter-spacing: 0.05em;
      border-bottom: 1px solid var(--color-border-tertiary);
    }
    tbody td { padding: 16px; color: var(--color-text-primary); border-bottom: 1px solid var(--color-border-tertiary); vertical-align: middle; }
    tbody tr:last-child td { border-bottom: none; }
    tbody tr:hover { background: var(--color-background-secondary); }
    
    .sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0, 0, 0, 0); border: 0; }
    </style>
</head>
<body>
    <h2 class="sr-only">MSME Credit Risk System Dashboard</h2>

    <div class="sidebar">
      <div class="logo">
        <div class="logo-mark">
          <div class="logo-icon">
            <svg viewBox="0 0 16 16" fill="none">
              <rect x="2" y="8" width="3" height="6" rx="1" fill="#fff" opacity="0.7"/>
              <rect x="6.5" y="4" width="3" height="10" rx="1" fill="#fff"/>
              <rect x="11" y="1" width="3" height="13" rx="1" fill="#fff" opacity="0.7"/>
            </svg>
          </div>
          <div>
            <div class="logo-text">CreditSight</div>
            <div class="logo-sub">MSME Risk Engine</div>
          </div>
        </div>
      </div>

      <div class="nav-section">
        <div class="nav-label">Core</div>
        <div class="nav-item active" onclick="switchView('dashboard')">
          <svg viewBox="0 0 16 16"><rect x="1" y="1" width="6" height="6" rx="1.5"/><rect x="9" y="1" width="6" height="6" rx="1.5"/><rect x="1" y="9" width="6" height="6" rx="1.5"/><rect x="9" y="9" width="6" height="6" rx="1.5"/></svg>
          Dashboard
        </div>
        <div class="nav-item" onclick="switchView('applications')">
          <svg viewBox="0 0 16 16"><path d="M2 4h12M2 8h8M2 12h10"/></svg>
          Applications
          <span class="nav-badge">12</span>
        </div>
        <div class="nav-item" onclick="sendPrompt('Opening borrower portfolio...')">
          <svg viewBox="0 0 16 16"><circle cx="6" cy="5" r="3"/><path d="M1 14c0-3 2.5-5 5-5s5 2 5 5"/><circle cx="12" cy="6" r="2"/><path d="M15 14c0-2-1-3.5-3-4"/></svg>
          Borrowers
        </div>
      </div>

      <div class="nav-section">
        <div class="nav-label">Analytics</div>
        <div class="nav-item" onclick="switchView('monitor')">
          <svg viewBox="0 0 16 16"><path d="M1 12L5 7l3 3 4-6 3 3"/></svg>
          Model Monitor
        </div>
        <div class="nav-item" onclick="switchView('risk')">
          <svg viewBox="0 0 16 16"><circle cx="8" cy="8" r="6"/><path d="M8 8l4-4M8 8V3"/></svg>
          Risk Analysis
        </div>
      </div>

      <div class="sidebar-footer">
        <div class="user-row">
          <div class="avatar">PG</div>
          <div class="user-info">
            <div class="user-name">Pradyum Guha</div>
            <div class="user-role">Risk Analyst</div>
          </div>
        </div>
      </div>
    </div>

    <div class="main">
      <div class="topbar">
        <div class="topbar-left">
          <div class="page-title" id="view-title">Portfolio Overview</div>
          <div class="page-sub" id="last-updated">Last updated: Apr 27, 2026 · 09:42 AM</div>
        </div>
        <div class="topbar-right">
          <div style="display:flex;align-items:center;gap:6px;font-size:11px;color:var(--color-text-tertiary);">
            <div class="status-dot"></div> Model live
          </div>
          <button class="topbar-btn" onclick="exportReport()">Export report</button>
          <button class="topbar-btn run-btn" onclick="openModal()">Run assessment</button>
        </div>
      </div>

      <div class="content" id="dashboard-view">
        <div class="metrics-row">
          <div class="metric-card">
            <div class="metric-label">Total applications</div>
            <div class="metric-value" id="total-apps">4,821</div>
            <div class="metric-delta delta-up">▲ +8.3%</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Avg credit score</div>
            <div class="metric-value" id="avg-score">674</div>
            <div class="metric-delta delta-up">▲ +12 pts</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Default rate (30d)</div>
            <div class="metric-value" id="default-rate">3.2%</div>
            <div class="metric-delta delta-down">▼ +0.4%</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Model AUC-ROC</div>
            <div class="metric-value" id="model-auc">0.923</div>
            <div class="metric-delta">Stable</div>
          </div>
        </div>

        <div class="charts-row">
          <div class="panel">
            <div class="panel-header">
              <div class="panel-title">Application volume & approvals</div>
              <div class="panel-actions">
                <button class="tab-pill sel" id="tab6m" onclick="switchTab('6m')">6 months</button>
                <button class="tab-pill" id="tab1y" onclick="switchTab('1y')">1 year</button>
              </div>
            </div>
            <div style="position:relative;width:100%;height:300px;">
              <canvas id="volChart"></canvas>
            </div>
          </div>

          <div class="panel">
            <div class="panel-header"><div class="panel-title">Risk distribution</div></div>
            <div class="donut-wrap" style="height:200px;">
              <canvas id="donutChart"></canvas>
              <div class="donut-center">
                <div class="donut-num" id="total-apps-donut">4,821</div>
                <div class="donut-sub">total</div>
              </div>
            </div>
            <div id="donut-legend" style="margin-top:24px;"></div>
          </div>
        </div>

        <div class="bottom-row">
          <div class="panel">
            <div class="panel-header">
              <div class="panel-title">Recent applications</div>
              <button class="topbar-btn" onclick="switchView('applications')">View all</button>
            </div>
            <div class="table-wrap">
              <table id="recent-apps-table">
                <thead><tr><th>Borrower</th><th>Sector</th><th>Score</th><th>Risk</th><th>Decision</th></tr></thead>
                <tbody></tbody>
              </table>
            </div>
          </div>
          <div style="display:flex;flex-direction:column;gap:20px;">
            <div class="panel"><div class="panel-header"><div class="panel-title">Predictive features</div></div><div id="feature-list"></div></div>
            <div class="panel"><div class="panel-header"><div class="panel-title">Model stats</div></div><div id="model-stats"></div></div>
          </div>
        </div>
      </div>

      <div class="content" id="applications-view" style="display:none;">
        <div class="panel">
          <div class="panel-header"><div class="panel-title">Application Review Queue</div></div>
          <div class="table-wrap">
            <table id="full-apps-table">
              <thead><tr><th>ID</th><th>Date</th><th>Business</th><th>Requested</th><th>Status</th><th>Score</th><th>Action</th></tr></thead>
              <tbody></tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="content" id="monitor-view" style="display:none;">
        <div class="metrics-row">
          <div class="metric-card">
            <div class="metric-label">Model Health Index</div>
            <div class="metric-value">98.4%</div>
            <div class="metric-delta delta-up">Optimal</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Data Drift (PSI)</div>
            <div class="metric-value">0.042</div>
            <div class="metric-delta delta-up">Low</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Avg Inference Time</div>
            <div class="metric-value">124ms</div>
            <div class="metric-delta">Stable</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Last Retrain</div>
            <div class="metric-value">3d ago</div>
            <div class="metric-delta">v2.0.0</div>
          </div>
        </div>
        <div class="charts-row">
          <div class="panel">
            <div class="panel-header"><div class="panel-title">Inference Drift (Evidently AI)</div></div>
            <div style="height:300px;"><canvas id="driftChart"></canvas></div>
          </div>
          <div class="panel">
            <div class="panel-header"><div class="panel-title">Performance Metrics</div></div>
            <div id="monitor-stats-list"></div>
          </div>
        </div>
      </div>

      <div class="content" id="risk-view" style="display:none;">
        <div class="charts-row">
          <div class="panel">
            <div class="panel-header"><div class="panel-title">Portfolio Sector Breakdown</div></div>
            <div style="height:300px;"><canvas id="sectorChart"></canvas></div>
          </div>
          <div class="panel">
            <div class="panel-header"><div class="panel-title">Exposure by Risk Band</div></div>
            <div style="height:300px;"><canvas id="exposureChart"></canvas></div>
          </div>
        </div>
        <div class="panel">
          <div class="panel-header"><div class="panel-title">High-Risk Flagged Entities</div></div>
          <div class="table-wrap">
            <table>
              <thead><tr><th>Entity</th><th>Sector</th><th>Exposure</th><th>Reason</th><th>Status</th></tr></thead>
              <tbody>
                <tr><td>Arora Textiles</td><td>Manufacturing</td><td>₹12.4L</td><td>High DTI Ratio</td><td><span class="risk-badge risk-high">Flagged</span></td></tr>
                <tr><td>Patel Constructions</td><td>Real Estate</td><td>₹25.0L</td><td>CIBIL < 500</td><td><span class="risk-badge risk-crit">Critical</span></td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div class="modal-overlay" id="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h3 class="panel-title">New Credit Assessment</h3>
          <button onclick="closeModal()" style="background:none;border:none;font-size:24px;cursor:pointer;">&times;</button>
        </div>
        <form id="assessment-form">
          <div class="modal-body">
            <div class="form-grid">
              <div class="form-group"><label>Business ID</label><input type="text" name="business_id" value="MSME_1024" required></div>
              <div class="form-group"><label>Business Vintage</label><input type="number" name="age_years" value="5" required></div>
              <div class="form-group"><label>Annual Turnover</label><input type="number" name="annual_revenue" value="120" required></div>
              <div class="form-group"><label>Net Profit</label><input type="number" name="net_profit" value="18.5" required></div>
              <div class="form-group"><label>CIBIL Rank</label><input type="number" name="cibil_score" value="780" required></div>
              <div class="form-group"><label>Promoter CIBIL</label><input type="number" name="promoter_cibil" value="740" required></div>
              <div class="form-group"><label>Total Assets</label><input type="number" name="total_assets" value="85" required></div>
              <div class="form-group"><label>Existing Debt</label><input type="number" name="existing_debt" value="12" required></div>
              <div class="form-group"><label>Requested Amount</label><input type="number" name="requested_amount" value="25" required></div>
              <div class="form-group"><label>Udyam?</label><select name="udyam_registered"><option value="true">Yes</option><option value="false">No</option></select></div>
              <div class="form-group"><label>GST?</label><select name="gst_compliant"><option value="true">Yes</option><option value="false">No</option></select></div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
            <button type="submit" class="btn btn-primary" id="submit-btn">Run Analysis</button>
          </div>
        </form>
  </div>
</div>

<div class="modal-overlay" id="result-modal">
  <div class="modal-content" style="width: 700px;">
    <div class="modal-header">
      <h3 class="panel-title">Assessment Report</h3>
      <button onclick="closeResultModal()" style="background:none;border:none;font-size:24px;cursor:pointer;">&times;</button>
    </div>
    <div class="modal-body">
      <div id="result-summary" style="text-align:center; margin-bottom:32px;">
        <div id="result-status-icon" style="font-size:48px; margin-bottom:12px;"></div>
        <h2 id="result-status-text" style="font-size:24px; font-weight:700;"></h2>
        <p id="result-remarks" style="color:var(--color-text-secondary); margin-top:8px;"></p>
      </div>
      
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:32px;">
        <div class="panel" style="padding:16px;">
          <div class="metric-label">Approval Probability</div>
          <div class="metric-value" id="res-prob-app" style="font-size:24px;"></div>
          <div style="height:4px; background:#f1f5f9; border-radius:2px; margin-top:8px; overflow:hidden;">
            <div id="res-prob-app-bar" style="height:100%; background:var(--color-success);"></div>
          </div>
        </div>
        <div class="panel" style="padding:16px;">
          <div class="metric-label">Default Risk (PD)</div>
          <div class="metric-value" id="res-prob-def" style="font-size:24px;"></div>
          <div style="height:4px; background:#f1f5f9; border-radius:2px; margin-top:8px; overflow:hidden;">
            <div id="res-prob-def-bar" style="height:100%; background:var(--color-danger);"></div>
          </div>
        </div>
      </div>

      <div class="panel" style="margin-bottom:32px; background:var(--color-accent-light); border-color:var(--color-accent-secondary);">
        <div class="metric-label" style="color:var(--color-accent-primary);">Recommended Credit Limit</div>
        <div class="metric-value" id="res-limit" style="font-size:32px; color:var(--color-accent-primary);"></div>
        <p style="font-size:11px; color:var(--color-accent-primary); margin-top:4px;">Max allowable: <span id="res-max-cap"></span></p>
      </div>

      <div class="panel">
        <div class="panel-header" style="margin-bottom:16px;">
          <div class="panel-title" style="font-size:14px;">Key Decision Drivers (Model Weights)</div>
        </div>
        <div id="res-weights-list"></div>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-primary" onclick="closeResultModal()" style="width: 100%;">Close & Sync Dashboard</button>
    </div>
  </div>
</div>
    </div>

    <div class="notification" id="notification"><div class="status-dot"></div><div id="notification-text"></div></div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
    <script>
    let currentChart = null;
    let currentDonut = null;
    const apiBase = 'http://localhost:8000';

    const mockData = {
      apps6m: { labels: ['Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr'], apps: [680, 590, 710, 760, 810, 870], approved: [441, 371, 469, 524, 567, 609] },
      apps1y: { labels: ['May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr'], apps: [540,610,580,630,660,700,680,590,710,760,810,870], approved: [351,403,385,410,442,476,441,371,469,524,567,609] },
      recentApps: [
        { business: 'Arora Textiles', amount: '₹12L', sector: 'Manufacturing', score: 781, risk: 'low', status: 'Approved' },
        { business: 'Meena Food Works', amount: '₹8L', sector: 'Food & Bev', score: 624, risk: 'med', status: 'Review' },
        { business: 'Patel Constructions', amount: '₹25L', sector: 'Real Estate', score: 481, risk: 'high', status: 'Flagged' },
        { business: 'Singh Auto Parts', amount: '₹5L', sector: 'Auto', score: 821, risk: 'low', status: 'Approved' },
        { business: 'Rao Digital Svcs', amount: '₹3L', sector: 'IT Services', score: 312, risk: 'crit', status: 'Rejected' }
      ],
      features: [{ name: 'Debt-to-income ratio', val: 91 }, { name: 'Cash flow volatility', val: 84 }, { name: 'GST regularity', val: 77 }, { name: 'Industry default', val: 68 }, { name: 'Years in operation', val: 55 }],
      modelStats: [{ label: 'AUC-ROC', val: 0.923, pct: 92 }, { label: 'Precision', val: 0.881, pct: 88 }, { label: 'Recall', val: 0.864, pct: 86 }],
      riskDist: { labels: ['Low risk', 'Medium', 'High', 'Critical'], data: [42, 31, 18, 9], colors: ['#10b981', '#f59e0b', '#ef4444', '#7f1d1d'] }
    };

    document.addEventListener('DOMContentLoaded', () => { renderDashboard(); setupForm(); });

    function renderDashboard() { buildChart(mockData.apps6m); buildDonut(); renderRecentApps(); renderFeatures(); renderModelStats(); }

    function switchView(view) {
      const views = ['dashboard', 'applications', 'monitor', 'risk'];
      views.forEach(v => document.getElementById(`${v}-view`).style.display = v === view ? 'block' : 'none');
      
      const titleMap = { 
        dashboard: 'Portfolio Overview', 
        applications: 'Review Queue',
        monitor: 'ML Model Performance & Health',
        risk: 'Portfolio Risk Analytics'
      };
      document.getElementById('view-title').innerText = titleMap[view];
      document.querySelectorAll('.nav-item').forEach(item => item.classList.toggle('active', item.innerText.toLowerCase().includes(view.slice(0, -2))));
      
      if (view === 'applications') renderFullApps();
      if (view === 'monitor') renderMonitorView();
      if (view === 'risk') renderRiskView();
    }

    let monitorCharts = [];
    function renderMonitorView() {
      monitorCharts.forEach(c => c.destroy());
      monitorCharts = [];
      
      // Drift Chart
      monitorCharts.push(new Chart(document.getElementById('driftChart'), {
        type: 'line',
        data: { labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'], datasets: [{ label: 'Prediction Drift', data: [0.02, 0.03, 0.02, 0.05, 0.04, 0.03], borderColor: '#3b82f6', tension: 0.4 }] },
        options: { responsive: true, maintainAspectRatio: false }
      }));
      
      document.getElementById('monitor-stats-list').innerHTML = [
        { l: 'Precision', v: '0.881', p: 88 },
        { l: 'Recall', v: '0.864', p: 86 },
        { l: 'F1 Score', v: '0.872', p: 87 },
        { l: 'KS Stat', v: '42.5', p: 42 }
      ].map(s => `
        <div style="margin-bottom:16px;">
          <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px;"><span>${s.l}</span><span style="font-weight:600">${s.v}</span></div>
          <div style="height:4px;background:#f1f5f9;border-radius:2px;overflow:hidden;"><div style="width:${s.p}%;height:100%;background:#10b981;"></div></div>
        </div>
      `).join('');
    }

    let riskCharts = [];
    function renderRiskView() {
      riskCharts.forEach(c => c.destroy());
      riskCharts = [];
      
      // Sector Chart
      riskCharts.push(new Chart(document.getElementById('sectorChart'), {
        type: 'polarArea',
        data: { labels: ['Manufacturing', 'Services', 'Trade', 'Agri', 'Tech'], datasets: [{ data: [40, 35, 15, 5, 5], backgroundColor: ['#1e40af', '#3b82f6', '#94a3b8', '#10b981', '#f59e0b'] }] },
        options: { responsive: true, maintainAspectRatio: false }
      }));
      
      // Exposure Chart
      riskCharts.push(new Chart(document.getElementById('exposureChart'), {
        type: 'bar',
        data: { labels: ['Low', 'Med', 'High', 'Crit'], datasets: [{ label: 'Exposure (₹ Cr)', data: [12.4, 8.2, 3.1, 1.2], backgroundColor: ['#10b981', '#f59e0b', '#ef4444', '#7f1d1d'] }] },
        options: { responsive: true, maintainAspectRatio: false }
      }));
    }

    function buildChart(d) {
      if (currentChart) currentChart.destroy();
      currentChart = new Chart(document.getElementById('volChart'), {
        type: 'bar', data: { labels: d.labels, datasets: [{ label: 'Total', data: d.apps, backgroundColor: '#3b82f6', borderRadius: 4 }, { label: 'Approved', data: d.approved, backgroundColor: '#10b981', borderRadius: 4 }] },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } } }
      });
    }

    function buildDonut() {
      if (currentDonut) currentDonut.destroy();
      currentDonut = new Chart(document.getElementById('donutChart'), { type: 'doughnut', data: { labels: mockData.riskDist.labels, datasets: [{ data: mockData.riskDist.data, backgroundColor: mockData.riskDist.colors, borderWidth: 0 }] }, options: { responsive: false, cutout: '75%', plugins: { legend: { display: false } } } });
      document.getElementById('donut-legend').innerHTML = mockData.riskDist.labels.map((l, i) => `<div style="display:flex;justify-content:space-between;margin-bottom:8px;font-size:12px;"><div style="display:flex;align-items:center;gap:8px;"><div style="width:8px;height:8px;border-radius:50%;background:${mockData.riskDist.colors[i]}"></div><span>${l}</span></div><span style="font-weight:600">${mockData.riskDist.data[i]}%</span></div>`).join('');
    }

    function switchTab(t) { buildChart(t === '6m' ? mockData.apps6m : mockData.apps1y); }

    function renderRecentApps() {
      document.querySelector('#recent-apps-table tbody').innerHTML = mockData.recentApps.map(app => `<tr><td><div style="font-weight:600;">${app.business}</div><div style="font-size:10px;color:#94a3b8;">${app.amount}</div></td><td><span class="risk-badge">${app.sector}</span></td><td>${app.score}</td><td><span class="risk-badge risk-${app.risk}">${app.risk}</span></td><td>${app.status}</td></tr>`).join('');
    }

    function renderFullApps() {
      const businesses = ['Arora Textiles', 'Meena Food Works', 'Patel Constructions', 'Singh Auto Parts', 'Rao Digital Svcs', 'Kishore Gems', 'Surya Solar Systems', 'Modern Bakary', 'Unity Logistics', 'Zigma Tech'];
      const sectors = ['Manufacturing', 'Food & Bev', 'Real Estate', 'Auto', 'IT Services', 'Trade', 'Energy', 'Retail', 'Logistics', 'Tech'];
      const statuses = ['Approved', 'Pending', 'Under Review', 'Flagged', 'Rejected'];
      
      const data = Array.from({length: 12}, (_, i) => {
        const amount = Math.floor(Math.random() * 45) + 5; // 5L to 50L
        const score = Math.floor(Math.random() * 400) + 400; // 400 to 800
        const statusIdx = score > 700 ? 0 : (score < 500 ? 4 : Math.floor(Math.random() * 3) + 1);
        const riskClass = statusIdx === 0 ? 'risk-low' : (statusIdx === 4 ? 'risk-crit' : 'risk-med');
        
        return { 
          id: `APP-${1024+i}`, 
          date: `Apr ${27 - (i%5)}`, 
          business: businesses[i % businesses.length], 
          amount: `₹${amount}L`, 
          status: statuses[statusIdx], 
          riskClass: riskClass,
          score: score 
        };
      });
      
      document.querySelector('#full-apps-table tbody').innerHTML = data.map(d => `
        <tr>
          <td>${d.id}</td>
          <td>${d.date}</td>
          <td style="font-weight:600;">${d.business}</td>
          <td>${d.amount}</td>
          <td><span class="risk-badge ${d.riskClass}">${d.status}</span></td>
          <td>${d.score}</td>
          <td><button class="topbar-btn" style="padding:4px 8px;">Details</button></td>
        </tr>
      `).join('');
    }

    function renderFeatures() { document.getElementById('feature-list').innerHTML = mockData.features.map(f => `<div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;"><div style="flex:1;font-size:13px;">${f.name}</div><div style="width:80px;height:6px;background:#f1f5f9;border-radius:3px;overflow:hidden;"><div style="width:${f.val}%;height:100%;background:#1e40af;"></div></div><div style="width:30px;font-size:11px;text-align:right;">${f.val}%</div></div>`).join(''); }
    function renderModelStats() { document.getElementById('model-stats').innerHTML = mockData.modelStats.map(s => `<div style="display:flex;justify-content:space-between;margin-bottom:8px;font-size:13px;"><span>${s.label}</span><span style="font-weight:600">${s.val}</span></div>`).join(''); }

    function openModal() { document.getElementById('modal').style.display = 'flex'; setTimeout(() => { document.getElementById('modal').style.opacity = '1'; }, 10); }
    function closeModal() { document.getElementById('modal').style.opacity = '0'; setTimeout(() => { document.getElementById('modal').style.display = 'none'; }, 300); }

    function setupForm() {
      document.getElementById('assessment-form').onsubmit = async (e) => {
        e.preventDefault();
        const btn = document.getElementById('submit-btn');
        btn.innerText = 'Analyzing...'; btn.disabled = true;
        const data = Object.fromEntries(new FormData(e.target).entries());
        data.age_years = parseInt(data.age_years); data.annual_revenue = parseFloat(data.annual_revenue); data.net_profit = parseFloat(data.net_profit); data.cibil_score = parseInt(data.cibil_score); data.promoter_cibil = parseInt(data.promoter_cibil); data.total_assets = parseFloat(data.total_assets); data.existing_debt = parseFloat(data.existing_debt); data.requested_amount = parseFloat(data.requested_amount); data.udyam_registered = data.udyam_registered === 'true'; data.gst_compliant = data.gst_compliant === 'true';
        data.employees = 5; data.fixed_assets = data.total_assets * 0.6; data.valuation = data.annual_revenue * 1.5;

        try {
          showNotification('Running Engine...', 'info');
          const res = await fetch(`${apiBase}/predict`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
          const result = await res.json();
          
          // Populate Result Modal
          document.getElementById('result-status-icon').innerText = result.is_approved ? '✅' : '❌';
          document.getElementById('result-status-text').innerText = result.is_approved ? 'Application Approved' : 'Application Flagged';
          document.getElementById('result-remarks').innerText = result.remarks;
          document.getElementById('res-prob-app').innerText = (result.approval_probability * 100).toFixed(1) + '%';
          document.getElementById('res-prob-app-bar').style.width = (result.approval_probability * 100) + '%';
          document.getElementById('res-prob-def').innerText = (result.default_probability * 100).toFixed(1) + '%';
          document.getElementById('res-prob-def-bar').style.width = (result.default_probability * 100) + '%';
          document.getElementById('res-limit').innerText = '₹' + result.final_loan_recommendation.toFixed(1) + ' Lakhs';
          document.getElementById('res-max-cap').innerText = '₹' + result.max_allowable_loan.toFixed(1) + 'L';
          
          // Render Weights
          const weightsDiv = document.getElementById('res-weights-list');
          weightsDiv.innerHTML = '';
          const sortedWeights = Object.entries(result.feature_importance || {})
            .sort((a,b) => b[1] - a[1])
            .slice(0, 5);
            
          sortedWeights.forEach(([name, val]) => {
            const pct = (val * 100).toFixed(1);
            weightsDiv.innerHTML += `
              <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
                <div style="flex:1;font-size:12px;color:var(--color-text-secondary);text-transform:capitalize;">${name.replace(/_/g, ' ')}</div>
                <div style="width:100px;height:4px;background:#f1f5f9;border-radius:2px;overflow:hidden;">
                  <div style="width:${pct*2}%;height:100%;background:var(--color-accent-primary);"></div>
                </div>
                <div style="width:40px;font-size:11px;font-weight:600;text-align:right;">${pct}%</div>
              </div>
            `;
          });

          closeModal();
          openResultModal();
          
          showNotification(result.is_approved ? '✅ Assessment Complete' : '❌ Decision: Flagged', result.is_approved ? 'success' : 'error');
          
          mockData.recentApps.unshift({ 
            business: data.business_id, 
            amount: '₹' + data.requested_amount + 'L', 
            sector: 'New Assessment', 
            score: Math.floor(result.approval_probability * 1000), 
            risk: result.is_approved ? 'low' : 'high', 
            status: result.is_approved ? 'Approved' : 'Rejected' 
          });
          renderRecentApps(); 
        } catch (err) { 
          showNotification('API Error: Connection Failed', 'error'); 
          console.error(err);
        }
        finally { btn.innerText = 'Run Analysis'; btn.disabled = false; }
      };
    }

    function openResultModal() { 
      const m = document.getElementById('result-modal');
      m.style.display = 'flex'; 
      setTimeout(() => m.style.opacity = '1', 10);
    }
    function closeResultModal() { 
      document.getElementById('result-modal').style.opacity = '0'; 
      setTimeout(() => { document.getElementById('result-modal').style.display = 'none'; }, 300);
    }

    function showNotification(text, type) {
      const n = document.getElementById('notification');
      document.getElementById('notification-text').innerText = text;
      n.style.borderLeftColor = type === 'success' ? '#10b981' : (type === 'error' ? '#ef4444' : '#1e40af');
      n.classList.add('show'); setTimeout(() => { n.classList.remove('show'); }, 4000);
    }

    function sendPrompt(p) { showNotification('AI: ' + p, 'info'); }
    function exportReport() { showNotification('Exporting...', 'info'); }
    </script>
</body>
</html>
"""

components.html(html_content, height=1200, scrolling=True)
