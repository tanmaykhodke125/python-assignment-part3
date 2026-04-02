# Part 3 - File I/O, APIs & Exception Handling
# Theme: Product Explorer & Error-Resilient Logger

import requests
from datetime import datetime

BASE_URL = "https://dummyjson.com/products"
LOG_FILE = "error_log.txt"


# ---- Task 1: File Read & Write ----

print("=" * 45)
print("TASK 1 - File Read & Write")
print("=" * 45)

# five topic lines to write
lines_to_write = [
    "Topic 1: Variables store data. Python is dynamically typed.\n",
    "Topic 2: Lists are ordered and mutable.\n",
    "Topic 3: Dictionaries store key-value pairs.\n",
    "Topic 4: Loops automate repetitive tasks.\n",
    "Topic 5: Exception handling prevents crashes.\n",
]

# write to file
with open("python_notes.txt", "w", encoding="utf-8") as f:
    f.writelines(lines_to_write)
print("File written successfully.")

# append two more lines
with open("python_notes.txt", "a", encoding="utf-8") as f:
    f.write("Topic 6: Functions help organize and reuse code.\n")
    f.write("Topic 7: Libraries extend Python with extra tools.\n")
print("Lines appended.")

# read back and print numbered
with open("python_notes.txt", "r", encoding="utf-8") as f:
    all_lines = f.readlines()

for i, line in enumerate(all_lines, 1):
    print(f"{i}. {line.rstrip()}")

print(f"\nTotal lines: {len(all_lines)}")

# keyword search
keyword: str = input("\nEnter a keyword to search: ")
matches = [l for l in all_lines if keyword.lower() in l.lower()]
if matches:
    print(f"Lines containing '{keyword}':")
    for m in matches:
        print(" ", m.rstrip())
else:
    print(f"No lines found with '{keyword}'.")


# ---- Task 2: API Integration ----

print("\n" + "=" * 45)
print("TASK 2 - API Integration")
print("=" * 45)

# step 1: fetch 20 products
try:
    resp = requests.get(BASE_URL + "?limit=20", timeout=5)
    products = resp.json()["products"]
    print(f"\n{'ID':<4}| {'Title':<30} | {'Category':<14} | {'Price':>8} | Rating")
    print("-" * 70)
    for p in products:
        print(f"{p['id']:<4}| {p['title']:<30} | {p['category']:<14} | ${p['price']:>7.2f} | {p['rating']}")
except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")
except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")
except Exception as e:
    print(f"Error: {e}")

# step 2: filter rating >= 4.5 and sort by price descending
try:
    filtered = [p for p in products if float(str(p["rating"])) >= 4.5]
    filtered.sort(key=lambda p: float(str(p["price"])), reverse=True)
    print("\nProducts with rating >= 4.5 (sorted by price):")
    for p in filtered:
        print(f"  {p['title']} - ${p['price']} - Rating: {p['rating']}")
except Exception as e:
    print(f"Filter error: {e}")

# step 3: fetch laptops category
try:
    resp2 = requests.get(BASE_URL + "/category/laptops", timeout=5)
    laptops = resp2.json()["products"]
    print("\nLaptops:")
    for p in laptops:
        print(f"  {p['title']} - ${p['price']}")
except requests.exceptions.ConnectionError:
    print("Connection failed.")
except requests.exceptions.Timeout:
    print("Request timed out.")
except Exception as e:
    print(f"Error: {e}")

# step 4: POST a new product
try:
    new_product = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API"
    }
    post_resp = requests.post(BASE_URL + "/add", json=new_product, timeout=5)
    print("\nPOST response:")
    print(post_resp.json())
except requests.exceptions.ConnectionError:
    print("Connection failed.")
except requests.exceptions.Timeout:
    print("Request timed out.")
except Exception as e:
    print(f"Error: {e}")


# ---- Task 3: Exception Handling ----

print("\n" + "=" * 45)
print("TASK 3 - Exception Handling")
print("=" * 45)

# part A: safe divide
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("ten", 2))

# part B: safe file reader
def read_file_safe(filename: str):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    finally:
        print("File operation attempt complete.")

read_file_safe("python_notes.txt")   # exists
read_file_safe("ghost_file.txt")     # does not exist

# part C: all API calls above already wrapped in try-except

# part D: input validation loop
print("\n--- Product Lookup (type 'quit' to exit) ---")
while True:
    user_input: str = input("Enter product ID (1-100) or 'quit': ").strip()
    if user_input.lower() == "quit":
        break
    try:
        pid: int = int(user_input)
        if not (1 <= pid <= 100):
            print("Please enter a number between 1 and 100.")
            continue
    except ValueError:
        print("That's not a valid number.")
        continue
    try:
        r = requests.get(f"{BASE_URL}/{pid}", timeout=5)
        if r.status_code == 404:
            print("Product not found.")
        elif r.status_code == 200:
            p = r.json()
            print(f"Title: {p['title']}, Price: ${p['price']}")
    except requests.exceptions.ConnectionError:
        print("Connection failed.")
    except requests.exceptions.Timeout:
        print("Request timed out.")
    except Exception as e:
        print(f"Error: {e}")


