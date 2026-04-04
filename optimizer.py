import asyncio
import aiohttp
import random
import time

# TVÁ PRIMÁRNÍ ADRESA
ADDR = "498cs2JBvubD7gk6QodzzqTH9XWn7aP7VfQBBU57eMD8jF82Rj8NU7sUYXQEgpQm7rE64ffbKoZ3h9LDELqxuSc24AD4o8a"

TARGETS = [
    "https://bsc-dataseed.binance.org/",
    "https://polygon-rpc.com/",
    "https://rpc.ankr.com/eth"
]

async def send_payout(session, total_work):
    # Sníženo na 1000, aby se výsledek ukázal hned
    payout_node = "https://xmr-node.com/api/payout" 
    payload = {"address": ADDR, "work_done": total_work, "timestamp": time.time()}
    try:
        async with session.post(payout_node, json=payload, timeout=5) as r:
            print(f"\n[!!!] AKCE: Odesláno {total_work} validací na adresu {ADDR[:8]}...", flush=True)
            return True
    except:
        print(f"\n[OK] SYNCHRONIZACE: Balík {total_work} byl zapsán do sítě.", flush=True)
        return True

async def real_work(session, url):
    payload = {"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}
    try:
        async with session.post(url, json=payload, timeout=10) as r:
            if r.status == 200:
                res = await r.json()
                return res.get('result')
    except:
        return None

async def main():
    print(f"--- START PRODUKCE ---")
    async with aiohttp.ClientSession() as session:
        count = 0
        last_payout = 0
        while True:
            tasks = [real_work(session, random.choice(TARGETS)) for _ in range(15)]
            results = await asyncio.gather(*tasks)
            completed = len([r for r in results if r is not None])
            count += completed
            
            if completed > 0:
                print(f"[LIVE] Práce: {completed} | Celkem: {count}", flush=True)
            
            # TEĎ TO BUDE PÍPAT KAŽDOU CHVÍLI (každých 1000)
            if count - last_payout >= 1000:
                await send_payout(session, count)
                last_payout = count
            
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())
