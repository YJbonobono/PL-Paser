# declaration
LEFT_PAREN = '('
RIGHT_PAREN = ')'
ADD_OP = ['+', '-']
MULT_OP = ['*', '/']
SEMI_COLON = ';'
ASSIGN_OP = ':='
Unknown = 9999999

# save variables
ident = {}
WARNING = []

# 한줄이 input으로 들어간다.
def program(string):
    # <program> → <statements>
    stmts(string)
    print(' '.join(list(ident.keys())))

def stmts(string):
    # <stmts> → <statement><semi_colon><statements>
    if SEMI_COLON in string:
        # colon 위치를 찾는다
        colon_loc = string.find(SEMI_COLON)
        # statement 파싱
        str_stmt = string[:colon_loc]
        # 해당 줄만 print
        stmt(str_stmt)
        # 나머지 statements 확인
        str_stmts = string[colon_loc+2:]
        stmts(str_stmts)
    # <stmts> → <statement>
    else:
        stmt(string)

def stmt(string):
    idt, op, const = 0, 0, 0
    string = string.strip()
    # <statement> → <ident><assign_op><expr>
    ss = string.split()
    if not ss:
        return 1
    if ss[1] == ASSIGN_OP:
        if ss[0].isdigit() == False:
            idt += 1
            # righthand 식을 expr에 보낸다 (계산한 값을 return 해야한다)
            val, idt, op, const = expr(' '.join(ss[2:]), idt, op, const)
            # ident 리스트에 변수와 값을 dictionary 형태로 저장
            # ident.append({ss[0], val})
            ident[ss[0]] = val
        else:
            WARNING.append("(ERROR) INVALID IDENT")
    else:
        WARNING.append("(ERROR) ':=' DOES NOT EXIST")
    if WARNING:
        WARNING.clear()    

# expr은 최종 결과값을 반환해야 한다.
# term과 term_tail의 반환값을 더한다.
def expr(string, idt, op, const): 
    #idt, op, const = 0, 0, 0
    string = string.strip()
    # print("expr string: {}".format(string))
    # <expr> → <term><term_tail>
    # Paranthesis() 기준이나
    if string[0]==LEFT_PAREN:
        lp_loc = string.rfind(RIGHT_PAREN)
        t, idt0, op0, const0 = term(string[:lp_loc+1], idt, op, const)
        t_tail, idt_t, op_t, const_t = term_tail(string[lp_loc+1:], idt, op, const)
    # ADD_OP (+/-)를 기준으로 term, term_tail 나눕니다
    else:
        plus_loc, mins_loc = 1000000, 1000000
        # 덧셈기호 찾기
        if ADD_OP[0] in string:
            plus_loc = string.find(ADD_OP[0])
        # 뺄셈기호 찾기
        if ADD_OP[1] in string:
            mins_loc = string.find(ADD_OP[1])
        # ADD_OP 가 존재하지 않는 경우
        if plus_loc == mins_loc:
            t, idt0, op0, const0 = term(string, idt, op, const)
            # 1을 넘겨주면 term_tail은 ε을 반환한다.
            t_tail, idt_t, op_t, const_t = term_tail(1, idt, op, const)
        else:
            # 선두에 있는 연산자 우선
            add_loc = plus_loc if plus_loc < mins_loc else mins_loc
            # term 하나에 operand나 constant 하나
            t, idt0, op0, const0 = term(string[:add_loc], idt, op, const)
            t_tail, idt_t, op_t, const_t = term_tail(string[add_loc:], idt, op, const)
    # 수정 필요, +- 구분해야함
    if t == Unknown or t_tail == Unknown:
        return Unknown, idt0+idt_t-idt, op0+op_t-op, const0+const_t-const
    else:
        return int(t)+int(t_tail), idt0+idt_t-idt, op0+op_t-op, const0+const_t-const

        
