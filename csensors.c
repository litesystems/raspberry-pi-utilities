#include <Python.h>

static PyObject *
craspiutil_dht11_get_data(PyObject *self, PyObject *args)
{
    int pin;

    if (!PyArg_ParseTuple(args, "i", &pin)) {
        return NULL;
    }

    return Py_BuildValue("i", 11);
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
