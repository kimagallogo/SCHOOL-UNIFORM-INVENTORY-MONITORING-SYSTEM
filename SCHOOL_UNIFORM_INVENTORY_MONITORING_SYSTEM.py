import re 
from datetime import date 
 
# ========================================== 
# SCHOOL UNIFORM INVENTORY MONITORING SYSTEM 
# ========================================== 
 
students = [] 
inventory = [] 
feedback_records = [] 
 
genders = ["Male", "Female"] 
uniform_types = ["Type A", "Type B", "Type C"] 
sizes = ["Small", "Medium", "Large"] 
 
REORDER_LEVEL = 100 
INITIAL_STOCK = 0 
 
stock = { 
    (gender, utype, size): INITIAL_STOCK 
    for gender in genders 
    for utype in uniform_types 
    for size in sizes 
} 
 
 
# ========================================== 
# ADMIN LOGIN DETAILS 
# ========================================== 
 
ADMIN_USERNAME = "admin" 
ADMIN_PASSWORD = "Admin123" 
 
 
# ========================================== 
# VALIDATION FUNCTIONS 
# ========================================== 
 
# Student ID format: 02-XXXX-XXXXXX 
def is_valid_student_id(sid): 
    return bool(re.fullmatch(r"02-\d{4}-\d{6}", sid)) 
 
 
# Allows letters, spaces, and dots in names 
def is_valid_name(name): 
    return bool(re.fullmatch(r"[A-Za-z. ]+", name.strip())) 
 
 
def get_positive_quantity(prompt): 
    while True: 
        qty_text = input(prompt).strip() 
 
        if qty_text.isdigit() and int(qty_text) > 0: 
            return int(qty_text) 
 
        print("[ERROR] Enter a positive whole number!") 
 
 
# ========================================== 
# AUTOMATIC TRANSACTION ID GENERATOR 
# ========================================== 
 
def generate_transaction_id(): 
    if not inventory: 
        return "000001" 
 
    last_id = max(int(item[1]) for item in inventory) 
    return f"{last_id + 1:06d}" 
 
 
# ========================================== 
# STOCK FUNCTIONS 
# ========================================== 
 
def get_stock(gender, utype, size): 
    return stock.get((gender, utype, size), 0) 
 
 
def show_reorder_warning(gender, utype, size): 
    remaining = get_stock(gender, utype, size) 
 
    if remaining <= REORDER_LEVEL: 
        print("\n[REORDER ALERT] LOW UNIFORM STOCK!") 
        print(f"Gender: {gender} | Type: {utype} | Size: {size}") 
        print(f"Remaining stock: {remaining}") 
        print("ACTION REQUIRED: Please reorder uniforms.") 
 
 
def add_stock(gender, utype, size, qty): 
    if qty <= 0: 
        print("[ERROR] Quantity must be greater than zero!") 
        return 
 
    key = (gender, utype, size) 
    stock[key] = get_stock(*key) + qty 
 
    print("\n[SUCCESS] Uniform stock added!") 
    print(f"Gender: {gender}") 
    print(f"Uniform Type: {utype}") 
    print(f"Size: {size}") 
    print(f"Quantity Added: {qty}") 
    print(f"Available Stock: {stock[key]}") 
 
    show_reorder_warning(*key) 
 
 
def view_stock(): 
    print("\n================ UNIFORM STOCK REPORT ================") 
    print( 
        f"{'GENDER':<12}{'TYPE':<12}{'SIZE':<12}" 
        f"{'AVAILABLE STOCK':<18}{'STATUS':<18}" 
    ) 
    print("-" * 72) 
 
    for gender in genders: 
        for utype in uniform_types: 
            for size in sizes: 
                quantity = get_stock(gender, utype, size) 
 
                status = ( 
                    "REORDER NEEDED" 
                    if quantity <= REORDER_LEVEL 
                    else "In Stock" 
                ) 
 
                print( 
                    f"{gender:<12}{utype:<12}{size:<12}" 
                    f"{quantity:<18}{status:<18}" 
                ) 
 
    print("-" * 72) 
    print(f"Reorder alert threshold: {REORDER_LEVEL} uniforms or fewer.") 
 
 
