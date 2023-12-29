// CppPythonTest.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#include "iostream"
#include "import_mat.h"
#include "mat.h"
#include <math.h>
#include <Python.h>
#include<string>
#include<vector>
#include<array>
#include <numpy/arrayobject.h>


# define PI 3.1415926
const int LENGTH_NUM = 10;		// data length_sum
const int Row = 3;				// the .mat file row
const int Col = 10;				// the .mat file column
const int Lane_Nums = 3;		// the numbers of matrix
extern uint16 col, row;
extern mxArray* pMxArray_w, * p1;
mxArray* pMxArray_r = NULL;
using namespace std;


void init_numpy() {
	_import_array();
}


int main()
{	
	/* # impur_test use less
	std::array<float, 10> x = { 2597.1, 2232.0, 2022.6, 1781.0, 1569.4, 1319.0, 1132.0, 946.0, 743.0, 532.3 };
	std::array<float, 10> y = { 696.9, 623.8, 550.8, 477.7, 404.6, 328.8, 255.7, 182.7, 109.6, 36.5 };
	std::array<float, 10> y2 = { 699.7, 696.7, 550.8, 477.7, 404.6, 328.8, 255.7, 182.7, 109.6, 36.5};
	std::array<std::array<float, 10>, 3> input_nums = { x, y, y2 };
	int rows = input_nums.size();
	int columns = x.size();
	float** array1 = (float**)malloc(sizeof(float*) * rows);
	for (int i = 0; i < rows; i++)
	{
		array1[i] = &input_nums[i][0];
	}
	npy_intp Dims[2] = { rows, columns }; // difine the dimension
	Py_Initialize(); //Initialize
	if (!Py_IsInitialized()) {
		std::cout << "python init failed" << std::endl;
		return 1;
	}
	init_numpy();

	PyRun_SimpleString("import sys");
	PyRun_SimpleString("sys.path.append('./../PythonAppTest/')"); // Python Project Path
	PyObject* pModule = PyImport_ImportModule("ZoomTest");
	PyObject* PyArray = PyArray_SimpleNewFromData(2, Dims, NPY_FLOAT, *array1);//delete the array to python
	PyObject* ArgArray = PyTuple_New(1);
	PyTuple_SetItem(ArgArray, 0, PyArray);// define the PyTuple object size as PythonFunction parameter
	// create PyObject object£¬2 representative dimension£¬second is dimension array Dims, third is the array types£¬forth is the input array
	*/
	// create mat file
	double double_nums[LENGTH_NUM * Lane_Nums] = { 0, PI / 2, PI, 1.5 * PI, 2 * PI, 2.5 * PI, 3 * PI, 3.5 * PI, 4 * PI, 4.5 * PI };
	char str[2000] = "x, sin(x), cos(x)"; // get the string matrix, set the init length 2000
	for (int i = 0; i < LENGTH_NUM; i++) {
		double_nums[i + LENGTH_NUM] = sin(double_nums[i]);
		double_nums[i + LENGTH_NUM * 2] = cos(double_nums[i]);
	}

	mat_init(Col, Row); // the mat_init, because the matlab write the column at first, write the rows at second, so make the row and col opposite
	import_data_array(double_nums, str, LENGTH_NUM * 3); // make the data to mat.matrix
	mat_exit();  // close file


	// invoke the py
	Py_Initialize(); //Initialize
	if (!Py_IsInitialized()) {
		std::cout << "python init failed" << std::endl;
		return 1;
	}
	init_numpy();

	PyRun_SimpleString("import sys");
	PyRun_SimpleString("sys.path.append('./../PythonAppTest/')"); // Python Project Path
	
	PyObject* pModule = PyImport_ImportModule("ZoomTest"); // copy the "py" to the PythonAppTest project
	
	if (!pModule)
	{
		std::cout << "Can't find your py file.";
		getchar();
		return -1;
	}
	PyObject* pFunc = PyObject_GetAttrString(pModule, "main"); // create python function object

	// set the arguments
	PyObject* pArg = PyTuple_New(3); // create a new Tuple

	// first argument is the Cell_number, second argument is the x_ticks, third argument is the x_ticks,
	PyTuple_SetItem(pArg, 0, Py_BuildValue("i", 1)); // "i" expand "int", cell numbers
	PyTuple_SetItem(pArg, 1, Py_BuildValue("i", 0)); // x_ticks
	PyTuple_SetItem(pArg, 2, (Py_BuildValue("[i, i]", 1, 2))); // y_ticks


	// Call the function and pass the parameter
	PyObject* py_result = PyObject_CallObject(pFunc, pArg);


	Py_DECREF(pModule);
	Py_DECREF(pFunc);
	Py_DECREF(py_result);
	Py_DECREF(pArg);
	Py_Finalize();
	system("pause");
	return 0;



}
