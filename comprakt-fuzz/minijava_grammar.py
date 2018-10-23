from gramfuzz.fields import *
from config import *

INTEGER_LITERAL = String(charset=String.charset_num, min=1, max=10)

class TokenDef(Def):
    cat = "token"
class TokenRef(Ref):
    cat = "token"

TokenDef("IDENT",
         And(
             String(charset=String.charset_alpha + "_", min=1, max=1),
             String(charset=String.charset_alphanum + "_", max=MAX_STRING_LENGTH - 1)
         ))

TokenDef("INTEGER_LITERAL",
         String(charset=String.charset_num, min=1, max=10))

TokenDef("class", "class ")
TokenDef("{", " {\n")
TokenDef("}", "\n}")
TokenDef("(", "(")
TokenDef(")", ")")
TokenDef("[", "[")
TokenDef("]", "]")
TokenDef(";", ";")
TokenDef("public", "public ")
TokenDef("static", "static ")
TokenDef("int", "int")
TokenDef("boolean", "boolean")
TokenDef("void", "void")
TokenDef("String", "String")
TokenDef("throws", "throws ")
TokenDef("=", " = ")
TokenDef("||", " ||")
TokenDef("&&", " &&")
TokenDef("==", " ==")
TokenDef("!=", " !=")
TokenDef("<", " <")
TokenDef("<=", " <=")
TokenDef(">", " >")
TokenDef(">=", " >=")
TokenDef("+", " +")
TokenDef("-", " -")
TokenDef("*", " +")
TokenDef("/", " /")
TokenDef("%", " %")
TokenDef("!", "!")
TokenDef(".", ".")
TokenDef(",", ", ")
TokenDef("null", "null")
TokenDef("false", "false")
TokenDef("true", "true")
TokenDef("this", "this")
TokenDef("new", "new ")
TokenDef("while", "while ")
TokenDef("if", "if ")
TokenDef("else", "else ")
TokenDef("return", "return")

Def("Program",
    Join(
        Ref("ClassDeclaration"),
        sep="\n\n",
        max=MAX_CLASSES
    ),
    cat="minijava")

Def("ClassDeclaration",
    And(
        TokenRef("class"),
        TokenRef("IDENT"),
        TokenRef("{"),
        Opt(
            Join(
                Ref("ClassMember"),
                sep="\n",
                max=MAX_CLASS_MEMBERS,
            )
        ),
        TokenRef("}"),
    ))

Def("ClassMember",
    Or(
        Ref("Field"),
        Ref("Method"),
        Ref("MainMethod"),
    ))

Def("Field",
    And(
        TokenRef("public"),
        Ref("Type"),
        " ",
        TokenRef("IDENT"),
        TokenRef(";"),
    ))

Def("MainMethod",
    And(
        TokenRef("public"),
        TokenRef("static"),
        TokenRef("void"),
        " ",
        TokenRef("IDENT"),
        TokenRef("("),
        TokenRef("String"),
        TokenRef("["),
        TokenRef("]"),
        " ",
        TokenRef("IDENT"),
        TokenRef(")"),
        " ",
        Opt(Ref("MethodRest")),
        Ref("Block"),
    ))

Def("Method",
    And(
        TokenRef("public"),
        Ref("Type"),
        " ",
        TokenRef("IDENT"),
        TokenRef("("),
        Opt(Ref("Parameters")),
        TokenRef(")"),
        " ",
        Opt(Ref("MethodRest")),
        Ref("Block"),
    ))

Def("MethodRest",
    And(
        TokenRef("throws"),
        TokenRef("IDENT"),
    ))

# TODO
Def("Parameters",
    Or(
        "",
        Ref("Parameter"),
        And(
            Ref("Parameter")
        )
    )
    Join(
        Ref("Parameter"),
        sep=", ",
        max=MAX_PARAMETERS,
    ))

Def("Parameter",
    And(
        Ref("Type"),
        " ",
        TokenRef("IDENT"),
    ))

Def("Type",
    Or(
        And(
            Ref("Type"),
            TokenRef("["),
            TokenRef("]"),
        ),
        Ref("BasicType"),
    ))

Def("BasicType",
    Or(
        TokenRef("int"),
        TokenRef("boolean"),
        TokenRef("void"),
        TokenRef("IDENT"),
    ))

Def("Statement",
    Or(
        Ref("Block"),
        Ref("EmptyStatement"),
        Ref("IfStatement"),
        Ref("ExpressionStatement"),
        Ref("WhileStatement"),
        Ref("ReturnStatement"),
    ))

Def("Block",
    And(
        TokenRef("{"),
        Join(
            Ref("BlockStatement"),
            sep="\n",
            max=MAX_BLOCK_STATEMENTS,
        ),
        TokenRef("}"),
    ))

Def("BlockStatement",
    Or(
        Ref("Statement"),
        Ref("LocalVariableDeclarationStatement"),
    ))

