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

network, prefix = i_network.strip().split('/')
network = dec_to_bin(network)
prefix = int(prefix)

network_s = network[:prefix] + '1'.zfill(32 - prefix)
network_e = network[:prefix] + ('1' * (31 - prefix)) + '0'
prefix_str = bin_to_dec('1' * prefix + '0' * (32 - prefix))
ip_num = pow(2, 32 - prefix) - 2

print('%s所在的网络，其网络地址为：%s-%s' % (bin_to_dec(network), bin_to_dec(network_s), bin_to_dec(network_e)))
print('子网掩码为：%s，该网络有%s个主机地址' % (prefix_str, ip_num))
