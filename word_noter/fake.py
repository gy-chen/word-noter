"""Generate some fake data for testing

Features:
  - Coroutine for generating fake words with specific delay

"""
import asyncio
import faker

fake_words = asyncio.Queue()


async def generate_words(out_queue=fake_words, delay=5):
    """Keep generating fake word to out queue

    :param out_queue: the async queue to put words in
    :param delay: delay in seconds between every words
    :return:
    """
    fake = faker.Faker()
    while True:
        await out_queue.put(fake.word())
        await asyncio.sleep(delay)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()


    async def main():
        while True:
            word = await fake_words.get()
            print(word)


    loop.run_until_complete(asyncio.gather(main(), generate_words()))
