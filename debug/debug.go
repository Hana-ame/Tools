// by gpt4o mini @ 240801
// https://chatgpt.com/share/943bfc66-0ba6-45aa-b680-9abbfbc02d36

package debug

import (
	"fmt"
	"log"
	"reflect"
	"runtime"
)

func DeepPrint(v any, indent string) {
	rv := reflect.ValueOf(v)

	if !rv.IsValid() {
		fmt.Println(indent + "Invalid")
		return
	}

	// Handle pointers by recursively dereferencing
	for rv.Kind() == reflect.Ptr {
		if rv.IsNil() {
			fmt.Println(indent + "Nil Pointer")
			return
		}
		rv = rv.Elem() // Dereference the pointer
	}

	switch rv.Kind() {
	case reflect.Struct:
		fmt.Println(indent + "Struct:")
		for i := 0; i < rv.NumField(); i++ {
			field := rv.Field(i)
			fieldName := rv.Type().Field(i).Name
			fmt.Printf("%sField %s: ", indent, fieldName)
			DeepPrint(field.Interface(), indent+indent)
		}
	case reflect.Slice:
		fmt.Println(indent + "Slice:")
		for i := 0; i < rv.Len(); i++ {
			fmt.Printf("%sElement %d:\n", indent, i)
			DeepPrint(rv.Index(i).Interface(), indent+indent)
		}
	case reflect.Map:
		fmt.Println(indent + "Map:")
		for _, key := range rv.MapKeys() {
			value := rv.MapIndex(key)
			fmt.Printf("%sKey %v: ", indent, key.Interface())
			DeepPrint(value.Interface(), indent+indent)
		}
	default:
		fmt.Println(rv.Interface())
	}
}

type logLevel int

const (
	Trace = iota
	Debug
	Info
	Warn
	Error
	Fatal
)

var LogLevel logLevel = Warn

func T(tag any, msg ...any) {
	if LogLevel > Trace {
		return
	}
	log.Printf("[%s] TRACE: %s", tag, fmt.Sprint(msg...))
}

func D(tag any, msg ...any) {
	if LogLevel > Debug {
		return
	}
	log.Printf("[%s] DEBUG: %s", tag, fmt.Sprint(msg...))
}

func I(tag any, msg ...any) {
	if LogLevel > Info {
		return
	}
	log.Printf("[%s] INFO: %s", tag, fmt.Sprint(msg...))
}

func W(tag any, msg ...any) {
	if LogLevel > Warn {
		return
	}
	log.Printf("[%s] WARN: %s", tag, fmt.Sprint(msg...))
}

func E(tag any, msg ...any) {
	if LogLevel > Error {
		return
	}
	log.Printf("[%s] ERROR: %s", tag, fmt.Sprint(msg...))
}

func F(tag any, msg ...any) {
	log.Fatalf("[%s] FATAL: %s", tag, fmt.Sprint(msg...))
}

func Print(v ...any) {
	// 获取调用栈信息
	_, file, line, ok := runtime.Caller(1)
	if ok {
		D(fmt.Sprintf("%s:%d", file, line), v...)
	}
}
