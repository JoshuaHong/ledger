# Ledger

Keep track of your transactions in the terminal.

[![asciicast](https://asciinema.org/a/SIHDMTpd94tHlXmXdG6ulC4rZ.png)](https://asciinema.org/a/SIHDMTpd94tHlXmXdG6ulC4rZ)

## Overview
A simple terminal interface to manage transactions locally. \
The transactions are stored in a ledger file, and the receipts are copied to the receipt directory. \
Transactions are saved in the following format:
* Description: A brief summary of the transaction.
* Items: The items involved.
* Address: The address of the transaction.
* Timestamp: When the transaction occurred.
* Payment Method: The payment method used for the transaction.
* Receipt: An image or PDF of the receipt.

## Getting Started
1. Install the following dependencies:
    * A Linux based system
    * Python 3.11 - For new features (E.g. StrEnum)
    * Fzf (Optional) - For easy searching (highly recommended)
2. Set the PAGER environment variable (Optional) - For listing search results
    * E.g. `export PAGER=less`
3. Create an empty directory for receipts:
    * E.g. `mkdir receipts/`
4. Run the program:
    ```
    python src/main.py -n ledger.json receipts/
    ```
    * `-n`: Create a new ledger file. This flag is only used to instantiate the ledger file.
    * `ledger.json`: The file in which the transactions are stored.
    * `receipts/`: The directory containing a copy of the receipts.
    * Optionally provide a `-s search_directory/` in which to search for receipts to copy to the `receipts/` directory.
    * See below for more information.

## Important
Do not manually modify the `ledger_file` or the `receipts_directory`.
    
## Usage
```
main.py [-h] [-n] [-s search_directory] ledger_file receipts_directory
    -h: Display the help menu and exit.
    -n: Create a new ledger file.
    -s search_directory: The directory in which to search for receipts to be copied to the receipts directory.
    ledger_file: The file containing the transactions in JSON format.
    receipts_directory: The directory containing a copy of the receipts.
```

## Future goals
* Metrics and visualizations:
    * Graphing the amount earned or spent over a given period of time.
    * Measuring trends. For example, how much was spent on groceries in 2022. This is where tags are useful.
* Convert to a curses TUI application

## Contributing
All contributions welcome.
