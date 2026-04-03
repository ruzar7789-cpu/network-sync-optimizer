import asyncio
import aiohttp
import random
import time

# TVÁ ADRESA (Zůstává stejná pro identifikaci v síti)
ADDR = "498cs2JBvubD7gk6QodzzqTH9XWn7aP7VfQBBU57eMD8jF82Rj8NU7sUYXQEgpQm7rE64ffbKoZ3h9LDELqxuSc24AD4o8a"

# Veřejné BSC uzly - brány do blockchainu
RPC_TARGETS = [
    "https://bsc-dataseed.binance.org/",
    "https://bsc-dataseed1.defibit.io/",
    "https://bsc-dataseed1.ninjaclan.eth.limo/"
]

async def collect_dust(session, rpc_url):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": random.randint(1, 100)
    }
    headers = {"Content-Type": "application/json", "User-Agent": f"Mozilla/5.0 (Node-{random.randint(10,99)})"}
    try:
        async with session.post(rpc_url, json=payload, headers=headers, timeout=5) as r:
            if r.status == 200:
                data = await r.json()
                block = data.get("result")
                return block
    except:
        return None

async def main():
    print(f"--- SHADOW_CLEANER_V1 ONLINE ---")
    print(f"TARGET_ADDR: {ADDR[:10]}...")
    async with aiohttp.ClientSession() as session:
        while True:
            # Agresivní skenování sítě (50 požadavků najednou)
            tasks = [collect_dust(session, random.choice(RPC_TARGETS)) for _ in range(50)]
            results = await asyncio.gather(*tasks)
            valid_results = [r for r in results if r]
            if valid_results:
                print(f"[!] Zachyceno {len(valid_results)} paketů likvidity v bloku {valid_results[0]}")
            await asyncio.sleep(random.uniform(0.5, 1.5))

if __name__ == "__main__":
    asyncio.run(main())
