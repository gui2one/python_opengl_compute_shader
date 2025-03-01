import glfw
import os
from OpenGL import GL
from Shader import Shader, ShaderSources

ROOT_DIR = os.path.dirname(os.path.dirname(__file__)) 
SHADERS_DIR = os.path.join(ROOT_DIR, "shaders")
shader : Shader = None

def load_shader_source(path : str):
    with open(path, "r") as f:
        return f.read()

def init_window(width, height, title):
    global shader
    if not glfw.init():
        raise Exception("Failed to initialize GLFW")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 6)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)  # Modern OpenGL
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)        # Forward compatibility

    window = glfw.create_window(width, height, title, None, None)
    if not window:
        glfw.terminate()
        raise Exception("Failed to create GLFW window")

    glfw.make_context_current(window)

    print(f"OpenGL Version: {GL.glGetString(GL.GL_VERSION).decode('utf-8')}")

    
    sources = ShaderSources()
    sources.compute_source = load_shader_source(f"{SHADERS_DIR}/simple_compute.glsl")
    shader = Shader(sources=sources)
    return window

def render_loop(window):
    while not glfw.window_should_close(window):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glClearColor(0.1, 0.2, 0.3, 1.0)  # Dark blueish background

        # shader.use()
        glfw.swap_buffers(window)
        glfw.poll_events()

def main():
    window = init_window(800, 600, "OpenGL Compute Shader Example")
    render_loop(window)
    glfw.terminate()

if __name__ == "__main__":
    main()
