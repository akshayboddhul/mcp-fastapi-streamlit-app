import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.title("Inventory Management System 📦")

# Display a form to create a new item
st.header("Add a New Item")
with st.form("add_item_form"):
    name = st.text_input("Item Name")
    quantity = st.number_input("Quantity", min_value=0, step=1)
    price = st.number_input("Price", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Add Item")

    if submitted and name:
        new_item = {"name": name, "quantity": quantity, "price": price}
        response = requests.post(f"{API_URL}/items/", json=new_item)
        if response.status_code == 200:
            st.success("Item added successfully!")
        else:
            st.error(f"Error adding item: {response.json()['detail']}")

# Get item by ID
st.header("Get Item by ID")
with st.form("get_item_form"):
    item_id = st.number_input("Item ID", min_value=1, step=1)
    get_submitted = st.form_submit_button("Get Item")

    if get_submitted:
        try:
            response = requests.get(f"{API_URL}/items/{item_id}")
            if response.status_code == 200:
                item_data = response.json()
                st.write("Item Details:")
                st.json(item_data)
            else:
                st.error(f"Error retrieving item: {response.json()['detail']}")
        except requests.exceptions.ConnectionError:
            st.warning(
                "Could not connect to the FastAPI backend. Please ensure it's running."
            )

# Delete item by ID
st.header("Delete Item by ID")
with st.form("delete_item_form"):
    delete_item_id = st.number_input("Item ID to Delete", min_value=1, step=1)
    delete_submitted = st.form_submit_button("Delete Item")

    if delete_submitted:
        try:
            response = requests.delete(f"{API_URL}/items/{delete_item_id}")
            if response.status_code == 200:
                st.success(f"Item with ID {delete_item_id} deleted successfully!")
            else:
                st.error(f"Error deleting item: {response.json()['detail']}")
        except requests.exceptions.ConnectionError:
            st.warning(
                "Could not connect to the FastAPI backend. Please ensure it's running."
            )

# Display the current inventory
st.header("Current Inventory")
if st.button("Refresh Inventory"):
    try:
        response = requests.get(f"{API_URL}/items/")
        items_data = response.json()
        if items_data:
            df = pd.DataFrame(items_data)
            st.dataframe(df)
        else:
            st.info("No items in the inventory yet.")
    except requests.exceptions.ConnectionError:
        st.warning(
            "Could not connect to the FastAPI backend. Please ensure it's running."
        )
