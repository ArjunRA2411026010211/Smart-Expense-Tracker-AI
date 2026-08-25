import pandas as pd
import random
from pathlib import Path


# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

TRAIN_FILE = DATA_DIR / "financial_transaction_train.csv"
TEST_FILE = DATA_DIR / "financial_transaction_test.csv"

OUTPUT_FILE = DATA_DIR / "final_transactions.csv"


# ==================================================
# LOAD EXISTING DATASET
# ==================================================

train_df = pd.read_csv(TRAIN_FILE)
test_df = pd.read_csv(TEST_FILE)

df = pd.concat(
    [train_df, test_df],
    ignore_index=True
)

df = df[
    ["Transaction_Text", "Label"]
].copy()

df["Transaction_Text"] = (
    df["Transaction_Text"]
    .astype(str)
    .str.strip()
)

df["Label"] = (
    df["Label"]
    .astype(str)
    .str.strip()
)


# ==================================================
# RECLASSIFY EXISTING DATA
# ==================================================

def fix_category(text, old_label):

    text = str(text).lower()

    # PETROL
    if any(word in text for word in [
        "petrol",
        "fuel",
        "diesel",
        "indian oil",
        "iocl",
        "hpcl",
        "bpcl",
        "bharat petroleum"
    ]):
        return "Petrol"

    # FOOD
    if any(word in text for word in [
        "swiggy",
        "zomato",
        "dominos",
        "pizza",
        "restaurant",
        "cafe",
        "food",
        "kfc",
        "mcdonald"
    ]):
        return "Food"

    # SHOPPING
    if any(word in text for word in [
        "amazon",
        "flipkart",
        "myntra",
        "ajio",
        "meesho",
        "shopping"
    ]):
        return "Shopping"

    # ENTERTAINMENT
    if any(word in text for word in [
        "netflix",
        "spotify",
        "hotstar",
        "bookmyshow",
        "prime video",
        "cinema"
    ]):
        return "Entertainment"

    # MEDICAL
    if any(word in text for word in [
        "hospital",
        "pharmacy",
        "medical",
        "apollo",
        "medplus",
        "clinic",
        "doctor"
    ]):
        return "Medical"

    # STUDIES
    if any(word in text for word in [
        "college",
        "school",
        "university",
        "tuition",
        "course",
        "education",
        "exam",
        "bookstore"
    ]):
        return "Studies"

    # RENT
    if any(word in text for word in [
        "house rent",
        "room rent",
        "hostel rent",
        "landlord",
        "rent payment"
    ]):
        return "Rent"

    # BILLS
    if any(word in text for word in [
        "electricity",
        "airtel",
        "jio recharge",
        "recharge",
        "broadband",
        "internet bill",
        "water bill",
        "gas bill"
    ]):
        return "Bills"

    # TRANSPORT
    if any(word in text for word in [
        "ola",
        "uber",
        "rapido",
        "irctc",
        "railway",
        "bus ticket",
        "metro",
        "taxi"
    ]):
        return "Transport"

    # EMI
    if old_label.lower() == "emi":
        return "EMI"

    # INVESTMENT
    if old_label.lower() == "investment":
        return "Investment"

    # Old Travel category
    if old_label.lower() == "travel":
        return "Transport"

    return old_label.title()


df["Label"] = df.apply(
    lambda row: fix_category(
        row["Transaction_Text"],
        row["Label"]
    ),
    axis=1
)


# ==================================================
# PROJECT-SPECIFIC TRAINING EXAMPLES
# ==================================================

