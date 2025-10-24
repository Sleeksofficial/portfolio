# --- IMPORT NECESSARY LIBRARIES ---
import smtplib
import ssl
import streamlit as st
import plotly.express as px
import pandas as pd
from PIL import Image  # To handle image files
import base64  # To encode PDF files for display
import datetime # For date filtering in the demo
import numpy as np # For generating sample data
import os # To check if files exist

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Oloruntoba Anate's Executive Portfolio",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. FILE PATHS & GLOBAL VARIABLES ---
PROFILE_IMAGE_FILE = "IMG_3675.jpg" 
CV_FILE_1 = "Oloruntoba business analyst cv.pdf"
CV_FILE_2 = "Oloruntoba Auditor_CV.pdf"
CV_FILE_3 = "Oloruntoba ict pmp cv.pdf"


# --- 3. LOAD ASSETS (IMAGE & CVs) ---
@st.cache_data
def load_profile_image(path):
    if not os.path.exists(path):
        st.error(f"Profile picture '{path}' not found.")
        return None
    return Image.open(path)

profile_image = load_profile_image(PROFILE_IMAGE_FILE)

@st.cache_data
def load_cv_file(file_path):
    if not os.path.exists(file_path):
        st.error(f"CV file '{file_path}' not found. Please check the filename and location.")
        return None
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except Exception as e:
        st.error(f"Error loading file {file_path}: {e}")
        return None

cv_data_1 = load_cv_file(CV_FILE_1)
cv_data_2 = load_cv_file(CV_FILE_2)
cv_data_3 = load_cv_file(CV_FILE_3)

# --- 4. HELPER FUNCTIONS ---
def display_pdf(file_data, file_name):
    if file_data:
        try:
            base64_pdf = base64.b64encode(file_data).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not display PDF '{file_name}'. Error: {e}.")
    else:
        st.error(f"Cannot display PDF. File '{file_name}' was not loaded or is missing.")
# --- 4. HELPER FUNCTIONS ---
# (After get_demo_data function)

def send_email(name, user_email, subject, message):
    try:
        # Get email credentials from Render's Environment Variables
        sender_email = os.environ.get("SENDER_EMAIL")
        password = os.environ.get("SENDER_PASSWORD")
        
        if not sender_email or not password:
            st.error("Email credentials are not set on the server. Please contact the admin.")
            return False
            
        receiver_email = "anatepapilo@gmail.com" 

        full_message = f"""\
Subject: New Portfolio Contact: {subject}

From: {name} <{user_email}>
Reply-To: {user_email}

{message}
"""
        context = ssl.create_default_context()
        
        # --- NEW: Connect to port 587 using standard SMTP ---
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
            server.set_debuglevel(1) 
            server.starttls(context=context) # <-- Upgrade to a secure connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, full_message)
        
        return True # Email sent successfully
    
    except smtplib.SMTPAuthenticationError:
        st.error("Authentication failed. Please check the server credentials.")
        return False
    except smtplib.SMTPServerDisconnected:
        st.error("Server disconnected. Please try again later.")
        return False
    except Exception as e:
        # This will catch timeouts and other errors
        st.error(f"An error occurred: {e}")
        return False
@st.cache_data
def get_demo_data():
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", end="2024-12-31", freq='D')
    data_size = len(dates)
    departments = np.random.choice(['Finance', 'Operations', 'IT', 'Marketing', 'Sales'], data_size, p=[0.15, 0.3, 0.25, 0.15, 0.15])
    expense_types = np.random.choice(['Software Licenses', 'Cloud Services (Azure)', 'Hardware', 'Travel', 'Consulting Fees'], data_size, p=[0.3, 0.25, 0.2, 0.1, 0.15])
    # FIX: Create as float array to prevent casting error
    amounts = np.random.randint(100, 5000, data_size).astype(float)
    amounts[expense_types == 'Consulting Fees'] *= 2
    amounts[departments == 'IT'] *= 1.5
    df = pd.DataFrame({'Date': dates, 'Department': departments, 'Expense Type': expense_types, 'Amount ($)': amounts})
    return df

