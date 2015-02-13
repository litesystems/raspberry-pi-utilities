#include <Python.h>
#include <wiringPi.h>

static int _read_dht11(int pin) {
    int value[5] = {0, 0, 0, 0, 0};
    int state = HIGH;
    int i;
    int num_bits = 0;
    int counter=0;

    if (wiringPiSetup() == -1) {
        return 1;
    }

    // Initialize DHT11
    pinMode(pin, INPUT);
    delay(100);

    // Set low to start
    pinMode(pin, OUTPUT);
    digitalWrite(pin, LOW);
    delay(18);
    pinMode(pin, INPUT);
    delayMicroseconds(60);

    // Wait response signal
    if (digitalRead(pin) == HIGH) {
        return -10;
    }
    delayMicroseconds(80);
    if (digitalRead(pin) == LOW) {
        return -11;
    }

    // Wait to start
    while (digitalRead(pin) == HIGH);

    // Read data
    for (i = 0; i < 40 * 2 + 1; i++) {
        counter = 0;
        while (digitalRead(pin) == state) {
            counter++;
            delayMicroseconds(1);
            if (counter == 255) {
                return -12;
            }
        }
        state = digitalRead(pin);
        if ((i >= 2) && (i % 2 == 0)){
            if (counter > 16) {
                value[num_bits / 8] |= (1 << (7 - (num_bits % 8)));
            }
            num_bits++;
        }
    }

    // Check number of bits & parity bits
    if (num_bits < 40) {
        return -1;
    } else if (value[4] != ((value[0] + value[1] + value[2] + value[3]) & 0xff)) {
        return -2;
    }

    return (value[0] << 24) + (value[1] << 16) + (value[2] << 8) + value[3];
}

static PyObject *
craspiutil_dht11_get_data(PyObject *self, PyObject *args)
{
    int pin;

    if (!PyArg_ParseTuple(args, "i", &pin)) {
        return NULL;
    }

    return Py_BuildValue("i", _read_dht11(pin));
}

static PyMethodDef CRaspiUtilMethods[] = {
    {"dht11_get_data", craspiutil_dht11_get_data, METH_VARARGS,
     "Get data from DHT11"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initcraspiutil(void){
    (void) Py_InitModule("craspiutil", CRaspiUtilMethods);
}
