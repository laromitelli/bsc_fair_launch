from order_handler import PairHandler

# SETTING is the only variable to edit!!!
SETTINGS = {
    # Wallet info
    "wallet_address": "<YOUR_ADDRESS>",                                  # Change <YOUR_ADDRESS> with your address
    "wallet_private_key": "<YOUR_PRIVATE_KEY>",                          # Change <YOUR_PRIVATE_KEY> with private key
    # Order info
    "ticker": "BNB/<COIN_TICKER>",                                       # Change <COIN_TICKER> with token ticker
    "is_buy_order": True,                                                # True to buy, False to sell
    "gas_limit": "176039",                                               # Raise this value on "fair launch" scenarios
    "gas_price": "5",                                                    # Raise this value on "fair launch" scenarios
    "token_address": "<TOKEN_CONTRACT>",                                 # Change <TOKEN_CONTRACT> with token contract
    "base_token_address": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",  # BNB is suggested (already set)
    "quantity": 2
}

if __name__ == '__main__':
    # handler constructor
    pair_handler = PairHandler(SETTINGS['ticker'],
                               SETTINGS['wallet_address'],
                               SETTINGS['wallet_private_key'],
                               SETTINGS['gas_limit'],
                               SETTINGS['gas_price'],
                               SETTINGS['token_address'],
                               SETTINGS['base_token_address'])
    # Performing swap
    swap_result = pair_handler.swap(SETTINGS['quantity'], SETTINGS['is_buy_order'])
    # Printing results
    if swap_result[0] == 1:
        print("Swap correctly performed.")
    else:
        print("Swap error. Check transaction to see details")
    print("{} - {}".format(swap_result[0], swap_result[1]))


# COMMENT PREVIOUS LINES AND DE-COMMENT THE BELOW TO TRY THIS SCRIPT ON BSC TESTNET. Example with BNB/BUSD pair
#
# from order_handler import PairHandler
#
#
# SETTINGS = {
#     # Wallet info
#     "wallet_address": "<YOUR_ADDRESS>",
#     "wallet_private_key": "<YOUR_PRIVATE_KEY>",
#     # Order info
#     "is_buy_order": True,
#     "ticker": "BNB/CAKE",
#     "gas_limit": 343478,                                                 # Raise this value on "fair launch" scenarios
#     "gas_price": 10,                                                     # Raise this value on "fair launch" scenarios
#     "token_address": "0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7",        # Token to swap. BUSD in this example
#     "base_token_address": "0xae13d989dac2f0debff460ac112a837c89baa7cd",   # BNB is suggested (already set)
#     "quantity": 5
# }
#
# if __name__ == '__main__':
#     # handler constructor
#     pair_handler = PairHandler(SETTINGS['ticker'],
#                                SETTINGS['wallet_address'],
#                                SETTINGS['wallet_private_key'],
#                                SETTINGS['gas_limit'],
#                                SETTINGS['gas_price'],
#                                SETTINGS['token_address'],
#                                SETTINGS['base_token_address'],
#                                test_mode=True)
#     # Performing swap
#     swap_result = pair_handler.swap(SETTINGS['quantity'], SETTINGS['is_buy_order'])
#     # Printing results
#     if swap_result[0] == 1:
#         print("Swap correctly performed.")
#     else:
#         print("Swap error. Check transaction to see details")
#     print("{} - {}".format(swap_result[0], swap_result[1]))
