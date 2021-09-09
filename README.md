# BSC FAIR LAUNCH PROJECT

## Install procedure:

* Download a recent python version (>= 3.6)
* Create a virtual environment: python3 -m venv “/path/to/new/virtual/environment”
* Activate you virtual environment: “/path/to/new/virtual/environment/Script/Activate” or source “/path/to/new/virtual/environment/bin/activate" on mac/linux
* Install Web3 library. Execute: pip install web3
* Clone this branch to a local path “/project/path/bsc_fair_launch”

## Script execution:

* Edit the main.py file located in your “/project/path/bsc_fair_launch” directory changing <YOUR_ADDRESS> with your address, <YOUR_PRIVATE_KEY> with private key, <COIN_TICKER> with the token ticker you want to swap, <TOKEN_CONTRACT> with token contract you want to swap. You can also edit some other property such as gas price, gas limit, etc..
* Activate the virtual environment as shown in previous lines (if not already activate). 
* Run the script executing python project/path/bsc_fair_launch/main.py

## Script results (Check the transaction on BSCscan anyway):
* Swap correctly performed
* Swap error. Check transaction to see details




