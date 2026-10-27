import os
import requests
import streamlit as st
from urllib.parse import quote


API_BASE = os.environ.get("BANK_API_URL", "http://127.0.0.1:8001")
st.set_page_config(page_title="Bank Account App", page_icon="🏦", layout="wide")

if "api_base" not in st.session_state:
    st.session_state.api_base = API_BASE


def call_api(path: str, method: str = "GET", payload: dict | None = None):
    base_url = st.session_state.get("api_base", API_BASE)
    url = f"{base_url.rstrip('/')}{path}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json=payload, timeout=10)

        try:
            data = response.json()
        except ValueError:
            data = response.text

        return response.status_code, data
    except requests.RequestException as exc:
        return 503, {"error": f"API request failed: {exc}"}


def api_is_connected(base_url: str) -> bool:
    try:
        response = requests.get(f"{base_url.rstrip('/')}/health", timeout=3)
        return response.ok and response.json().get("status") == "ok"
    except (requests.RequestException, ValueError):
        return False


st.title("🏦 Bank Account Manager")

with st.sidebar:
    st.subheader("API Settings")
    api_base = st.text_input("FastAPI base URL", value=st.session_state.api_base)
    if api_base:
        st.session_state.api_base = api_base
        API_BASE = api_base

    if api_is_connected(st.session_state.api_base):
        st.success("Backend connected")
    else:
        st.error("Backend unavailable. Start the FastAPI server and check its URL.")


if "last_result" not in st.session_state:
    st.session_state.last_result = None


col1, col2 = st.columns(2)

with col1:
    st.subheader("Create Account")
    with st.form("create_account_form"):
        owner = st.text_input("Owner")
        balance = st.number_input("Starting balance", min_value=0, step=1)
        create_clicked = st.form_submit_button("Create account")

    if create_clicked:
        status, result = call_api("/account/create", "POST", {"owner": owner, "balance": int(balance)})
        st.session_state.last_result = {"status": status, "result": result}
        st.write(result)

with col2:
    st.subheader("Check Account")
    with st.form("get_account_form"):
        owner_lookup = st.text_input("Owner name", key="lookup_owner")
        lookup_clicked = st.form_submit_button("Get account")

    if lookup_clicked:
        status, result = call_api(f"/account/{quote(owner_lookup, safe='')}")
        st.session_state.last_result = {"status": status, "result": result}
        st.write(result)

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Deposit")
    with st.form("deposit_form"):
        deposit_owner = st.text_input("Owner", key="deposit_owner")
        deposit_amount = st.number_input("Amount", min_value=1, step=1, key="deposit_amount")
        deposit_clicked = st.form_submit_button("Deposit")

    if deposit_clicked:
        status, result = call_api("/account/deposit", "POST", {"owner": deposit_owner, "amount": int(deposit_amount)})
        st.session_state.last_result = {"status": status, "result": result}
        st.write(result)

with col4:
    st.subheader("Withdraw")
    with st.form("withdraw_form"):
        withdraw_owner = st.text_input("Owner", key="withdraw_owner")
        withdraw_amount = st.number_input("Amount", min_value=1, step=1, key="withdraw_amount")
        withdraw_clicked = st.form_submit_button("Withdraw")

    if withdraw_clicked:
        status, result = call_api("/account/withdraw", "POST", {"owner": withdraw_owner, "amount": int(withdraw_amount)})
        st.session_state.last_result = {"status": status, "result": result}
        st.write(result)

st.markdown("---")

st.subheader("Transfer")
with st.form("transfer_form"):
    from_owner = st.text_input("From owner", key="from_owner")
    to_owner = st.text_input("To owner", key="to_owner")
    transfer_amount = st.number_input("Transfer amount", min_value=1, step=1, key="transfer_amount")
    transfer_clicked = st.form_submit_button("Transfer")

if transfer_clicked:
    status, result = call_api(
        "/account/transfer",
        "POST",
        {"from_owner": from_owner, "to_owner": to_owner, "amount": int(transfer_amount)},
    )
    st.session_state.last_result = {"status": status, "result": result}
    st.write(result)

st.markdown("---")

st.subheader("Saved Accounts")
accounts_status, saved_accounts = call_api("/account")
if accounts_status == 200:
    if saved_accounts:
        st.dataframe(saved_accounts, hide_index=True, use_container_width=True)
    else:
        st.info("No accounts have been saved yet.")
else:
    st.error(f"Could not load saved accounts: {saved_accounts}")

st.markdown("---")

st.subheader("Latest API Response")
if st.session_state.last_result:
    st.code(st.session_state.last_result)
else:
    st.info("No API request has been made yet.")
