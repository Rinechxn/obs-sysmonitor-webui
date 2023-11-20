from flask import Flask, render_template
import psutil
import humanize
import time
import cpuinfo

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/system_info')
def system_info():
    cpu_info = get_cpu_info()
    cpu_usage = get_cpu_usage()
    memory_info = get_memory_info()
    gpu_info = get_gpu_info()

    return {
        'cpu_info': cpu_info,
        'cpu_usage': cpu_usage,
        'memory_info': memory_info,
        'gpu_info': gpu_info
    }

def get_cpu_info():
    return f"CPU: {cpuinfo.get_cpu_info()['brand_raw']} {psutil.cpu_count(logical=False)} Core {psutil.cpu_count(logical=True)} Threads)"

def get_cpu_usage():
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    return {f"Core {i+1}": f"{usage}%" for i, usage in enumerate(cpu_percent)}

def get_memory_info():
    mem_info = psutil.virtual_memory()
    total_gb = humanize.naturalsize(mem_info.total, binary=True)
    available_gb = humanize.naturalsize(mem_info.available, binary=True)
    used_gb = humanize.naturalsize(mem_info.used, binary=True)
    return f"RAM: {total_gb} / {available_gb} Free", f"USED: {used_gb} ({mem_info.percent}%)"

def get_gpu_info():
    try:
        import GPUtil
        gpu = GPUtil.getGPUs()[0]
        total_vram_gb = humanize.naturalsize(gpu.memoryTotal * 1024 * 1024, binary=True)
        used_vram_gb = humanize.naturalsize(gpu.memoryUsed * 1024 * 1024, binary=True)
        return f"GPU: {gpu.name} {total_vram_gb}", f"USED: {used_vram_gb} ({gpu.load * 100}%)", f"VRAM USED: {used_vram_gb} / {total_vram_gb}"
    except ImportError:
        return "GPU: No GPU information available", "", ""

if __name__ == '__main__':
    app.run(debug=True, port=1688)
