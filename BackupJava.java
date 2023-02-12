public class java{
    public static void main(String[] args){
        // code for demonstration.
        
        // different PRINTS
        System.out.println("HELLO FIRST ATTEMPT"); 
        String str = "Variable string";
        System.out.println(str);
        System.out.println(123456);


        // ASSIGNMENT ARITHMETIC and PRINT on a variable
        int p = 8;
        int x = 2 * 2;
        p = p / 2;
        int q = x - p;
        //  q = 4 - 4 = 0
        System.out.println(q);
        

        // IF ELSE statements
        if (x == 4){
            p = p + 1;
            System.out.println("should be printed");
        }
        else{
            p = p + 100;
            System.out.println("should not be printed");
        }
        // should print 5
        System.out.println(p);


        // WHILE loop
        int i = 2;
        while (i <= 4){
            System.out.println("Should Print 3x");
            i = i + 1;
        }

        // FOR loop
        for (int k = 0; k < 4; k = k + 1){
            System.out.println("Should Print 4x with counter");
	        System.out.println(k);
        }
    }
}