from adt7410 import ADT7410

if __name__ == '__main__':
    adt = ADT7410(1, 0x48)
    # 13-bit resolution
    adt.resolution = 0
    # Print current temperature
    print("Current temp.: %f" % adt.temperature)
    # 16-bit resolution
    adt.resolution = 1
    # Print current temperature
    print("Current temp.: %f" % adt.temperature)
