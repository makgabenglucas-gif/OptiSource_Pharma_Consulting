# config.py

# =============================================================================
# CONFIGURATION FILE
# =============================================================================
# This file stores all the settings and static information for the application.
# Think of it as the central control panel where you can change text, addresses,
# and translations without having to dig into the complex application logic.
# 
# Sections:
# 1. Network Setup: How we connect to the blockchain.
# 2. Smart Contract Data: The address and the "instruction manual" (ABI).
# 3. Application Branding: Text displayed to the user.
# 4. Status Translations: Converts blockchain numbers into plain English.
# =============================================================================

# --- 1. Network Setup ---
# The URL used to connect to the Sepolia test network
RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"

# --- 2. Smart Contract Data ---
# PLACEHOLDER: The unique identifier for our smart contract on the Sepolia network.
CONTRACT_ADDRESS = "0x001543Ef78646247C9a412DAb98E5Ac4Df064163" 

# PLACEHOLDER: The ABI (Application Binary Interface). 
# This is a JSON list that tells our Python code exactly what functions the contract has.
# Paste your generated ABI inside the brackets.
CONTRACT_ABI =[
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "orderId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "int256",
				"name": "recordedTemp",
				"type": "int256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"name": "ColdChainBreach",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "orderId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "bool",
				"name": "success",
				"type": "bool"
			}
		],
		"name": "DeliveryVerified",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "address",
				"name": "supplier",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "newScore",
				"type": "uint256"
			}
		],
		"name": "ESGReported",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "string",
				"name": "batchNumber",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "reason",
				"type": "string"
			}
		],
		"name": "MedicineRecalled",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "orderId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "address",
				"name": "supplier",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "OrderPlaced",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "orderId",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "PaymentReleased",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "supplier",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "enum CounterfeitMedicineTracker.EntityStatus",
				"name": "status",
				"type": "uint8"
			}
		],
		"name": "SupplierUpdated",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			}
		],
		"name": "applyAsSupplier",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "batches",
		"outputs": [
			{
				"internalType": "string",
				"name": "medicineName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "batchNumber",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "expiryDate",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "minTemp",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "maxTemp",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "isRecalled",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_supplier",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_amount",
				"type": "uint256"
			}
		],
		"name": "createPurchaseOrder",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "hospitalAdmin",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_orderId",
				"type": "uint256"
			},
			{
				"internalType": "int256",
				"name": "_currentTemp",
				"type": "int256"
			},
			{
				"internalType": "uint256",
				"name": "_maxAllowed",
				"type": "uint256"
			}
		],
		"name": "logTemperature",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "orderCount",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "orders",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "id",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "supplier",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "hospital",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			},
			{
				"internalType": "enum CounterfeitMedicineTracker.OrderStatus",
				"name": "status",
				"type": "uint8"
			},
			{
				"internalType": "bool",
				"name": "coldChainViolated",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "paymentReleased",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_orderId",
				"type": "uint256"
			}
		],
		"name": "releasePayment",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "suppliers",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "walletAddress",
				"type": "address"
			},
			{
				"internalType": "enum CounterfeitMedicineTracker.EntityStatus",
				"name": "status",
				"type": "uint8"
			},
			{
				"internalType": "bool",
				"name": "isVerified",
				"type": "bool"
			},
			{
				"internalType": "uint256",
				"name": "esgScore",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_batchNumber",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_reason",
				"type": "string"
			}
		],
		"name": "triggerRecall",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_supplier",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_score",
				"type": "uint256"
			}
		],
		"name": "updateESGScore",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_orderId",
				"type": "uint256"
			}
		],
		"name": "verifyDelivery",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_supplier",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_initialESG",
				"type": "uint256"
			}
		],
		"name": "verifySupplier",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
] 

# --- 3. Application Branding ---
APP_NAME = "PharmaChain Tracker"
TAGLINE = "Securing the Medical Supply Chain"
DESCRIPTION = "A transparent, permanent, and verifiable system ensuring the safe journey of pharmaceuticals from procurement to patient delivery."
LOGO_PATH = "assets/logo.png" # Path to the local logo image

# --- 4. Status Translations ---
# Smart contracts often store statuses as numbers (0, 1, 2...) to save space. 
# These dictionaries map those numbers back to plain English for our users.

ENTITY_STATUS = {
    0: "Application Submitted",
    1: "Under Review",
    2: "Verified",
    3: "Active",
    4: "Flagged for Investigation",
    5: "Suspended",
    6: "Reactivated",
    7: "Blacklisted"
}

ORDER_STATUS = {
    0: "Pending Approval",
    1: "Approved",
    2: "Shipped",
    3: "Delivered",
    4: "Completed",
    5: "Cancelled"
}
