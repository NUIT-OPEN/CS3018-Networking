import math


def dec_to_bin(s):
    return ''.join([bin(int(i))[2:].zfill(8) for i in s.split('.')])


def bin_to_dec(s):
    return '%d.%d.%d.%d' % (
        eval('0b' + s[:8]),
        eval('0b' + s[8:16]),
        eval('0b' + s[16:24]),
        eval('0b' + s[24:32])
    )


i_network = input('请输入网段：')
i_split_num = int(input('请输入划分网络数（2的倍数）：'))

network, prefix = i_network.strip().split('/')
network = dec_to_bin(network)
prefix = int(prefix)

subnet_prefix_distance = math.ceil(math.log2(i_split_num))
subnet_prefix = prefix + subnet_prefix_distance

for i in range(i_split_num):
    subnet = bin(eval('0b' + network[:subnet_prefix]) + i)[2:]
    subnet = subnet + ('0' * (32 - len(subnet)))

    print(subnet, end=' 即：')
    print('%s/%d' % (
        bin_to_dec(subnet),
        subnet_prefix
    ))
