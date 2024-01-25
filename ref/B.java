public class B extends Printer {
  A a;
  B(){
    super("B");
  }
  public void setA(A a){
    this.a = a;
  }

  public void anotherPrint() {
    a.print();
  }

  public static void main(String[] args) {
    B b = new B();
    A a = new A();
    a.setB(b);
    b.setA(a);

    a.anotherPrint();
    b.anotherPrint();
  }
}
