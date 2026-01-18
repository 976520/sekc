import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class Main {
  public static void main(String[] args) {
    if (args.length < 1) {
      System.err.println("Usage: sekc <source_file>");
      System.exit(1);
    }

    String sourceFile = args[0];
    try {
      String lexerCmd = System.getProperty("sekc.lexer", "./bin/lexer");
      String parserCmd = System.getProperty("sekc.parser", "./bin/run_parser.sh");
      String analyzerCmd = System.getProperty("sekc.analyzer", "python3 src/analyzer/main.py");
      String interpreterCmd = System.getProperty("sekc.interpreter", "./bin/runner");

      File file = new File(sourceFile);

      Process pLexer = new ProcessBuilder(lexerCmd.split(" ")).start();
      try (FileInputStream fis = new FileInputStream(file);
          OutputStream os = pLexer.getOutputStream()) {
        byte[] buffer = new byte[1024];
        int len;
        while ((len = fis.read(buffer)) != -1) {
          os.write(buffer, 0, len);
        }
      }

      Process pParser = new ProcessBuilder(parserCmd.split(" ")).start();
      pipe(pLexer.getInputStream(), pParser.getOutputStream());
      pLexer.waitFor();
      Process pAnalyzer = new ProcessBuilder(analyzerCmd.split(" ")).start();
      pipe(pParser.getInputStream(), pAnalyzer.getOutputStream());
      pParser.waitFor();

      File astFile = File.createTempFile("sekc_ast", ".json");
      astFile.deleteOnExit();

      try (FileOutputStream fos = new FileOutputStream(astFile);
          InputStream is = pAnalyzer.getInputStream()) {
        byte[] buffer = new byte[1024];
        int len;
        while ((len = is.read(buffer)) != -1) {
          fos.write(buffer, 0, len);
        }
      }
      pAnalyzer.waitFor();

      List<String> cmd = new ArrayList<>();
      for (String s : interpreterCmd.split(" "))
        cmd.add(s);
      cmd.add(astFile.getAbsolutePath());

      ProcessBuilder pbInterpreter = new ProcessBuilder(cmd);
      pbInterpreter.redirectInput(ProcessBuilder.Redirect.INHERIT);
      pbInterpreter.redirectOutput(ProcessBuilder.Redirect.INHERIT);
      pbInterpreter.redirectError(ProcessBuilder.Redirect.INHERIT);

      Process pInterpreter = pbInterpreter.start();
      pInterpreter.waitFor();

    } catch (Exception e) {
      e.printStackTrace();
    }
  }

  private static void pipe(InputStream in, OutputStream out) {
    new Thread(() -> {
      try {
        byte[] buffer = new byte[1024];
        int len;
        while ((len = in.read(buffer)) != -1) {
          out.write(buffer, 0, len);
        }
        out.close();

      } catch (IOException e) {
        // e.printStackTrace();
      }
    }).start();
  }
}
