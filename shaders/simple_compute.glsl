#version 430

layout(local_size_x = 16, local_size_y = 16) in; // Work group size

layout(std430, binding = 0) buffer DataBuffer {
    float data[];
};

void main() {
    uint index = gl_GlobalInvocationID.x;
    if (index < 1024) {
        data[index] = float(index) * 2.0; // Simple computation
    }
}