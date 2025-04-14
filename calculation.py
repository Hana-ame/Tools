# 想到什么就算什么。


# 计算焦距
def convex_lens_image(u, f):
    """
    凸透镜虚像计算函数
    参数:
        u (float): 物距（单位：cm，必须为正值）
        f (float): 焦距（单位：cm，凸透镜为正值）
    返回:
        dict: 包含像距、放大率、像的性质等信息的字典
    """
    try:
        # 符号规则验证[3,7](@ref)
        if u <= 0 or f <= 0:
            raise ValueError("物距和焦距必须为正值")

        # 核心公式计算[3,6](@ref)
        if u < f:  # 虚像条件
            v = (u * f) / (u - f)  # 虚像像距公式推导[3](@ref)
            magnification = abs(v / u)  # 放大率计算
            return {
                "像距": round(v, 2),
                "放大倍率": round(magnification, 2),
                "成像性质": "正立、放大虚像",
                "光路特征": "像与物同侧"
            }
        else:
            return {"错误": "不符合虚像条件（物距需小于焦距）"}

    except ZeroDivisionError:
        return {"错误": "物距等于焦距时无法成像"}
    except ValueError as e:
        return {"错误": str(e)}

# # 示例使用
# if __name__ == "__main__":
#     # 案例1：网页3的示例（物距0.3m，焦距2m）
#     print("案例1（u=0.3m, f=2m）：", convex_lens_image(0.4, 2))
    
#     # # 案例2：网页7的示例（物距15cm，焦距20mm需单位转换）
#     # print("\n案例2（u=15mm, f=20mm）：", convex_lens_image(15, 20))
    
#     # # 用户自定义输入
#     # u_input = float(input("\n请输入物距（cm）: "))
#     # f_input = float(input("请输入焦距（cm）: "))
#     # print(convex_lens_image(u_input, f_input))
