########################################################################

def test_vat(chain):
    # deploy one cloning-vat by regular means
    vat0, _ = chain.provider.get_or_deploy_contract('cloning-vat')
    vat0address = chain.web3.toChecksumAddress(vat0.address)
    print('vat0:', vat0address)

    print(chain.web3.eth.getCode(vat0address))

    # use the cloning-vat to clone a copy of itself
    txhash = vat0.transact().clone(vat0.address)
    txreceipt = chain.wait.for_receipt(txhash)

    print('txhash:', txhash)
    print('tx:')
    print(chain.web3.eth.getTransaction(txhash))
    print('txreceipt:')
    print(txreceipt)

    print('-'*33 + 'MEMDMP' + '-'*33)
    data = txreceipt['logs'][0]['data']
    data = data[2:] # snip 0x
    for i in range(int(len(data)/64)):
        print(chain.web3.toHex(i*32), data[i*64:i*64+64], sep='\t')

    # extract cloned contract's address from log entry
    vat1address = chain.web3.toChecksumAddress(txreceipt['logs'][1]['data'])
    print('vat1:', vat1address)

    print(chain.web3.eth.getCode(vat1address))

    # form an object so the cloned contract can be interacted with
    CloningVat = chain.provider.get_contract_factory('cloning-vat')
    vat1 = CloningVat(address=vat1address)

    assert vat0.address != vat1.address

    # use the cloned cloning-vat to clone another copy
    txhash = vat1.transact().clone(vat1.address)
    txreceipt = chain.wait.for_receipt(txhash)

    print('txhash:', txhash)
    print('txreceipt:')
    print(txreceipt)

    # form another object, for the twice cloned cloning-vat
    vat2address = chain.web3.toChecksumAddress(txreceipt['logs'][1]['data'])
    print('vat2:', vat2address)
    print(chain.web3.eth.getCode(vat2address))
    vat2 = CloningVat(address=vat2address)

    assert False