# ========================================== 
# SELECT UNIFORM DETAILS 
# ========================================== 
 
def select_gender(): 
    while True: 
        print("\nSelect Gender:") 
        print("[1] Male") 
        print("[2] Female") 
 
        choice = input("Enter choice: ").strip() 
 
        if choice == "1": 
            return "Male" 
        elif choice == "2": 
            return "Female" 
 
        print("[ERROR] Enter 1 or 2.") 
 
 
def select_uniform_type(): 
    while True: 
        print("\nSelect Uniform Type:") 
        print("[1] Type A") 
        print("[2] Type B") 
        print("[3] Type C") 
 
        choice = input("Enter choice: ").strip() 
 
        if choice in ["1", "2", "3"]: 
            return uniform_types[int(choice) - 1] 
 
        print("[ERROR] Enter 1, 2, or 3.") 
 
 
def select_size(): 
    while True: 
        print("\nSelect Uniform Size:") 
        print("[1] Small") 
        print("[2] Medium") 
        print("[3] Large") 
 
        choice = input("Enter choice: ").strip() 
 
        if choice in ["1", "2", "3"]: 
            return sizes[int(choice) - 1] 
 
        print("[ERROR] Enter 1, 2, or 3.") 
 
 
# ========================================== 
# REGISTER STUDENT 
# ========================================== 
 
def register_student_menu(): 
    while True: 
        sid = input( 
            "Enter Student ID (02-XXXX-XXXXXX): " 
        ).strip() 
 
        if not is_valid_student_id(sid): 
            print( 
                "[ERROR] Invalid Student ID! " 
                "Required format: 02-XXXX-XXXXXX" 
            ) 
            continue 
 
        if any(student[0] == sid for student in students): 
            print("[ERROR] Student ID already exists!") 
            continue 
 
        break 
 
    while True: 
        name = input("Enter Student Name: ").strip() 
 
        if not is_valid_name(name): 
            print( 
                "[ERROR] Student name must contain " 
                "letters, spaces, and dots only!" 
            ) 
            continue 
 
        break 
 
    students.append([sid, name]) 
 
    print("\n[SUCCESS] Student registered successfully!") 
    print(f"Student ID: {sid}") 
    print(f"Student Name: {name}") 
 
 
def view_students(): 
    print("\n================ REGISTERED STUDENTS ================") 
 
    if not students: 
        print("No registered students found.") 
        return 
 
    print(f"{'STUDENT ID':<22}{'STUDENT NAME':<30}") 
    print("-" * 52) 
 
    for student in students: 
        print(f"{student[0]:<22}{student[1]:<30}") 
 
 
# ========================================== 
# ISSUE UNIFORM 
# ========================================== 
 
def issue_uniform(sid, uid, gender, utype, size, qty): 
    if not is_valid_student_id(sid): 
        print( 
            "[ERROR] Invalid Student ID! " 
            "Required format: 02-XXXX-XXXXXX" 
        ) 
        return False 
 
    if not any(student[0] == sid for student in students): 
        print("[ERROR] Student not found. Register first!") 
        return False 
 
    if any(item[1] == uid for item in inventory): 
        print("[ERROR] Transaction ID already exists!") 
        return False 
 
    if ( 
        gender not in genders 
        or utype not in uniform_types 
        or size not in sizes 
    ): 
        print("[ERROR] Invalid uniform details!") 
        return False 
 
    if qty <= 0: 
        print("[ERROR] Quantity must be greater than zero!") 
        return False 
 
    key = (gender, utype, size) 
    available = get_stock(*key) 
 
    if qty > available: 
        print("[ERROR] Not enough uniform stock!") 
        print(f"Available Stock: {available}") 
        return False 
 
    stock[key] -= qty 
    issue_date = date.today().strftime("%Y-%m-%d") 
 
    inventory.append([ 
        sid, 
        uid, 
        gender, 
        utype, 
        size, 
        qty, 
        0, 
        "Success", 
        issue_date 
    ]) 
 
    print("\n[SUCCESS] Uniform issued successfully!") 
    print(f"Student ID: {sid}") 
    print(f"Transaction ID: {uid}") 
    print(f"Gender: {gender}") 
    print(f"Uniform Type: {utype}") 
    print(f"Size: {size}") 
    print(f"Quantity Issued: {qty}") 
    print(f"Remaining Stock: {stock[key]}") 
    print(f"Issue Date: {issue_date}") 
 
    show_reorder_warning(*key) 
    return True 
 
 
