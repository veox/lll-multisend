def test_multisend(chain):
    ms, _ = chain.provider.get_or_deploy_contract('multisend')

    to = [
        '0x0101010101010101010101010101010101010101'
    ]
    amt = [42]*len(to)
    txhash = ms.transact({'value': sum(amt)}).sendMany(to, amt)
    chain.wait.for_receipt(txhash)
