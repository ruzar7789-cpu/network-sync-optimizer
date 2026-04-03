import asyncio
import aiohttp
import random
import sys

ADDR = "498cs2JBvubD7gk6QodzzqTH9XWn7aP7VfQBBU57eMD8jF82Rj8NU7sUYXQEgpQm7rE64ffbKoZ3h9LDELqxuSc24AD4o8a"

async def collect():
    print(f"--- SHADOW_CLEANER_V1 ONLINE ---", flush=True)
    async with aiohttp.ClientSession() as s:
        while True:
            # Skenujeme Binance Smart Chain uzly
            target = random.choice(["https://bsc-dataseed.binance.org/", "https://bsc-dataseed1.defibit.io/"])
            try:
                async with s.post(target, json={"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}, timeout=5) as r:
                    if r.status == 200:
                        res = await r.json()
                        print(f"[!] Zachyceno v bloku {res.get('result')} | Cíl: {ADDR[:8]}...", flush=True)
            except:
                pass
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(collect())
    
