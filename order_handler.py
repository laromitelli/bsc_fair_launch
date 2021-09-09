import time

import yaml
from web3 import Web3
from datetime import datetime, timezone

# BSC url
from web3.exceptions import TransactionNotFound

BSC_CHAIN_URL = "https://bsc-dataseed1.binance.org:443"
BSC_CHAIN_URL_TEST = "https://data-seed-prebsc-1-s1.binance.org:8545/"
# ABIs
GENERIC_ABI = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"_decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"_symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getOwner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"mint","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"renounceOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
PANCAKE_ABI = '[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[],"name":"INIT_CODE_PAIR_HASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
POOL_ABI = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
PANCAKE_ROUTER_ABI = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
# Coin Addresses
BNB_ADDRESS = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
BUSD_ADDRESS = '0xe9e7cea3dedca5984780bafc599bd69add087d56'
BNB_ADDRESS_TEST = '0xae13d989dac2f0debff460ac112a837c89baa7cd'
BUSD_ADDRESS_TEST = '0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7'
# Contract Addresses
PANCAKE_V1_FACTORY = '0xBCfCcbde45cE874adCB698cC183deBcF17952812'
PANCAKE_V2_FACTORY = '0xca143ce32fe78f1f7019d7d551a6402fc5350c73'
PANCAKE_V1_ROUTER = '0x05fF2B0DB69458A0750badebc4f9e13aDd608C7F'
PANCAKE_V2_ROUTER = '0x10ed43c718714eb63d5aa57b78b54704e256024e'
PANCAKE_ROUTER_TEST = '0x9Ac64Cc6e4415144C455BD8E4837Fea55603e5c3'
# BSC chain IDs
BSC_CHAIN_ID = 56
BSC_CHAIN_ID_TEST = 97
# Useful variables
OPERATION_WAITING_TIME = 5
DEFAULT_SLIPPAGE = 0.8
# Enums
BUY = 'BUY'
SELL = 'SELL'
OPEN_ORDER = 'OPEN_ORDER'
FAILED_ORDER = 'FAILED_ORDER'
FILLED_ORDER = 'FILLED_ORDER'


