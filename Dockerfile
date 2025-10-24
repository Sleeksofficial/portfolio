# (Keep everything else in your Dockerfile the same)

# This new CMD uses the $PORT variable Render provides, 
# and defaults to 8501 if it's not set (for local testing).
CMD streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0