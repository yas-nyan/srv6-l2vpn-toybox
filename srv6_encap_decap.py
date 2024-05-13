from scapy.all import *
from scapy.layers.inet6 import IPv6, IPv6ExtHdrSegmentRouting
from scapy.layers.l2 import Ether
import sys
import threading

my_ip = sys.argv[1]
nei_ip = sys.argv[2]
src_mac = sys.argv[3]
dst_mac = sys.argv[4]

print("my ip-> " + my_ip)
print("nei ip-> " + nei_ip)
print("src mac-> " + src_mac)
print("dst mac-> " + dst_mac)

# 送信先IPアドレスを引数から取得
dst_ip = nei_ip

def encap_packet(packet):
    if packet.haslayer(Ether):
        ethernet_frame = bytes(packet)

        # SRHの追加
        srh = IPv6ExtHdrSegmentRouting(addresses=[dst_ip], nh=143, segleft=0, lastentry=0)

        # 新しいIPv6パケットの作成
        new_packet = IPv6(src=my_ip, dst=nei_ip, nh=43) / srh / Raw(load=ethernet_frame)

        # Ethernetフレームの作成
        ether = Ether(src=src_mac, dst=dst_mac) / new_packet

        # 送信前にパケットを表示
        #ether.show2()

        # エンカプセレートされたパケットの送信
        sendp(ether, iface="net0")  # インターフェースを指定して送信

def decap_packet(packet):
    print("Decapsulation function called")
    if packet.haslayer(IPv6) and packet.haslayer(IPv6ExtHdrSegmentRouting):
        srh = packet[IPv6ExtHdrSegmentRouting]
        if srh.nh == 143:
            # カプセル化されたEthernetフレームを取り出す
            ethernet_frame = packet[Raw].load
            ether_pkt = Ether(ethernet_frame)

            # 送信前にデカプセル化されたパケットを表示
            #ether_pkt.show2()
            
            # デカプセル化されたEthernetフレームを送信
            sendp(ether_pkt, iface="net1")

# スニファーを並列に実行するためのスレッドを作成
thread_encap = threading.Thread(target=sniff, kwargs={'iface': 'net1', 'prn': encap_packet, 'filter': 'inbound'})
thread_decap = threading.Thread(target=sniff, kwargs={'iface': 'net0', 'filter': f'ip6 and dst {my_ip} and inbound', 'prn': decap_packet})

# スレッドを開始
thread_encap.start()
thread_decap.start()

# スレッドの終了を待機
thread_encap.join()
thread_decap.join()

