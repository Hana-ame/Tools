public class A extends Printer{
  B b;
  A(){
    super("A");
  }
  public void setB(B b){
    this.b = b;
  }
  public void anotherPrint() {
    b.print();
  }
}
