public class Printer {
  String s;
  Printer o;
  Printer(String s){
    this.s = s;
  }
  public void print() {
    System.out.println(s);
  }
  public void setPrinter(Printer o){
    this.o = o;
  }
}
