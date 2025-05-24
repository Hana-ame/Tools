// 字符串截断函数
export function truncateString(str: string, num: number) {
    if (str.length <= num) {
      return str;
    }
    return str.slice(0, num) + '...';
  };
  
  
export function delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}



// [min, max]
function getRandomIntInclusive(min: number, max: number): number {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min; // [3,6,7](@ref)
}



/**
 * Sets the document's title.
 *
 * @param title The new title for the document. If null or undefined,
 *              the title will not be changed.
 *
 * @example
 * ```ts
 * import { setDocumentTitle } from './utils';
 *
 * setDocumentTitle("My Awesome Page");
 * setDocumentTitle("New Post - My Forum");
 * ```
 *
 * @warning If using a library like React Helmet or react-helmet-async,
 *          prefer using that library's mechanisms to manage the document title
 *          to avoid conflicts. This function directly manipulates `document.title`.
 */
export const setDocumentTitle = (title?: string | null): void => {
    if (typeof title === 'string' && document.title !== title) {
        document.title = title;
    }
    // If title is null or undefined, we do nothing.
    // You could also choose to set a default title here if title is null/undefined,
    // e.g., document.title = "Default App Title";
};

/**
 * Gets the current document's title.
 *
 * @returns The current value of `document.title`.
 */
export const getDocumentTitle = (): string => {
    return document.title;
};
