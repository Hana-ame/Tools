
/**
 * 使用URL API解析主域名（需完整URL）
 * @param url 完整URL（如 "https://abc.example.com/path"）
 * @returns 主域名（如 "example.com"）
 */
export function parseRootDomain(hostname: string): string {
    try {
        const parts = hostname.split('.');
        return parts.length > 2
            ? parts.slice(-2).join('.')
            : hostname;
    } catch {
        throw new Error("Invalid URL format");
    }
}