# --- 5. SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page_selection = st.sidebar.radio(
    "Explore My Portfolio",
    [
        "🏆 Overview Dashboard",
        "💡 Live Dashboard Demo",
        "🚀 Case Studies (Projects)",
        "🧠 My Approach",
        "🛠️ Skills & Expertise",
        "🎓 Education & Certifications",
        "💼 Professional Experience",
        "📄 My CVs",
        "💬 Contact"
    ]
)
st.sidebar.markdown("---")
st.sidebar.info(
    """
    **How to Navigate:**
    * Use the menu above to explore different sections.
    * Visit the **'Live Dashboard Demo'** page. The filters for that demo will appear here.
    """
)


# --- 6. HEADER & "IRRESISTIBLE" PITCH ---
with st.container():
    col_img, col_header = st.columns([1, 4])
    with col_img:
        if profile_image:
            st.image(profile_image, width=160, caption="Oloruntoba Peter Anate") 
    with col_header:
        st.title("Oloruntoba Peter Anate")
        st.subheader("ICT Project Manager | Business & Financial Analyst | Auditor")
        st.markdown(
            """
            I am a multi-disciplinary leader who combines an **auditor's eye for risk**, a **financial analyst's mind for value**, 
            and an **ICT project manager's skill for execution**.
            
            I don't just find financial risks; I build the automated systems to prevent them. 
            I don't just analyze data; I deploy the technology that turns it into profit. 
            My 9+ years of experience has...
            
            * Reduced **fraud risk by 60%** by designing new internal controls.
            * Saved over **15% in operational costs** through ICT automation.
            * Cut **reporting time by 30%** by building and deploying Power BI dashboards.
            """
        )
        st.markdown(
            "**[LinkedIn](https://www.linkedin.com/in/sleeksofficial)** | "
            "**[GitHub](https://github.com/Sleeksofficial)** | "
            "**[Email](mailto:anatepapilo@gmail.com)**"
        )
    st.markdown("---")


