def test_black_hole(chain):
    bh, _ = chain.provider.get_or_deploy_contract('black-hole', {'value': 42})

    # has balance that it was deployed with
    assert chain.web3.eth.getBalance(bh.address) == 42

    transaction = {
        'from': chain.web3.eth.coinbase,
        'to':   bh.address,
        'value': 42,
    }
    txhash = chain.web3.eth.sendTransaction(transaction)
    txreceipt = chain.wait.for_receipt(txhash)

    # all balance cleared, old and new
    assert chain.web3.eth.getBalance(bh.address) == 0
