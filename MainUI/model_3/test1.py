from desc import func2

def function(x=[], a=[]):
    result = a[0] * x[0]**3;
    result += a[1] * x[1]**2;
    result += a[2] * x[2];
    result += a[3];
    result = func2.func2(result)
    return result;

def description():
    param = [];
    param.append(['参数1', 'a1', '无量纲']);
    param.append(['参数2', 'a2', '无量纲']);
    param.append(['参数3', 'a3', '无量纲']);
    param.append(['参数4', 'a4', '无量纲']);
    return param;

def descr_var():
    var = [];
    var.append(['变量1', 'x1', '无量纲']);
    var.append(['变量2', 'x2', '无量纲']);
    var.append(['变量3', 'x3', '无量纲']);
    return var;

if __name__ == '__main__':
    variable = [1,2,3]
    print function(x = variable)
    
    
