# Oloruntoba Anate's Interactive Portfolio

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://oloruntoba-portfolio.onrender.com)
## 🚀 Live Demo

**View the live, deployed application here:**
https://oloruntoba-portfolio.onrender.com/
---

## 📸 Project Showcase

(I highly recommend you take a screenshot of your dashboard and drag it into this file here. A visual makes a huge difference!)

<img width="955" height="388" alt="Screenshot 2025-10-24 025530" src="https://github.com/user-attachments/assets/1dc5ebcd-c395-4b34-9abe-6d8fadcb5b70" />


---

## 💡 About This Project

This is not just a resume; it's a live, multi-page web application built with Python and Streamlit.

I created this portfolio to be a real-time demonstration of my capabilities. It's a containerized application that shows my ability to not only analyze an organization's business challenges but to **build and deploy the technical solutions**.

It showcases my multi-disciplinary skills as an **Auditor**, a **Financial Analyst**, and an **ICT Project Manager**.

## ✨ Key Features

* **Multi-Page Navigation:** A clean sidebar separates the app into logical sections.
* **Interactive Demo Dashboard:** A live, filterable dashboard built with Plotly and Pandas, proving my ability to build data-driven tools.
* **In-Depth Case Studies:** Breaks down my key projects into `Problem`, `Solution`, and `Impact`.
* **Skills & Methodology:** Dedicated pages for my technical/financial skills and my professional problem-solving approach.
* **Functional Contact Form:** A secure, automated contact form that uses `smtplib` and Google's SMTP server to send emails directly to my inbox.
* **CV Viewer & Downloader:** Allows users to view or download my three tailored CVs directly.
* **Containerized Deployment:** The entire application is containerized with Docker, proving my skills in modern deployment workflows.

## 🛠️ Tech Stack

* **Python 3.11**
* **Streamlit:** For the web app framework.
* **Pandas & NumPy:** For data manipulation in the demo dashboard.
* **Plotly Express:** For all interactive charts and graphs.
* **Pillow (PIL):** For image handling.
* **smtplib & ssl:** For the secure, backend email functionality.
* **Docker:** For containerization.
* **Render:** For cloud hosting and CI/CD.

## 🏃‍♂️ How to Run Locally

You can run this entire application on your local machine.

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Sleeksofficial/portfolio.git](https://github.com/Sleeksofficial/portfolio.git)
    cd Portfolio
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Email Secrets:**
    To make the contact form work, you must provide your email credentials.
    * Create a folder named `.streamlit` in the root of the project.
    * Inside that folder, create a file named `secrets.toml`.
    * Add the following content (Use a **[Google App Password](https://myaccount.google.com/apppasswords)**, not your regular password):
        ```toml
        [email]
        address = "your-email@gmail.com"
        password = "your-16-digit-app-password"
        ```

5.  **Run the App:**
    ```bash
    streamlit run app.py
    ```
    Your portfolio will open in your browser at `http://localhost:8501`.

## ☁️ Deployment

This application is containerized using the provided `Dockerfile` and is configured for continuous deployment on [Render](https://render.com/).

When pushed to the main branch, Render automatically:
1.  Builds the Docker image from the `Dockerfile`.
2.  Injects the `secrets.toml` file (configured as a Secret File in Render).
3.  Deploys the new container, ensuring zero downtime.
