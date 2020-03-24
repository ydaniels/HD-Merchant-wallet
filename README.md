
What is HD Merchant Wallet ?
===============
It is a simple lightweight tool for receiving cryptocurrency payment, generating hd cryptocurrency wallet addresses and verifying payment made to an address. You can
receive cryptocurrency payment easily in any python script or web app in just 3 simple steps. It perfectly works with electrum wallet so you can receive payment with this tool and spend your coins with electrum wallet.

Installation
==============
pip install merchant_wallet

Running
========

  
 - Get your master public key from a local or personal wallet e.g Electrum.
 - Generate addresses with this script, addresses will correspond with addresses on your electrum wallet, so you can easily spend your coins.
 - Give address for payment and verify transaction using this tool.


Accept Bitcoin on a website In 3 Steps
======================
 
          from merchant_wallet.backend.btc import BitcoinBackend
          
          
          btc = BitcoinBackend('master_public_key_gotten_from_an_offline_wallet')
          
          btc.generate_new_address(index=0) #index=0 will give the first address displayed on your electrum wallet, increase index to get more addresses as displayed on your wallet
          
          btc.confirm_address_payment(
            address="1Ge6rDuyCdYVGhXZjcK4251q67GXMKx6xK", total_crypto_amount=0.01, confirmation_number=3
          )#Confirm payment on the address with the specified confirmation and amount it will return tuple of transaction status and value of transaction
          
          #For unconfirmed payment, hash of the found transaction is returned (UNCONFIRMED_ADDRESS_BALANCE, transaction_hash)
          btc.confirm_address_payment(
            address="1Ge6rDuyCdYVGhXZjcK4251q67GXMKx6xK", total_crypto_amount=0.01, confirmation_number=5000, tx_hash='hash_returned_when_transaction_was_unconfirmed'
          )
Note
======================    
  This tool depends on blockcypher for verifying blockchain transactions and uses forex-python tool for calculating crypto prices
    
 
 
Helper methods
======================    
  
- bitcoin.convert_to_fiat( amount, currency)
- bitcoin.convert_from_fiat(amount, currency)
- Check tests for more
                 
Todo
======================              
 - Add more crypto currency support
 - Add support for local private blockchain service e.g bitcoind
    
**LICENSE**
=========
MIT
                    
     
     
                    
                    
                  
                  
    