Def("LocalVariableDeclarationStatement",
    And(
        Ref("Type"),
        " ",
        TokenRef("IDENT"),
        Opt(
            And(
                TokenRef("="),
                Ref("Expression"),
            )
        ),
        TokenRef(";"),
    ))

Def("EmptyStatement",
    TokenRef(";"))

Def("WhileStatement",
    And(
        TokenRef("while"),
        TokenRef("("),
        Ref("Expression"),
        TokenRef(")"),
        " ",
        Ref("Statement"),
    ))

Def("IfStatement",
    And(
        TokenRef("if"),
        TokenRef("("),
        Ref("Expression"),
        TokenRef(")"),
        " ",
        Ref("Statement"),
        Opt(
            And(
                TokenRef("else"),
                Ref("Statement"),
            )
        )
    ))

Def("ExpressionStatement",
    And(
        Ref("Expression"),
        TokenRef(";"),
    ))

Def("ReturnStatement",
    And(
        TokenRef("return"),
        " ",
        Opt(
            Ref("Expression"),
        ),
        TokenRef(";"),
    ))

Def("Expression",
    Ref("AssignmentExpression"))

Def("AssignmentExpression",
    And(
        Ref("LogicalOrExpression"),
        Opt(
            TokenRef("="),
            Ref("AssignmentExpression"),
        )
    ))

Def("LogicalOrExpression",
    And(
        Opt(
            Ref("LogicalOrExpression"),
            TokenRef("||"),
        ),
        Ref("LogicalAndExpression"),
    ))

Def("LogicalAndExpression",
    And(
        Opt(
            Ref("LogicalAndExpression"),
            TokenRef("&&"),
        ),
        Ref("EqualityExpression"),
    ))

Def("EqualityExpression",
    And(
        Opt(
            Ref("EqualityExpression"),
            Or(
                TokenRef("=="),
                TokenRef("!="),
            ),
        ),
        Ref("RelationalExpression"),
    ))

Def("RelationalExpression",
    And(
        Opt(
            Ref("RelationalExpression"),
            Or(
                TokenRef("<"),
                TokenRef("<="),
                TokenRef(">"),
                TokenRef(">="),
            ),
        ),
        Ref("AdditiveExpression"),
    ))

Def("AdditiveExpression",
    And(
        Opt(
            Ref("AdditiveExpression"),
            Or(
                TokenRef("+"),
                TokenRef("-"),
            ),
        ),
        Ref("MultiplicativeExpression"),
    ))

Def("MultiplicativeExpression",
    And(
        Opt(
            Ref("MultiplicativeExpression"),
            Or(
                TokenRef("*"),
                TokenRef("/"),
                TokenRef("%"),
            ),
        ),
        And(
            Ref("UnaryExpression"),
        )
    ))

Def("UnaryExpression",
    Or(
        Ref("PostfixExpression"),
        And(
            Or(
                TokenRef("!"),
                TokenRef("-"),
            ),
            Ref("UnaryExpression"),
        )
    ))

Def("PostfixExpression",
    And(
        Ref("PrimaryExpression"),
        Opt(
            Join(
                Ref("PostfixOp"),
                sep="",
                max=MAX_POSTFIX_OPS,
            )
        )
    ))

Def("PostfixOp",
    Or(
        Ref("MethodInvocation"),
        Ref("FieldAccess"),
        Ref("ArrayAccess"),
    ))

Def("MethodInvocation",
    And(
        TokenRef("."),
        TokenRef("IDENT"),
        TokenRef("("),
        Ref("Arguments"),
        TokenRef(")"),
    ))

Def("FieldAccess",
    And(
        TokenRef("."),
        TokenRef("IDENT"),
    ))

Def("ArrayAccess",
    And(
        TokenRef("["),
        Ref("Expression"),
        TokenRef("]"),
    ))

# TODO
Def("Arguments",
    Opt(
        Join(
            Ref("Expression"),
            sep=", ",
            max=MAX_ARGUMENTS,
        )
    ))

Def("PrimaryExpression",
    Or(
        TokenRef("null"),
        TokenRef("false"),
        TokenRef("true"),
        TokenRef("INTEGER_LITERAL"),
        TokenRef("IDENT"),
        And(
            TokenRef("IDENT"),
            TokenRef("("),
            Ref("Arguments"),
            TokenRef(")"),
        ),
        TokenRef("this"),
        And(
            TokenRef("("),
            Ref("Expression"),
            TokenRef(")"),
        ),
        Ref("NewObjectExpression"),
        Ref("NewArrayExpression"),
    ))

Def("NewObjectExpression",
    And(
        TokenRef("new"),
        TokenRef("IDENT"),
        TokenRef("("),
        TokenRef(")"),
    ))

Def("NewArrayExpression",
    And(
        TokenRef("new"),
        Ref("BasicType"),
        TokenRef("["),
        Ref("Expression"),
        TokenRef("]"),
        Opt(
            Join(
                TokenRef("["),
                TokenRef("]"),
                sep="",
                max=MAX_ARRAY_DECL_DIMENSION,
            )
        )
    ))
