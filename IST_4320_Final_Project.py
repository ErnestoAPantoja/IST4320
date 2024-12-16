#I decided to make my final project a credit card debt calculator.
#I am did this project to help visualize how I can pay down debt.
#This project is personal and I want to use it as a means to not only motivate my debt payment journey, but also to improve my Python skills.
#This credit card debt calculator will determine how many months it will take to pay down the debt and the accumulated interest within that time.
from time import sleep
import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal, getcontext     #I imported the Decimal class for higher decimal computational accuracy over float.

getcontext().prec = 50       #50 degrees of numerical accuracy by setting decimal places to 50.

def suggestedmin (interest_rate_per_period,total_payment,balanceOG):   #The minimum total payment calculation.
    offset = Decimal(0)       #Offset initialization.
    stop = int(0)             #Stops initialization.
    while(1):
        balance = balanceOG     #The balance value resets to original balance value.
        total_interest_paid = 0 #Will reset the total interest paid to 0.
        if balance > 0:
            interest = balance * interest_rate_per_period
            total_interest_paid += interest
            balance += interest - (total_payment+offset)
            if balance < balanceOG:    #This conditional will check if the minimum payment value is reached.
                stop = 1
        offset += Decimal(0.01)  #Offset increments by 0.01 for 2 decimal accurate computation for minimum payment suggestion.
        if stop == 1:
            break
    return((total_payment+offset))    #Suggested minimum payment return.

def calculate_debt():
    try:
        #This will get inputs.
        balance = Decimal(balance_entry.get())
        balanceOG = balance
        annual_interest_rate = Decimal(interest_rate_entry.get()) / Decimal(100)
        minimum_payment = Decimal(min_payment_entry.get())
        epCheck = len(extra_payment_entry.get())   #The len() function is to detect an empty field to automatically set to 0 on the succeeding conditional.
        warning = int(0)             #This is initialization for a runaway effect error for low minimum payment values.
        try:            
            extra_payment = Decimal(extra_payment_entry.get())
        except Exception:
            if epCheck == 0:     #If the field is empty, extra_payment is automatically set to 0.
                extra_payment = Decimal(0);
        payment_frequency = frequency_combo.get()
        
        #Payment frequency gets to be validated here.
        if payment_frequency == "Monthly":
            periods_per_year = Decimal(12)
        elif payment_frequency == "Weekly":
            periods_per_year = Decimal(52)
        
            return
        
        #Interest will be calculated here.
        interest_rate_per_period = annual_interest_rate / periods_per_year
        total_payment = minimum_payment + extra_payment
        
        #Payment simulations.
        months = 0
        total_interest_paid = Decimal(0)
        
        while balance > 0:
            interest = balance * interest_rate_per_period
            total_interest_paid += interest
            balance += interest - total_payment
            
            if balance < 0:  #This statement handles adjustments to the final payment.
                balance = 0
            
            months += 1

            if balance > balanceOG:      #Low minimum payment detection.
                warning = 1
                break
        
        #The results are displayed here with this code.
        if warning == 1:      #A warning if there is a low minimum payment.
            results_label.config(   #Suggested minimum payment total is called by using suggestedmin().
                text=f"Warning!\nYour minimum total payment is too low!\nThis will result to unpayable debt!\nMinimum must be at least: ${(suggestedmin(interest_rate_per_period,total_payment,balanceOG)):.2f}"
            )
        else:
            results_label.config(  #Added total credit cost as insight to how much was spent overall.
                text=f"Debt paid off in {months} months.\nTotal interest paid: ${total_interest_paid:.2f}\nTotal cost of debt: ${(total_interest_paid+balanceOG):.2f}"
            )
    except Exception:    #Exception to accomodate decimal class errors.
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

#The main window is created here.
root = tk.Tk()
root.resizable(width=False, height=False)     #Added this line for aspect ratio locking.
root.title("Credit Card Debt Calculator")

#The labels, entries, and combo boxes necessary are created.
tk.Label(root, text="Balance:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
balance_entry = tk.Entry(root)
balance_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Annual Interest Rate (%):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
interest_rate_entry = tk.Entry(root)
interest_rate_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Minimum Payment:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
min_payment_entry = tk.Entry(root)
min_payment_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Extra Payment:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
extra_payment_entry = tk.Entry(root)
extra_payment_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Payment Frequency:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
frequency_combo = ttk.Combobox(root, state="readonly", values=["Monthly", "Weekly"])   #I set tkinter combobox to readonly to disable editing/typing.
frequency_combo.grid(row=4, column=1, padx=10, pady=5)
frequency_combo.set("Monthly")  

#The button to calculate credit card debt is created.
calculate_button = tk.Button(root, text="Calculate", command=calculate_debt)
calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

#Results are displayed.
results_label = tk.Label(root, text="", justify="left")
results_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

#Run the app to calculate credit card debt.
root.mainloop()

