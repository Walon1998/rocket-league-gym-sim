"""
A basic library for useful mathematical operations.
"""

import numpy as np
from numba import jit


@jit(nopython=True, nogil=True, cache=True, parallel=False, fastmath=True)
def get_dist(x, y):
    return np.subtract(x, y)


@jit(nopython=True, nogil=True, cache=True, parallel=False, fastmath=True)
def vector_projection(vec, dest_vec, mag_squared=None):
    if mag_squared is None:
        norm = vecmag(dest_vec)
        if norm == 0:
            return dest_vec
        mag_squared = norm * norm

    if mag_squared == 0:
        return dest_vec

    dot = np.dot(vec, dest_vec)
    projection = np.multiply(np.divide(dot, mag_squared), dest_vec)
    return projection


@jit(nopython=True, nogil=True, cache=True, parallel=False, fastmath=True)
def scalar_projection(vec, dest_vec):
    norm = vecmag(dest_vec)

    if norm == 0:
        return 0

    dot = np.dot(vec, dest_vec) / norm
    return dot


@jit(nopython=True, nogil=True, cache=True, parallel=False, fastmath=True)
def vecmean(vecs):
    return np.mean(vecs)

@jit(nopython=True, nogil=True, cache=True, parallel=False, fastmath=True)
def vecdot(a, b):
    return np.dot(a, b)

@jit(nopython=True, nogil=True, cache=True, parallel=False, fastmath=True)
def squared_vecmag(vec):
    x = np.linalg.norm(vec)
    return x * x


@jit(nopython=True, nogil=True, cache=True, parallel=False, fastmath=True)
def vecmag(vec):
    norm = np.linalg.norm(vec)
    return norm


@jit(nopython=True, nogil=True, cache=True, parallel=False, fastmath=True)
def unitvec(vec):
    return np.divide(vec, vecmag(vec))


@jit(nopython=True, nogil=True, cache=True, parallel=False, fastmath=True)
def cosine_similarity(a, b):
    return np.dot(a / np.linalg.norm(a), b / np.linalg.norm(b))


@jit(nopython=True, nogil=True, cache=True, parallel=False, fastmath=True)
def quat_to_euler(quat):
    w, x, y, z = quat
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    sinp = 2 * (w * y - z * x)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)

    roll = np.arctan2(sinr_cosp, cosr_cosp)
    if abs(sinp) > 1:
        pitch = np.pi / 2
    else:
        pitch = np.arcsin(sinp)
    yaw = np.arctan2(siny_cosp, cosy_cosp)

    return np.array([-pitch, yaw, -roll])


# From RLUtilities
@jit(nopython=True, nogil=True, cache=True, parallel=False, fastmath=True)
def quat_to_rot_mtx(quat: np.ndarray) -> np.ndarray:
    w = -quat[0]
    x = -quat[1]
    y = -quat[2]
    z = -quat[3]

    theta = np.zeros((3, 3))

    norm = np.dot(quat, quat)
    if norm != 0:
        s = 1.0 / norm

        # front direction
        theta[0, 0] = 1.0 - 2.0 * s * (y * y + z * z)
        theta[1, 0] = 2.0 * s * (x * y + z * w)
        theta[2, 0] = 2.0 * s * (x * z - y * w)

        # left direction
        theta[0, 1] = 2.0 * s * (x * y - z * w)
        theta[1, 1] = 1.0 - 2.0 * s * (x * x + z * z)
        theta[2, 1] = 2.0 * s * (y * z + x * w)

        # up direction
        theta[0, 2] = 2.0 * s * (x * z + y * w)
        theta[1, 2] = 2.0 * s * (y * z - x * w)
        theta[2, 2] = 1.0 - 2.0 * s * (x * x + y * y)

    return theta


