/**
 * 创建一个坐标转换器
 * @param centerX - canvas的中心x坐标
 * @param centerY - canvas的中心y坐标
 * @returns 一个包含两个函数的对象,分别用于坐标系之间的相互转换
 */
function createCoordinateConverter(centerX: number, centerY: number) {
  /**
   * 将canvas坐标系中的坐标转换为平面直角坐标系中的坐标
   * @param x - canvas坐标系中的x坐标
   * @param y - canvas坐标系中的y坐标
   * @returns 包含平面直角坐标系中x和y坐标的对象
   */
  function canvasToCartesian(x: number, y: number): { x: number; y: number } {
    const cartesianX = x - centerX;
    const cartesianY = centerY - y;
    return { x: cartesianX, y: cartesianY };
  }

  /**
   * 将平面直角坐标系中的坐标转换为canvas坐标系中的坐标
   * @param x - 平面直角坐标系中的x坐标
   * @param y - 平面直角坐标系中的y坐标
   * @returns 包含canvas坐标系中x和y坐标的对象
   */
  function cartesianToCanvas(x: number, y: number): { x: number; y: number } {
    const canvasX = x + centerX;
    const canvasY = centerY - y;
    return { x: canvasX, y: canvasY };
  }

  return { canvasToCartesian, cartesianToCanvas };
}

// usage
// const canvas = document.getElementById('myCanvas');
// const ctx = canvas.getContext('2d');
// const centerX = canvas.width / 2;
// const centerY = canvas.height / 2;

// // 创建一个坐标转换器
// const converter = createCoordinateConverter(centerX, centerY);
// const { canvasToCartesian, cartesianToCanvas } = converter;
// const { x: cartesianX, y: cartesianY } = canvasToCartesian(canvasX, canvasY);
// const { x: canvasX, y: canvasY } = cartesianToCanvas(cartesianX, cartesianY);