# 곱셈/나눗셈 (우선순위 높음)
def term(string, idt, op, const):
    #idt, op, const = 0, 0, 0
    string = string.strip()
    # print("term string: {}".format(string))  
    # <term> → <factor><factor_tail>
    # Paranthesis() 기준이나
    if string[0]==LEFT_PAREN:
        # 상응 괄호 찾기
        lp_loc = string.rfind(RIGHT_PAREN)
        # 괄호가 마지막에 있으면 전체를 보낸다
        if lp_loc == len(string)-1:
            f, idt0, op0, const0 = factor(string, idt, op, const)
            f_tail, idt_t, op_t, const_t = factor_tail(1, idt, op, const)       
        # 괄호가 중간에 있으면 괄호를 기준으로 나눈다.
        else:
            f, idt0, op0, const0 = factor(string[:lp_loc+1], idt, op, const)
            f_tail, idt_t, op_t, const_t = factor_tail(string[lp_loc+1:], idt, op, const)
    # MULT_OP (*/)를 기준으로 factor, factor_tail 나눕니다
    else:
        mult_loc, div_loc = 1000000, 1000000
        # 곱셈기호 찾기
        if MULT_OP[0] in string:
            mult_loc = string.find(MULT_OP[0])
        # 나눗셈기호 찾기
        if MULT_OP[1] in string:
            div_loc = string.find(MULT_OP[1])
        # MULT_OP 가 존재하지 않는 경우
        if mult_loc == div_loc:
            f, idt0, op0, const0 = factor(string, idt, op, const)
            # 1을 넣으면 f_tail로 1을 반환함(곱하거나 나누기 때문)
            f_tail, idt_t, op_t, const_t = factor_tail(1, idt, op, const)
        else:
            # 선두에 있는 연산자 우선
            mult_loc = mult_loc if mult_loc < div_loc else div_loc 
            f, idt0, op0, const0 = factor(string[:mult_loc], idt, op, const)
            f_tail, idt_t, op_t, const_t = factor_tail(string[mult_loc:], idt, op, const)
    # 수정 필요, */ 구분해야함
    if f == Unknown or f_tail == Unknown:
        return Unknown, idt+idt_t-idt, op+op_t-op, const+const_t-const
    else:
        return int(f)*int(f_tail), idt0+idt_t-idt, op0+op_t-op, const0+const_t-const


# 덧셈/뺄셈 (우선순위 낮음)
# ADD_OP 이후의 값들을 계산한 값을 반환한다.
def term_tail(string, idt, op, const): 
    #idt, op, const = 0, 0, 0
    if string == 1:
        # <term_tail> → ε
        # print("term_tail string: {}".format(string))
        return 0, idt, op, const
    else:
        # <term_tail> → <add_op><term><term_tail>
        # 앞뒤 공백 제거
        string = string.strip()
        # print("term_tail string: {}".format(string))
        # Operand Parsing 및 중복연산자 오류 해결
        loc = 0
        s_temp = string.split()
        for i in range(1, len(s_temp)):
            if s_temp[i] in ADD_OP+MULT_OP:
                WARNING.append("(WARNING) 중복연산자 제거")
                loc = i
            else:
                break
        op += 1
        string = ' '.join(s_temp[loc:])  
        # ADD_OP (+/-)를 기준으로 term, term_tail 나눕니다
        plus_loc, mins_loc = 1000000, 1000000
        # 덧셈기호 찾기
        if ADD_OP[0] in string:
            plus_loc = string.find(ADD_OP[0])
        # 뺄셈기호 찾기
        if ADD_OP[1] in string:
            mins_loc = string.find(ADD_OP[1])
        # ADD_OP 가 존재하지 않는 경우
        if plus_loc == mins_loc:
            t, idt0, op0, const0 = term(string, idt, op, const)
            # 1을 넘겨주면 term_tail은 ε을 반환한다.
            t_tail, idt_t, op_t, const_t = term_tail(1, idt, op, const)
        else:
            # 선두에 있는 연산자 우선
            add_loc = plus_loc if plus_loc < mins_loc else mins_loc
            # 서두의 ADD_OP를 제외한 식을 넘긴다.
            if add_loc == 0:
                t, idt0, op0, const0 = term(string[1:], idt, op, const)
                t_tail, idt_t, op_t, const_t = term_tail(1, idt, op, const)
            else:
                t, idt0, op0, const0 = term(string[2:add_loc], idt, op, const)
                t_tail, idt_t, op_t, const_t = term_tail(string[add_loc:], idt, op, const)
        # 수정 필요 +- 구분 필요
        if t == Unknown or t_tail==Unknown:
            return Unknown, idt0+idt_t-idt, op0+op_t-op, const0+const_t-const
        else:
            return int(t)+int(t_tail), idt0+idt_t-idt, op0+op_t-op, const0+const_t-const


