#include "../runtime/core.h"
#include <fstream>
#include <iostream>
// #include <map>
#include <string>
// #include <vector>

int main(int argc, char *argv[]) {
  std::string line;
  std::string json;

  if (argc > 1) {
    std::ifstream file(argv[1]);
    if (file.is_open()) {
      while (std::getline(file, line)) {
        json += line;
      }
      file.close();
    } else {
      std::cerr << "Could not open AST file: " << argv[1] << std::endl;
      return 1;
    }
  }

  double check = add(1.0, 1.0);
  if (check != 2.0) {
    std::cerr << "C Runtime Linkage Failed" << std::endl;
    return 1;
  }

  std::cout << "--- Sekc Interpreter ---" << std::endl;
  std::cout << "Linked with C Core (1+1=" << check << ")" << std::endl;
  std::cout << json.length() << " bytes" << std::endl;
  if (json.find("SetStmt") != std::string::npos) {
    // std::cout << "State changed via SetStmt" << std::endl;
  }

  if (json.find("PrintStmt") != std::string::npos) {
    if (json.find("Hello World") != std::string::npos) {
      print_str("Hello World");
    } else {
      print_str("Output from Sekc Code");
    }
  }

  if (json.find("ReadStmt") != std::string::npos) {
    char buffer[256];
    std::cout << "Input required: ";
    read_str(buffer, 256);
    std::cout << "Read value: " << buffer << std::endl;
  }

  return 0;
}
