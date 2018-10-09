from desc import func2

def function(x=[], a=[]):
    result = a[0] * x[0]**3
    result1 = result
    result += a[1] * x[1]**2
    result2 = result
    result += a[2] * x[2]
    result3 = result
    result += a[3]
    result4 = result
    result5 = func2.func2(result)
    result=[]
    result.append(result1)
    result.append(result2)
    result.append(result3)
    result.append(result4)
    result.append(result5)
    return result

def description():
    param = []
    param.append(['参数1', 'a1', '无量纲'])
    param.append(['参数2', 'a2', '无量纲'])
    param.append(['参数3', 'a3', '无量纲'])
    param.append(['参数4', 'a4', '无量纲'])
    return param

def descr_var():
    var = []
    var.append(['变量1', 'x1', '无量纲'])
    var.append(['变量2', 'x2', '无量纲'])
    var.append(['变量3', 'x3', '无量纲'])
    return var

def formula():
    param = []
    param.append(['参数1', 'a1', '无量纲'])
    param.append(['参数2', 'a2', '无量纲'])
    param.append(['参数3', 'a3', '无量纲'])
    param.append(['参数4', 'a4', '无量纲'])
    return param

if __name__ == '__main__':
    variable = [1,2,3]
    print function(x = variable)
