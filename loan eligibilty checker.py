import random
from rich.console import Console
from rich.prompt import Prompt
from prettytable import PrettyTable

users_db = {}
loan_applications = {}

console = Console()
console.print("----- [bold red]    LoanMate  [/bold red] -----")
console.print("[bold yellow]  Quick Loans, Smart Decisions  [/bold yellow]")
console.print("[blue]                   Loanify by Rohan[/blue]")


def generate_otp():
    otp = random.randint(1000, 9999)  
    additional_number = random.randint(0, 9)  
    otp_with_additional_number = otp + additional_number
    return otp_with_additional_number


def is_valid_mobile_number(mobile_number):
    return len(mobile_number) == 10 and mobile_number.isdigit()


def register_user():
    console.print("----- [bold blue]User Registration[/bold blue] -----")
    username = Prompt.ask("Enter a username")
    if username in users_db:
        console.print("[bold red]Username already exists! Please choose a different username.[/bold red]")
        return False
    password = Prompt.ask("Enter a password")
    income = float(Prompt.ask("Enter your monthly income: ₹ "))
    credit_score = int(Prompt.ask("Enter your credit score: "))
    
    while True:
        mobile_number = Prompt.ask("Enter your mobile number: ")
        if is_valid_mobile_number(mobile_number):
            break
        else:
            console.print("[bold red]Invalid mobile number! It should be a 10-digit number.[/bold red]")
    
    otp = generate_otp()
    console.print(f"[bold green]An OTP has been sent to your mobile number: {otp}[/bold green]")
    entered_otp = int(Prompt.ask("Enter the OTP to verify your registration: "))
    
    if entered_otp == otp:
        users_db[username] = {'password': password, 'income': income, 'credit_score': credit_score, 'mobile_number': mobile_number}
        console.print(f"[bold green]User '{username}' registered successfully![/bold green]")
        return True
    else:
        console.print("[bold red]Invalid OTP! Registration failed.[/bold red]")
        return False


def login_user():
    console.print("----- [bold blue]User Login[/bold blue] -----")
    username = Prompt.ask("Enter your username")
    if username not in users_db:
        console.print("[bold red]Username does not exist! Please register first.[/bold red]")
        return None
    
    password = Prompt.ask("Enter your password")
    if users_db[username]['password'] == password:
        otp = generate_otp()
        mobile_number = users_db[username]['mobile_number']
        console.print(f"[bold green]An OTP has been sent to your mobile number: {mobile_number}[/bold green]")
        console.print(f"[bold green]Your OTP is: {otp}[/bold green]")
        entered_otp = int(Prompt.ask("Enter the OTP to verify your login: "))
        
        if entered_otp == otp:
            console.print(f"[bold green]Welcome back, {username}![/bold green]")
            return username  
        else:
            console.print("[bold red]Invalid OTP! Login failed.[/bold red]")
    else:
        console.print("[bold red]Incorrect password! Please try again.[/bold red]")
    return None

# Check loan eligibility
def check_loan_eligibility(income, credit_score):
    if income >= 30000 and credit_score >= 300:
        console.print("[bright_yellow]Congratulations! You are eligible for the loan.[/bright_yellow]")
    elif income >= 20000 and credit_score >= 250:
        console.print("[green]You are eligible for the loan with conditions. Please review your terms.[green]")
    else:
        console.print("[bold red]Sorry, you are not eligible for the loan based on the given details.[/bold red]")

# Calculate amortization (monthly loan repayment)
def calculate_amortization(principal, annual_rate, years):
    monthly_rate = annual_rate / 12 / 100
    months = years * 12
    monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
    return monthly_payment

# Apply for a loan
def apply_for_loan(username):
    console.print("----- [bold blue]Loan Application[/bold blue] -----")
    income = users_db[username]['income']
    credit_score = users_db[username]['credit_score']
    
  
    check_loan_eligibility(income, credit_score)
    
    # Prompt for loan details if eligible
    loan_amount = float(Prompt.ask("Enter the loan amount you want to apply for: ₹ "))
    loan_term_years = int(Prompt.ask("Enter the loan term (in years): "))
    annual_interest_rate = float(Prompt.ask("Enter the annual interest rate (in %): "))
    
    if loan_amount <= 0 or loan_term_years <= 0 or annual_interest_rate <= 0:
        console.print("[bold red]Loan amount, term, and interest rate must be greater than zero.[/bold red]")
        return
    
    monthly_payment = calculate_amortization(loan_amount, annual_interest_rate, loan_term_years)
    console.print(f"Your monthly payment will be ₹ {round(monthly_payment, 2)}.", style="bold green")
    
    loan_applications[username] = {
        'loan_amount': loan_amount, 'loan_term_years': loan_term_years,
        'annual_interest_rate': annual_interest_rate, 'monthly_payment': monthly_payment
    }
    console.print("[bold green]Your loan application has been submitted![/bold green]")

# View loan application history
def view_loan_history(username):
    if username in loan_applications:
        application = loan_applications[username]
        table = PrettyTable()
        table.field_names = ["Loan Amount", "Loan Term (Years)", "Annual Interest Rate (%)", "Monthly Payment"]
        table.add_row([f"₹ {application['loan_amount']}", application['loan_term_years'], application['annual_interest_rate'], f"₹ {round(application['monthly_payment'], 2)}"])
        console.print("----- [bold blue]Loan Application History[/bold blue] -----")
        console.print(table)
    else:
        console.print("[bold red]No loan application history found.[/bold red]")

# Main function to handle the menu and user choices
def main():
    current_user = None

    while True:
        console.print("\n----- [bold blue]Loan Application System[/bold blue] -----")
        console.print("[1] Register")
        console.print("[2] Login")
        console.print("[3] Exit")
        
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3"])

        if choice == '1':
            registration_successful = register_user()
            if registration_successful:
                console.print("[bold green]Registration successful, please login now.[/bold green]")
            else:
                console.print("[bold red]Registration failed. Try again.[/bold red]")

        elif choice == '2':
            current_user = login_user()
            if current_user:
                while True:
                    console.print("\n----- [bold blue]Welcome to Your Dashboard[/bold blue] -----")
                    console.print("[1] Check Loan Eligibility")
                    console.print("[2] Apply for a Loan")
                    console.print("[3] View Loan Application History")
                    console.print("[4] Logout")
                    dashboard_choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4"])

                    if dashboard_choice == '1':
                        income = users_db[current_user]['income']
                        credit_score = users_db[current_user]['credit_score']
                        check_loan_eligibility(income, credit_score)

                    elif dashboard_choice == '2':
                        apply_for_loan(current_user)

                    elif dashboard_choice == '3':
                        view_loan_history(current_user)

                    elif dashboard_choice == '4':
                        console.print("[bold yellow]Logging out...[/bold yellow]")
                        current_user = None
                        break  

                    else:
                        console.print("[bold red]Invalid choice. Please try again.[/bold red]")
        
        elif choice == '3':
            console.print("[bold yellow]Thank you for using the Loan Application System![/bold yellow]")
            break
        
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")

if __name__ == "__main__":
    main()