# --- 7. PAGE CONTENT ROUTING ---
# ==============================================================================
# PAGE 1: OVERVIEW DASHBOARD
# ==============================================================================
if page_selection == "🏆 Overview Dashboard":
    st.header("🏆 Overview Dashboard")

    # Welcome note moved here for high visibility
    with st.container(border=True):
        st.subheader("Welcome to my live portfolio!")
        st.markdown("This app demonstrates my ability to not only analyze an organization's business challenges but to **build and deploy the technical solutions**.")
        st.markdown(f"**How to Navigate:**")
        st.markdown(f"""
        * Use the menu in the sidebar to explore different sections.
        * **Hover** over any chart for more details.
        * Visit the **'Live Dashboard Demo'** page. The filters for that demo will appear in the sidebar.
        """)
    
    st.markdown("---")

    # --- KEY METRICS ---
    st.subheader("🚀 Quantifiable Achievements at a Glance")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Peak Fraud Risk Mitigation", "60%", "At Milano Orchid")
    col2.metric("Peak Data Accuracy", "80%", "At Treasure Solutions")
    col3.metric("Process Speed (Invoicing)", "30%", "At Treasure Solutions")
    col4.metric("Operational Cost Reduction", "10-15%", "At Milano Orchid")
    st.markdown("---")

    # --- SKILLS CHART ---
    st.subheader("📈 Project-Driven Impact Analysis")
    achievements_data = {
        "Specific Impact": [
            "Data Accuracy (ERP Migration)", "Fraud Risk Mitigation (Controls)",
            "Invoicing Process Speed (Automation)", "Reporting Time (Power BI Dashboards)",
            "Operational Costs (ICT Optimization)", "Cross-Department Efficiency (ERP)",
            "Audit Irregularities (Automated Checks)"
        ],
        "Improvement (%)": [80, 60, 30, 30, 15, 25, 60],
    }
    df_achievements = pd.DataFrame(achievements_data)
    fig_achievements = px.bar(
        df_achievements.sort_values(by="Improvement (%)", ascending=False),
        x="Improvement (%)", y="Specific Impact", orientation='h',
        title="<b>Quantifiable Business Outcomes</b>", text="Improvement (%)",
        color="Improvement (%)", color_continuous_scale=px.colors.sequential.Tealgrn,
    )
    fig_achievements.update_traces(texttemplate='%{text}%', textposition='outside')
    fig_achievements.update_layout(yaxis_title=None, xaxis_title="Percentage Improvement", height=450)
    st.plotly_chart(fig_achievements, use_container_width=True)

    st.markdown("---")
    
    # --- GITHUB SECTION ---
    st.header("💻 My Top 3 GitHub Repositories")
    st.markdown("Here are a few projects I've built. Click the titles to see the code.")
    col_git1, col_git2, col_git3 = st.columns(3)
    with col_git1:
        with st.container(border=True):
            st.subheader("[This Portfolio App 🌟](https://github.com/sleeksofficial/streamlit-portfolio)") # <-- EDIT LINK
            st.markdown("The very portfolio you are viewing right now! A dynamic, multi-page dashboard built to showcase my projects, skills, and analytics.")
            st.markdown("**Technologies:** `Streamlit`, `Python`, `Pandas`, `Plotly`")
    with col_git2:
        with st.container(border=True):
            st.subheader("[Automated Audit Tool ⚙️](https://github.com/sleeksofficial/audit-tool)") # <-- EDIT LINK
            st.markdown("A Python script that ingests financial transaction data (CSV/Excel) and automatically flags anomalies based on custom-defined rules.")
            st.markdown("**Technologies:** `Python`, `Pandas`, `NumPy`")
    with col_git3:
        with st.container(border=True):
            st.subheader("[Dash Sales Dashboard 📈](https://github.com/sleeksofficial/dash-dashboard)") # <-- EDIT LINK
            st.markdown("A multi-page interactive dashboard for analyzing sales performance, built with Dash and deployed to Render. Includes user authentication.")
            st.markdown("**Technologies:** `Dash`, `Plotly`, `Pandas`, `Docker`")

# ==============================================================================
# PAGE 2: LIVE DASHBOARD DEMO
# ==============================================================================
elif page_selection == "💡 Live Dashboard Demo":
    st.header("💡 Live Interactive Dashboard Demo")
    st.markdown("""
    This is a **live, functional dashboard** built with Streamlit and Plotly, running on the same Python script as this portfolio. 
    It demonstrates my ability to build and deploy interactive data applications, not just use off-the-shelf tools.
    
    **Scenario:** Analyzing a sample 'IT & Operations Expense' dataset.
    """)
    df_demo = get_demo_data()
    st.sidebar.header("Demo Filters")
    min_date = df_demo['Date'].min().date()
    max_date = df_demo['Date'].max().date()
    start_date, end_date = st.sidebar.date_input(
        "Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date
    )
    all_departments = df_demo['Department'].unique()
    selected_departments = st.sidebar.multiselect("Select Departments", all_departments, default=all_departments)
    all_expense_types = df_demo['Expense Type'].unique()
    selected_expense_types = st.sidebar.multiselect("Select Expense Types", all_expense_types, default=all_expense_types)
    df_filtered = df_demo[
        (df_demo['Date'].dt.date >= start_date) & (df_demo['Date'].dt.date <= end_date) &
        (df_demo['Department'].isin(selected_departments)) & (df_demo['Expense Type'].isin(selected_expense_types))
    ]
    if df_filtered.empty:
        st.warning("No data matches your filter criteria. Please adjust the filters.")
    else:
        total_spend = df_filtered['Amount ($)'].sum()
        avg_transaction = df_filtered['Amount ($)'].mean()
        num_transactions = len(df_filtered)
        st.subheader("Filtered KPIs")
        kpi_cols = st.columns(3)
        kpi_cols[0].metric("Total Spend", f"${total_spend:,.0f}")
        kpi_cols[1].metric("Average Transaction", f"${avg_transaction:,.2f}")
        kpi_cols[2].metric("Number of Transactions", f"{num_transactions:,}")
        st.markdown("---")
        chart_cols = st.columns([2, 1])
        with chart_cols[0]:
            st.subheader("Spend Over Time")
            df_time = df_filtered.set_index('Date').resample('ME')['Amount ($)'].sum().reset_index()
            fig_time = px.line(df_time, x='Date', y='Amount ($)', title="Total Spend per Month", markers=True)
            fig_time.update_layout(hovermode="x unified")
            st.plotly_chart(fig_time, use_container_width=True)
        with chart_cols[1]:
            st.subheader("Spend by Department")
            df_dept = df_filtered.groupby('Department')['Amount ($)'].sum().reset_index()
            fig_pie_dept = px.pie(df_dept, names='Department', values='Amount ($)', title="Share of Spend", hole=0.3)
            fig_pie_dept.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie_dept, use_container_width=True)
        st.markdown("---")
        st.subheader("Spend Breakdown by Expense Type and Department")
        df_bar = df_filtered.groupby(['Department', 'Expense Type'])['Amount ($)'].sum().reset_index()
        fig_bar_stacked = px.bar(df_bar, x='Department', y='Amount ($)', color='Expense Type', title="Detailed Spend Breakdown", barmode='stack')
        st.plotly_chart(fig_bar_stacked, use_container_width=True)
        with st.expander("View Filtered Raw Data"):
            st.dataframe(df_filtered.sort_values(by="Date", ascending=False))

