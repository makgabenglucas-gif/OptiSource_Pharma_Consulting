import streamlit as st

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image("logo.png.png", width=300)


# =============================================================================
# DEPENDENCIES & SETUP
# Run this command in your terminal to install the required packages:
# pip install streamlit web3 streamlit-js-eval
# =============================================================================

import json
import streamlit as st
from web3 import Web3
# from web3.middleware import geth_poa_middleware
from streamlit_js_eval import streamlit_js_eval
from config import CONTRACT_ABI, CONTRACT_ADDRESS
import config



# =============================================================================
# BLOCKCHAIN CONNECTION
# =============================================================================
# Connect to the Sepolia network using the URL from config.py
w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
# Inject Proof of Authority middleware, which is required for Sepolia
# w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Initialize the contract using the placeholders from our config
# contract_abi = json.loads(CONTRACT_ABI) if CONTRACT_ABI != "[]" else []
contract_abi = CONTRACT_ABI if isinstance(CONTRACT_ABI, list) else json.loads(CONTRACT_ABI)
contract = w3.eth.contract(address=w3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)
print('contract', contract)

# try:
    
# except Exception:
#     contract = None

# =============================================================================
# HEADER UI LOGIC
# =============================================================================
def render_header():
    """Renders the logo or app name, tagline, and description on every page."""
    try:
        # Attempt to open the logo file to check if it exists safely
        with open(config.LOGO_PATH, "rb"):
            st.image(config.LOGO_PATH, width=200)
    except Exception:
        # Fall back to the text title if the logo is missing
        st.title(config.APP_NAME)
        
    st.caption(config.TAGLINE)
    st.write(config.DESCRIPTION)
    st.divider()

# =============================================================================
# METAMASK INTEGRATION
# =============================================================================
def get_connected_wallet():
    """Asks the browser for the connected MetaMask wallet address."""
    # This JavaScript asks MetaMask for the active account
    js_code = "window.ethereum ? window.ethereum.request({method: 'eth_requestAccounts'}).then(res => res[0]) : null"
    # Execute the JS in the browser and return the result to Python
    return streamlit_js_eval(js_expressions=js_code, key="wallet_conn")

def send_transaction(func_name, args, wallet_address, tx_key):
    """Builds an unsigned transaction and sends it to MetaMask to be signed."""
    if not contract:
        st.error("Smart contract not properly configured. Please update config.py with the ABI.")
        return
        
    with st.spinner("Preparing transaction... Please check your MetaMask extension."):
        try:
            # Package the function call into raw data
            tx_data = contract.encode_abi(func_name, args=args)
            
            # Create the transaction details dictionary
            tx_params = {
                "to": CONTRACT_ADDRESS,
                "from": wallet_address,
                "data": tx_data
            }
            
            # Send the transaction details to MetaMask via JavaScript
            js_code = f"window.ethereum.request({{method: 'eth_sendTransaction', params: [{json.dumps(tx_params)}]}})"
            tx_hash = streamlit_js_eval(js_expressions=js_code, key=tx_key)
            
            if tx_hash:
                st.success("Action submitted successfully!")
                st.markdown(f"[View Transaction Details on Etherscan](https://sepolia.etherscan.io/tx/{tx_hash})")
        except Exception as e:
            st.error(f"Could not process action. Make sure you are the authorised user. Error details: {e}")

# =============================================================================
# PAGES
# =============================================================================

def page_overview(wallet_address):
    """The landing page showing system health and basic statistics."""
    st.header("System Overview")
    
    if contract:
        try:
            with st.spinner("Fetching live network data..."):
                # Read basic data from the contract
                admin_address = contract.functions.hospitalAdmin().call()
                total_orders = contract.functions.orderCount().call()
                
            col1, col2, col3 = st.columns(3)
            
            col1.metric("Total Purchase Orders", total_orders)
            
            # Show if the connected user is the hospital administrator
            is_admin = "Yes" if wallet_address and wallet_address.lower() == admin_address.lower() else "No"
            col2.metric("Are you the Administrator?", is_admin)
            
            # Check network connection status
            network_status = "Connected to Sepolia" if w3.is_connected() else "Offline"
            col3.metric("Network Status", network_status)
            
            st.info(f"**Administrator Wallpython -m pip install streamlit:** {admin_address}")
            
        except Exception as e:
            st.error("Could not fetch data from the blockchain. Please ensure the ABI and Address are correct.")
    else:
        st.warning("Application is in Setup Mode. Please add the ABI to config.py.")

