import glfw
from OpenGL import GL


from Shader import Shader, ShaderSources

def init_window(width, height, title):
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
    sources.compute_source = '''#version 460
void main(){
    vec4 pos = vec4(0.2);
}
    '''
    shader = Shader(sources=sources)
    return window

def render_loop(window):
    while not glfw.window_should_close(window):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glClearColor(0.1, 0.2, 0.3, 1.0)  # Dark blueish background

        glfw.swap_buffers(window)
        glfw.poll_events()

def main():
    window = init_window(800, 600, "OpenGL Compute Shader Example")
    render_loop(window)
    glfw.terminate()

if __name__ == "__main__":
    main()
