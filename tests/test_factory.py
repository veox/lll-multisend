def get_greeter_addr_from_log(chain, receipt):
    logtopic = receipt['logs'][0]['topics'][2]
    addr = chain.web3.toChecksumAddress(logtopic)
    return addr

def create_greeter(chain, factory):
    txhash = factory.transact().stamp()
    txreceipt = chain.wait.for_receipt(txhash)

    greeteraddr = get_greeter_addr_from_log(chain, txreceipt)

    return greeteraddr

########################################################################

def test_factory_creates_greeters(chain):
    factory, _ = chain.provider.get_or_deploy_contract('factory')

    greeter0addr = create_greeter(chain, factory)
    greeter1addr = create_greeter(chain, factory)

    assert greeter0addr != greeter1addr

def test_greeter(chain):
    factory, _ = chain.provider.get_or_deploy_contract('factory')

    Greeter = chain.provider.get_contract_factory('greeter')
    greeteraddr = create_greeter(chain, factory)
    greeter = Greeter(address=greeteraddr)

    greeting = greeter.call().greet()
    assert greeting == 42

    set_txn_hash = greeter.transact().setGreeting(1337)
    chain.wait.for_receipt(set_txn_hash)

    greeting = greeter.call().greet()
    assert greeting == 1337
