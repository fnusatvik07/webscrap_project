import streamlit as st 
from src.oxylabs_client import scrape_product_details
from src.services import scrape_and_store,fetch_and_store_competitors
from src.db import Database


def render_header():
    st.title("Amazon Competitor Analysis")
    st.subheader("Enter Product Name or ASIN to get product Insights")

def render_inputs():
    asin=st.text_input("ASIN",placeholder="B0N32423SAD")
    geo=st.text_input("ZIP/Postal Code",placeholder="e.g., 10001")
    domain=st.selectbox("Domain",[
        "com",
        "co.uk",
        "ca",
        "in",
        "fr",
        "it",
        "es"
    ])

    return asin.strip(),geo.strip(),domain

def render_product_card(product):
    with st.container(border=True):
        cols=st.columns([1,2])

        try:
            images=product.get("images",[])
            if images and len(images)>0:
                cols[0].image(images[0],width=200)
            else:
                cols[0].write("No Image Found")
        
        except:
            cols[0].write("Error Loading Image")

        with cols[1]:
            st.subheader(product.get("title") or product["asin"])
            info_cols=st.columns(3)

            currency=product.get("currency","")
            price=product.get("price","-")

            info_cols[0].metric("Price",f"{currency}{price}" if currency else price)
            info_cols[1].write(f"Brand: {product.get("brand",'-')}")
            info_cols[2].write(f"Product: {product.get('product','-')}")

            domain_info=f"Amazon.{product.get('amazon_domain','com')}"
            geo_info=product.get("geo_location","-")
            st.caption(f"Domain: {domain_info} | Geo Location: {geo_info}")

            st.write(product.get("url",""))
            if st.button("Start Analyzing Competitors",key=f"analyze_{product['asin']}"):
                st.session_state["analyzing_asin"]=product["asin"]

def main():
    st.set_page_config(page_title="Amazon Competitor Analysis", page_icon="🛒", layout='wide')

    # Header + user inputs
    render_header()
    asin, geo, domain = render_inputs()

    # --------------------------
    # 1️⃣ SCRAPE PRODUCT SECTION
    # --------------------------
    if st.button("Scrape Product") and asin:
        with st.spinner("Scraping Product Data..."):
            product_data = scrape_and_store(asin, geo, domain)

        st.success(f"Product scraped successfully for ASIN: {asin}")
        render_product_card(product_data)

        # Store the latest product in session_state (optional but useful)
        st.session_state["current_product"] = product_data

    # If product was scraped earlier in this session, show it again
    elif "current_product" in st.session_state:
        render_product_card(st.session_state["current_product"])

    # -----------------------------------------------------
    # 2️⃣ CHECK IF USER CLICKED "START ANALYZING COMPETITORS"
    # -----------------------------------------------------
    selected_asin = st.session_state.get("analyzing_asin")

    if selected_asin:
        st.divider()
        st.subheader(f"Competitor Analysis for {selected_asin}")

        db = Database()

        # Check if competitors already stored in DB
        existing_comps = db.search_products({"parent_asin": selected_asin})

        if not existing_comps:
            with st.spinner("Fetching competitor data..."):
                comps = fetch_and_store_competitors(selected_asin, domain, geo)
            st.success(f"Found {len(comps)} competitors!")
        else:
            st.info(f"Found {len(existing_comps)} competitors already in database.")

        # --------------------------
        # 3️⃣ ANALYZE WITH LLM (Placeholder for now)
        # --------------------------
        if st.button("Analyze with LLM", type="primary"):
            st.info("Running placeholder LLM logic...")

            # Temporary until you create real LLM function
            analysis_text = f"LLM analysis for ASIN {selected_asin} is not implemented yet."
            st.markdown(analysis_text)





if __name__=="__main__":
    main()
