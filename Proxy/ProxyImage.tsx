// 完全配合 utils.ts/Proxy 指定的代理
// 

import React, { forwardRef } from 'react';
import { END_POINT } from './utils';

interface CustomImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
    origin?: string;
    referer?: string;
}

const CustomImage = forwardRef<HTMLImageElement, CustomImageProps>((props, ref) => {

    const url = new URL(props.src!)

    // 添加或更新查询参数
    url.searchParams.set('proxy_host', url.hostname); // 不包含端口，包含端口的是host   
    url.hostname = END_POINT
    if (props.origin) {
        url.searchParams.set('proxy_origin', props.origin);   
    }
    if (props.referer) {
        url.searchParams.set('proxy_referer', props.referer);   
    }
    return <img ref={ref} {...props} src={url.toString()} />;
    // 为了消掉提示要这么做的，有什么大病吧。
    // const alt = props.alt || "";
    // return <img ref={ref} {...props} alt={alt}/>; // 为了消掉提示这么做的，有什么大病吧。
});

CustomImage.displayName = 'CustomImage'; // 可选：设置 displayName 以便于调试

export default CustomImage;