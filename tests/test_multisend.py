def test_multisend(chain):
    ms, _ = chain.provider.get_or_deploy_contract('multisend')

    to = [
        '0x0101010101010101010101010101010101010101',
        '0x0202020202020202020202020202020202020202',
        '0x0303030303030303030303030303030303030303',
        '0x0404040404040404040404040404040404040404',
        '0x0505050505050505050505050505050505050505',
        '0x0606060606060606060606060606060606060606',
    ]
    amt = list(range(42,42+len(to)))

    assert len(to) == len(amt)

    # seed balances so we don't pay for account creation
    for addr in to:
        chain.web3.eth.sendTransaction({
            'from': chain.web3.eth.coinbase,
            'to': addr,
            'value': 1
        })

    txhash = ms.transact({
        'value': sum(amt),
        'gas': 21000 * len(to)
    }).sendMany(to, amt)
    txreceipt = chain.wait.for_receipt(txhash)

    # pretty when run as `pytest --capture=no tests/test_multisend.py`
    print('')
    print('Gas used (total):', txreceipt['gasUsed'])
    print('Gas used (avg/xfer):', txreceipt['gasUsed']/len(to))

    assert chain.web3.eth.getBalance(ms.address) == 0
    assert chain.web3.eth.getBalance(to[0]) >= amt[0]
