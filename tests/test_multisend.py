def test_multisend(chain):
    ms, _ = chain.provider.get_or_deploy_contract('multisend')

    to = [
        '0x0101010101010101010101010101010101010101',
        '0x0202020202020202020202020202020202020202',
        '0x0303030303030303030303030303030303030303'
    ]
    amt = list(range(42,42+len(to)))

    assert len(to) == len(amt)

    txhash = ms.transact({'value': sum(amt)}).sendMany(to, amt)
    txreceipt = chain.wait.for_receipt(txhash)

    print(txreceipt)
    print(len(txreceipt['logs']))

    assert chain.web3.eth.getBalance(ms.address) == 0
    assert chain.web3.eth.getBalance(to[0]) == amt[0]

    assert False
