export async function worker<T>(tasks: (() => Promise<T>)[]) {
    try {
        const results: T[] = []
        while (tasks.length > 0) {
            const task = tasks.shift()
            if (!task) return results;
            const result = await task();
            results.push(result);
        }
        return results;
    } catch (err) {
        throw err
    }
}