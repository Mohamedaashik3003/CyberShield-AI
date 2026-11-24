
import time

def monitor_events(event_stream, analysis_function):
    for i, event in enumerate(event_stream, 1):
        print("\\n" + "=" * 45)
        print(f"CYBERSHIELD AI - EVENT {i}")
        print("=" * 45)

        result = analysis_function(
            event["event"],
            event["features"]
        )

        for key, value in result.items():
            print(f"\\n{key}:")
            print(value)

        time.sleep(1)
