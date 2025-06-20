# Binance Futures Testnet Trading Bot  
*(One‑file submission: code + docs)*

A Python command‑line bot that places **Market, Limit, and Stop‑Limit** orders on the **Binance Futures Testnet (USDT‑M)**.  
It uses the official Binance API (`python‑binance`), validates symbols, syncs timestamps, and logs every request to `trading_bot.log`.

---

## 🚀 Features
- Place **BUY / SELL** orders
- Order types: **MARKET**, **LIMIT**, **STOP‑LIMIT**
- Works only on the **Binance Futures Testnet**
- Graceful error handling & detailed logging
- Symbol validation to prevent typos (e.g., `BTCUSTD`)
- Automatic timestamp sync to avoid `‑1021` errors

---

## 🛠 Requirements
| Item | Version |
|------|---------|
| Python | 3.7 or higher |
| Library | `python‑binance` (`pip install python-binance`) |
| Keys   | Binance **Futures Testnet** API key/secret (Futures + Trade enabled) |

---

## 📦 Installation

```bash
# 1) Clone / download this repo (or just this README)
# 2) Install dependency
pip install python-binance
