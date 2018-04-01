#

# TODO: seriously, put this in a lib or something!
def _print_memdump(chain, txreceipt):
    '''Hacky helper for memory inspection.'''
    print('-'*33 + 'MEMDMP' + '-'*33)
    data = txreceipt['logs'][0]['data']
    data = data[2:] # snip 0x
    for i in range(int(len(data)/64)):
        print(chain.web3.toHex(i*32), data[i*64:i*64+64], sep='\t')

    # FIXME: required since accessing logs by index instead of event id;
    # also, forces the dump to be displayed
    assert False
    return

# ==============================================================================

def test_graffiti(chain):
    graffiti, _ = chain.provider.get_or_deploy_contract('graffiti')

    ntimes = 2
    data = '0x' + ('000102030405060708090a0b0c0d0e0f'*2)*ntimes

    # data-as-text length is a multiple of 64
    assert len(data[2:]) % 2*32 == 0

    transaction = {
        'to': graffiti.address,
        'data': data,
    }
    txhash = chain.web3.eth.sendTransaction(transaction)
    txreceipt = chain.wait.for_receipt(txhash)

    #_print_memdump(chain, txreceipt)

    # FIXME: some actual tests please