category_examples = {

    # ==================================================
    # FOOD
    # ==================================================

    "Food": [
        "Swiggy food order",
        "Zomato online food order",
        "Dominos pizza payment",
        "Restaurant food payment",
        "Cafe payment",
        "KFC restaurant payment",
        "KFC UPI transaction",
        "KFC food order",
        "McDonalds online payment",
        "McDonalds restaurant purchase",
        "McDonalds UPI payment",
        "Burger restaurant payment",
        "Fast food restaurant UPI"
    ],


    # ==================================================
    # PETROL
    # ==================================================

    "Petrol": [
        "Indian Oil petrol pump payment",
        "IOCL fuel station UPI",
        "HPCL petrol payment",
        "Bharat Petroleum fuel purchase",
        "BPCL petrol station transaction",
        "Shell fuel payment",
        "Diesel filling payment",
        "Petrol bunk UPI payment"
    ],


    # ==================================================
    # GROCERIES
    # ==================================================

    "Groceries": [
        "DMart grocery purchase",
        "Reliance Fresh supermarket payment",
        "Mithran Super Stores purchase",
        "BigBasket grocery order",
        "Blinkit grocery payment",
        "Zepto grocery delivery",
        "Supermarket grocery purchase",
        "Provision store payment"
    ],


    # ==================================================
    # SHOPPING
    # ==================================================

    "Shopping": [
        "Amazon online shopping",
        "Amazon seller services payment",
        "Flipkart online purchase",
        "Myntra shopping payment",
        "AJIO retail purchase",
        "AJIO UPI payment",
        "Meesho online order",
        "Meesho shopping payment",
        "Clothing store UPI payment",
        "Clothes shop purchase",
        "Electronics store purchase",
        "Retail clothing purchase",
        "Shopping mall purchase"
    ],


    # ==================================================
    # STUDIES
    # ==================================================

    "Studies": [
        "College fee payment",
        "University tuition fee",
        "School fee payment",
        "Exam fee payment",
        "Udemy course purchase",
        "Coursera course payment",
        "Bookstore study material",
        "Tuition class payment",
        "Education institute UPI payment",
        "Educational institution fee",
        "Institute fee payment",
        "Coaching institute UPI",
        "Academic fee payment"
    ],


    # ==================================================
    # RENT
    # ==================================================

    "Rent": [
        "House rent payment",
        "Room rent August",
        "Monthly rent transfer",
        "Landlord rent payment",
        "Hostel rent payment",
        "PG rent payment",
        "Flat rent transfer",
        "Apartment rent payment"
    ],


    # ==================================================
    # TRANSPORT
    # ==================================================

    "Transport": [
        "IRCTC online ticket",
        "Uber cab payment",
        "Ola cab fare",
        "Rapido bike ride",
        "Metro ticket payment",
        "Railway ticket booking",
        "Bus ticket payment",
        "Taxi fare payment",
        "Metro card recharge",
        "Metro travel card payment",
        "Metro recharge transaction",
        "Railway reservation online",
        "Train reservation payment",
        "Taxi fare UPI payment"
    ],


    # ==================================================
    # BILLS
    # ==================================================

    "Bills": [
        "Airtel recharge",
        "Jio mobile recharge",
        "Electricity bill payment",
        "Internet broadband bill",
        "Water bill payment",
        "Gas bill payment",
        "Mobile bill payment",
        "Utility bill payment"
    ],


    # ==================================================
    # MEDICAL
    # ==================================================

    "Medical": [
        "Apollo Pharmacy payment",
        "MedPlus pharmacy purchase",
        "Hospital bill payment",
        "Doctor consultation fee",
        "Medical shop purchase",
        "Clinic payment",
        "Diagnostic lab payment",
        "Medicine purchase"
    ],


    # ==================================================
    # ENTERTAINMENT
    # ==================================================

    "Entertainment": [
        "Netflix monthly payment",
        "Spotify subscription",
        "Disney Hotstar subscription",
        "BookMyShow movie ticket",
        "Cinema ticket payment",
        "Prime Video subscription",
        "Gaming purchase",
        "Theatre ticket payment"
    ],


    # ==================================================
    # EMI
    # ==================================================

    "EMI": [
        "Personal loan EMI payment",
        "Home loan EMI payment",
        "Car loan EMI payment",
        "Bike loan EMI payment",
        "Monthly loan installment",
        "Finance EMI monthly payment",
        "Finance company EMI debit",
        "Monthly finance installment",
        "Loan finance installment",
        "Loan EMI auto debit"
    ],


    # ==================================================
    # INVESTMENT
    # ==================================================

    "Investment": [
        "Zerodha investment payment",
        "Groww investment payment",
        "Mutual fund investment",
        "Monthly SIP investment",
        "Stock market investment",
        "Fixed deposit investment",
        "SIP auto debit investment",
        "Upstox stock purchase"
    ],


    # ==================================================
    # PERSONAL TRANSFER
    # ==================================================

    "Personal Transfer": [
        "UPI transfer to friend",
        "UPI payment to Ravi",
        "Money sent to Deepak",
        "Personal UPI transfer",
        "Transfer to family member",
        "Payment to friend",
        "UPI transfer to Arun",
        "Money transfer to person",
        "Personal bank transfer"
    ],


    # ==================================================
    # SALARY
    # ==================================================

    "Salary": [
        "Salary credited",
        "Monthly salary credit",
        "Employer salary payment",
        "Payroll credit",
        "Company salary deposit",
        "Salary August credit",
        "Monthly wages credited",
        "Office salary received"
    ],


    # ==================================================
    # INCOME
    # ==================================================

    "Income": [
        "Income credited",
        "Bank credit received",
        "Money received",
        "Freelance payment received",
        "Bonus credited",
        "Commission received",
        "Cash deposit credit",
        "Payment received",
        "General credit to account",
        "Bank account credit received",
        "Incoming bank credit",
        "General income credit"
    ],


    # ==================================================
    # OTHER
    # ==================================================

    "Other": [
        "Unknown merchant payment",
        "Miscellaneous expense",
        "General payment",
        "Other transaction",
        "Unknown bank transaction",
        "Misc expense payment",
        "Unclassified transaction",
        "General purchase"
    ]

}


