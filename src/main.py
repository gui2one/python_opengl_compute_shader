import glfw
import os
from OpenGL import GL
from Shader import Shader, ShaderSources
import imgui
from imgui.integrations.glfw import GlfwRenderer

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
SHADERS_DIR = os.path.join(ROOT_DIR, "shaders")
shader: Shader = None
IMGUI_IMPL = None
ssbo = None
buffer_size = None
def init_imgui():
    # initilize imgui context (see documentation)
    imgui.create_context()

    # imgui.get_io().display_size = 500, 500
    # imgui.get_io().fonts.get_tex_data_as_rgba32()


def imgui_start_frame():
    imgui.new_frame()


def imgui_end_frame():
    # pass all drawing comands to the rendering pipeline
    # and close frame context
    imgui.render()
    imgui.end_frame()


def load_shader_source(path: str):
    with open(path, "r") as f:
        return f.read()


def init_window(width, height, title):
    global shader
    global ssbo
    global buffer_size
    if not glfw.init():
        raise Exception("Failed to initialize GLFW")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 6)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)  # Modern OpenGL
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)  # Forward compatibility

    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        raise Exception("Failed to create GLFW window")

    glfw.make_context_current(window)

    print(f"OpenGL Version: {GL.glGetString(GL.GL_VERSION).decode('utf-8')}")

    sources = ShaderSources()
    sources.compute_source = load_shader_source(f"{SHADERS_DIR}/simple_compute.glsl")
    shader = Shader(sources=sources)
    
    buffer_size = 1024 * 4  # 1024 floats * 4 bytes
    ssbo = create_ssbo(buffer_size)

    return window


def render_loop(window):
    global buffer_size
    glfw.swap_interval(1)
    while not glfw.window_should_close(window):
        glfw.wait_events()
        IMGUI_IMPL.process_inputs()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glClearColor(0.1, 0.2, 0.3, 1.0)  # Dark blueish background

        imgui_start_frame()
        imgui.begin("First window", True)
        imgui.text("hello")
        imgui.end()
        imgui_end_frame()

        IMGUI_IMPL.render(imgui.get_draw_data())
        
        shader.use()
        GL.glDispatchCompute(64, 1, 1)  # 64 groups of 16 threads (1024 threads total)
        GL.glMemoryBarrier(GL.GL_SHADER_STORAGE_BARRIER_BIT)
        result = read_ssbo(ssbo, buffer_size)
        print("SSBO Data (first 10):", result[:10])     
        glfw.swap_buffers(window)
        
        # break # just once for testing 


def create_ssbo(size):
    ssbo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_SHADER_STORAGE_BUFFER, ssbo)
    GL.glBufferData(GL.GL_SHADER_STORAGE_BUFFER, size, None, GL.GL_DYNAMIC_DRAW)
    GL.glBindBufferBase(GL.GL_SHADER_STORAGE_BUFFER, 0, ssbo)
    GL.glBindBuffer(GL.GL_SHADER_STORAGE_BUFFER, 0)
    print(f"SSBO Created with {size} bytes")
    
    
    return ssbo

def read_ssbo(ssbo, size):
    GL.glBindBuffer(GL.GL_SHADER_STORAGE_BUFFER, ssbo)
    # ptr = GL.glMapBuffer(GL.GL_SHADER_STORAGE_BUFFER, GL.GL_READ_ONLY)
    data = bytearray(GL.glGetBufferSubData(GL.GL_SHADER_STORAGE_BUFFER, 0, size))
    # GL.glUnmapBuffer(GL.GL_SHADER_STORAGE_BUFFER)
    GL.glBindBuffer(GL.GL_SHADER_STORAGE_BUFFER, 0)

    floats = [float.fromhex(data[i:i+4].hex()) for i in range(0, len(data), 4)]
    return floats


def main():
    global IMGUI_IMPL
    window = init_window(800, 600, "OpenGL Compute Shader Example")
    init_imgui()
    IMGUI_IMPL = GlfwRenderer(window)
    render_loop(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