def page_supplier_management(wallet_address):
    """Allows companies to apply, and admins to verify them."""
    st.header("Supplier Management")
    
    tab1, tab2, tab3 = st.tabs(["Apply as Supplier", "Verify Supplier (Admin)", "Supplier Lookup"])
    
    with tab1:
        st.subheader("Join the Network")
        company_name = st.text_input("Company Name", help="Enter the legal name of your pharmaceutical company.")
        if st.button("Submit Application"):
            if not wallet_address:
                st.error("Please connect your wallet first.")
            elif company_name:
                send_transaction("applyAsSupplier", [company_name], wallet_address, "tx_apply_supp")
            else:
                st.warning("Please provide a company name.")
                
    with tab2:
        st.subheader("Approve a Supplier")
        supplier_wallet = st.text_input("Supplier Wallet Address", help="Enter a valid Ethereum wallet address starting with 0x.")
        esg_score = st.number_input("Initial Environmental, Social, and Governance (ESG) Score", min_value=0, max_value=100, value=50)
        if st.button("Verify & Activate"):
            if not wallet_address:
                st.error("Please connect your wallet first.")
            elif supplier_wallet:
                try:
                    clean_address = w3.to_checksum_address(supplier_wallet)
                    send_transaction("verifySupplier", [clean_address, int(esg_score)], wallet_address, "tx_verify_supp")
                except ValueError:
                    st.error("Invalid wallet address format.")
            else:
                st.warning("Please provide the supplier's wallet address.")
                
    with tab3:
        st.subheader("Check Supplier Status")
        lookup_wallet = st.text_input("Wallet Address to Lookup", help="Starts with 0x...")
        if st.button("Search Database"):
            if lookup_wallet and contract:
                try:
                    clean_address = w3.to_checksum_address(lookup_wallet)
                    with st.spinner("Querying blockchain..."):
                        # Returns a tuple of the Supplier struct
                        supplier_data = contract.functions.suppliers(clean_address).call()
                        
                        st.write("### Supplier Details")
                        st.write(f"**Name:** {supplier_data[0]}")
                        
                        # Translate the numeric status into English
                        human_status = config.ENTITY_STATUS.get(supplier_data[2], "Unknown")
                        st.write(f"**Current Status:** {human_status}")
                        st.write(f"**Is Verified?** {'Yes' if supplier_data[3] else 'No'}")
                        st.write(f"**ESG Score:** {supplier_data[4]}/100")
                except ValueError:
                    st.error("Invalid wallet address format.")
                except Exception as e:
                    st.error(f"Could not retrieve supplier: {e}")

def page_purchase_orders(wallet_address):
    """Handling the creation and tracking of purchase orders."""
    st.header("Purchase Orders")
    
    tab1, tab2 = st.tabs(["Create New Order (Admin)", "Track Existing Order"])
    
    with tab1:
        st.subheader("Initiate a Procurement")
        target_supplier = st.text_input("Authorised Supplier Wallet", help="The supplier must be 'Active' to receive an order.")
        order_amount = st.number_input("Order Quantity", min_value=1, step=1, help="Number of pharmaceutical units requested.")
        
        if st.button("Place Order"):
            if not wallet_address:
                st.error("Please connect your wallet.")
            elif target_supplier:
                try:
                    clean_address = w3.to_checksum_address(target_supplier)
                    send_transaction("createPurchaseOrder", [clean_address, int(order_amount)], wallet_address, "tx_create_po")
                except ValueError:
                    st.error("Invalid supplier wallet address.")
            else:
                st.warning("Supplier address is required.")
                
    with tab2:
        st.subheader("Order Lookup")
        order_id = st.number_input("Enter Order ID", min_value=1, step=1)
        if st.button("Search Order"):
            if contract:
                try:
                    with st.spinner("Fetching order..."):
                        order_data = contract.functions.orders(int(order_id)).call()
                        
                        # order_data mapping: [id, supplier, hospital, amount, status, coldChainViolated, paymentReleased]
                        if order_data[0] == 0:
                            st.warning("Order not found.")
                        else:
                            st.write("### Order Details")
                            st.write(f"**Supplier:** {order_data[1]}")
                            st.write(f"**Quantity:** {order_data[3]} units")
                            
                            human_status = config.ORDER_STATUS.get(order_data[4], "Unknown")
                            st.write(f"**Fulfillment Status:** {human_status}")
                            
                            if order_data[5]:
                                st.error("Cold Chain Violated: Temperature limits breached during transit.")
                            else:
                                st.success("Cold Chain Intact: No temperature alerts recorded.")
                                
                            st.write(f"**Payment Released?** {'Yes' if order_data[6] else 'No'}")
                except Exception as e:
                    st.error("Could not retrieve order details.")

