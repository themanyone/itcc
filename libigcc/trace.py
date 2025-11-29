import trace

def trace_func(frame, event, arg):
    if event == 'line':
        print(f"line {frame.f_lineno}: {frame.f_code.co_filename}")
    return trace_func

tracer = trace.Trace(trace=0, count=0)
tracer.run('../irust', trace_func)

results = tracer.results()
results.write_results(summary=True, coverdir='.')
