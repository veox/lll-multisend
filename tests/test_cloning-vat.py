########################################################################

def test_vat(chain):
    vat0, _ = chain.provider.get_or_deploy_contract('cloning-vat')
    txhash  = vat0.transact().clone(vat0.address)
    txreceipt = chain.wait.for_receipt(txhash)

    print(vat0.address)
    print(txhash)
    print(txreceipt)
    assert False

    #assert vat0.address != vat1.address
