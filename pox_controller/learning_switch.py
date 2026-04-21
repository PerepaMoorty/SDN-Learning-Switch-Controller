from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

# Dictionary: {dpid: {mac: port}}
mac_to_port = {}


def _handle_PacketIn(event):
    packet = event.parsed
    dpid = event.connection.dpid
    in_port = event.port

    if dpid not in mac_to_port:
        mac_to_port[dpid] = {}

    # Learn source MAC
    mac_to_port[dpid][packet.src] = in_port

    log.info(f"Learned MAC {packet.src} on port {in_port}")

    # If destination known → install flow
    if packet.dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][packet.dst]

        # Install flow rule
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, in_port)
        msg.actions.append(of.ofp_action_output(port=out_port))
        msg.idle_timeout = 10
        msg.hard_timeout = 30

        event.connection.send(msg)

        # Send packet out
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=out_port))
        msg.in_port = in_port
        event.connection.send(msg)

        log.info(f"Installed flow: {packet.src} → {packet.dst} via port {out_port}")

    else:
        # Flood if unknown
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        msg.in_port = in_port
        event.connection.send(msg)

        log.info(f"Flooding packet from {packet.src} to {packet.dst}")


def launch():
    def start_switch(event):
        log.info(f"Switch {event.dpid} connected")
        event.connection.addListeners(globals())

    core.openflow.addListenerByName("ConnectionUp", start_switch)