import threading
import time


N = 10 ** 9
N_THREADS = 10
N_JOBS = N // N_THREADS


def counter(a, b):
    print(f"name={threading.current_thread().name} {a=}, {b=} -- started")
    while a < b:
        a += 1
    print(f"name={threading.current_thread().name} -- finished")


def run():
    threads = [
        threading.Thread(
            target=counter,
            args=(i * N_JOBS, (i + 1) * N_JOBS),
            name=f"th_counter_{i}"
        )
        for i in range(N_THREADS)
    ]

    for th in threads:
        th.start()

    for th in threads:
        th.join()


if __name__ == "__main__":
    t1 = time.time()
    run()
    t2 = time.time()
    print(f"time={t2 - t1}")
