import subprocess
import json
import os
# import bit
# print(bit.__version__)
from bit import Key
from constants import *


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


coins = {
    BTCTEST: derive_wallets(mnemonic, BTCTEST, numderive),
    ETH: derive_wallets(mnemonic, ETH, numderive)
    
}

print(json.dumps(coins, indent=4))


eth_key = coins['eth'][1]['privkey']
btc_key = coins['btc-test'][0]['privkey']

def priv_key_to_account(coin, priv_key):
    global account
    if coin == 'eth':
        account=Account.privateKeyToAccount(priv_key)
    else:
        account=PrivateKeyTestnet(priv_key)
    return account

priv_key_to_account(ETH,eth_key)

    
priv_key_to_account(BTCTEST,btc_key)

def create_tx(coin,account,recipient,amount):
    global tx_data
    if coin =='eth':
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        tx_data= {
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
        }
        return tx_data
    else:
        tx_data = PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])
        return tx_data

create_tx(BTCTEST,account,'moXSjCRnNxXK1njCsdVaSUz2zR7La8KPat',0.0001)

def send_tx(coin, account, recipient, amount):
    if coin == ETH:
        tx = create_tx(coin,account, recipient, amount)
        signed_tx = account.sign_transaction(tx)
        result = w3.eth.sendRawTransaction(signed.rawTransaction)
        print(result.hex())
        return result.hex()
    else:
        tx_data = create_tx(coin,account,recipient,amount)
        signed = account.sign_transaction(tx_data)
        NetworkAPI.broadcast_tx_testnet(signed)
        return signed


