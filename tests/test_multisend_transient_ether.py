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
    # FIXME: manual copy-paste from `lllc -o -x multisend-transient-ether.lll`
    mscode = '0x' + '6060356060525b606051156043576020606051026080016040526000806000806020604051013560405135617530f1603657600080fd5b6001606051036060526006565b00'

    nrecipients = 2
    to = [chain.web3.toHex(
        chain.web3.toBytes(addr).rjust(20, b'\0')
    ) for addr in range(4096, 4096+nrecipients)]
    amt = list(range(42, 42 + len(to)))

    assert nrecipients == len(to) == len(amt)

    # add zeros on the right (i.e. left-align)
    mscode_bytes = chain.web3.toBytes(hexstr=mscode).ljust(96, b'\0')

    nrecipients_bytes = chain.web3.toBytes(len(to)).rjust(32, b'\0')

    # `to` is already in hex-string, but 20-bytes, not 32-bytes each
    to_hexstr = [chain.web3.toHex(
        chain.web3.toBytes(hexstr=val).rjust(32, b'\0')
    ) for val in to]
    # `amt` is in `int`s
    amt_hexstr = [chain.web3.toHex(
        chain.web3.toBytes(val).rjust(32, b'\0')
    ) for val in amt]

    # interleave `to` and `amt`, converting to `bytes` in the process
    msdata_bytes = b''.join([chain.web3.toBytes(hexstr=val)
                             for pair in zip(to_hexstr, amt_hexstr) for val in pair])

    txdata_bytes = mscode_bytes + nrecipients_bytes + msdata_bytes
    txdata = chain.web3.toHex(txdata_bytes)

    pp(txdata)

    # sloppy data chunk alignment check
    assert len(mscode_bytes) == 96
    assert len(nrecipients_bytes) == 32
    assert len(txdata_bytes) % 32 == 0

    # seed balances so we don't pay for account creation (skews gas use benchmark)
    # TODO: use own multisend! much faster to test than making `nrecipients` blocks
    give_balances(chain, to)

    # build/send tx
    txhash = chain.web3.eth.sendTransaction({
        'from': chain.web3.eth.coinbase,
        'to': '', # sic!
        'data': txdata,
        'value': sum(amt),
        # FIXME: magicnum 3000
        # magicnum 50000: to work around Populllus thinking empty-`to` equates CREATE call
        'gas': 50000 + 30000 * len(to),
        })
    txreceipt = chain.wait.for_receipt(txhash)

    # pretty when run as `pytest --capture=no <path/to/file>`
    print('')
    print('Gas limit:          ', chain.web3.eth.getTransaction(txhash)['gas'])
    print('Gas used (total):   ', txreceipt['gasUsed'])
    print('Gas used (avg/xfer):', txreceipt['gasUsed']/len(to))

    #assert chain.web3.eth.getBalance(to[0]) >= amt[0]
    assert chain.web3.eth.getBalance(to[1]) >= amt[1]
    #assert chain.web3.eth.getBalance(to[-1]) >= amt[-1]

    #assert chain.web3.eth.getBalance('0x'+'00'*20) == 0
