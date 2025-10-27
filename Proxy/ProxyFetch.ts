export default class ProxyFetch {
    private endpoint: string;

    constructor(endpoint: string) {
        this.endpoint = endpoint;
    }

    async fetch(input: string | URL, init?: RequestInit): Promise<Response> {
        const originalUrl = new URL(input);

        // 构建新的目标URL：使用https协议和指定的endpoint
        const targetUrl = new URL(originalUrl);
        targetUrl.protocol = 'https:';
        targetUrl.host = this.endpoint;

        // 准备请求配置
        const requestInit: RequestInit = { ...init };

        // 处理headers
        const headers = new Headers(requestInit.headers);
        headers.set('X-Host', originalUrl.hostname);
        headers.set('X-Scheme', originalUrl.protocol.slice(0, -1)); // 移除末尾的冒号

        requestInit.headers = headers;

        return fetch(targetUrl.toString(), requestInit);
    }
}