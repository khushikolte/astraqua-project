import numpy as np


INPUT_DIM = 32
OUTPUT_DIM = 8


def generate_gps_lost_samples(n=10000):
    X = np.random.rand(n, INPUT_DIM).astype(np.float32)

    # GPS channels fail
    X[:, 0:4] = 0

    y = np.zeros((n, OUTPUT_DIM), dtype=np.float32)

    y[:,0] = 1.0      # GPS Denied
    y[:,1] = 0.90     # Multi Agent
    y[:,2] = 0.30     # Edge AI

    return X,y


def generate_comms_down_samples(n=10000):

    X = np.random.rand(n, INPUT_DIM).astype(np.float32)

    # Communication channels fail
    X[:,4:8] = 0

    y = np.zeros((n, OUTPUT_DIM),dtype=np.float32)

    y[:,1] = 1.0
    y[:,2] = 0.95

    return X,y


def generate_battery_critical_samples(n=10000):

    X = np.random.rand(n, INPUT_DIM).astype(np.float32)

    # Batteries low
    X[:,8:16] = np.random.uniform(0,.15,(n,8))

    y = np.zeros((n,OUTPUT_DIM),dtype=np.float32)

    y[:,3] = 1.0
    y[:,1] = .85

    return X,y


if __name__ == "__main__":

    X,y = generate_gps_lost_samples(5)

    print("Input Shape:",X.shape)
    print("Output Shape:",y.shape)

    print("\nFirst Input\n")
    print(X[0])

    print("\nFirst Label\n")
    print(y[0])