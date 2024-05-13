from scapy.all import *
from scapy.layers.inet6 import IPv6, IPv6ExtHdrSegmentRouting

def send_srh_packet():
    # 送信元と宛先のIPv6アドレスを設定
    src_ip = "2001:db8::1"
    dst_ip = "2001:db8::2"

    # Segment Routing Header (SRH) の設定
    srh = IPv6ExtHdrSegmentRouting(addresses=["2001:db8::5", "2001:db8::6"])

    # IPv6 パケットの作成
    packet = IPv6(src=src_ip, dst=dst_ip) / srh / ICMPv6EchoRequest()
    print(packet)

    # パケットを送信する
    send(packet)

# スクリプトを実行する
send_srh_packet()