@jit(nopython=True, nogil=True, cache=True, parallel=False, fastmath=True)
def rotation_to_quaternion(m: np.ndarray) -> np.ndarray:
    trace = np.trace(m)
    q = np.zeros(4)

    if trace > 0:
        s = (trace + 1) ** 0.5
        q[0] = s * 0.5
        s = 0.5 / s
        q[1] = (m[2, 1] - m[1, 2]) * s
        q[2] = (m[0, 2] - m[2, 0]) * s
        q[3] = (m[1, 0] - m[0, 1]) * s
    else:
        if m[0, 0] >= m[1, 1] and m[0, 0] >= m[2, 2]:
            s = (1 + m[0, 0] - m[1, 1] - m[2, 2]) ** 0.5
            inv_s = 0.5 / s
            q[1] = 0.5 * s
            q[2] = (m[1, 0] + m[0, 1]) * inv_s
            q[3] = (m[2, 0] + m[0, 2]) * inv_s
            q[0] = (m[2, 1] - m[1, 2]) * inv_s
        elif m[1, 1] > m[2, 2]:
            s = (1 + m[1, 1] - m[0, 0] - m[2, 2]) ** 0.5
            inv_s = 0.5 / s
            q[1] = (m[0, 1] + m[1, 0]) * inv_s
            q[2] = 0.5 * s
            q[3] = (m[1, 2] + m[2, 1]) * inv_s
            q[0] = (m[0, 2] - m[2, 0]) * inv_s
        else:
            s = (1 + m[2, 2] - m[0, 0] - m[1, 1]) ** 0.5
            inv_s = 0.5 / s
            q[1] = (m[0, 2] + m[2, 0]) * inv_s
            q[2] = (m[1, 2] + m[2, 1]) * inv_s
            q[3] = 0.5 * s
            q[0] = (m[1, 0] - m[0, 1]) * inv_s
    return -q


@jit(nopython=True, nogil=True, cache=True, parallel=False, fastmath=True)
def other_rot_to_quat(a):
    q = [0,0,0,0]
    trace = a[0][0] + a[1][1] + a[2][2]
    if trace > 0:
        s = 0.5 / np.sqrt(trace+ 1.0)
        q[0] = 0.25 / s
        q[1] = ( a[2][1] - a[1][2] ) * s
        q[2] = ( a[0][2] - a[2][0] ) * s
        q[3] = ( a[1][0] - a[0][1] ) * s
    else: 
        if a[0][0] > a[1][1] and a[0][0] > a[2][2]:
            s = 2.0 * np.sqrt( 1.0 + a[0][0] - a[1][1] - a[2][2])
            q[0] = (a[2][1] - a[1][2] ) / s
            q[1] = 0.25 * s
            q[2] = (a[0][1] + a[1][0] ) / s
            q[3] = (a[0][2] + a[2][0] ) / s
        elif a[1][1] > a[2][2]:
            s = 2.0 * np.sqrt( 1.0 + a[1][1] - a[0][0] - a[2][2])
            q[0] = (a[0][2] - a[2][0] ) / s
            q[1] = (a[0][1] + a[1][0] ) / s
            q[2] = 0.25 * s
            q[3] = (a[1][2] + a[2][1] ) / s
        else:
            s = 2.0 * np.sqrt( 1.0 + a[2][2] - a[0][0] - a[1][1] )
            q[0] = (a[1][0] - a[0][1] ) / s
            q[1] = (a[0][2] + a[2][0] ) / s
            q[2] = (a[1][2] + a[2][1] ) / s
            q[3] = 0.25 * s

    return q


@jit(nopython=True, nogil=True, cache=True, parallel=False, fastmath=True)
def euler_to_rotation(pyr):
    cp, cy, cr = np.cos(pyr)
    sp, sy, sr = np.sin(pyr)

    theta = np.zeros((3, 3))

    # front
    theta[0, 0] = cp * cy
    theta[1, 0] = cp * sy
    theta[2, 0] = sp

    # left
    theta[0, 1] = cy * sp * sr - cr * sy
    theta[1, 1] = sy * sp * sr + cr * cy
    theta[2, 1] = -cp * sr

    # up
    theta[0, 2] = -cr * cy * sp - sr * sy
    theta[1, 2] = -cr * sy * sp + sr * cy
    theta[2, 2] = cp * cr

    return theta


@jit(nopython=True, nogil=True, cache=True, parallel=False, fastmath=True)
def rand_uvec3(rng: np.random.Generator = np.random):
    vec = rng.random(3) - 0.5
    return vec / np.linalg.norm(vec)


@jit(nopython=True, nogil=True, cache=True, parallel=False, fastmath=True)
def rand_vec3(max_norm, rng: np.random.Generator = np.random):
    return rand_uvec3(rng) * (rng.random() * max_norm)