# ==============================================================================
# PAGE 3: CASE STUDIES (PROJECTS)
# ==============================================================================
elif page_selection == "🚀 Case Studies (Projects)":
    st.header("🚀 High-Impact Projects (Case Studies)")
    st.markdown("Here's *how* I approach problems and deliver solutions. Each project is presented as a case study.")
    col_proj1, col_proj2 = st.columns(2)
    with col_proj1:
        with st.container(border=True):
            st.subheader("Cloud Migration & AI Dashboard")
            st.markdown(
                """
                * **The Problem:** Legacy on-premise systems were slow, expensive, and couldn't provide real-time predictive insights.
                * **My Solution:** I led the full migration of legacy systems to Azure Cloud. Simultaneously, I designed and deployed AI-powered Power BI dashboards that used Azure ML for predictive forecasting.
                * **The Impact (Quantified):** **40% faster report generation**, **25% reduction in server costs**, and a 15% improvement in forecast accuracy.
                * **Technologies Used:** `Azure Cloud`, `Power BI`, `Azure ML`, `SQL`, `Project Management`
                """
            )
    with col_proj2:
        with st.container(border=True):
            st.subheader("Unified ERP Integration")
            st.markdown(
                """
                * **The Problem:** Accounting, procurement, and inventory data were siloed in separate, non-communicating systems, causing manual data entry and reconciliation nightmares.
                * **My Solution:** I managed the integration of these disparate modules into a single, unified ERP platform (Odoo), creating a single source of truth for all financial and operational data.
                * **The Impact (Quantified):** **25% improvement in cross-departmental efficiency**, eliminated data redundancy, and provided 100% data traceability.
                * **Technologies Used:** `ERP (Odoo)`, `SQL`, `Business Process Re-engineering`, `Stakeholder Management`
                """
            )
    with col_proj1:
        with st.container(border=True):
            st.subheader("Audit System Strengthening")
            st.markdown(
                """
                * **The Problem:** The company faced high fraud risk and audit irregularities due to manual, error-prone financial controls.
                * **My Solution:** I designed and implemented a framework of automated internal control checks directly within the financial software, flagging suspicious transactions in real-time.
                * **The Impact (Quantified):** **60% reduction in audit irregularities** and a **60% mitigation of identified fraud risks**.
                * **Technologies Used:** `Internal Control Design`, `ERP Customization`, `Financial Analysis`, `Regulatory Compliance`
                """
            )
    with col_proj2:
        with st.container(border=True):
            st.subheader("Automated Invoicing System")
            st.markdown(
                """
                * **The Problem:** The manual accounts payable process was slow, delaying payments and straining vendor relationships. It took days to process a single invoice.
                * **My Solution:** I deployed an automated invoicing solution that scanned, digitized, and routed invoices for approval, integrating directly with the accounts payable system.
                * **The Impact (Quantified):** **30% reduction in invoice processing time**, near-100% elimination of manual data entry errors, and improved cash flow management.
                * **Technologies Used:** `Process Automation`, `Power BI`, `Excel`, `Financial Modeling`, `BI Integration`
                """
            )

