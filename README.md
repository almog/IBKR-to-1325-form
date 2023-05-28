# Interactive Brokers (IBKR) to Israel 1325 Tax Form Converter

This script automates the conversion of an Interactive Brokers (IBKR) financial statement CSV file into a format suitable for Israel's 1325 tax form.

## Description

The script processes the statement produced by IBKR's custom report, as described in this [fintranslator.com article](https://fintranslator.com/2022/07/11/ib-annual-statement-for-israel-tax-reporting/).
Each Trade row is merged with its corresponding ClosedLot and the currency rates for the buy and sale days (currently only supports USD), as well as other calculations necessary for the 1325 form, as detailed [here](https://fintranslator.com/israel-tax-return-example-2019).

## How to Use

1. Clone the repository.
2. Copy your IBKR statement into the root directory of the project.
3. Install requirements:
```bash
$ pip install -r ./requirements.txt
```

4. Run the script using the following commands:

```bash
$ python src
```

The output, an Excel spreadsheet, will be generated in the same directory.

# DISCLAIMER
This software is provided "as is" without any warranty of any kind. The author(s) disclaim all warranties, including implied warranties of merchantability, fitness for a particular purpose, and non-infringement. The software is intended for educational and informational purposes only.

This software is NOT a substitute for professional tax advice or services, nor does it provide legal, financial, or tax advice of any kind. Please consult a professional tax advisor or accountant to ensure the accuracy of tax information.

In no event shall the author(s) or copyright holder(s) be liable for any claim, damages or other liability, arising from, out of, or in connection with the software or its use.

By using this software, you acknowledge and accept these terms.
