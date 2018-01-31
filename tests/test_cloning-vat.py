########################################################################

def test_vat(chain):
    # deploy one cloning-vat by regular means
    vat0, _ = chain.provider.get_or_deploy_contract('cloning-vat')
    vat0address = chain.web3.toChecksumAddress(vat0.address)

    # use the cloning-vat to clone a copy of itself
    txhash = vat0.transact().clone(vat0.address)
    txreceipt = chain.wait.for_receipt(txhash)

    # DEBUG: uncomment to view memory during execution
    # print('-'*33 + 'MEMDMP' + '-'*33)
    # data = txreceipt['logs'][0]['data']
    # data = data[2:] # snip 0x
    # for i in range(int(len(data)/64)):
    #     print(chain.web3.toHex(i*32), data[i*64:i*64+64], sep='\t')

    # extract cloned contract's address from log entry
    vat1address = chain.web3.toChecksumAddress(txreceipt['logs'][0]['data'])
    # DEBUG: use this instead when viewing memory during execution
    # vat1address = chain.web3.toChecksumAddress(txreceipt['logs'][1]['data'])

    # form an object so the cloned contract can be interacted with
    CloningVat = chain.provider.get_contract_factory('cloning-vat')
    vat1 = CloningVat(address=vat1address)

    assert vat0.address != vat1.address
    assert chain.web3.eth.getCode(vat0.address) == chain.web3.eth.getCode(vat1.address)

    # use the cloned cloning-vat to clone another copy
    txhash = vat1.transact().clone(vat1.address)
    txreceipt = chain.wait.for_receipt(txhash)

    # form another object, for the twice cloned cloning-vat
    vat2address = chain.web3.toChecksumAddress(txreceipt['logs'][0]['data'])
    # DEBUG: use this instead when viewing memory during execution
    # vat2address = chain.web3.toChecksumAddress(txreceipt['logs'][1]['data'])

    vat2 = CloningVat(address=vat2address)

    assert vat1.address != vat2.address
    assert chain.web3.eth.getCode(vat1.address) == chain.web3.eth.getCode(vat2.address)