# ========================================== 
# RETURN UNIFORM 
# ========================================== 
 
def return_uniform(uid, ret_qty): 
    item = next( 
        (record for record in inventory if record[1] == uid), 
        None 
    ) 
 
    if item is None: 
        print("[ERROR] Transaction ID not found!") 
        return False 
 
    if ret_qty <= 0: 
        print("[ERROR] Return quantity must be greater than zero!") 
        return False 
 
    remaining = item[5] - item[6] 
 
    if remaining <= 0: 
        print("[ERROR] All uniforms have already been returned!") 
        return False 
 
    if ret_qty > remaining: 
        print( 
            f"[ERROR] Only {remaining} uniform(s) " 
            "can still be returned!" 
        ) 
        return False 
 
    item[6] += ret_qty 
 
    key = (item[2], item[3], item[4]) 
    stock[key] += ret_qty 
 
    item[7] = ( 
        "Returned" 
        if item[6] == item[5] 
        else "Partially Returned" 
    ) 
 
    print("\n[SUCCESS] Uniform return recorded!") 
    print(f"Transaction ID: {uid}") 
    print(f"Quantity Returned: {ret_qty}") 
    print(f"Total Returned: {item[6]}") 
    print(f"Remaining to Return: {item[5] - item[6]}") 
    print(f"Updated Available Stock: {stock[key]}") 
    print(f"Status: {item[7]}") 
 
    show_reorder_warning(*key) 
    return True 
 
 
# ========================================== 
# SUBMIT REASON FOR RETURN 
# ========================================== 
 
def submit_feedback(uid): 
    item = next( 
        (record for record in inventory if record[1] == uid), 
        None 
    ) 
 
    if item is None or item[6] == 0: 
        print("[ERROR] No successful return found.") 
        return 
 
    if any(record[0] == uid for record in feedback_records): 
        print("[ERROR] A return reason was already submitted!") 
        return 
 
    print("\n========== UNIFORM RETURN REASON ==========") 
    print(f"Transaction ID: {uid}") 
 
    while True: 
        reason = input( 
            "Enter reason for returning the uniform: " 
        ).strip() 
 
        if reason: 
            break 
 
        print("[ERROR] Please enter a reason.") 
 
    feedback_records.append([ 
        uid, 
        item[0], 
        reason, 
        date.today().strftime("%Y-%m-%d") 
    ]) 
 
    print("[SUCCESS] Return reason submitted successfully!") 
    print(f"Reason: {reason}") 
 
 
# ========================================== 
# VIEW RETURN REASONS 
# ========================================== 
 
def view_feedback(): 
    print("\n================ UNIFORM RETURN REASONS ================") 
 
    if not feedback_records: 
        print("No return reasons found.") 
        return 
 
    for record in feedback_records: 
        print("-" * 55) 
        print(f"Transaction ID: {record[0]}") 
        print(f"Student ID: {record[1]}") 
        print(f"Reason: {record[2]}") 
        print(f"Date: {record[3]}") 
 
    print("-" * 55) 
 
 
# ========================================== 
# INVENTORY REPORT 
# ========================================== 
 
def show_report(): 
    print("\n================ INVENTORY REPORT ================") 
 
    if not inventory: 
        print("No uniform records found.") 
        return 
 
    headers = ( 
        "STUDENT ID", 
        "TRANSACTION ID", 
        "GENDER", 
        "TYPE", 
        "SIZE", 
        "ISSUED", 
        "RETURNED", 
        "STATUS", 
        "ISSUE DATE" 
    ) 
 
    widths = (22, 18, 10, 10, 10, 9, 11, 21, 12) 
 
    print("-" * sum(widths)) 
 
    print("".join( 
        f"{header:<{width}}" 
        for header, width in zip(headers, widths) 
    )) 
 
    print("-" * sum(widths)) 
 
    for item in inventory: 
        print("".join( 
            f"{str(value):<{width}}" 
            for value, width in zip(item, widths) 
        )) 
 
    print("-" * sum(widths)) 
 
 
