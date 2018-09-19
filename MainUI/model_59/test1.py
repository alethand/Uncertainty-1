from desc import func2

def function(x=[], a1=1, a2=1, a3=1, a4=1):
    result = a1 * x[0]**3;
    result += a2 * x[1]**2;
    result += a3 * x[2];
    result += a4;
    result = func2.func2(result)
    return result;

def description():
    param = [];
    param.append(['变量1', 'a1']);
    param.append(['变量2', 'a2']);
    param.append(['变量3', 'a3']);
    param.append(['变量4', 'a4']);
    return param;

if __name__ == '__main__':
    variable = [1,2,3]
    print function(x = variable)
    
    