class PairHandler:

    def __init__(self, pair_id, wallet_address, private_key, gas, gas_price,
                 coin_address, base_coin_address=BNB_ADDRESS, pancake_version=2, test_mode=False):
        # Variables set by user
        self.pair_id = pair_id
        self.coin_address = coin_address
        self.base_coin_address = base_coin_address
        self.pancake_version = pancake_version
        self.wallet_address = wallet_address
        self.private_key = private_key
        self.test_mode = test_mode
        self.gas_price = gas_price
        self.gas = gas
        # Initializing blockchain web3 obj
        self.web3 = Web3(Web3.HTTPProvider(BSC_CHAIN_URL_TEST if test_mode else BSC_CHAIN_URL))
        self.pancake_factory_address = PANCAKE_V1_FACTORY
        if self.pancake_version == 2:
            self.pancake_factory_address = PANCAKE_V2_FACTORY
        # Setting chain configurations
        self.pancake_router_addr = PANCAKE_V1_ROUTER
        if self.test_mode:
            self.pancake_router_addr = PANCAKE_ROUTER_TEST
        elif self.pancake_version == 2:
            self.pancake_router_addr = PANCAKE_V2_ROUTER
        self.chain_id = BSC_CHAIN_ID_TEST if self.test_mode else BSC_CHAIN_ID
        # Other useful variables
        self.orders = []
        self.pair_check_enabled = True

    def approve_contract(self, contract_address, amount=1000):
        # Method to approve contract
        account_check = self.web3.eth.account.privateKeyToAccount(self.private_key).privateKey
        coin_contract = self.web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=GENERIC_ABI)
        nonce = self.web3.eth.get_transaction_count(self.wallet_address)
        # Calling contract method
        approve_txn = coin_contract.functions.approve(Web3.toChecksumAddress(contract_address),
                                                      self.web3.toWei(amount, 'ether')).buildTransaction({
            'chainId': self.chain_id,
            'gas': self.gas,
            'gasPrice': self.web3.toWei(self.gas_price, 'gwei'),
            'nonce': nonce
        })
        signed_txn = self.web3.eth.account.sign_transaction(approve_txn, private_key=account_check)
        txt = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # Returning transaction hash
        return txt

    def get_transaction_status(self, tnx_hash):
        # Method to get Transaction status: -1 Not mined. 0 Failed. 1 Successful
        try:
            transtaction_receipt = self.web3.eth.getTransactionReceipt(tnx_hash)
        except TransactionNotFound as e:
            return -1
        if transtaction_receipt is None:
            return -1
        return self.web3.eth.getTransactionReceipt(tnx_hash).status

    def is_allowance_ready(self, contract_address, min_allowance=0):
        # Checking if the contract was approved
        coin_contract = self.web3.eth.contract(address=Web3.toChecksumAddress(contract_address), abi=GENERIC_ABI)
        allowance = coin_contract.functions.allowance(Web3.toChecksumAddress(self.wallet_address),
                                                      Web3.toChecksumAddress(contract_address)).call()
        return allowance > min_allowance

    def swap(self, payable_amount, from_base_to_token=True, amount_min=0, deadline_seconds_from_now=300):
        # Method to generic swap
        if from_base_to_token and self.base_coin_address in [BNB_ADDRESS, BNB_ADDRESS_TEST]:
            swap_tnx = self.swap_bnb_to_token(payable_amount, amount_min, deadline_seconds_from_now)
        else:
            swap_tnx = self.swap_token_to_token(payable_amount, from_base_to_token, amount_min,
                                                deadline_seconds_from_now)
        swap_tnx_status = self.get_transaction_status(swap_tnx)
        while swap_tnx_status != 0 and swap_tnx_status != 1:
            print("[{}] - Waiting for swap to be mined ({}). Checking again in {} seconds..".format(self.pair_id,
                                                                                             swap_tnx_status,
                                                                                             OPERATION_WAITING_TIME))
            time.sleep(OPERATION_WAITING_TIME)
            swap_tnx_status = self.get_transaction_status(swap_tnx)
        return swap_tnx_status, swap_tnx

    def swap_bnb_to_token(self, payable_amount, amount_min, deadline_seconds_from_now):
        # Approving both contracts
        if not self.is_allowance_ready(self.base_coin_address):
            approve_tnx = self.approve_contract(self.base_coin_address)
            while self.get_transaction_status(approve_tnx) != 0 and self.get_transaction_status(approve_tnx) != 1:
                print("[{}] - Waiting until token approve is mined. Checking again in {} seconds..".format(self.pair_id,
                                                                                                    OPERATION_WAITING_TIME))
                time.sleep(OPERATION_WAITING_TIME)
        if not self.is_allowance_ready(self.coin_address):
            approve_tnx = self.approve_contract(self.coin_address)
            while self.get_transaction_status(approve_tnx) != 0 and self.get_transaction_status(approve_tnx) != 1:
                print("[{}] - Waiting until token approve is mined. Checking again in {} seconds..".format(self.pair_id,
                                                                                                    OPERATION_WAITING_TIME))
                time.sleep(OPERATION_WAITING_TIME)
        # Swapping base coin to token coin through pancake router contract
        pancake_router_address = Web3.toChecksumAddress(self.pancake_router_addr)
        pancake_router_contract = self.web3.eth.contract(address=pancake_router_address, abi=PANCAKE_ROUTER_ABI)
        # preparing request variables
        account_check = self.web3.eth.account.privateKeyToAccount(self.private_key).privateKey
        path = [Web3.toChecksumAddress(self.base_coin_address), Web3.toChecksumAddress(self.coin_address)]
        utc_time_now = datetime.now(timezone.utc).replace(tzinfo=timezone.utc)
        utc_timestamp_deadline = round(utc_time_now.timestamp() + deadline_seconds_from_now)
        tnx = {
            'chainId': self.chain_id,
            'gas': self.gas,
            'gasPrice': self.web3.toWei(self.gas_price, 'gwei'),
            'nonce': self.web3.eth.get_transaction_count(self.wallet_address),
            'value': Web3.toWei(payable_amount, 'ether')
        }
        # Swapping base coin to token coin through pancake router contract
        swap_txn = pancake_router_contract.functions.swapExactETHForTokens(
            Web3.toWei(amount_min, 'ether'),
            path,
            Web3.toChecksumAddress(self.wallet_address),
            utc_timestamp_deadline).buildTransaction(tnx)
        signed_txn = self.web3.eth.account.sign_transaction(swap_txn, private_key=account_check)
        # returning transaction id
        result_tnx = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # Returning transaction hash
        return result_tnx

    def swap_token_to_token(self, payable_amount, from_base_to_token, amount_min, deadline_seconds_from_now):
        # Approving both contracts
        if not self.is_allowance_ready(self.base_coin_address):
            approve_tnx = self.approve_contract(self.base_coin_address)
            while self.get_transaction_status(approve_tnx) != 0 and self.get_transaction_status(approve_tnx) != 1:
                print("[{}] - Waiting until token approve is mined. Checking again in {} seconds..".format(self.pair_id,
                                                                                                    OPERATION_WAITING_TIME))
                time.sleep(OPERATION_WAITING_TIME)
        if not self.is_allowance_ready(self.coin_address):
            approve_tnx = self.approve_contract(self.coin_address)
            while self.get_transaction_status(approve_tnx) == 0 and self.get_transaction_status(approve_tnx) != 1:
                print("[{}] - Waiting until token approve is mined. Checking again in {} seconds..".format(self.pair_id,
                                                                                                    OPERATION_WAITING_TIME))
                time.sleep(OPERATION_WAITING_TIME)
        # If base contract is not BNB, need to approve BNB in order to add BNB in swapping route
        if self.base_coin_address not in [BNB_ADDRESS, BNB_ADDRESS_TEST] and \
                self.coin_address not in [BNB_ADDRESS, BNB_ADDRESS_TEST]:
            token_provider_address = BNB_ADDRESS
            if self.test_mode:
                token_provider_address = BNB_ADDRESS_TEST
            if not self.is_allowance_ready(token_provider_address):
                approve_tnx = self.approve_contract(token_provider_address)
                while self.get_transaction_status(approve_tnx) != 0 and self.get_transaction_status(approve_tnx) != 1:
                    print("[{}] - Waiting until token approve is mined. Checking again in {} seconds..".format(self.pair_id,
                                                                                                        OPERATION_WAITING_TIME))
                    time.sleep(OPERATION_WAITING_TIME)
        # Swapping base coin to token coin through pancake router contract
        pancake_router_address = Web3.toChecksumAddress(self.pancake_router_addr)
        pancake_router_contract = self.web3.eth.contract(address=pancake_router_address, abi=PANCAKE_ROUTER_ABI)
        # preparing request variables
        account_check = self.web3.eth.account.privateKeyToAccount(self.private_key).privateKey
        # Setting route path. If the tokens to swap are not bnb, then we have to add bnb in the middle of the route
        bnb_address = None
        if self.base_coin_address not in [BNB_ADDRESS, BNB_ADDRESS_TEST] and \
                self.coin_address not in [BNB_ADDRESS, BNB_ADDRESS_TEST]:
            token_provider_address = BNB_ADDRESS
            if self.test_mode:
                token_provider_address = BNB_ADDRESS_TEST
            bnb_address = Web3.toChecksumAddress(token_provider_address)
        path = [Web3.toChecksumAddress(self.base_coin_address), Web3.toChecksumAddress(self.coin_address)]
        if not from_base_to_token:
            path = [Web3.toChecksumAddress(self.coin_address), Web3.toChecksumAddress(self.base_coin_address)]
        if bnb_address is not None:
            start_route_element = path[0]
            end_route_element = path[1]
            path = [start_route_element, bnb_address, end_route_element]
        # Setting expire timestamp to the transaction. Default 5 minutes.
        utc_time_now = datetime.now(timezone.utc).replace(tzinfo=timezone.utc)
        utc_timestamp_deadline = round(utc_time_now.timestamp() + deadline_seconds_from_now)
        tnx = {
            'chainId': self.chain_id,
            'gas': self.gas,
            'gasPrice': self.web3.toWei(self.gas_price, 'gwei'),
            'nonce': self.web3.eth.get_transaction_count(self.wallet_address)
        }
        # Swapping base coin to token coin through pancake router contract
        swap_txn = pancake_router_contract.functions.swapExactTokensForTokens(
            Web3.toWei(payable_amount, 'ether'),
            Web3.toWei(amount_min, 'ether'),
            path,
            Web3.toChecksumAddress(self.wallet_address),
            utc_timestamp_deadline).buildTransaction(tnx)
        signed_txn = self.web3.eth.account.sign_transaction(swap_txn, private_key=account_check)
        result_tnx = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        # Returning transaction hash
        return result_tnx
