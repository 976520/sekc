#!/bin/bash

# Sekc Polyglot Pipeline Runner
# Components: Java (Driver) -> Python (Lexer) -> Python (Parser) -> Python (Analyzer) -> C++ (Interpreter)

echo "[BUILD] Starting..."

mkdir -p bin

# 1. Lexer (Python)
echo "[PYTHON] Setting up Lexer..."
cat <<EOF > bin/lexer
#!/bin/bash
python3 src/lexer/main.py
EOF
chmod +x bin/lexer

# 2. Parser (Python)
echo "[PYTHON] Setting up Parser..."
cat <<EOF > bin/run_parser.sh
#!/bin/bash
python3 src/parser/main.py
EOF
chmod +x bin/run_parser.sh

# 3. C Runtime & C++ Interpreter
echo "[C/C++] Building Runtime & Interpreter..."
if command -v g++ &> /dev/null; then
    # Compile C Core
    gcc -c src/runtime/core.c -o src/runtime/core.o
    # Link with C++ Interpreter
    g++ src/interpreter/main.cpp src/runtime/core.o -o bin/runner -std=c++17
else
    echo "❌ Error: 'g++' (clang) not found."
    exit 1
fi

# 4. Java Driver
echo "[JAVA] Building Driver..."
if command -v javac &> /dev/null; then
    javac src/driver/Main.java -d bin
else 
    echo "❌ Error: 'javac' not found."
    exit 1
fi

# 5. Create Launcher
echo "[SETUP] Creating 'sekc' launcher..."
cat <<EOF > sekc
#!/bin/bash
java -Dsekc.lexer=./bin/lexer -Dsekc.parser=./bin/run_parser.sh -Dsekc.analyzer="python3 src/analyzer/main.py" -Dsekc.interpreter=./bin/runner -cp bin Main \$1
EOF
chmod +x sekc

echo "[BUILD] Complete. Run ./sekc <file>"