# ==============================================================================
# PAGE 4: MY APPROACH
# ==============================================================================
elif page_selection == "🧠 My Approach":
    st.header("🧠 My Problem-Solving Methodology")
    st.markdown("I believe that technology is a tool to solve business problems, not the other way around. My approach is a structured, four-step process focused on delivering measurable value.")
    with st.container(border=True):
        st.subheader("1. Discover & Analyze")
        st.markdown(
            """
            I start by meeting with stakeholders—from executives to end-users—to understand the true business pain point, not just the technical request. 
            I ask *'Why?'* to uncover root causes and map existing processes. This stage is all about data gathering and requirement analysis.
            """
        )
    with st.container(border=True):
        st.subheader("2. Design & Model")
        st.markdown(
            """
            With a clear problem defined, I design the solution. This could be a financial model in Excel, a new Power BI dashboard architecture,
            or a re-engineered business process. I create prototypes and cost-benefit analyses to ensure the solution aligns with strategic goals.
            """
        )
    with st.container(border=True):
        st.subheader("3. Implement & Test")
        st.markdown(
            """
            This is where the plan comes to life. I lead the implementation, whether it's an ERP migration, 
            deploying an automated system, or rolling out new internal controls. 
            I manage the project using Agile principles and conduct rigorous testing to ensure data accuracy and system integrity.
            """
        )
    with st.container(border=True):
        st.subheader("4. Deliver, Train, & Iterate")
        st.markdown(
            """
            A solution is useless if no one uses it. I deliver the final product with comprehensive training for all end-users.
            I create documentation and establish KPIs to measure success. Finally, I gather user feedback to iterate and continuously improve the solution.
            """
        )

