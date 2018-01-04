def test_factory_stamps_greeter(chain):
    factory, _ = chain.provider.get_or_deploy_contract('factory')

    txhash = factory.transact().stamp()
    txreceipt = chain.wait.for_receipt(txhash)
    print(txreceipt)

    assert False
