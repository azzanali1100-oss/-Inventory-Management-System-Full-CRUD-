import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="Inventory Management System",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Inventory Management System (Full CRUD)")
st.caption("FastAPI + MySQL + Streamlit")

st.divider()

def fetch_all_items():
    """Helper to fetch all items."""
    try:
        response = requests.get(f"{API_URL}/items/", timeout=5)
        if response.status_code == 200:
            return response.json().get("data", []), None
        return None, f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return None, f"Connection error: {str(e)}"

# --- SECTION 1: INVENTORY TABLE ---
st.subheader("📋 Current Inventory")

items_list, error = fetch_all_items()

if error:
    st.error(f"🚨 {error}")
elif items_list:
    st.dataframe(items_list, use_container_width=True)
else:
    st.info("No items found in database.")

st.divider()

# --- SECTION 2: CRUD OPERATIONS (TABS) ---
tab_create, tab_update, tab_delete = st.tabs(["➕ Add Item", "✏️ Update Item", "🗑️ Delete Item"])

# --- TAB 1: CREATE (POST) ---
with tab_create:
    st.subheader("Add New Item")
    with st.form("create_form", clear_on_submit=True):
        name = st.text_input("Name*")
        description = st.text_area("Description")
        price = st.number_input("Price ($)*", min_value=0.00, value=10.00, step=0.50, format="%.2f")
        submit_create = st.form_submit_button("Save Item")

        if submit_create:
            if not name.strip():
                st.warning("Item name is required.")
            else:
                payload = {"name": name.strip(), "description": description.strip(), "price": float(price)}
                res = requests.post(f"{API_URL}/items/", json=payload)
                if res.status_code == 200:
                    st.success("Item created successfully!")
                    st.rerun()
                else:
                    st.error(f"Failed to create: {res.text}")

# --- TAB 2: UPDATE (PUT) ---
with tab_update:
    st.subheader("Edit Existing Item")
    if items_list:
        # Create a dropdown mapping "ID - Name" to the full item dictionary
        item_options = {f"{item['id']} - {item['name']}": item for item in items_list}
        selected_option = st.selectbox("Select item to update:", list(item_options.keys()))
        selected_item = item_options[selected_option]

        with st.form("update_form"):
            up_name = st.text_input("Name*", value=selected_item["name"])
            up_desc = st.text_area("Description", value=selected_item["description"] or "")
            up_price = st.number_input("Price ($)*", min_value=0.00, value=float(selected_item["price"]), step=0.50, format="%.2f")
            submit_update = st.form_submit_button("Update Item")

            if submit_update:
                payload = {"name": up_name.strip(), "description": up_desc.strip(), "price": float(up_price)}
                res = requests.put(f"{API_URL}/items/{selected_item['id']}", json=payload)
                if res.status_code == 200:
                    st.success("Item updated successfully!")
                    st.rerun()
                else:
                    st.error(f"Failed to update: {res.text}")
    else:
        st.info("No items available to update.")

# --- TAB 3: DELETE (DELETE) ---
with tab_delete:
    st.subheader("Delete Item")
    if items_list:
        item_options = {f"{item['id']} - {item['name']}": item for item in items_list}
        selected_option = st.selectbox("Select item to delete:", list(item_options.keys()), key="delete_select")
        selected_item = item_options[selected_option]

        st.warning(f"Are you sure you want to delete **{selected_item['name']}** (ID: {selected_item['id']})?")
        if st.button("🔴 Confirm Delete"):
            res = requests.delete(f"{API_URL}/items/{selected_item['id']}")
            if res.status_code == 200:
                st.success("Item deleted successfully!")
                st.rerun()
            else:
                st.error(f"Failed to delete: {res.text}")
    else:
        st.info("No items available to delete.")