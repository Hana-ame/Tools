// azure-go @ 2023-12-21

package tools

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"strings"

	"github.com/Hana-ame/neo-moonchan/Tools/orderedmap"
)

// this function receive json request.
func ReadJSONFile(fn string) (*orderedmap.OrderedMap, error) {
	jsonFile, err := os.Open(fn)
	if err != nil {
		return nil, err
	}
	o := orderedmap.New()
	err = json.NewDecoder(jsonFile).Decode(&o)
	return o, err
}

func ReaderToJSON(reader io.Reader) (*orderedmap.OrderedMap, error) {
	o := orderedmap.New()
	err := json.NewDecoder(reader).Decode(&o)
	return o, err
}

func StringToJSON(s string) (*orderedmap.OrderedMap, error) {
	return ReaderToJSON(strings.NewReader(s))
}

func BytesToJSON(b []byte) (*orderedmap.OrderedMap, error) {
	return ReaderToJSON(bytes.NewReader(b))
}

func ReadFileToJSON(fn string) (*orderedmap.OrderedMap, error) {
	f, err := os.Open(fn)
	if err != nil {
		return nil, err
	}
	return ReaderToJSON(f)
}

// 将结构体数据写入到 JSON 文件
func SaveStructToJsonFile(data interface{}, filePath string) error {
	// 将结构体编码为 JSON 格式的字节数组
	jsonData, err := json.MarshalIndent(data, "", "  ") // 使用两个空格缩进
	if err != nil {
		return fmt.Errorf("JSON 编码失败: %w", err)
	}

	// 将 JSON 数据写入文件
	err = os.WriteFile(filePath, jsonData, 0644) // 0644 是权限模式
	if err != nil {
		return fmt.Errorf("写入文件失败: %w", err)
	}

	return nil
}

// readJsonFileToStruct 将 JSON 文件读取并反序列化到结构体
func ReadJsonFileToStruct(filePath string, data interface{}) error {
	// 打开文件
	file, err := os.Open(filePath)
	if err != nil {
		return fmt.Errorf("打开 JSON 文件失败: %w", err)
	}
	defer file.Close()

	// 创建 JSON 解码器
	decoder := json.NewDecoder(file)

	// 解码 JSON 数据到结构体
	err = decoder.Decode(data)
	if err != nil {
		if err == io.EOF {
			return fmt.Errorf("文件为空或者没有JSON数据: %w", err)
		}
		return fmt.Errorf("JSON 解码失败: %w", err)
	}

	return nil
}

func OrderedMap(kvArray Slice[*orderedmap.Pair]) *orderedmap.OrderedMap {
	o := orderedmap.New()
	for _, kv := range kvArray {
		o.Set(kv.Key(), kv.Value())
	}
	return o
}
