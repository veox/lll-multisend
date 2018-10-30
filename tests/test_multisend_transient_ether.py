from pprint import pprint as pp

def give_balances(chain, to):
    for addr in to:
        chain.web3.eth.sendTransaction({
            'from': chain.web3.eth.coinbase,
            'to': addr,
            'value': 1,
        })
    return

def test_multisend_transient_ether(chain):
    ms, _ = chain.provider.get_or_deploy_contract('multisend-resident-ether')

    pp(ms)

    # FIXME: manual copy-paste from `lllc -o -x multisend-transient-ether.lll`
    mscode = '0x' + '6040356060525b60605115603c5760206060510260a0016040526000806000806020604051013560405135611337f1506001606051036060526006565b00'

    to = [
        '0x0101010101010101010101010101010101010101',
        '0x0202020202020202020202020202020202020202',
        '0x0303030303030303030303030303030303030303',
        '0x0404040404040404040404040404040404040404',
        '0x0505050505050505050505050505050505050505',
        '0x0606060606060606060606060606060606060606',
    ]
    amt = list(range(42, 42 + len(to)))

    assert len(to) == len(amt)

    # add zeros on the right (i.e. left-align)
    mscode_bytes = chain.web3.toBytes(hexstr=mscode).ljust(64, b'\0')

    nrecipients_bytes = chain.web3.toBytes(len(to)).rjust(32, b'\0')

    # `to` is already in hex-string, need same for `amt`
    amt_hexstr = [chain.web3.toHex(
        chain.web3.toBytes(val).rjust(32, b'\0')
        ) for val in amt]

    # interleave `to` and `amt`, converting to `bytes` in the process
    msdata_bytes = b''.join([chain.web3.toBytes(hexstr=val)
                             for pair in zip(to, amt_hexstr) for val in pair])

    # WORKHERE
    txdata = mscode_bytes + nrecipients_bytes + msdata_bytes
    pp(txdata)

    # seed balances so we don't pay for account creation (skews gas use benchmark)
    give_balances(chain, to)

    # build/send tx
    txhash = chain.web3.eth.sendTransaction({
        'from': chain.web3.eth.coinbase,
        'to': '', # sic!
        'data': '',
        'value': sum(amt),
        'gas': 30000 * len(to), # FIXME: magicnum
        })
    txreceipt = chain.wait.for_receipt(txhash)

    # pretty when run as `pytest --capture=no <path/to/file>`
    print('')
    print('Gas used (total):', txreceipt['gasUsed'])
    print('Gas used (avg/xfer):', txreceipt['gasUsed']/len(to))

    assert chain.web3.eth.getBalance(ms.address) == 0
    assert chain.web3.eth.getBalance(to[0]) >= amt[0]