# ==============================================================================
# PAGE 5: SKILLS & EXPERTISE
# ==============================================================================
elif page_selection == "🛠️ Skills & Expertise":
    st.header("🛠️ Skills & Expertise")
    st.markdown("A detailed breakdown of my capabilities, combining technical, financial, and managerial expertise.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container(border=True):
            st.subheader("📊 Data & Analytics")
            st.markdown(
                """
                * Power BI (Advanced)
                * Tableau
                * Advanced Excel (Modeling, VBA)
                * SQL
                * Data Visualization
                * Data Analytics for Business
                * Financial Forecasting
                * Economic & Data Analysis
                """
            )
            
    with col2:
        with st.container(border=True):
            st.subheader("🛠️ Project & ICT Management")
            st.markdown(
                """
                * Agile Project Management
                * PRINCE2 Certification (In-Prog)
                * Scrum Master (In-Prog)
                * ERP Integration (SAP, Odoo)
                * Digital Transformation
                * ICT-Enabled Process Automation
                * Stakeholder Engagement
                * Change Management
                * Risk & Cost Control
                * Governance & Compliance
                """
            )

    with col3:
        with st.container(border=True):
            st.subheader("💰 Finance, Audit & Compliance")
            st.markdown(
                """
                * Internal Control Systems
                * Audit Readiness
                * Financial Reporting (IFRS)
                * Risk Management
                * Fraud Prevention
                * Regulatory Compliance (VAT, Tax)
                * Financial Analysis
                * Budget Forecasting
                * Variance Analysis
                * Accounting Software (Tally, SAP, Quick-book, AL-Ameen)
                """
            )

# ==============================================================================
# PAGE 6: EDUCATION & CERTIFICATIONS
# ==============================================================================
elif page_selection == "🎓 Education & Certifications":
    st.header("🎓 Education & Certifications")
    
    st.subheader("Education")
    with st.container(border=True):
        st.markdown("**Bsc Economics** (2018)")
        st.markdown("*University of Ilorin, Kwara State, Nigeria*")
        
    with st.container(border=True):
        st.markdown("**Diploma in Business Management** (2021)")
        st.markdown("*University of South Florida, Muna college of Business, USA*")

    with st.container(border=True):
        st.markdown("**Diploma in Business Administration & Management** (2012-2015)")
        st.markdown("*Federal Polytechnic Offa, Nigeria*")
        
    with st.container(border=True):
        st.markdown("**Diploma - Business Administration** (2014)")
        st.markdown("*International Business Management Institute, Berlin, Germany*")
        
    st.markdown("---")
    
    st.subheader("Certifications & Training")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown("**PRINCE2 Project Management** (In Progress)")
        with st.container(border=True):
            st.markdown("**Scrum Master** (In Progress)")
        with st.container(border=True):
            st.markdown("**Power BI Essentials** (2022)")
            st.markdown("*NASBA, USA*")
        with st.container(border=True):
            st.markdown("**Data Analytics for Business Professionals** (2022)")
            st.markdown("*NASBA, USA*")
    
    with col2:
        with st.container(border=True):
            st.markdown("**Economic & Data Analysis** (2022)")
            st.markdown("*IIBA & PMI*")
        with st.container(border=True):
            st.markdown("**Financial Forecasting with Analytics Essentials**")
            st.markdown("*NASBA, USA*")
        with st.container(border=True):
            st.markdown("**Business Intelligence for Consultants**")
            st.markdown("*NASBA, USA*")

# ==============================================================================
# PAGE 7: PROFESSIONAL EXPERIENCE
# ==============================================================================
elif page_selection == "💼 Professional Experience":
    st.header("💼 Professional Experience")
    st.markdown("My career has been focused on leveraging technology and data to drive strategic business outcomes.")
    
    with st.expander("**Business & ICT Analyst** - Milano Orchid Aluminum Trading LLC (Dubai, UAE)", expanded=True):
        st.markdown(
            """
            * **Dates:** May 2021 - Sept 2024
            * Spearheaded development of **Power BI dashboards**, resulting in a **30% reduction in reporting time**.
            * Led end-to-end **ERP migration**, enhancing data accuracy by **20%**.
            * Conducted **cost-benefit analyses** for ICT upgrades, saving **10% in operational costs**.
            * Implemented internal controls that mitigated **fraud risk by 60%**.
            """
        )
    
    with st.expander("**Business & Financial Analyst** - Treasure Solutions General Trading LLC (Ajman, UAE)"):
        st.markdown(
            """
            * **Dates:** Jan 2020 - Mar 2021
            * Designed and implemented **automated invoicing solutions**, reducing processing time by **30%**.
            * Integrated financial data sources into **BI tools** for real-time decision support.
            * Led implementation of accounting software, driving an **80% improvement in data accuracy**.
            """
        )

    with st.expander("**Accountant / Business Analyst** - Zenith Accounting Agency (Lagos, Nigeria)"):
        st.markdown(
            """
            * **Dates:** Jan 2016 - Dec 2020
            * Implemented **standardized accounting and ICT systems**, improving reporting accuracy by **20%**.
            * Maintained **100% compliance** in tax filings and VAT documentation.
            * Developed **fraud-prevention procedures** that lowered discrepancy incidents by **30%**.
            """
        )

# ==============================================================================
# PAGE 8: MY CVS
# ==============================================================================
elif page_selection == "📄 My CVs":
    st.header("📄 Download & Review My Tailored CVs")
    st.markdown("Select a CV below to download or view it directly in the browser. Each is tailored for a specific role.")
    col_cv1, col_cv2, col_cv3 = st.columns(3)
    
    with col_cv1:
        st.subheader("Business/ICT Analyst")
        st.markdown("Focus on Power BI, process re-engineering, and BI.")
        if cv_data_1:
            st.download_button(
                label="Download CV (BI Analyst) ⬇️", data=cv_data_1,
                file_name="Oloruntoba_Anate_BI_Analyst_CV.pdf",
                mime="application/pdf", use_container_width=True
            )
            if st.button("View CV (BI Analyst) 👁️", key="view_cv1", use_container_width=True):
                display_pdf(cv_data_1, CV_FILE_1)
        else: st.error(f"File '{CV_FILE_1}' not found.")
        
    with col_cv2:
        st.subheader("Auditor / Fin. Analyst")
        st.markdown("Focus on financial controls, compliance, and analysis.")
        if cv_data_2:
            st.download_button(
                label="Download CV (Auditor) ⬇️", data=cv_data_2,
                file_name="Oloruntoba_Anate_Auditor_CV.pdf",
                mime="application/pdf", use_container_width=True
            )
            if st.button("View CV (Auditor) 👁️", key="view_cv2", use_container_width=True):
                display_pdf(cv_data_2, CV_FILE_2)
        else: st.error(f"File '{CV_FILE_2}' not found.")
        
    with col_cv3:
        st.subheader("ICT Project Manager")
        st.markdown("Focus on digital transformation, ERP, and Agile delivery.")
        if cv_data_3:
            st.download_button(
                label="Download CV (ICT PM) ⬇️", data=cv_data_3,
                file_name="Oloruntoba_Anate_ICT_PM_CV.pdf",
                mime="application/pdf", use_container_width=True
            )
            if st.button("View CV (ICT PM) 👁️", key="view_cv3", use_container_width=True):
                display_pdf(cv_data_3, CV_FILE_3)
        else: st.error(f"File '{CV_FILE_3}' not found.")

# ==============================================================================
# PAGE 9: CONTACT
# ==============================================================================
elif page_selection == "💬 Contact":
    st.header("💬 Get in Touch!")
    st.markdown("I'm open to discussing new opportunities, collaborations, or innovative projects. Let's connect.")
    st.markdown("---")
    
    col_form, col_links = st.columns([2, 1])
    
    with col_form:
        st.subheader("Send me a message:")
        
        # --- THIS IS THE FIX ---
        
        # 1. Initialize the session state variable if it doesn't exist
        if "form_submitted" not in st.session_state:
            st.session_state.form_submitted = False
            
        # 2. Create an empty placeholder for status messages
        status_placeholder = st.empty()
        
        # 3. Check the state. If form_submitted is True, show success and stop.
        if st.session_state.form_submitted:
            status_placeholder.success("Thank you for your message! I've received it. \n\n*Please refresh the page if you need to send another.*")
        
        # 4. If form_submitted is False, show the form.
        else:
            with st.form("contact_form"):
                name = st.text_input("Your Name *")
                email = st.text_input("Your Email *")
                subject = st.text_input("Subject")
                message = st.text_area("Your Message *", height=150)
                submit_button = st.form_submit_button("Send Message")
                
                if submit_button:
                    if not name or not email or not message:
                        status_placeholder.error("Please fill in all required fields (*).")
                    else:
                        status_placeholder.info("Sending your message... Please wait.")
                        
                        success = send_email(name, email, subject, message)
                        
                        if success:
                            # 5. On success, set the state to True
                            st.session_state.form_submitted = True
                            # Rerun the script immediately to show the success message
                            st.rerun() 
                        else:
                            status_placeholder.error("Sorry, there was a problem sending your message. Please try emailing me directly.")
                    
    with col_links:
        st.subheader("Contact Details:")
        st.markdown(
            """
            **📧 Email:**
            [anatepapilo@gmail.com](mailto:anatepapilo@gmail.com)
            
            **📞 Phone:**
            [+2348141269872](tel:+2348141269872) | [+971585056864](tel:+9T1585056864)
            
            **🔗 LinkedIn:**
            [linkedin.com/in/sleeksofficial](https.linkedin.com/in/sleeksofficial)
            
            **💻 GitHub:**
            [github.com/Sleeksofficial](https://github.com/Sleeksofficial)
            
            **📍 Location:**
            Dubai, UAE | Lagos, Nigeria
            """

        )

