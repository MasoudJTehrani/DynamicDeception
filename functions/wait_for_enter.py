def wait_for_enter(stop_event):
    import sys, select
    print("--------Press Enter at any time to abort the scenario early--------")
    # loop until either input is received or stop_event is set
    while not stop_event.is_set():
        # wait up to 0.1s for stdin to be readable
        try:
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        except Exception:
            # If select fails (platforms without stdin FD), fall back to blocking input once
            try:
                sys.stdin.readline()
                stop_event.set()
            except Exception:
                pass
            break
        if rlist:
            _ = sys.stdin.readline()
            stop_event.set()
            break