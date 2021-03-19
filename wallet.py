import subprocess
import json
import os
# import bit
# print(bit.__version__)
from bit import Key
from bit import PrivateKeyTestnet
from bit.net


work import NetworkAPI

from constants import *

from web3 import Web3, Account, middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

w3.middleware_onion.inject(geth_poa_middleware, layer=0)

w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

mnemonic = os.getenv('MNEMONIC', "wisdom knock poet solution adult save alcohol close fruit razor win almost")
coin = BTC
numderive = 3

def derive_wallets(mnemonic, coin, numderive):
    # command = './derive -g --mnemonic="INSERT HERE" --cols=path,address,privkey,pubkey --format=json'
    command = f'php ./hd-wallet-derive/hd-wallet-derive.php -g --mnemonic="{mnemonic}" --coin={coin} --numderive={numderive} --format=json'
    # print(command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()

    return json.loads(output)


def priv_key_to_account(coin, priv_key):
    if coin == 'eth':
        return Account.privateKeyToAccount(priv_key)
    else:
        return PrivateKeyTestnet(priv_key)

eth_account = priv_key_to_account(ETH,eth_key)

    
btc_account = priv_key_to_account(BTCTEST,btc_key)

def create_tx(coin,account,recipient,amount):
    global tx_data
    if coin =='eth':
        value = w3.toWei(amount, "ether")
        gasEstimate = w3.eth.estimateGas(
            {"from": account, "to": recipient, "value": value}
        )
        tx_data = {
            "from": account,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.generateGasPrice(),
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account),
            "chainId": w3.eth.chain_id
        }
        return tx_data
    else:
        tx_data = PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])
        return tx_data



def send_tx(coin, account, recipient, amount):
    tx = create_tx(coin, account, recipient, amount)
    signed_tx = account.sign_transaction(tx)
    if coin == ETH:
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(result)
        return result
    else:
        result = NetworkAPI.broadcast_tx_testnet(signed_tx)
        return result

coins = {
    BTCTEST: derive_wallets(mnemonic, BTCTEST, numderive),
    ETH: derive_wallets(mnemonic, ETH, numderive)
    
}

print(json.dumps(coins, indent=4))


# eth_key = coins['eth'][1]['privkey']
# btc_key = coins['btc-test'][0]['privkey']
# print("eth_key", eth_key)
# print("btc_key", btc_key)
# eth_to_acc = coins['eth'][0]['address']
# btc_to_acc = coins['btc-test'][1]['address']
# print("eth_to_acc", eth_to_acc)
# print("btc_to_acc", btc_to_acc)

# # send_tx(ETH, eth_account, str(eth_to_acc), 1)
# send_tx(BTC, btc_account, eth_to_acc, 1)

