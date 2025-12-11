import streamlit as st 
from src.oxylabs_client import scrape_product_details
from src.services import scrape_and_store

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
            if st.button("Start Analzong Competitors",key=f"analyze_{product['asin']}"):
                st.session_state["analyzing_asin"]=product["asin"]


def main():
    st.set_page_config(page_title="Amazon Competitor Analysis",page_icon="🛒",layout='wide')
    render_header()
    asin,geo,domain=render_inputs() 

    if st.button("Scrape Product") and asin:
        with st.spinner("Scraping Product Data"):
            product_data=scrape_and_store(asin,geo,domain)
        st.success(f"Product Scraped Successfully for ASIN : {asin}")
        render_product_card(product_data)
        



if __name__=="__main__":
    main()
