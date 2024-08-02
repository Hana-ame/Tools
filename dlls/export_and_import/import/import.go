package main

import (
	"fmt"
	"math"
	"syscall"
	"unsafe"
)

const DLL_PATH = "../export/example.dll"

func main() {
	// Load the DLL
	dll, err := syscall.LoadDLL(DLL_PATH)
	if err != nil {
		panic(err)
	}
	defer dll.Release()

	// Find the Add procedure
	addProc, err := dll.FindProc("Add")
	if err != nil {
		panic(err)
	}

	// Call the Add function
	a, b := 5, 3
	ret, _, err := addProc.Call(uintptr(a), uintptr(b))
	if err != syscall.Errno(0) {
		fmt.Println("Syscall returned error:", err)
	}

	fmt.Printf("Add function result: %d\n", int(ret))
}

func importSampleFunction() {
	// Load the DLL
	dll, err := syscall.LoadDLL(DLL_PATH)
	if err != nil {
		panic(err)
	}
	defer dll.Release()

	// Find the procedure
	proc, err := dll.FindProc("SampleFunction")
	if err != nil {
		panic(err)
	}

	// Prepare arguments
	intArg := 42
	floatArg := float32(3.14)
	doubleArg := 2.71828
	strArg := "Hello, DLL!"
	boolArg := true

	// Convert string to *byte
	strPtr, err := syscall.BytePtrFromString(strArg)
	if err != nil {
		panic(err)
	}

	fmt.Printf("Calling DLL with: int=%d, float=%f, double=%f, string=%s, bool=%v\n",
		intArg, floatArg, doubleArg, strArg, boolArg)

	// Call the function
	ret, _, err := proc.Call(
		uintptr(intArg),
		uintptr(math.Float32bits(floatArg)),
		uintptr(math.Float64bits(doubleArg)),
		uintptr(unsafe.Pointer(strPtr)),
		uintptr(boolToInt(boolArg)),
	)

	if err != syscall.Errno(0) {
		fmt.Println("Syscall returned error:", err)
	}

	// Print raw return value
	fmt.Printf("Raw return value: %v\n", ret)

	// Convert the result back to float64
	result := math.Float64frombits(uint64(ret))

	fmt.Printf("Result from DLL (as float64): %f\n", result)
}

func boolToInt(b bool) int {
	if b {
		return 1
	}
	return 0
}
