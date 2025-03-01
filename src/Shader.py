from OpenGL import GL

class ShaderSources :
    def __init__(self, vetex_source : str = None, fragment_source : str = None, geometry_source : str = None, compute_source : str = None):
        self.vertex_source = vetex_source
        self.fragment_source = fragment_source
        self.geometry_source = geometry_source
        self.compute_source = compute_source

class Shader:
    def __init__(self, sources : ShaderSources):
        if sources.compute_source != None :
            self.program = GL.glCreateProgram()
            
            shader = GL.glCreateShader(GL.GL_COMPUTE_SHADER)
            
            GL.glShaderSource(shader,  sources.compute_source)
            GL.glCompileShader(shader)
            
            # Check for compile errors
            result = GL.glGetShaderiv(shader, GL.GL_COMPILE_STATUS)
            if not result:
                error_log = GL.glGetShaderInfoLog(shader)
                print(f"Shader Compilation Failed:\n{error_log.decode('utf-8')}")
                raise Exception("Shader Compilation Error")
            else:
                print("Shader compiled successfully")
                
            GL.glAttachShader(self.program, shader)    
            GL.glLinkProgram(self.program)

            # Check for linking errors
            result = GL.glGetProgramiv(self.program, GL.GL_LINK_STATUS)
            if not result:
                error_log = GL.glGetProgramInfoLog(self.program)
                print(f"Program Linking Failed:\n{error_log.decode('utf-8')}")
                raise Exception("Shader Program Linking Error")
            else:
                print("Program linked successfully")

            GL.glDeleteShader(shader)        
        else :
            print("got other shader type ...")
            
    def use(self):
        GL.glUseProgram(self.program)