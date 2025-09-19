import { useState, useEffect, useCallback, Dispatch, SetStateAction } from 'react';

// 类型定义，让 Hook 的返回值更清晰
type UseLocalStorageReturn<T> = [
    T, // 存储的值
    Dispatch<SetStateAction<T>>, // 更新值的函数，API 与 useState 的 setter 相同
    Error | null // 错误状态
];

/**
 * 一个与 React.useState API 类似，但将状态持久化到 localStorage 的 Hook。
 * 它还支持跨标签页的同步和错误处理。
 * 
 * @param key - 在 localStorage 中使用的键。
 * @param initialValue - 如果 localStorage 中没有值，则使用的初始值。
 * @returns [storedValue, setValue, error] - 一个包含当前值、更新函数和错误状态的数组。
 */
export default function useLocalStorage<T>(key: string, initialValue: T): UseLocalStorageReturn<T> {
    // 初始化 initial Value
    // 使用一个函数作为 useState 的初始值，以确保 localStorage.getItem 只在客户端初始渲染时执行一次。
    // 这可以避免性能问题，并防止在 SSR (服务器端渲染) 环境下因 window 未定义而出错。
    const [storedValue, setStoredValue] = useState<T>(() => {
        // 如果在非浏览器环境（如 Next.js 服务器端），直接返回初始值
        if (typeof window === 'undefined') {
            return initialValue;
        }

        try {
            // 尝试从 localStorage 获取已存在的值
            const item = window.localStorage.getItem(key);
            // 如果有值，则解析它；否则，返回初始值
            return item ? (JSON.parse(item) as T) : initialValue;
        } catch (error) {
            // 如果解析出错，则打印错误并返回初始值
            console.error(`Error reading localStorage key “${key}”:`, error);
            return initialValue;
        }
    });

    // 状态2: 存储可能发生的错误
    const [error, setError] = useState<Error | null>(null);

    // 使用 useCallback 来包装 setValue 函数，以确保其引用在渲染间保持稳定，
    // 除非其依赖项（storedValue）发生变化。
    // 不加入 storedValue会出现旧值。
    const setValue: Dispatch<SetStateAction<T>> = useCallback(
        (value) => {
            try {
                // 允许传入一个函数来计算新值，就像 useState 的 setter 一样
                const valueToStore = value instanceof Function ? value(storedValue) : value;

                setStoredValue(valueToStore);

                if (typeof window !== 'undefined') {
                    const newValue = JSON.stringify(valueToStore);
                    // 在浏览器环境中，将新值持久化到 localStorage
                    window.localStorage.setItem(key, newValue);
                    // 手动触发一个 storage 事件，以便同一页面内的其他 Hook 实例也能同步
                    // `storage` 事件通常只通知其他页面
                    // isTrusted = false, 且需要自己填数字。
                    window.dispatchEvent(new StorageEvent('storage', { key, newValue }));
                } else {
                    // 更新 React 状态
                }

            } catch (err) {
                // 如果 stringify 出错，则捕获并更新错误状态
                const e = err as Error;
                console.error(`Error setting localStorage key “${key}”:`, e);
                setError(e);
            }
        },
        [key, storedValue]
    );

    // Effect: 监听 localStorage 的 'storage' 事件
    // 这个事件在其他标签页（或 iframe）修改了 localStorage 时触发
    useEffect(() => {
        // 确保在浏览器环境中执行
        if (typeof window === 'undefined') return;

        const handleStorageChange = (event: StorageEvent) => {
            // 当事件对应的 key 是我们正在监听的 key，并且有新值时
            console.log(event, event.key === key, event.newValue)
            if (event.key === key && event.newValue) {
                try {
                    setStoredValue(JSON.parse(event.newValue) as T);
                    setError(null); // 同步成功，清除错误
                } catch (err) {
                    const e = err as Error;
                    console.error(`Error parsing new value for key “${key}” from storage event:`, e);
                    setError(e);
                }
            }
        };

        // 添加事件监听器
        window.addEventListener('storage', handleStorageChange);

        // 清理函数：在组件卸载时移除监听器，防止内存泄漏
        return () => {
            window.removeEventListener('storage', handleStorageChange);
        };
    }, [key]); // 依赖数组中只有 key，因此只在 key 改变时重新绑定事件监听

    return [storedValue, setValue, error];
}