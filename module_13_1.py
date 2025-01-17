import asyncio

async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')
    for i in range(1,6):
        await asyncio.sleep(1/power)
        if i == 2:
            print(f'Силач {name} поднял {i}-ой шар')
        elif i == 3:
            print(f'Силач {name} поднял {i}-ий шар')
        else:
            print(f'Силач {name} поднял {i}-ый шар')
    print(f'Силач {name} закончил соревнования.')

async def start_tournament():
    task_1 = asyncio.create_task(start_strongman('Валерий', 7))
    task_2 = asyncio.create_task(start_strongman('Дмитрий', 10))
    task_3 = asyncio.create_task(start_strongman('Роман', 3))

    await task_1
    await task_2
    await task_3
asyncio.run(start_tournament())