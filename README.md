# Blockchain-Python
HD (Hierarchial Deterministic) Wallets can allow for many crpyto wallets to be generated from a single seed phrase. It's a public/private key tree starting from a root node which is the master node. 
Any node can have an number of children. The master private key's sole purpose is wallet tree regeneration and is unable to sign transactions. The HD wallet is able to generate many public/private keys pairs from a single seed or mnemonic. Ideally every parent should have one child until reaching the chain node at which point an unlimited number of children should be allowed. The "children" represent the address nodes.
In order to construct a transaction, you need to make sure the address has currency associated with it and use the private key of the address node to sign. This uses the address node's private key to sign a transaction spending money from the address node's public key.  
 