# ==================================================
# GENERATE VARIATIONS
# ==================================================

prefixes = [
    "",
    "UPI ",
    "POS ",
    "PAYTM ",
    "GPAY ",
    "PHONEPE ",
    "ONLINE ",
    "BANK "
]

suffixes = [
    "",
    " PAYMENT",
    " UPI",
    " ONLINE",
    " TRANSACTION",
    " PURCHASE"
]

generated_rows = []

random.seed(42)

for category, examples in category_examples.items():

    for example in examples:

        # Original example
        generated_rows.append({
            "Transaction_Text": example,
            "Label": category
        })

        # Generate variations
        for _ in range(30):

            prefix = random.choice(prefixes)
            suffix = random.choice(suffixes)

            generated_text = (
                prefix
                + example
                + suffix
            )

            generated_rows.append({
                "Transaction_Text": generated_text,
                "Label": category
            })


generated_df = pd.DataFrame(
    generated_rows
)


# ==================================================
# COMBINE DATASETS
# ==================================================

final_df = pd.concat(
    [
        df,
        generated_df
    ],
    ignore_index=True
)


# Remove empty rows
final_df = final_df.dropna()

final_df = final_df[
    final_df["Transaction_Text"].str.strip() != ""
]


# Remove exact duplicates
final_df = final_df.drop_duplicates(
    subset=[
        "Transaction_Text",
        "Label"
    ]
)


# Shuffle dataset
final_df = final_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)
# ==================================================
# BALANCE DATASET
# ==================================================

target_per_category = 2000

balanced_groups = []

for category in final_df["Label"].unique():

    category_df = final_df[
        final_df["Label"] == category
    ]

    if len(category_df) < target_per_category:

        category_df = category_df.sample(
            n=target_per_category,
            replace=True,
            random_state=42
        )

    else:

        category_df = category_df.sample(
            n=target_per_category,
            random_state=42
        )

    balanced_groups.append(category_df)


final_df = pd.concat(
    balanced_groups,
    ignore_index=True
)


final_df = final_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)


# ==================================================
# SAVE FINAL DATASET
# ==================================================

final_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ==================================================
# SHOW RESULTS
# ==================================================

print("\nDataset created successfully.")

print(
    "\nTotal rows:",
    len(final_df)
)

print("\nCategories:")

print(
    final_df["Label"]
    .value_counts()
)

print(
    "\nSaved to:",
    OUTPUT_FILE
)