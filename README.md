asn-memo is a simple flash card application written in Python (using the Textual framework) to aid in memorization of important networks and their ASN numbers.

Written by Opus 4.5 with Claude Code.

  Project Structure

```
  asn-memo/
  ├── main.py              # Entry point
  ├── app.py               # TUI screens (MainMenu, Study, Browse, Statistics)
  ├── data.py              # 60 networks with AS numbers and facts
  ├── spaced_repetition.py # SM-2 algorithm for intelligent scheduling
  ├── progress.py          # JSON persistence (~/.asn-memo/progress.json)
  ├── asn_memo.tcss        # Textual CSS styling
  ├── requirements.txt     # textual>=0.47.0
  └── .venv/               # Virtual environment (already set up)
```

  Networks Included (60 total)

  - Tier 1: Lumen, Cogent, NTT, Arelion, GTT, Sparkle, TATA, Verizon, AT&T, PCCW, Orange, Liberty Global, Sprint, Telefonica
  - Tier 2: Hurricane Electric, Comcast, China Telecom/Unicom, RETN, Deutsche Telekom, KDDI, Korea Telecom, Bharti Airtel
  - Tier 3: Charter, Cox, Frontier, Verizon FiOS, Starlink
  - CDNs: Cloudflare, Akamai, Fastly, Netflix, Twitch
  - Cloud: AWS, Google, Azure, Alibaba, Meta, Apple, DigitalOcean, Linode, Vultr
  - IXPs: DE-CIX, AMS-IX, LINX, Netnod

  Running the App

  ```
  cd /home/admin/Projects/asn-memo
  source .venv/bin/activate
  python main.py
  ```

  Keyboard Controls

  - S: Start study session
  - B: Browse all networks by tier
  - T: View statistics
  - Space: Reveal answer (in study mode)
  - 1-4: Rate difficulty (Again/Hard/Good/Easy)
  - Escape: Go back
  - Q: Quit