def page_logistics_and_cold_chain(wallet_address):
    """Logging temperatures, verifying deliveries, and releasing funds."""
    st.header("Logistics & Cold Chain Control")
    
    tab1, tab2, tab3 = st.tabs(["Log Temperature", "Verify Delivery", "Release Funds"])
    
    with tab1:
        st.subheader("IoT Sensor Check-in")
        st.caption("In a live environment, automated sensors in transport vehicles would submit these records.")
        target_order = st.number_input("Tracking Order ID", min_value=1, step=1)
        current_temp = st.number_input("Current Temperature (°C)", value=4)
        max_allowed = st.number_input("Maximum Allowed Temperature (°C)", value=8)
        
        if st.button("Record Temperature"):
            if wallet_address:
                send_transaction("logTemperature", [int(target_order), int(current_temp), int(max_allowed)], wallet_address, "tx_log_temp")
            else:
                st.error("Please connect your wallet.")
                
    with tab2:
        st.subheader("Confirm Goods Receipt (Admin)")
        delivery_order_id = st.number_input("Received Order ID", min_value=1, step=1)
        if st.button("Mark as Delivered"):
            if wallet_address:
                send_transaction("verifyDelivery", [int(delivery_order_id)], wallet_address, "tx_verify_del")
            else:
                st.error("Please connect your wallet.")
                
    with tab3:
        st.subheader("Finalise Financial Settlement (Admin)")
        payment_order_id = st.number_input("Completed Order ID", min_value=1, step=1)
        if st.button("Release Payment"):
            if wallet_address:
                send_transaction("releasePayment", [int(payment_order_id)], wallet_address, "tx_release_pay")
            else:
                st.error("Please connect your wallet.")

def page_governance_and_esg(wallet_address):
    """Triggering recalls and maintaining supplier ESG scores."""
    st.header("Governance & Public Safety")
    
    tab1, tab2 = st.tabs(["Trigger Medicine Recall", "Update ESG Scores"])
    
    with tab1:
        st.subheader("Initiate Emergency Recall (Admin)")
        batch_number = st.text_input("Defective Batch Number")
        recall_reason = st.text_input("Reason for Recall", help="e.g., Contamination, Incorrect Labeling")
        
        if st.button("Broadcast Recall Alert"):
            if wallet_address and batch_number and recall_reason:
                send_transaction("triggerRecall", [batch_number, recall_reason], wallet_address, "tx_recall")
            elif not wallet_address:
                st.error("Please connect your wallet.")
            else:
                st.warning("Please provide both the batch number and reason.")
                
    with tab2:
        st.subheader("Maintain Sustainability Profiles (Admin)")
        esg_supplier = st.text_input("Supplier Wallet Address to Update")
        new_esg = st.number_input("New ESG Score", min_value=0, max_value=100)
        
        if st.button("Publish New Score"):
            if wallet_address and esg_supplier:
                try:
                    clean_address = w3.to_checksum_address(esg_supplier)
                    send_transaction("updateESGScore", [clean_address, int(new_esg)], wallet_address, "tx_esg")
                except ValueError:
                    st.error("Invalid wallet address format.")
            elif not wallet_address:
                st.error("Please connect your wallet.")
            else:
                st.warning("Please provide the supplier's address.")

# =============================================================================
# MAIN APPLICATION FLOW
# =============================================================================
def main():
    # Set up the basic layout configuration of the browser tab
    st.set_page_config(page_title=config.APP_NAME, layout="centered")
    
    render_header()
    
    # Request the connected wallet on every page load
    wallet_address = get_connected_wallet()
    
    # Render the navigation sidebar
    st.sidebar.title("Navigation")
    pages = [
        "Dashboard Overview", 
        "Supplier Management", 
        "Purchase Orders", 
        "Logistics & Cold Chain", 
        "Governance & Safety"
    ]
    selection = st.sidebar.radio("Go to:", pages)
    
    st.sidebar.divider()
    
    # Display network connectivity instructions
    if wallet_address:
        st.sidebar.success(f"Wallet Connected:\n\n`{wallet_address[:6]}...{wallet_address[-4:]}`")
    else:
        st.sidebar.warning(
            "MetaMask not detected or disconnected. "
            "Please ensure you have the MetaMask browser extension installed "
            "and switch to the Sepolia test network to interact."
        )

    # Route the user to the correct page based on their sidebar selection
    if selection == "Dashboard Overview":
        page_overview(wallet_address)
    elif selection == "Supplier Management":
        page_supplier_management(wallet_address)
    elif selection == "Purchase Orders":
        page_purchase_orders(wallet_address)
    elif selection == "Logistics & Cold Chain":
        page_logistics_and_cold_chain(wallet_address)
    elif selection == "Governance & Safety":
        page_governance_and_esg(wallet_address)

if __name__ == "__main__":
    main()
