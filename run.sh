#!/bin/bash

echo "Starting..."

mkdir -p bin

echo "Setting up Lexer..."
cat <<EOF > bin/lexer
#!/bin/bash
python3 src/lexer/main.py
EOF
chmod +x bin/lexer

echo "Setting up Parser..."
cat <<EOF > bin/run_parser.sh
#!/bin/bash
python3 src/parser/main.py
EOF
chmod +x bin/run_parser.sh

if command -v g++ &> /dev/null; then
    gcc -c src/runtime/core.c -o src/runtime/core.o
    g++ src/interpreter/main.cpp src/runtime/core.o -o bin/runner -std=c++17
else
    echo "Error: 'g++' (clang) not found."
    exit 1
fi

echo "Building Driver..."
if command -v javac &> /dev/null; then
    javac src/driver/Main.java -d bin
else 
    echo "Error: 'javac' not found."
    exit 1
fi

echo "Creating 'sekc' launcher..."
cat <<EOF > sekc
#!/bin/bash
java -Dsekc.lexer=./bin/lexer -Dsekc.parser=./bin/run_parser.sh -Dsekc.analyzer="python3 src/analyzer/main.py" -Dsekc.interpreter=./bin/runner -cp bin Main \$1
EOF
chmod +x sekc

echo "Complete. Run ./sekc <file>"