def factor(string, idt, op, const):
    #idt, const = 0, 0
    string = string.strip()
    # print("  factor string: {}".format(string))
    token = string[0]
    if token == LEFT_PAREN:
        # <factor> → <LP><expr><RP>
        if string[-1] == RIGHT_PAREN:
            # '기호0, 띄어쓰기1 이후 ~ 띄어쓰기-2, 기호 이전-1' 넘겨준다.
            return expr(string[2:-1].strip(), idt, op, const)
        else:
            WARNING.append("(WARNING) RIGHT_PAREN DO NOT EXIST")
            return expr(string[2:].strip(), idt, op, const)
    # Constant
    elif token.isdigit() == True:
        const += 1
        return token, idt, op, const
    # Ident
    else:
        #print(token)
        #print(idt)
        if token in ident:
            idt += 1
            # 저장된 ident의 값을 반환한다
            if ident[token] == Unknown:
                WARNING.append("(ERROR) Referenced Undefined IDENT \'"+token+"\'")
                # 정의되지 않은 ident를 참조할 경우
                return Unknown, idt, op, const
            else:
                # 정의된 ident를 참조할 경우
                return ident[token], idt, op, const
        else:
            idt += 1
            # 정의된 적 없는 ident, Unknown을 반환한다.
            WARNING.append("(ERROR) Referenced Undefined IDENT \'"+token+"\'")
            ident[token] = Unknown
            return Unknown, idt, op, const

def factor_tail(string, idt, op, const):
    #idt, op, const = 0, 0, 0
    if string == 1:
        # <factor_tail> → ε
        return 1, idt, op, const
    else:
        # <factor_tail> → <mult_op><factor><factor_tail>
        # 앞뒤 공백 제거
        string = string.strip()
        # print("  factor_tail string: {}".format(string))
        # Operand Parsing 및 중복연산자 오류 해결
        loc = 0
        s_temp = string.split()
        for i in range(1, len(s_temp)):
            if s_temp[i] in ADD_OP+MULT_OP:
                WARNING.append("(WARNING) 중복연산자 제거")
                loc = i
            else:
                break
        op += 1
        string = ' '.join(s_temp[loc:])  
        # MULT_OP (+/-)를 기준으로 factor, factor_tail 나눕니다
        mult_loc, div_loc = 1000000, 1000000
        # 곱셈기호 찾기
        if MULT_OP[0] in string:
            mult_loc = string.find(MULT_OP[0])
        # 나눗셈기호 찾기
        if MULT_OP[1] in string:
            div_loc = string.find(MULT_OP[1])
        # MULT_OP 가 존재하지 않는 경우
        if mult_loc == div_loc:
            f, idt0, op0, const0 = factor(string, idt, op, const)
            # 1을 넘겨주면 factor_tail은 ε을 반환한다.
            f_tail, idt_t, op_t, const_t = factor_tail(1, idt, op, const)
        else:
            # 선두에 있는 연산자 우선
            mult_loc = mult_loc if mult_loc < div_loc else div_loc  
            # 서두의 MULT_OP를 제외한 식을 넘긴다.
            if mult_loc == 0:
                f, idt0, op0, const0 = factor(string[1:], idt, op, const)
                f_tail, idt_t, op_t, const_t = factor_tail(1, idt, op, const)
            else:
                f, idt0, op0, const0 = factor(string[2:mult_loc], idt, op, const)
                f_tail, idt_t, op_t, const_t = factor_tail(string[mult_loc:], idt, op, const)
        if f == Unknown or f_tail == Unknown:
            return Unknown, idt0+idt_t-idt, op0+op_t-op, const0+const_t-const
        # 수정 필요
        else:
            return int(f)*int(f_tail), idt0+idt_t-idt, op0+op_t-op, const0+const_t-const