# ========================================== 
# ADMIN LOGIN 
# ========================================== 
 
def admin_login(): 
    print("\n==========================================") 
    print("       SCHOOL UNIFORM SYSTEM LOGIN") 
    print("==========================================") 
 
    for attempt in range(3): 
        username = input("Admin username: ").strip() 
        password = input("Admin password: ").strip() 
 
        if ( 
            username == ADMIN_USERNAME 
            and password == ADMIN_PASSWORD 
        ): 
            print("[SUCCESS] Admin login successful!") 
            return True 
 
        print("[ERROR] Incorrect username or password!") 
        print(f"Attempts remaining: {2 - attempt}") 
 
    print("[ERROR] Too many failed attempts.") 
    return False 
 
 
# ========================================== 
# MAIN MENU 
# ========================================== 
 
def main(): 
    if not admin_login(): 
        return 
 
    while True: 
        print("\n====================================================") 
        print("       SCHOOL UNIFORM INVENTORY MONITORING SYSTEM") 
        print("====================================================") 
        print("[1] Register Student") 
        print("[2] View Registered Students") 
        print("[3] Issue Uniform") 
        print("[4] Return Uniform and Enter Return Reason") 
        print("[5] View Inventory Report") 
        print("[6] Add Uniform Stock") 
        print("[7] View Uniform Stock") 
        print("[8] View Uniform Return Reasons") 
        print("[9] Logout / Exit") 
 
        choice = input("Enter your choice: ").strip() 
 
        # REGISTER STUDENT 
        if choice == "1": 
            register_student_menu() 
 
        # VIEW REGISTERED STUDENTS 
        elif choice == "2": 
            view_students() 
 
        # ISSUE UNIFORM 
        elif choice == "3": 
            sid = input( 
                "Enter Student ID (02-XXXX-XXXXXX): " 
            ).strip() 
 
            if not is_valid_student_id(sid): 
                print( 
                    "[ERROR] Invalid Student ID! " 
                    "Required format: 02-XXXX-XXXXXX" 
                ) 
                continue 
 
            if not any(student[0] == sid for student in students): 
                print("[ERROR] Student not found. Register first!") 
                continue 
 
            gender = select_gender() 
            utype = select_uniform_type() 
            size = select_size() 
 
            qty = get_positive_quantity( 
                "Enter Quantity to Issue: " 
            ) 
 
            # Generate transaction ID automatically 
            uid = generate_transaction_id() 
 
            print(f"\nGenerated Transaction ID: {uid}") 
 
            success = issue_uniform( 
                sid, uid, gender, utype, size, qty 
            ) 
 
            if success: 
                print(f"Please save your Transaction ID: {uid}") 
 
        # RETURN UNIFORM 
        elif choice == "4": 
            if not inventory: 
                print("[ERROR] No uniform transactions found.") 
                continue 
 
            uid = input( 
                "Enter Transaction ID to Return " 
                "(e.g., 000001): " 
            ).strip() 
 
            qty = get_positive_quantity( 
                "Enter Quantity to Return: " 
            ) 
 
            if return_uniform(uid, qty): 
                submit_feedback(uid) 
 
        # VIEW INVENTORY REPORT 
        elif choice == "5": 
            show_report() 
 
        # ADD UNIFORM STOCK 
        elif choice == "6": 
            gender = select_gender() 
            utype = select_uniform_type() 
            size = select_size() 
 
            qty = get_positive_quantity( 
                "Enter Quantity to Add: " 
            ) 
 
            add_stock(gender, utype, size, qty) 
 
        # VIEW STOCK 
        elif choice == "7": 
            view_stock() 
 
        # VIEW RETURN REASONS 
        elif choice == "8": 
            view_feedback() 
 
        # LOGOUT / EXIT 
        elif choice == "9": 
            print("[SUCCESS] Logging out. Thank you!") 
            break 
 
        else: 
            print("[ERROR] Invalid choice. Please try again.") 
 
 
# ========================================== 
# RUN PROGRAM 
# ========================================== 
 
if __name__ == "__main__": 
    main() 
