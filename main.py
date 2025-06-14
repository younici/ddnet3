import asyncio
import Telegram.bot as tg
import Discord.bot as dc
import db.upd_data_base as upd
import db.data_base as db

async def delayed_upd():
    await asyncio.sleep(5)
    await upd.update_db()

async def main():
    await db.main()
    tg_task = asyncio.create_task(tg.main())
    dc_task = asyncio.create_task(dc.main())
    upd_task = asyncio.create_task(delayed_upd())
    await asyncio.gather(tg_task, upd_task, dc_task)

if __name__ == "__main__":
    asyncio.run(main())
