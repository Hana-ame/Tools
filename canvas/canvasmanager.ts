class CanvasManager {
    protected canvas: HTMLCanvasElement;
    private context: CanvasRenderingContext2D;
    private width: number;
    private height: number;
    protected baseWidth: number;  // 操作数基准宽度
    protected baseHeight: number; // 操作数基准高度

    constructor(canvas: HTMLCanvasElement, baseWidth: number, baseHeight: number) {
        this.canvas = canvas;
        this.context = canvas.getContext('2d') as CanvasRenderingContext2D;
        this.baseWidth = baseWidth;
        this.baseHeight = baseHeight;
        this.width = canvas.width;
        this.height = canvas.height;

        this.context.scale(this.baseWidth / this.width, this.baseHeight / this.height);
    }

    getContext() {
        return this.context;
    }

    // 设置 canvas 尺寸
    setSize(width: number, height: number): void {
        this.width = width;
        this.height = height;
        this.canvas.width = width;
        this.canvas.height = height;

        this.context.scale(this.width / this.baseWidth, this.height / this.baseHeight);
    }

    // 坐标系变换函数
    transformCoordinates(x: number, y: number): [number, number] {
        const scaleX = this.width / this.baseWidth;
        const scaleY = this.height / this.baseHeight;
        return [x / scaleX, y / scaleY];
        // return [x, y]
    }

    // 绘制矩形
    drawRect(x: number, y: number, width: number, height: number, color: string = 'lightblue'): void {
        this.context.fillStyle = color;
        this.context.fillRect(x, y, width, height);
    }

    drawPoint(x: number, y: number, color: string = "red") {
        // 在点击位置绘制一个圆圈
        this.context.beginPath();
        this.context.arc(x, y, 5, 0, Math.PI * 2);
        this.context.fillStyle =color;
        this.context.fill();
        this.context.closePath();

    }

    // 清空画布
    clear(): void {
        this.context.clearRect(0, 0, this.width, this.height);
    }

    // 示例：绘制背景
    drawBackground(color: string = 'lightblue'): void {
        this.clear();
        this.drawRect(0, 0, this.baseWidth, this.baseHeight, color); // 使用基准大小绘制背景
    }

    setAlpha(alpha: number = 1): void {
        this.context.globalAlpha = alpha
    }
    // x, y 是画布上的位置
    drawImage(img: HTMLImageElement, x: number, y: number,): void;
    // x, y 是画布上的位置, width, height 是画布上的 size
    drawImage(img: HTMLImageElement, x: number, y: number, width: number, height: number,): void;

    drawImage(img: HTMLImageElement, x: number, y: number, width?: number, height?: number): void {
        if (width && height) {
            this.context.drawImage(img, x, y, width, height);
        } else {
            this.context.drawImage(img, x, y);
        }
    }

    // 前四个参数是图片的 位置, 大小
    // 后四个是在画布上的 位置, 大小
    drawImageSlice(img: HTMLImageElement, sx: number, sy: number, sWidth: number, sHeight: number, x: number, y: number, width: number, height: number): void {
        this.context.drawImage(img, sx, sy, sWidth, sHeight, x, y, width, height);
    }

    // 返回句点的位置，最后一个字符的右下角。
    drawText(text: string, x: number, y: number, maxWidth: number, fillStyle?: string): [number, number] {
        this.context.fillStyle = fillStyle ?? this.context.fillStyle;


        // console.log(text)

        const match = this.context.font.match(/(\d+)px/)!; // 使用正则表达式匹配数字和“px”
        const heightInPx = parseInt(match[1], 10); // 提取数字并转换为整数
        // console.log(heightInPx)
        y = y + heightInPx;

        let i = 0;
        while (this.context.measureText(text.substring(0, i)).width < maxWidth) {
            i++;
            if (i > text.length) break;
        }
        i--;

        this.context.strokeText(text.substring(0, i), x, y, maxWidth);
        this.context.fillText(text.substring(0, i), x, y, maxWidth);

        if (text.substring(i).length === 0) return [x + this.context.measureText(text.substring(0, i)).width, y];

        // 下一行和之后的行
        return this.drawText(text.substring(i), x, y, maxWidth);
    }

}

export default CanvasManager;