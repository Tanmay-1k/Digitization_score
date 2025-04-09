import os
import pandas as pd
import PyPDF2
import re


# Define the keywords and their weights
keywords = {
    "Artificial Intelligence (AI) & Machine Learning (ML)": [
        "Artificial Intelligence", "Business Intelligence", "Image Understanding", "Investment Decision Aid System",
        "Intelligent Data Analysis", "Intelligent Robotics", "Machine Learning", "Deep Learning", "Semantic Search",
        "Biometrics", "Face Recognition", "Voice Recognition", "Identity Verification", "Autonomous Driving",
        "Natural Language Processing", "AI/ML", "Chatbots", "Credit Risk Assessment Models", "Robo-advisor", "Generative AI"
    ],
    "Blockchain Technology": [
        "Blockchain", "Digital Currency", "Cryptocurrency", "Crypto", "Distributed Computing",
        "Differential Privacy Technology", "Smart Financial Contracts", "NFT", "Web 3.0"
    ],
    "Cloud Computing & Infrastructure": [
        "Cloud Computing", "Cloud", "Cloud Technologies", "Streaming Computing", "Graph Computing",
        "In-Memory Computing", "Multi-party Secure Computing", "Brain-like Computing", "Green Computing",
        "Cognitive Computing", "Converged Architecture", "Billion-level Concurrency", "EB-level Storage",
        "APIs", "Digital Infrastructure"
    ],
    "Big Data & Analytics": [
        "Big Data", "Data Mining", "Text Mining", "Data Visualization", "Heterogeneous Data",
        "Credit Analytics", "Augmented Reality", "Mixed Reality", "Virtual Reality", "Transaction Monitoring"
    ],
    "Digital Technology Applications": [
        "Mobile Internet", "Industrial Internet", "Internet Healthcare", "E-commerce", "Mobile Payment",
        "Third-party Payment", "NFC Payment", "Smart Energy", "B2B", "B2C", "C2B", "C2C", "O2O", "Netlink",
        "Smart Wear", "Smart Agriculture", "Smart Transportation", "Smart Healthcare", "Smart Customer Service",
        "Smart Home", "Smart Investment", "Smart Cultural Tourism", "Smart Environmental Protection", "Smart Grid",
        "Smart Marketing", "Digital Marketing", "Unmanned Retail", "Internet Finance", "Digital Finance",
        "Fintech", "Quantitative Finance", "Open Banking", "Embedded Finance", "Peer-to-Peer", "Buy Now Pay Later",
        "Contactless Payments", "Request to Pay", "Payment Service Directive", "Neobank", "Mobile-first Banking",
        "Banking-as-a-Service", "Metaverse"
    ],
    "Cybersecurity & Compliance": [
        "Cyber Security", "Anti-Money Laundering", "Fraud Detection"
    ],
    "Digital Banking & Transformation": [
        "Digitization", "Digital Transformation", "Net Banking", "Internet Banking", "New-to-Digital Customers",
        "E-money", "Robotic Process Automation", "Internet of Things", "Digital Adoption", "Branch on the Move",
        "DBT", "Innovation", "Banking Technology"
    ]
}

weights = {
    "Artificial Intelligence (AI) & Machine Learning (ML)": 5,
    "Blockchain Technology": 4,
    "Cloud Computing & Infrastructure": 3,
    "Big Data & Analytics": 3,
    "Digital Technology Applications": 2,
    "Cybersecurity & Compliance": 2,
    "Digital Banking & Transformation": 1
}

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            
            return text.lower()
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return ""

# Function to compute weighted and normalized scores
def compute_digitization_score(text, keywords, weights):
    total_words = len(re.findall(r'\w+', text))
   
    
    category_details = {}
    total_normalized_score = 0
    
    for category, keyword_list in keywords.items():
        category_score = 0
        for keyword in keyword_list:
            count = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text))
            category_score += count
        
        
        # Weighted score
        weighted_score = category_score * weights[category]
        # Normalized score (per 1000 words)
        normalized_score = (weighted_score / total_words) * 1000 if total_words > 0 else 0
        
        category_details[category] = {
            "raw_count": category_score,
            "weighted_score": weighted_score,
            "normalized_score": round(normalized_score, 2)
        }
        total_normalized_score += normalized_score
    
    total_normalized_score = round(total_normalized_score, 2)
    return total_normalized_score, category_details

