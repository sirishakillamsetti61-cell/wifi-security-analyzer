# Wi-Fi Security Analyzer

A Python tool for auditing the security and health of your own Wi-Fi network:
encryption strength, unknown devices, latency/performance, and an overall risk score.

Only run this against networks you own or have explicit permission to test.

## Status: Phase 1 - Basic Scanner

Currently implemented:
- Local IP detection
- Default gateway detection
- Subnet calculation
- Device discovery (reads your OS existing ARP cache, no special privileges required)

## Setup

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

## Run

python main.py

## Roadmap

- [x] Phase 1 - Basic scanner (IP / gateway / subnet / devices)
- [ ] Phase 2 - Security configuration analyzer (encryption, WPS)
- [ ] Phase 3 - Performance analyzer (latency, packet loss)
- [ ] Phase 4 - Packet analyzer (Scapy protocol stats)
- [ ] Phase 5 - Risk scoring engine
- [ ] Phase 6 - Dashboard (Tkinter/Flask)
