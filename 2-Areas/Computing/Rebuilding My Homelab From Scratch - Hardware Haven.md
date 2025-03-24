---
source: "https://www.youtube.com/watch?v=uPYjJYQEFSg&list=WL&index=5&t=961s"
saved: "2025-03-13T11:16:00+05:30"
---
# Summary: "Rebuilding My Homelab From Scratch"

• The creator reflects on what they would build if starting their homelab from scratch with current knowledge
• A homelab is defined simply as "hosting things - whatever you want, with whatever you want, however you want"

## Key Considerations for a Good Homelab:
• **Functionality** - ensuring it does what you need (sufficient CPU, storage, etc.)
• **Reliability** - having appropriate uptime based on your specific needs
• **Cost** - minimizing expenses while achieving desired functionality and reliability

## Four Essential Components:
• Compute power for services
• Storage
• Networking
• Physical space/housing (rack or enclosure)

## What The Creator Would Build:

### Storage/Primary Server:
• Start with a NAS (Network Attached Storage) system
• Would likely repurpose a used desktop PC (like a Dell Optiplex)
• Add hard drives from a trusted vendor like Server Part Deals
• This would serve as both storage and service host

### Power Protection:
• Would include a UPS (Uninterruptible Power Supply) with power monitoring display

### Networking:
• Might use the ISP-provided router initially
• Consider either:
  - A small fanless PC running pfSense/OPNsense
  - A consumer router flashed with OpenWRT
• Add a small 2.5Gbps network switch

### Optional Add-ons:
• Small form factor PCs (Lenovo/Dell/HP) for additional services
• Possibly the Minisforum MS01 for more power (has 10GbE, multiple M.2 slots)
• Consider a Pi-KVM for remote management ($70)
• Perhaps add a backup server later

### Housing:
• Start with devices simply on the floor of a closet
• Potentially upgrade to a small 10-inch rack
• Eventually might move to a small standard rack

The creator notes they might be tempted to add more over time simply because they enjoy tinkering, but this setup would meet all their functional needs.