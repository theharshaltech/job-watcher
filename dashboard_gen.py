import os
import json
import datetime
from database.job_store import get_all_jobs, get_stats

def generate_dashboard():
    jobs = get_all_jobs()
    stats = get_stats()
    
    # Define monitored companies list
    monitored_companies = [
        "Cognizant", "Infosys", "Accenture", "Wipro", "Capgemini", 
        "TCS", "HCL", "IBM", "Deloitte", "Tech Mahindra"
    ]
    
    # Calculate company stats (how many jobs in DB for each)
    company_counts = {}
    for j in jobs:
        c_lower = j["company"].lower()
        matched = False
        for mc in monitored_companies:
            if mc.lower() in c_lower:
                company_counts[mc] = company_counts.get(mc, 0) + 1
                matched = True
                break
        if not matched:
            company_counts[j["company"]] = company_counts.get(j["company"], 0) + 1
            
    companies_html = ""
    for company in monitored_companies:
        count = company_counts.get(company, 0)
        companies_html += f"""
        <div class="company-card">
            <div class="company-info">
                <span class="company-name">{company}</span>
                <span class="status-badge active">Active</span>
            </div>
            <div class="company-stats">
                <span class="stat-value">{count}</span>
                <span class="stat-label">Jobs Found</span>
            </div>
        </div>
        """

    # Generate job list rows
    jobs_rows_html = ""
    if not jobs:
        jobs_rows_html = """
        <tr>
            <td colspan="5" class="empty-state">
                <div class="empty-icon">🔍</div>
                <p>No jobs found yet. Scraper will run shortly!</p>
            </td>
        </tr>
        """
    else:
        for job in jobs:
            # Clean link for displaying
            display_link = job["link"]
            jobs_rows_html += f"""
            <tr class="job-row" data-company="{job['company'].replace('"', '&quot;')}" data-role="{job['role'].replace('"', '&quot;')}" data-location="{job['location'].replace('"', '&quot;')}">
                <td class="company-cell">
                    <span class="company-tag">{job['company']}</span>
                </td>
                <td class="role-cell">
                    <div class="role-title">{job['role']}</div>
                </td>
                <td class="location-cell">
                    <div class="loc-text"><i class="loc-icon">📍</i> {job['location']}</div>
                </td>
                <td class="date-cell">
                    <span class="date-badge">{job['date_posted']}</span>
                    <small class="scraped-at">Found: {job['date_scraped'].split()[0]}</small>
                </td>
                <td class="action-cell">
                    <a href="{job['link']}" target="_blank" class="apply-btn">Apply Now 🚀</a>
                </td>
            </tr>
            """

    # Last updated time
    last_updated = datetime.datetime.now().strftime("%B %d, %Y %I:%M %p")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Job Watcher for MCA & Freshers</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0b0f19;
            --surface-color: rgba(17, 25, 40, 0.75);
            --border-color: rgba(255, 255, 255, 0.08);
            --accent-primary: #8b5cf6;
            --accent-secondary: #06b6d4;
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --success-color: #10b981;
            --card-glow: rgba(139, 92, 246, 0.15);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-image: 
                radial-gradient(at 0% 0%, rgba(139, 92, 246, 0.1) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(6, 182, 212, 0.1) 0px, transparent 50%);
            min-height: 100vh;
            padding-bottom: 3rem;
            overflow-x: hidden;
        }}

        .container {{
            max-width: 1280px;
            margin: 0 auto;
            padding: 2rem 1.5rem;
        }}

        /* Header Styling */
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2.5rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 1.5rem;
        }}

        .brand-title {{
            font-size: 1.8rem;
            font-weight: 700;
            background: linear-gradient(135deg, #a78bfa, #22d3ee);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .brand-subtitle {{
            font-size: 0.85rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
        }}

        .last-updated {{
            text-align: right;
        }}

        .last-updated .time {{
            font-weight: 600;
            color: var(--accent-secondary);
        }}

        .last-updated .status {{
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-top: 0.25rem;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            gap: 0.35rem;
        }}

        .pulse-dot {{
            width: 8px;
            height: 8px;
            background-color: var(--success-color);
            border-radius: 50%;
            display: inline-block;
            box-shadow: 0 0 8px var(--success-color);
            animation: pulse 2s infinite;
        }}

        @keyframes pulse {{
            0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
            70% {{ transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }}
            100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
        }}

        /* Metrics grid */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }}

        .metric-card {{
            background: var(--surface-color);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 1rem;
            padding: 1.5rem;
            position: relative;
            overflow: hidden;
            transition: transform 0.3s ease, border-color 0.3s ease;
        }}

        .metric-card:hover {{
            transform: translateY(-5px);
            border-color: rgba(139, 92, 246, 0.3);
            box-shadow: 0 10px 20px -10px var(--card-glow);
        }}

        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(to bottom, var(--accent-primary), var(--accent-secondary));
        }}

        .metric-title {{
            font-size: 0.9rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}

        .metric-value {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #fff;
            margin-bottom: 0.25rem;
        }}

        .metric-desc {{
            font-size: 0.85rem;
            color: var(--text-muted);
        }}

        /* Companies grid */
        .companies-section {{
            margin-bottom: 2.5rem;
        }}

        .section-header {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1.25rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .companies-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 1rem;
        }}

        .company-card {{
            background: var(--surface-color);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 0.75rem;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 0.75rem;
            transition: all 0.2s ease;
        }}

        .company-card:hover {{
            background: rgba(255, 255, 255, 0.02);
            border-color: rgba(255, 255, 255, 0.15);
        }}

        .company-info {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .company-name {{
            font-weight: 600;
            font-size: 0.95rem;
        }}

        .status-badge {{
            font-size: 0.7rem;
            padding: 0.15rem 0.4rem;
            border-radius: 20px;
            font-weight: 500;
        }}

        .status-badge.active {{
            background: rgba(16, 185, 129, 0.1);
            color: var(--success-color);
            border: 1px solid rgba(16, 185, 129, 0.2);
        }}

        .company-stats {{
            display: flex;
            align-items: baseline;
            gap: 0.35rem;
        }}

        .company-stats .stat-value {{
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--accent-secondary);
        }}

        .company-stats .stat-label {{
            font-size: 0.75rem;
            color: var(--text-muted);
        }}

        /* Table Filters & Search */
        .table-controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            gap: 1rem;
            flex-wrap: wrap;
        }}

        .search-box {{
            position: relative;
            flex-grow: 1;
            max-width: 400px;
        }}

        .search-box input {{
            width: 100%;
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            padding: 0.75rem 1rem 0.75rem 2.5rem;
            color: #fff;
            font-family: inherit;
            outline: none;
            transition: all 0.2s ease;
        }}

        .search-box input:focus {{
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
        }}

        .search-icon {{
            position: absolute;
            left: 0.85rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
        }}

        .filter-dropdown {{
            background: var(--surface-color);
            border: 1px solid var(--border-color);
            border-radius: 0.5rem;
            padding: 0.75rem 1.5rem;
            color: #fff;
            outline: none;
            cursor: pointer;
            font-family: inherit;
        }}

        .filter-dropdown:focus {{
            border-color: var(--accent-primary);
        }}

        /* Jobs Table section */
        .jobs-section {{
            background: var(--surface-color);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 1rem;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}

        .table-responsive {{
            width: 100%;
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}

        th {{
            background: rgba(17, 25, 40, 0.9);
            padding: 1.15rem 1.5rem;
            font-weight: 600;
            color: var(--text-muted);
            border-bottom: 1px solid var(--border-color);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        td {{
            padding: 1.25rem 1.5rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            vertical-align: middle;
        }}

        .job-row {{
            transition: background-color 0.2s ease;
        }}

        .job-row:hover {{
            background-color: rgba(255, 255, 255, 0.015);
        }}

        .company-cell {{
            font-weight: 600;
        }}

        .company-tag {{
            display: inline-block;
            padding: 0.35rem 0.75rem;
            border-radius: 0.5rem;
            background: rgba(139, 92, 246, 0.1);
            color: #c084fc;
            border: 1px solid rgba(139, 92, 246, 0.15);
            font-size: 0.85rem;
        }}

        .role-title {{
            font-weight: 600;
            font-size: 1rem;
            color: #fff;
        }}

        .location-cell {{
            color: var(--text-muted);
            font-size: 0.9rem;
        }}

        .date-badge {{
            display: inline-block;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 4px;
            padding: 0.15rem 0.4rem;
            font-size: 0.75rem;
            margin-right: 0.5rem;
            font-weight: 500;
        }}

        .scraped-at {{
            display: block;
            color: var(--text-muted);
            font-size: 0.75rem;
            margin-top: 0.25rem;
        }}

        .apply-btn {{
            display: inline-block;
            background: linear-gradient(135deg, var(--accent-primary), #7c3aed);
            color: #fff;
            text-decoration: none;
            padding: 0.55rem 1rem;
            border-radius: 0.5rem;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.2s ease;
            text-align: center;
            border: none;
        }}

        .apply-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4);
            filter: brightness(1.1);
        }}

        .empty-state {{
            text-align: center;
            padding: 4rem 2rem;
            color: var(--text-muted);
        }}

        .empty-icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 1rem;
            }}
            .last-updated {{
                text-align: left;
            }}
            .last-updated .status {{
                justify-content: flex-start;
            }}
            .table-controls {{
                flex-direction: column;
                align-items: stretch;
            }}
            .search-box {{
                max-width: 100%;
            }}
            th {{
                padding: 0.8rem 1rem;
            }}
            td {{
                padding: 0.8rem 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1 class="brand-title">🤖 AI Job Watcher</h1>
                <p class="brand-subtitle">Automated notifications for MCA & Fresher eligibility</p>
            </div>
            <div class="last-updated">
                <div>Last Checked: <span class="time">{last_updated}</span></div>
                <div class="status"><span class="pulse-dot"></span> 24/7 Cloud Monitoring Active</div>
            </div>
        </header>

        <!-- Metrics Overview -->
        <section class="metrics-grid">
            <div class="metric-card">
                <div class="metric-title">Total Jobs Tracked</div>
                <div class="metric-value">{stats['total_jobs']}</div>
                <div class="metric-desc">Matched eligibility keywords</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">New Jobs Today</div>
                <div class="metric-value" style="color: var(--accent-secondary);">{stats['jobs_today']}</div>
                <div class="metric-desc">Found in the last 24 hours</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Monitored Companies</div>
                <div class="metric-value" style="color: var(--success-color);">{len(monitored_companies)}</div>
                <div class="metric-desc">Top IT service & product firms</div>
            </div>
        </section>

        <!-- Monitored Companies list -->
        <section class="companies-section">
            <h2 class="section-header">🏢 Active Target Companies</h2>
            <div class="companies-grid">
                {companies_html}
            </div>
        </section>

        <!-- Jobs Table section -->
        <section class="jobs-wrapper">
            <h2 class="section-header" style="margin-bottom: 0.5rem;">🚨 Recent Job Openings</h2>
            
            <div class="table-controls">
                <div class="search-box">
                    <span class="search-icon">🔍</span>
                    <input type="text" id="searchInput" placeholder="Search roles or locations...">
                </div>
                
                <select id="companyFilter" class="filter-dropdown">
                    <option value="">All Companies</option>
                    {"".join(f'<option value="{c}">{c}</option>' for c in monitored_companies)}
                </select>
            </div>

            <div class="jobs-section">
                <div class="table-responsive">
                    <table>
                        <thead>
                            <tr>
                                <th style="width: 15%;">Company</th>
                                <th style="width: 40%;">Role Title</th>
                                <th style="width: 20%;">Location</th>
                                <th style="width: 13%;">Posted</th>
                                <th style="width: 12%;">Action</th>
                            </tr>
                        </thead>
                        <tbody id="jobsTableBody">
                            {jobs_rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </section>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const searchInput = document.getElementById('searchInput');
            const companyFilter = document.getElementById('companyFilter');
            const tableBody = document.getElementById('jobsTableBody');
            const rows = tableBody.querySelectorAll('.job-row');

            function filterTable() {{
                const searchTerm = searchInput.value.toLowerCase().trim();
                const selectedCompany = companyFilter.value.toLowerCase();

                rows.forEach(row => {{
                    const company = row.getAttribute('data-company').toLowerCase();
                    const role = row.getAttribute('data-role').toLowerCase();
                    const location = row.getAttribute('data-location').toLowerCase();
                    
                    const matchesSearch = company.includes(searchTerm) || role.includes(searchTerm) || location.includes(searchTerm);
                    const matchesCompany = !selectedCompany || company.includes(selectedCompany);

                    if (matchesSearch && matchesCompany) {{
                        row.style.display = '';
                    }} else {{
                        row.style.display = 'none';
                    }}
                }});
            }}

            searchInput.addEventListener('input', filterTable);
            companyFilter.addEventListener('change', filterTable);
        }});
    </script>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Dashboard index.html generated successfully!")

if __name__ == "__main__":
    generate_dashboard()