# ---- Task 4: Logging to File ----

print("\n" + "=" * 45)
print("TASK 4 - Logging to File")
print("=" * 45)

def log_error(function_name: str, error_type: str, error_message: str) -> None:
    # write a timestamped error entry to the log file
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] ERROR in {function_name}: {error_type} — {error_message}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)

# trigger ConnectionError with unreachable URL
try:
    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except requests.exceptions.ConnectionError as e:
    log_error("fetch_products", "ConnectionError", str(e)[:80])

# trigger HTTP 404 by requesting non-existent product
r404 = requests.get(f"{BASE_URL}/999", timeout=5)
if r404.status_code != 200:
    log_error("lookup_product", "HTTPError", "404 Not Found for product ID 999")

# print the log file contents
print("\nContents of error_log.txt:")
with open(LOG_FILE, "r", encoding="utf-8") as f:
    print(f.read())


'''
Output:
=============================================
TASK 1 - File Read & Write
=============================================
File written successfully.
Lines appended.
1. Topic 1: Variables store data. Python is dynamically typed.    
2. Topic 2: Lists are ordered and mutable.
3. Topic 3: Dictionaries store key-value pairs.
4. Topic 4: Loops automate repetitive tasks.
5. Topic 5: Exception handling prevents crashes.
6. Topic 6: Functions help organize and reuse code.
7. Topic 7: Libraries extend Python with extra tools.

Total lines: 7

Enter a keyword to search: loops
Lines containing 'loops':
  Topic 4: Loops automate repetitive tasks.

=============================================
TASK 2 - API Integration
=============================================

ID  | Title                          | Category       |    Price | Rating
----------------------------------------------------------------------
1   | Essence Mascara Lash Princess  | beauty         | $   9.99 | 2.56
2   | Eyeshadow Palette with Mirror  | beauty         | $  19.99 | 2.86
3   | Powder Canister                | beauty         | $  14.99 | 4.64
4   | Red Lipstick                   | beauty         | $  12.99 | 4.36
5   | Red Nail Polish                | beauty         | $   8.99 | 4.32
6   | Calvin Klein CK One            | fragrances     | $  49.99 | 4.37
7   | Chanel Coco Noir Eau De        | fragrances     | $ 129.99 | 4.26
8   | Dior J'adore                   | fragrances     | $  89.99 | 3.8
9   | Dolce Shine Eau de             | fragrances     | $  69.99 | 3.96
10  | Gucci Bloom Eau de             | fragrances     | $  79.99 | 2.74
11  | Annibale Colombo Bed           | furniture      | $1899.99 | 4.77
12  | Annibale Colombo Sofa          | furniture      | $2499.99 | 3.92
13  | Bedside Table African Cherry   | furniture      | $ 299.99 | 2.87
14  | Knoll Saarinen Executive Conference Chair | furniture      | $ 499.99 | 4.88
15  | Wooden Bathroom Sink With Mirror | furniture      | $ 799.99 | 3.59
16  | Apple                          | groceries      | $   1.99 | 4.19
17  | Beef Steak                     | groceries      | $  12.99 | 4.47
18  | Cat Food                       | groceries      | $   8.99 | 3.13
19  | Chicken Meat                   | groceries      | $   9.99 | 3.19
20  | Cooking Oil                    | groceries      | $   4.99 | 4.8

Products with rating >= 4.5 (sorted by price):
  Annibale Colombo Bed - $1899.99 - Rating: 4.77
  Knoll Saarinen Executive Conference Chair - $499.99 - Rating: 4.88
  Powder Canister - $14.99 - Rating: 4.64
  Cooking Oil - $4.99 - Rating: 4.8

Laptops:
  Apple MacBook Pro 14 Inch Space Grey - $1999.99
  Asus Zenbook Pro Dual Screen Laptop - $1799.99
  Huawei Matebook X Pro - $1399.99
  Lenovo Yoga 920 - $1099.99
  New DELL XPS 13 9300 Laptop - $1499.99

POST response:
{'id': 195, 'title': 'My Custom Product', 'price': 999, 'description': 'A product I created via API', 'category': 'electronics'}    

=============================================
TASK 3 - Exception Handling
=============================================
5.0
Error: Cannot divide by zero
Error: Invalid input types
File operation attempt complete.
Error: File 'ghost_file.txt' not found.
File operation attempt complete.

--- Product Lookup (type 'quit' to exit) ---
Enter product ID (1-100) or 'quit': 2
Title: Eyeshadow Palette with Mirror, Price: $19.99
Enter product ID (1-100) or 'quit': quit

=============================================
TASK 4 - Logging to File
=============================================

Contents of error_log.txt:
[2026-03-31 18:08:08] ERROR in fetch_products: ConnectionError — HTTPSConnectionPool(host='this-host-does-not-exist-xyz.com', port=443): Max retr
[2026-03-31 18:08:08] ERROR in lookup_product: HTTPError — 404 Not Found for product ID 999
'''