import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")

    url_input = st.text_input(
        "Enter a job posting URL:",
        value="https://jobs.nike.com/job/R-33460"
    )
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            docs = loader.load()

            if not docs:
                st.error("❌ Failed to load content from the provided URL.")
                return

            data = clean_text(docs[0].page_content)

            portfolio.load_portfolio()

            jobs = llm.extract_jobs(data)
            if not jobs:
                st.warning("⚠️ No jobs found on this page.")
                return

            for job in jobs:
                skills = job.get("skills", [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language="markdown")

        except Exception as e:
            st.error(f"⚠️ An Error Occurred: {e}")


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

    chain = Chain()
    portfolio = Portfolio()

    create_streamlit_app(chain, portfolio, clean_text)
