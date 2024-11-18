// 完全配合 utils.ts/Proxy

import React, { forwardRef } from 'react';
import ProxyImage from './Proxy/ProxyImage';

interface CustomImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
    alt: string; // alt 属性是必需的
}

const CustomImage = forwardRef<HTMLImageElement, CustomImageProps>((props, ref) => {
    const proxyList: string[] = [
        "https://img.youtube.com",
    ]

    // for (const index in proxyList) {
    //     console.log(props.src, index, props.src!.startsWith(proxyList[index]))

    //     if (props.src!.startsWith(proxyList[index])) {
    //         return <ProxyImage ref={ref} {...props}/>
    //     }
    // }
    for (const prefix of proxyList) {
        console.log(props.src, prefix, props.src!.startsWith(prefix))

        if (props.src!.startsWith(prefix)) {
            return <ProxyImage ref={ref} {...props}/>
        }
    }

    // 如果是不需要ProxyImage代理的连接

    const prefixMap: { [key: string]: string | undefined } = {
        "https://exhentai.org/s": "https://ehwv.moonchan.xyz/image/s",
        "https://e-hentai.org/s": "https://ehwv.moonchan.xyz/image/s",
        "https://ex.moonchan.xyz/s": "https://ehwv.moonchan.xyz/image/s",
        "https://ehwv.moonchan.xyz/s": "https://ehwv.moonchan.xyz/image/s",
        "https://ex.nmbyd1.top/s": "https://ehwv.moonchan.xyz/image/s",
        "https://ex.nmbyd2.top/s": "https://ehwv.moonchan.xyz/image/s"
    };

    let src = props.src

    // 遍历对象的键
    if (src) {
        for (const prefix in prefixMap) {
            if (src.startsWith(prefix)) {
                // 替换前缀
                src = src.replace(prefix, prefixMap[prefix]!);
                break; // 找到第一个匹配后可以退出循环
            }
        }
    }

    return <img ref={ref} {...props} src={src} />;
    // 为了消掉提示要这么做的，有什么大病吧。
    // const alt = props.alt || "";
    // return <img ref={ref} {...props} alt={alt}/>; // 为了消掉提示这么做的，有什么大病吧。
});

CustomImage.displayName = 'CustomImage'; // 可选：设置 displayName 以便于调试

export default CustomImage;