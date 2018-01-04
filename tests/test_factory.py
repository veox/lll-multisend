def get_greeter_addr_from_log(chain, receipt):
    logtopic = receipt['logs'][0]['topics'][2]
    addr = chain.web3.toChecksumAddress(logtopic)
    return addr

def test_factory_stamps_greeter(chain):
    factory, _ = chain.provider.get_or_deploy_contract('factory')

    txhash = factory.transact().stamp()
    txreceipt = chain.wait.for_receipt(txhash)
    greeter0addr = get_greeter_addr_from_log(chain, txreceipt)
    print(greeter0addr)

    txhash = factory.transact().stamp()
    txreceipt = chain.wait.for_receipt(txhash)
    greeter1addr = get_greeter_addr_from_log(chain, txreceipt)
    print(greeter1addr)

    assert False
